#!/usr/bin/env python3
"""QUEUE idea 163 — does-the-4b-aware-screen-only-pay-through-DD  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 163)
    "idea 152's rule 8 gave the cleanest instance yet of the IS screen earning its keep: on
     broad@10bps plain IS-Sharpe picked m=1.00 and failed the OOS-window 4b on DRAWDOWN while
     the 4b-aware screen picked m=0.60 and passed.  Ideas 151/110 found no selector beats
     do-nothing on Sharpe.  Reconcile them: re-run the selector comparison scoring OOS
     DRAWDOWN rather than OOS Sharpe, on the widened corpus.  If the screen's whole value is
     drawdown control, that is what it should be sold as."

WHAT IS ACTUALLY BEING TESTED
    The record has scored one object (the rule-8 SELECTOR) on one metric (OOS Sharpe) and
    concluded nothing beats doing nothing.  Idea 152's instance is about a DIFFERENT object —
    the 4b-AWARE SCREEN, i.e. the admissible POOL the selector picks from — and a different
    metric (OOS drawdown).  This run separates the two objects and scores BOTH on all three
    OOS metrics, so the reconciliation is a measurement rather than a rhetorical move:

      PANEL 1  THE SCREEN'S PRICE.  Holding the selector fixed, what does replacing the
               unscreened pool with the IS-4b-screened pool buy or cost in OOS MaxDD, OOS
               Sharpe and OOS CAGR?  This is idea 163's sentence, made paired.
      PANEL 2  THE SELECTOR, RESCORED.  Each selector minus the do-nothing control (hold the
               cell's ungated control arm) on OOS MaxDD instead of OOS Sharpe, inside each
               pool.  This is the "re-run the selector comparison scoring OOS DRAWDOWN" half.
      PANEL 3  KEEP PATHS.  Does the screen buy 4b passes?  Idea 152's instance is exactly a
               4b(OOS-window) pass bought by the screen; if that generalises it shows up here
               as a positive net swap, and if it does not, idea 152's instance is anecdote.
      PANEL 4  LEVELS against the LIVE book and SPY, with a freshly computed RULES v2 / SPY
               OOS leg (imports research/baseline.py) rather than a quoted one.

CORPUS — a census of EVERY committed grid in the record that carries a 4b-aware admission
mask, not one file.  All four are re-derived from their own committed `.grid.csv`, never read
from their `.picks.csv` except as the verdict gate's target:
      132  2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud      18 cells, 306 rows, S0/S1/S2
      142  2026-09-08_selector-comparison-needs-more-cells_B          48 cells, 816 rows, S0/S1/S2
      151  2026-09-08_does-any-selector-beat-doing-nothing_B          72 cells, 1224 rows, P_ALL/P_S1
      416  2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud 72 cells, 1224 rows, P_ALL/P_S1
    142/151 share (panel, book) with 132; 416 has ZERO (panel, book) overlap with 142/151 by
    construction, so 416 is an out-of-corpus REPLICATION of whatever the others say, and is
    reported separately as such.  Pooled readings are over DISTINCT (panel, book, cost) cells
    with the dedup rule stated in the console.

VERDICT GATE (this run is a census, so it must earn the right to read each file)
    For every admitted file this script re-derives every deterministic pick — sort arms by
    name, apply the file's own admission mask, take the argmax of the selector's IS column,
    fall back to the control arm when the mask admits nothing — and requires EXACT arm-for-arm
    agreement with that file's committed picks.csv on EVERY row.  A file that does not
    reproduce is REJECTED and contributes nothing.  The seeded K_Random control is excluded
    from the gate and from every reading (its draw depends on the parent's RNG call order,
    which is not reconstructible from the grid); the four deterministic selectors are not.

TUNED PARAMETERS: ZERO.  Selector (4), screen variant (S1 with the phi=0.70 CAGR floor, S2
    with the floor deleted), panel, book, cost rung and OOS metric are all REPORTED axES swept
    in full — every one of the 2,232 census rows is written to .census.csv and every paired
    statistic to .paired.csv.  Nothing here is chosen by looking at an OOS number.

WALK-FORWARD (PROTOCOL rule 8) — this run IS a walk-forward experiment, not a re-fit
    Every pool and every selector reads the IS window (through 2016-12-31) ONLY; every number
    reported is read ONCE on 2017-01-01..2026.  The screened and unscreened picks are
    therefore two rule-8 policies evaluated on the same untouched window, which is the
    comparison idea 152's instance is a single draw from.  OOS CAGR/Sharpe/MaxDD are reported
    for both policies against the cell's own ungated control, the LIVE RULES v2 book and SPY.

PRE-REGISTERED DECISION RULE (fixed before any Panel-1 number was read)
    First, INERTNESS caps everything: report the fraction of picks the screen actually moves.
    Then, on the MOVED cells (the only ones where the screen can express anything), pooled
    over distinct cells:
      SELL-AS-DD   mean d(OOS_MaxDD) > 0 with |t| >= 2, AND mean d(OOS_Sharpe) not significant
                   (|t| < 2), AND the d(OOS_MaxDD) sign holds in at least 3 of the 4 files.
      NULL         |t| < 2 on all three OOS metrics -> idea 152's instance does not generalise.
      COST         mean d(OOS_MaxDD) <= 0 -> the screen does not even buy drawdown.
    If SELL-AS-DD fires, the exchange rate (pp OOS CAGR given up per pp OOS MaxDD bought) is
    the number the screen should be sold at, and PROTOCOL rule 8's screen language should say
    so.  This run cannot promote a book and does not try; PROTOCOL.md is NOT modified.

CAVEATS carried, not buried
    * Survivorship (idea 54): every panel is current constituents, so every CAGR here is
      optimistic and no level in this file is an achievable return.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so an IS-window
      drawdown cap is measured on a window that cannot express a deep drawdown.  This biases
      the screen toward admitting too much and is exactly why the screen may be near-inert.
    * Idea 401: data/prices.csv was restated after 132/142 were committed while the broad and
      small caches were not; the gate below is arm-identity, which is insensitive to that, and
      no metric is re-derived from prices for the census rows.
    * The parents' OOS metric columns are taken as committed.  This run re-derives POOLS and
      PICKS, not backtests; PANEL 4's v2/SPY leg is the one freshly computed thing.
    * Idea 126: every row is quoted at t+1 execution, 10/25 bps (and 0 bps where the parent
      swept it), per PROTOCOL rule 2.

Deterministic, standalone.  Writes .console.txt, .census.csv, .paired.csv, .keeppaths.csv and
.walkforward.csv next to itself.  Modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_does-the-4b-aware-screen-only-pay-through-DD_B"
OUT = ROOT / "research" / "backtests"

SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
METRICS = ["OOS_MaxDD", "OOS_Sharpe", "OOS_CAGR"]
OOS_START = "2017-01-01"

# (tag, stem, unscreened mask column, {screen label: mask column}, picks-file key columns)
FILES = [
    ("132", "2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud",
     "adm_S0", {"S1": "adm_S1", "S2": "adm_S2"}, ("sel", "screen"), "arm"),
    ("142", "2026-09-08_selector-comparison-needs-more-cells_B",
     "adm_S0", {"S1": "adm_S1", "S2": "adm_S2"}, ("sel", "screen"), "arm"),
    ("151", "2026-09-08_does-any-selector-beat-doing-nothing_B",
     "adm_P_ALL", {"S1": "adm_P_S1"}, ("default", "pool"), "arm"),
    ("416", "2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud",
     "adm_P_ALL", {"S1": "adm_P_S1"}, ("default", "pool"), "pick"),
]
POOL_LABEL = {"132": {"U": "S0", "S1": "S1", "S2": "S2"},
              "142": {"U": "S0", "S1": "S1", "S2": "S2"},
              "151": {"U": "P_ALL", "S1": "P_S1"},
              "416": {"U": "P_ALL", "S1": "P_S1"}}

LINES = []


def say(s=""):
    print(s)
    LINES.append(s)


# ---------------------------------------------------------------- pick machinery
def pick_arm(cell, mask_col, is_col):
    """The parents' pick rule, re-derived: sort by arm, apply mask, argmax the IS column,
    fall back to the control arm when the mask admits nothing."""
    s = cell.sort_values("arm").reset_index(drop=True)
    cand = s[s[mask_col]] if mask_col in s.columns else s
    if not len(cand):
        return s[s.arm == "control"].iloc[0].arm, True, 0
    return cand.loc[cand[is_col].idxmax()].arm, False, len(cand)


def gate(tag, stem, u_col, screens, keycols, armcol):
    """Reproduce every deterministic committed pick arm-for-arm.  Returns (grid, ok, n, hits)."""
    g = pd.read_csv(OUT / f"{stem}.grid.csv")
    p = pd.read_csv(OUT / f"{stem}.picks.csv")
    selkey, poolkey = keycols
    lab = POOL_LABEL[tag]
    rows = []
    for (pk, b, c), s in g.groupby(["panel", "book", "cost"], sort=True):
        for sel, is_col in SELECTORS.items():
            for key, col in [("U", u_col)] + [(k, v) for k, v in screens.items()]:
                a, _, _ = pick_arm(s, col, is_col)
                rows.append(dict(panel=pk, book=b, cost=c, **{selkey: sel, poolkey: lab[key]},
                                 arm_re=a))
    R = pd.DataFrame(rows)
    m = p.merge(R, on=["panel", "book", "cost", selkey, poolkey], how="inner")
    hits = int((m[armcol] == m.arm_re).sum())
    return g, hits == len(m) and len(m) > 0, len(m), hits


# ---------------------------------------------------------------- census build
def build_census(tag, g, u_col, screens):
    """One row per (file, cell, selector, screen variant): the unscreened pick, the screened
    pick, the ungated control, and every committed OOS/KEEP column for each."""
    has_oos4b = "pass4b_oos" in g.columns
    a4a = "pass4a_v2" if "pass4a_v2" in g.columns else "pass4a"
    rows = []
    for (pk, b, c), s in g.groupby(["panel", "book", "cost"], sort=True):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl = s[s.arm == "control"].iloc[0]
        for sel, is_col in SELECTORS.items():
            ua, _, un = pick_arm(s, u_col, is_col)
            U = s[s.arm == ua].iloc[0]
            for scr, col in screens.items():
                sa, fell, sn = pick_arm(s, col, is_col)
                S = s[s.arm == sa].iloc[0]
                r = dict(file=tag, panel=pk, book=b, cost=c, sel=sel, screen=scr,
                         u_arm=ua, s_arm=sa, moved=bool(sa != ua), pool_empty=fell,
                         n_arms=len(s), n_admitted=sn,
                         ctl_arm=ctl.arm)
                for m in METRICS:
                    r[f"U_{m}"], r[f"S_{m}"], r[f"C_{m}"] = float(U[m]), float(S[m]), float(ctl[m])
                    r[f"d_{m}"] = float(S[m]) - float(U[m])          # screen minus unscreened
                    r[f"uc_{m}"] = float(U[m]) - float(ctl[m])       # unscreened minus control
                    r[f"sc_{m}"] = float(S[m]) - float(ctl[m])       # screened minus control
                for nm, src in (("U", U), ("S", S), ("C", ctl)):
                    r[f"{nm}_pass4a"] = bool(src[a4a])
                    r[f"{nm}_pass4b"] = bool(src["pass4b"])
                    r[f"{nm}_pass4b_oos"] = bool(src["pass4b_oos"]) if has_oos4b else np.nan
                r["has_4b_oos"] = has_oos4b
                rows.append(r)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- statistics
def paired(x, label, **extra):
    """Paired-difference summary of a single series: n, mean, t, W/L/T, two-sided sign p."""
    x = pd.Series(x).dropna().astype(float)
    n = len(x)
    if n == 0:
        return dict(label=label, n=0, mean=np.nan, t=np.nan, wins=0, losses=0, ties=0,
                    sign_p=np.nan, **extra)
    w, l = int((x > 0).sum()), int((x < 0).sum())
    sd = x.std(ddof=1)
    t = float(x.mean() / (sd / np.sqrt(n))) if n > 1 and sd > 0 else np.nan
    nz = w + l
    if nz:                                   # exact two-sided binomial sign test, p=0.5
        k = min(w, l)
        c = sum(np.exp(_lchoose(nz, i) - nz * np.log(2.0)) for i in range(0, k + 1))
        sp = float(min(1.0, 2.0 * c))
    else:
        sp = np.nan
    return dict(label=label, n=n, mean=float(x.mean()), t=t, wins=w, losses=l,
                ties=n - w - l, sign_p=sp, **extra)


def _lchoose(n, k):
    from math import lgamma
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def fmt(d, unit="pp", scale=100.0):
    m = d["mean"] * (scale if unit == "pp" else 1.0)
    u = " pp" if unit == "pp" else ""
    return (f"n {d['n']:4d}  mean {m:+8.4f}{u}  t {d['t']:+6.2f}  "
            f"{d['wins']:3d}W/{d['losses']:3d}L/{d['ties']:3d}T  sign p {d['sign_p']:.4f}"
            if d["n"] else f"n {d['n']:4d}  (empty)")


# ---------------------------------------------------------------- main
def main():
    say("=" * 108)
    say("IDEA 163 — does the 4b-aware screen only pay through DRAWDOWN?  (lane B, 2026-09-08)")
    say("Census of every committed grid carrying a 4b-aware admission mask.  0 tuned parameters.")
    say("=" * 108)

    # ---- gate -------------------------------------------------------------
    say("\n[GATE] every deterministic committed pick must reproduce arm-for-arm from the grid")
    admitted, grids = [], {}
    for tag, stem, u_col, screens, keycols, armcol in FILES:
        g, ok, n, hits = gate(tag, stem, u_col, screens, keycols, armcol)
        say(f"  {tag}: {hits}/{n} picks reproduced  ->  {'ADMITTED' if ok else 'REJECTED'}"
            f"   ({len(g)} rows, {g.groupby(['panel','book','cost']).ngroups} cells)")
        if ok:
            admitted.append((tag, u_col, screens))
            grids[tag] = g
    say(f"  {len(admitted)} of {len(FILES)} files admitted; K_Random excluded from the gate and "
        f"from every reading (RNG order not reconstructible from a grid).")
    if not admitted:
        say("  NO FILE ADMITTED — nothing can be read.  Stopping.")
        return

    # ---- census -----------------------------------------------------------
    C = pd.concat([build_census(t, grids[t], u, s) for t, u, s in admitted], ignore_index=True)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    cells = C.groupby(["file", "panel", "book", "cost"]).ngroups
    say(f"\n[CENSUS] {len(C)} rows | {cells} (file,cell) pairs | "
        f"{C.groupby(['panel','book','cost']).ngroups} DISTINCT (panel,book,cost) cells | "
        f"selectors {sorted(C.sel.unique())} | screens {sorted(C.screen.unique())}")
    say(f"         panels {sorted(C.panel.unique())} | cost rungs {sorted(C.cost.unique())}")

    # dedup rule for pooled readings, stated before use
    order = {"416": 0, "151": 1, "142": 2, "132": 3}      # newest/widest schema wins a duplicate
    C["_o"] = C.file.map(order)
    D = (C.sort_values("_o").drop_duplicates(["panel", "book", "cost", "sel", "screen"])
         .drop(columns="_o"))
    say(f"         DEDUP for pooled readings: one row per (panel,book,cost,sel,screen), file "
        f"preferred 416>151>142>132  ->  {len(D)} distinct rows (from {len(C)}).")

    # ---- inertness --------------------------------------------------------
    say("\n" + "-" * 108)
    say("[PANEL 0] INERTNESS — the screen cannot express anything on a pick it does not move")
    say("-" * 108)
    rows = []
    for (f, scr), s in C.groupby(["file", "screen"]):
        mv = int(s.moved.sum())
        rows.append(dict(file=f, screen=scr, n=len(s), moved=mv, rate=mv / len(s),
                         empty=int(s.pool_empty.sum()),
                         med_admitted=float(s.n_admitted.median())))
        say(f"  {f} {scr}: moves {mv:4d} of {len(s):4d} picks ({mv/len(s):5.1%}); "
            f"pool empty in {int(s.pool_empty.sum()):3d}; median admitted "
            f"{s.n_admitted.median():.1f} of {int(s.n_arms.iloc[0])} arms")
    mv_all = int(D[D.screen == "S1"].moved.sum()); n_all = int((D.screen == "S1").sum())
    say(f"  POOLED (distinct cells, S1): the screen moves {mv_all} of {n_all} picks "
        f"({mv_all/n_all:.1%}).")

    # ---- PANEL 1: the screen's price -------------------------------------
    say("\n" + "=" * 108)
    say("[PANEL 1] THE SCREEN'S PRICE — screened pick MINUS unscreened pick, same selector,")
    say("          same cell, same untouched OOS window.  Positive d_OOS_MaxDD = SHALLOWER.")
    say("=" * 108)
    P = []
    for scope, frame, sname in [("POOLED-DISTINCT", D, "pooled")] + \
                               [(f"FILE {t}", C[C.file == t], t) for t, _, _ in admitted]:
        for scr in sorted(frame.screen.unique()):
            s = frame[frame.screen == scr]
            for subset, sub in [("ALL", s), ("MOVED", s[s.moved])]:
                say(f"\n  {scope:16s} {scr}  {subset:5s}")
                for m in METRICS:
                    unit = "pp" if m != "OOS_Sharpe" else "raw"
                    d = paired(sub[f"d_{m}"], f"{scope}|{scr}|{subset}|{m}",
                               scope=scope, file=sname, screen=scr, subset=subset,
                               metric=m, comparison="S_minus_U")
                    P.append(d)
                    say(f"      d {m:11s} {fmt(d, unit)}")
                if len(sub):
                    dd = sub["d_OOS_MaxDD"].mean() * 100
                    dc = sub["d_OOS_CAGR"].mean() * 100
                    say(f"      exchange rate: {dc:+.3f} pp OOS CAGR per "
                        f"{dd:+.3f} pp OOS MaxDD"
                        + (f"   ({dc/dd:+.3f} pp CAGR per +1 pp of shallower DD)"
                           if abs(dd) > 1e-9 else "   (no DD move)"))

    # ---- PANEL 1b: the FALLBACK confound, decomposed ----------------------
    say("\n" + "=" * 108)
    say("[PANEL 1b] THE FALLBACK CONFOUND — decomposed, because Panel 0 says the screen admits")
    say("           NOTHING in most cells.  When the pool is empty the 'screened pick' IS the")
    say("           ungated control arm, so a pooled Panel-1 number mixes two different objects:")
    say("             EMPTY-POOL  the screen selected nothing and the cell fell back to")
    say("                         DO-NOTHING.  Any d here is idea 418's menu effect in reverse,")
    say("                         not a statement about screening.")
    say("             LIVE-POOL   the screen admitted >=1 arm and the selector chose inside it.")
    say("                         THIS is the only place the screen itself can be priced.")
    say("=" * 108)
    for scr in sorted(D.screen.unique()):
        s = D[D.screen == scr]
        for subname, sub in [("EMPTY-POOL (fell back to control)", s[s.pool_empty & s.moved]),
                             ("LIVE-POOL, pick MOVED", s[~s.pool_empty & s.moved]),
                             ("LIVE-POOL, pick UNCHANGED", s[~s.pool_empty & ~s.moved])]:
            say(f"\n  {scr}  {subname}   (n {len(sub)})")
            if not len(sub):
                say("      (empty)")
                continue
            for m in METRICS:
                unit = "pp" if m != "OOS_Sharpe" else "raw"
                d = paired(sub[f"d_{m}"], f"1b|{scr}|{subname}|{m}", scope="POOLED-DISTINCT",
                           file="pooled", screen=scr, subset=subname, metric=m,
                           comparison="S_minus_U")
                P.append(d)
                say(f"      d {m:11s} {fmt(d, unit)}")
    say("\n  PER-FILE replication of the LIVE-POOL/MOVED reading (the screen's own price):")
    for t, _, _ in admitted:
        sub = C[(C.file == t) & (C.screen == "S1") & ~C.pool_empty & C.moved]
        if not len(sub):
            say(f"    {t}: no live-pool moved cells")
            continue
        dd = paired(sub["d_OOS_MaxDD"], f"1b|file{t}", scope=f"FILE {t}", file=t, screen="S1",
                    subset="LIVE-POOL/MOVED", metric="OOS_MaxDD", comparison="S_minus_U")
        sh = paired(sub["d_OOS_Sharpe"], f"1b|file{t}|sh", scope=f"FILE {t}", file=t, screen="S1",
                    subset="LIVE-POOL/MOVED", metric="OOS_Sharpe", comparison="S_minus_U")
        cg = paired(sub["d_OOS_CAGR"], f"1b|file{t}|cg", scope=f"FILE {t}", file=t, screen="S1",
                    subset="LIVE-POOL/MOVED", metric="OOS_CAGR", comparison="S_minus_U")
        P += [dd, sh, cg]
        say(f"    {t}: n {dd['n']:3d}  dDD {dd['mean']*100:+7.3f} pp (t {dd['t']:+5.2f})  "
            f"dSharpe {sh['mean']:+7.4f} (t {sh['t']:+5.2f})  "
            f"dCAGR {cg['mean']*100:+7.3f} pp (t {cg['t']:+5.2f})")

    # per-selector reading, pooled, MOVED only
    say("\n  PER SELECTOR (pooled-distinct, S1, MOVED cells only):")
    for sel in sorted(D.sel.unique()):
        sub = D[(D.screen == "S1") & D.moved & (D.sel == sel)]
        for m in METRICS:
            d = paired(sub[f"d_{m}"], f"perSel|{sel}|{m}", scope="POOLED-DISTINCT", file="pooled",
                       screen="S1", subset=f"MOVED/{sel}", metric=m, comparison="S_minus_U")
            P.append(d)
        say(f"    {sel:9s} dDD {paired(sub['d_OOS_MaxDD'],'')['mean']*100:+7.3f} pp  "
            f"dSharpe {paired(sub['d_OOS_Sharpe'],'')['mean']:+7.4f}  "
            f"dCAGR {paired(sub['d_OOS_CAGR'],'')['mean']*100:+7.3f} pp  (n {len(sub)})")

    # ---- PANEL 2: the selector, rescored on drawdown ----------------------
    say("\n" + "=" * 108)
    say("[PANEL 2] THE SELECTOR, RESCORED — each selector MINUS the do-nothing control (hold")
    say("          the cell's ungated control arm), inside each pool, on all three OOS metrics.")
    say("          This is idea 163's 'score OOS DRAWDOWN rather than OOS Sharpe' half.")
    say("=" * 108)
    for pool_key, pool_name in [("uc", "UNSCREENED pool"), ("sc", "SCREENED pool (S1)")]:
        frame = D[D.screen == "S1"] if pool_key == "sc" else \
            D.drop_duplicates(["panel", "book", "cost", "sel"])
        say(f"\n  {pool_name} — selector minus do-nothing, pooled over distinct cells:")
        for sel in sorted(frame.sel.unique()):
            sub = frame[frame.sel == sel]
            out = []
            for m in METRICS:
                d = paired(sub[f"{pool_key}_{m}"], f"{pool_key}|{sel}|{m}",
                           scope="POOLED-DISTINCT", file="pooled",
                           screen=("S1" if pool_key == "sc" else "U"), subset="vs_do_nothing",
                           metric=m, comparison=f"{sel}_minus_control")
                P.append(d)
                v = d["mean"] * (100 if m != "OOS_Sharpe" else 1)
                out.append(f"{m.replace('OOS_',''):6s} {v:+7.3f} (t {d['t']:+5.2f}, p {d['sign_p']:.3f})")
            say(f"    {sel:9s} " + " | ".join(out))

    pd.DataFrame(P).to_csv(OUT / f"{STEM}.paired.csv", index=False)

    # ---- PANEL 3: KEEP paths ---------------------------------------------
    say("\n" + "=" * 108)
    say("[PANEL 3] KEEP PATHS — does the screen BUY 4b passes?  (idea 152's instance is exactly")
    say("          a 4b(OOS-window) pass bought by the screen; here is its population.)")
    say("=" * 108)
    K = []
    for scope, frame in [("POOLED-DISTINCT", D)] + [(f"FILE {t}", C[C.file == t])
                                                    for t, _, _ in admitted]:
        for scr in sorted(frame.screen.unique()):
            s = frame[frame.screen == scr]
            for path, cols in [("4a(v2)", ("U_pass4a", "S_pass4a")),
                               ("4b(full)", ("U_pass4b", "S_pass4b")),
                               ("4b(OOS)", ("U_pass4b_oos", "S_pass4b_oos"))]:
                uc, sc = cols
                sub = s.dropna(subset=[uc, sc])
                if not len(sub):
                    continue
                u = sub[uc].astype(bool); v = sub[sc].astype(bool)
                gain = int((~u & v).sum()); loss = int((u & ~v).sum())
                K.append(dict(scope=scope, screen=scr, path=path, n=len(sub),
                              U_pass=int(u.sum()), S_pass=int(v.sum()),
                              screen_gains=gain, screen_loses=loss, net=gain - loss))
                say(f"  {scope:16s} {scr} {path:9s}: unscreened {int(u.sum()):4d}/{len(sub):4d} "
                    f"pass, screened {int(v.sum()):4d}/{len(sub):4d}; screen GAINS {gain}, "
                    f"LOSES {loss}, NET {gain-loss:+d}")
    pd.DataFrame(K).to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say("  BOTH PATHS (a row passing 4a(v2) AND 4b): "
        f"unscreened {int((D.U_pass4a & D.U_pass4b).sum())}, "
        f"screened {int((D.S_pass4a & D.S_pass4b).sum())} of {len(D)}.")

    # ---- PANEL 4: levels vs the live book and SPY -------------------------
    say("\n" + "=" * 108)
    say("[PANEL 4] LEVELS on the untouched OOS window (2017-01-01..) against the LIVE book")
    say("          and SPY.  The RULES v2 / SPY leg is COMPUTED HERE from research/baseline.py.")
    say("=" * 108)
    px = load_universe()
    spy_oos = metrics(px["SPY"].pct_change().fillna(0).loc[OOS_START:])
    wf = []
    for c in (10.0, 25.0):
        r = backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[OOS_START:]
        m = metrics(r)
        wf.append(dict(leg=f"RULES v2 (live book) @{c:.0f}bps", CAGR=m["CAGR"],
                       Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], n=np.nan))
        say(f"  RULES v2 @{c:.0f} bps  OOS CAGR {m['CAGR']:7.2%}  Sharpe {m['Sharpe']:.4f}  "
            f"MaxDD {m['MaxDD']:7.2%}   [freshly computed, universe.json panel]")
    wf.append(dict(leg="SPY buy-and-hold", CAGR=spy_oos["CAGR"], Sharpe=spy_oos["Sharpe"],
                   MaxDD=spy_oos["MaxDD"], n=np.nan))
    say(f"  SPY               OOS CAGR {spy_oos['CAGR']:7.2%}  Sharpe {spy_oos['Sharpe']:.4f}  "
        f"MaxDD {spy_oos['MaxDD']:7.2%}")
    say("  4b OOS bars off this SPY leg: CAGR floor "
        f"{0.70*spy_oos['CAGR']:.2%}, MaxDD cap {0.60*spy_oos['MaxDD']:.2%}.")
    say("")
    S1 = D[D.screen == "S1"]
    for nm, pre in [("do-nothing control", "C"), ("UNSCREENED pick", "U"), ("SCREENED pick", "S")]:
        say(f"  {nm:20s} mean OOS CAGR {S1[f'{pre}_OOS_CAGR'].mean():7.2%}  "
            f"Sharpe {S1[f'{pre}_OOS_Sharpe'].mean():.4f}  "
            f"MaxDD {S1[f'{pre}_OOS_MaxDD'].mean():7.2%}   (n {len(S1)} distinct rows)")
        wf.append(dict(leg=f"census mean, {nm}", CAGR=S1[f"{pre}_OOS_CAGR"].mean(),
                       Sharpe=S1[f"{pre}_OOS_Sharpe"].mean(),
                       MaxDD=S1[f"{pre}_OOS_MaxDD"].mean(), n=len(S1)))
    mvd = S1[S1.moved]
    for nm, pre in [("UNSCREENED pick", "U"), ("SCREENED pick", "S")]:
        say(f"  MOVED cells only: {nm:16s} OOS CAGR {mvd[f'{pre}_OOS_CAGR'].mean():7.2%}  "
            f"Sharpe {mvd[f'{pre}_OOS_Sharpe'].mean():.4f}  "
            f"MaxDD {mvd[f'{pre}_OOS_MaxDD'].mean():7.2%}   (n {len(mvd)})")
        wf.append(dict(leg=f"census mean MOVED, {nm}", CAGR=mvd[f"{pre}_OOS_CAGR"].mean(),
                       Sharpe=mvd[f"{pre}_OOS_Sharpe"].mean(),
                       MaxDD=mvd[f"{pre}_OOS_MaxDD"].mean(), n=len(mvd)))
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---- verdict ----------------------------------------------------------
    say("\n" + "=" * 108)
    say("[VERDICT] the pre-registered decision rule, applied")
    say("=" * 108)
    mv = D[(D.screen == "S1") & D.moved]
    dDD = paired(mv["d_OOS_MaxDD"], "final_DD")
    dSH = paired(mv["d_OOS_Sharpe"], "final_Sharpe")
    dCG = paired(mv["d_OOS_CAGR"], "final_CAGR")
    signs = {}
    for t, _, _ in admitted:
        s = C[(C.file == t) & (C.screen == "S1") & C.moved]
        signs[t] = float(s["d_OOS_MaxDD"].mean()) if len(s) else np.nan
    n_pos = sum(1 for v in signs.values() if v > 0)
    say(f"  moved cells (pooled, S1): n {len(mv)}")
    say(f"  d OOS MaxDD  {fmt(dDD)}")
    say(f"  d OOS Sharpe {fmt(dSH,'raw')}")
    say(f"  d OOS CAGR   {fmt(dCG)}")
    say(f"  per-file sign of mean d OOS MaxDD: " +
        ", ".join(f"{k} {v*100:+.3f} pp" for k, v in signs.items()) +
        f"  -> positive in {n_pos} of {len(signs)}")
    dd_sig = (not np.isnan(dDD["t"])) and abs(dDD["t"]) >= 2 and dDD["mean"] > 0
    sh_sig = (not np.isnan(dSH["t"])) and abs(dSH["t"]) >= 2
    if dDD["mean"] is not np.nan and dDD["mean"] <= 0:
        verdict = "COST — the screen does not even buy drawdown"
    elif dd_sig and not sh_sig and n_pos >= 3:
        verdict = "SELL-AS-DD — the screen's value is drawdown control and should be sold as that"
    elif (not dd_sig) and (not sh_sig) and abs(dCG["t"]) < 2:
        verdict = "NULL — idea 152's instance does not generalise on any OOS metric"
    else:
        verdict = "MIXED — see panels; the pre-registered rule does not fire cleanly"
    say(f"\n  PRE-REGISTERED VERDICT (as written, on ALL moved cells): {verdict}")
    if abs(dDD["mean"]) > 1e-9:
        say(f"  exchange rate on moved cells: {dCG['mean']*100:+.3f} pp OOS CAGR for "
            f"{dDD['mean']*100:+.3f} pp OOS MaxDD "
            f"({dCG['mean']/dDD['mean']:+.3f} pp CAGR per +1 pp shallower DD).")

    say("\n  DECLARED POST-HOC (the pre-registration did not anticipate Panel 0's empty pools;")
    say("  this reading is labelled post-hoc and does NOT overwrite the rule above):")
    lp = D[(D.screen == "S1") & ~D.pool_empty & D.moved]
    lDD, lSH, lCG = (paired(lp["d_OOS_MaxDD"], "lp_DD"), paired(lp["d_OOS_Sharpe"], "lp_SH"),
                     paired(lp["d_OOS_CAGR"], "lp_CG"))
    lsigns = {}
    for t, _, _ in admitted:
        s = C[(C.file == t) & (C.screen == "S1") & ~C.pool_empty & C.moved]
        lsigns[t] = float(s["d_OOS_MaxDD"].mean()) if len(s) else np.nan
    lpos = sum(1 for v in lsigns.values() if v > 0)
    say(f"  LIVE-POOL moved cells: n {len(lp)}")
    say(f"    d OOS MaxDD  {fmt(lDD)}")
    say(f"    d OOS Sharpe {fmt(lSH,'raw')}")
    say(f"    d OOS CAGR   {fmt(lCG)}")
    say(f"    per-file sign of mean d OOS MaxDD: " +
        ", ".join(f"{k} {v*100:+.3f} pp" for k, v in lsigns.items() if not np.isnan(v)) +
        f"  -> positive in {lpos} of {len([v for v in lsigns.values() if not np.isnan(v)])}")
    ldd_sig = (not np.isnan(lDD["t"])) and abs(lDD["t"]) >= 2 and lDD["mean"] > 0
    lsh_sig = (not np.isnan(lSH["t"])) and abs(lSH["t"]) >= 2
    if lDD["mean"] <= 0:
        lverdict = "COST — screening inside a live pool does not buy drawdown either"
    elif ldd_sig and not lsh_sig and lpos >= 3:
        lverdict = "SELL-AS-DD"
    elif (not ldd_sig) and (not lsh_sig) and abs(lCG["t"]) < 2:
        lverdict = "NULL"
    else:
        lverdict = "MIXED"
    say(f"    SAME RULE ON THE LIVE-POOL OBJECT: {lverdict}")
    ep = D[(D.screen == "S1") & D.pool_empty & D.moved]
    say(f"    share of the pooled Panel-1 drawdown move carried by EMPTY-POOL fallback: "
        f"{(ep['d_OOS_MaxDD'].sum() / D[(D.screen=='S1') & D.moved]['d_OOS_MaxDD'].sum()):.1%} "
        f"of the total, on {len(ep)} of {len(D[(D.screen=='S1') & D.moved])} moved cells.")
    say("\n  PROTOCOL.md NOT modified.  No book promoted.  RULES.md / scan.py / bot.py / "
        "baseline.py untouched.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
