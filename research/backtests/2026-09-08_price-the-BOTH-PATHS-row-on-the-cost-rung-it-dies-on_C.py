#!/usr/bin/env python3
"""QUEUE idea 414 — price-the-BOTH-PATHS-row-on-the-cost-rung-it-dies-on  (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 414)
    "idea 142's both-paths candidate clears every bar at 10 bps by +0.61 pp (u56) / +0.84 pp
     (broad) of CAGR and fails at 25 bps on both panels, on 8.2x/10.9x annual turnover.  Sweep
     the rung finely (10, 12, 15, 18, 20, 25 bps) and report c*, the rung at which each of the
     five 4b bars and the 4a drawdown bar crosses, so the Sunday review sees the execution
     assumption the candidate rests on rather than a binary.  Max 2 params."

THE ROW UNDER TEST — idea 142's, not re-specified here
    panel in {u56, broad}, book S3-50 (idea 133's blend: 0.50 x composite-ranked TOP20 +
    0.50 x the TLT/GLD/UUP momentum-vote x risk-parity sleeve, rescaled to gross 0.75),
    arm band3-rw (the 200d +/-3% hysteresis band in the RE-WEIGHT convention), weekly, t+1.
    These are the only two of idea 142's 150 keep-path rows with full_4a_v2 AND full_4b True.
    Book construction is IMPORTED from idea 133 (D.book_weights) and idea 94 (H.run,
    H.arm_specs, H.halves, H.window, H.pass4a) and idea 129 (C.bars_win, C.margins_at,
    C.fails), so the row priced here is literally idea 142's row, re-derived not re-coded.

WHAT IS BEING MEASURED
    A cost rung is not a parameter of the book; it is an assumption about execution.  Idea 142
    published a binary (passes at 10, fails at 25).  A binary hides which of the six bars gives
    way and how much execution slack the candidate actually owns.  This run reports, for each
    bar, c* = the rung at which that bar's margin crosses zero, and the BINDING bar (smallest
    c*) per panel and per window.  A candidate whose c* is 10.4 bps is a different object from
    one whose c* is 24.9 bps, and the Sunday review cannot tell them apart from idea 142's row.

    EXACTNESS.  With no stop / no drawdown control / no entry budget, both H.run and
    engine.backtest hold a weight path that does not depend on the cost rung, so
        r(c) = r(0) - turnover * c / 1e4
    is an IDENTITY, not an approximation.  Every rung on the fine grid is therefore computed
    exactly from one zero-cost run, and check (a) asserts the identity against a real H.run at
    each of the six named rungs.  c* is then located by bisection on a continuous margin.

TUNED PARAMETERS — exactly two, both fully reported
    1. the cost rung c: named grid {10, 12, 15, 18, 20, 22, 25} bps, every point reported;
       plus a 0.05-bps scan over [0, 60] used only to LOCATE the crossings.
    2. the 4a comparand convention (idea 398's open defect), 2 values:
         MATCHED  RULES v2 priced at the same rung as the arm  [idea 142's convention]
         FIXED10  RULES v2 priced at 10 bps whatever the arm pays
       Reported for both; the headline uses MATCHED because that is what idea 142's row means.
    Panels (u56, broad), windows (full / IS / OOS), and the individual bars are REPORTED AXES,
    never selected on.  Nothing about the book itself is tuned here.

THE SIX BARS (PROTOCOL rule 4, with idea 129's coefficients phi=0.70, delta=0.60)
    4b_H1    book H1 Sharpe   - SPY H1 Sharpe          > 0
    4b_H2    book H2 Sharpe   - SPY H2 Sharpe          > 0
    4b_OOS   book OOS Sharpe  - SPY OOS Sharpe         > 0      (rule 8)
    4b_DD    0.60*|SPY MaxDD| - |book MaxDD|           > 0
    4b_CAGR  book CAGR        - 0.70*SPY CAGR          > 0
    4a_DD    book MaxDD       - RULES v2 MaxDD         >= 0     (the queue's named bar)
    4a_H1 / 4a_H2 are carried too, because 4a is a conjunction and the review needs to know
    whether the DD bar is the one that gives way first.

WALK-FORWARD (PROTOCOL rule 8) — run in the form this idea admits
    The book has no fitted parameter to walk forward; the rung is the dial.  So rule 8 is run
    ON THE RUNG: c* is located on the IS window (2009-2016) alone, and the OOS window
    (2017-2026) is then read ONCE at that IS-chosen rung and at every named rung, reported
    against RULES v2 (live), RULES v1 and SPY.  If the IS window says the candidate owns 22 bps
    of slack and the OOS window says 11, the published execution assumption is IS-fitted.

PRE-REGISTERED PREDICTIONS (written before any number in this file was read)
    P1  The binding bar at the crossing is CAGR on both panels (idea 404/142: 4b's floor is the
        bar that moves with cost, the Sharpe bars move slowly and the DD bars barely at all).
    P2  c*_4b lands between 10 and 25 bps on both panels, i.e. idea 142's binary is real and
        the candidate's slack is a single-digit number of bps.
    P3  c*(4a_DD) is far outside [10, 25] on both panels: a drawdown ratio is nearly invariant
        to a proportional cost drag, so 4a dies (if it dies) on its Sharpe legs, not its DD leg.
    P4  The FIXED10 convention gives a LOWER c* for the 4a bars than MATCHED, because under
        MATCHED the comparand is taxed too.

CAVEATS carried, not buried
    * Survivorship (idea 54): u56 and broad are current constituents; every CAGR here is
      optimistic, so every c* driven by the CAGR floor is an UPPER bound on the real slack.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so IS-window DD
      bars are measured on a window that cannot express a deep drawdown.
    * Idea 401: data/prices.csv was restated after idea 133 was committed while the broad cache
      was not, so the u56 leg reproduces idea 142 to ~1e-5 and the broad leg exactly; check (b)
      reports the per-panel tolerance instead of asserting one number.
    * Idea 126: every row is quoted at t+1 execution only.  A 25-bps rung is a statement about
      spread+impact, not about a different execution rule.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .crossings.csv and .walkforward.csv
next to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_price-the-BOTH-PATHS-row-on-the-cost-rung-it-dies-on_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I142_KEEP = OUT / "2026-09-08_selector-comparison-needs-more-cells_B.keeppaths.csv"

PANELS = ["u56", "broad"]
BOOK, GATE, CONV, ARM = "S3-50", "band3", "rw", "band3-rw"
RUNGS = [10.0, 12.0, 15.0, 18.0, 20.0, 22.0, 25.0]     # tuned param 1, all reported
CONVENTIONS = ["MATCHED", "FIXED10"]                    # tuned param 2, both reported
PHI0, DELTA0 = 0.70, 0.60
SCAN_HI, SCAN_STEP = 60.0, 0.05                         # crossing locator only
BARS4B = ["H1", "H2", "OOS", "DD", "CAGR"]
BARS4A = ["H1", "H2", "DD"]

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
D = _load(I133, "i133")

FREQ, IS_END, OOS_START = H.FREQ, H.IS_END, H.OOS_START


# ------------------------------------------------------------------ affine cost algebra ----
class Affine:
    """A return series as (gross returns, per-day turnover): r(c) = r0 - to * c/1e4, exact."""

    def __init__(self, r0, to):
        self.r0, self.to = r0, to

    def at(self, c):
        return self.r0 - self.to * c / 1e4

    @property
    def ann_turnover(self):
        return self.to.sum() / metrics(self.r0)["Years"]


def arm_affine(px, start):
    W = D.book_weights(px, BOOK, GATE, CONV)
    res = H.run(px, W, bps=0.0)
    return Affine(res["r"].loc[start:], res["to"].loc[start:])


def engine_affine(px, weights, start):
    res = backtest(px, weights, cost_bps=0.0, freq=FREQ)
    return Affine(res["returns"].loc[start:], res["turnover"].loc[start:])


# ------------------------------------------------------------------ bars as functions of c ---
def margins4b(r, bars, which):
    return C.margins_at(r, bars, PHI0, DELTA0, which)


def margins4a(r, b, which):
    rw, bw = H.window(r, which), H.window(b, which)
    h1, h2 = H.halves(rw)
    b1, b2 = H.halves(bw)
    return dict(H1=h1 - b1, H2=h2 - b2,
                DD=metrics(rw)["MaxDD"] - metrics(bw)["MaxDD"])


def margin_fn(kind, bar, arm, base, bars, which, convention):
    """margin(c) for one bar; continuous in c.  4b bars ignore the convention (SPY is the
    comparand and pays no cost); 4a bars price RULES v2 at c (MATCHED) or at 10 bps (FIXED10)."""
    if kind == "4b":
        return lambda c: margins4b(arm.at(c), bars, which)[bar]
    cb = (lambda c: c) if convention == "MATCHED" else (lambda c: 10.0)
    return lambda c: margins4a(arm.at(c), base.at(cb(c)), which)[bar]


def crossing(f, lo=0.0, hi=SCAN_HI, step=SCAN_STEP, tol=1e-4):
    """First c in [lo, hi] where f crosses from > 0 to <= 0, by scan + bisection.
    Returns (c*, note).  note='fails at 0' if the bar never holds; 'holds past hi' if it
    survives the whole scan (either way c* is nan and the note carries the meaning)."""
    if f(lo) <= 0:
        return np.nan, "fails at 0"
    grid = np.arange(lo, hi + step / 2, step)
    prev = lo
    for c in grid[1:]:
        if f(float(c)) <= 0:
            a, b = prev, float(c)
            while b - a > tol:
                m = (a + b) / 2
                if f(m) > 0:
                    a = m
                else:
                    b = m
            return (a + b) / 2, "crosses"
        prev = float(c)
    return np.nan, f"holds past {hi:.0f}"


# ------------------------------------------------------------------------------- main -------
def main():
    say(f"=== {STEM} ===")
    say(f"row under test: book {BOOK}, arm {ARM}, weekly, t+1, panels {PANELS} "
        f"(idea 142's only two both-paths rows)")
    say(f"tuned params: (1) cost rung, named grid {RUNGS} + {SCAN_STEP}-bps scan to {SCAN_HI};"
        f" (2) 4a comparand convention {CONVENTIONS}")

    i142 = pd.read_csv(I142_KEEP)
    grid_rows, cross_rows, wf_rows = [], [], []

    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        BARS = {w: C.bars_win(spy, w) for w in ("full", "IS", "OOS")}
        arm = arm_affine(px, start)
        v2 = engine_affine(px, rules_v2_weights(px), start)
        v1 = engine_affine(px, rules_v1_weights(px), start)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])

        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {BARS['full']['s1']:.3f}/{BARS['full']['s2']:.3f} | OOS Sharpe "
            f"{mso['Sharpe']:.3f} CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        say(f"    annual turnover: arm {arm.ann_turnover:.2f}x, RULES v2 {v2.ann_turnover:.2f}x, "
            f"RULES v1 {v1.ann_turnover:.2f}x  (queue quotes 8.2x/10.9x for the arm)")

        # ---- (a) the affine identity that every fine-grid point rests on ----
        worst = 0.0
        W = D.book_weights(px, BOOK, GATE, CONV)
        for c in RUNGS:
            direct = H.run(px, W, bps=c)["r"].loc[start:]
            worst = max(worst, float((direct - arm.at(c)).abs().max()))
        worst_e = 0.0
        for c in RUNGS:
            direct = backtest(px, rules_v2_weights(px), cost_bps=c,
                              freq=FREQ)["returns"].loc[start:]
            worst_e = max(worst_e, float((direct - v2.at(c)).abs().max()))
        say(f"[a] affine-cost identity over {len(RUNGS)} rungs: arm max|diff| {worst:.3e}, "
            f"RULES v2 max|diff| {worst_e:.3e} "
            f"({'EXACT' if max(worst, worst_e) < 1e-14 else 'NOT EXACT - unsafe'})")

        # ---- (b) reproduction of idea 142's committed row at 10 and 25 bps ----
        ref = i142[(i142.panel == pk) & (i142.book == BOOK) & (i142.arm == ARM)]
        for _, rr in ref.iterrows():
            r = arm.at(float(rr["cost"]))
            m = metrics(r)
            h1, h2 = H.halves(r)
            mo = metrics(H.window(r, "OOS"))
            d = max(abs(m["CAGR"] - rr["CAGR"]), abs(m["Sharpe"] - rr["Sharpe"]),
                    abs(m["MaxDD"] - rr["MaxDD"]), abs(h1 - rr["H1"]), abs(h2 - rr["H2"]),
                    abs(mo["Sharpe"] - rr["OOS_Sharpe"]))
            say(f"[b] idea 142 row {pk}/{BOOK}/{ARM}@{rr['cost']:.0f}bps reproduced to "
                f"max|diff| {d:.3e} (CAGR {m['CAGR']:.4%} vs {rr['CAGR']:.4%}, "
                f"Sharpe {m['Sharpe']:.4f} vs {rr['Sharpe']:.4f})")

        # ---- the named grid: every rung, every bar, every window, both conventions ----
        for c in RUNGS:
            r = arm.at(c)
            for which in ("full", "IS", "OOS"):
                rw = H.window(r, which)
                m = metrics(rw)
                h1, h2 = H.halves(rw)
                m4b = margins4b(r, BARS[which], which)
                fail4b = C.fails(m4b)
                row = dict(panel=pk, book=BOOK, arm=ARM, cost=c, window=which,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           **{f"m4b_{k}": m4b[k] for k in BARS4B},
                           pass4b=(len(fail4b) == 0), fail4b=",".join(fail4b) or "-")
                for cv in CONVENTIONS:
                    b = v2.at(c if cv == "MATCHED" else 10.0)
                    m4a = margins4a(r, b, which)
                    row.update({f"m4a_{k}_{cv}": m4a[k] for k in BARS4A})
                    row[f"pass4a_{cv}"] = bool(m4a["H1"] > 0 and m4a["H2"] > 0 and m4a["DD"] >= 0)
                row["pass_both_MATCHED"] = bool(row["pass4b"] and row["pass4a_MATCHED"])
                grid_rows.append(row)

            # walk-forward table: OOS read against every comparand at this rung
            ro, bo2, bo1 = (H.window(r, "OOS"), H.window(v2.at(c), "OOS"),
                            H.window(v1.at(c), "OOS"))
            mo, mo2, mo1 = metrics(ro), metrics(bo2), metrics(bo1)
            wf_rows.append(dict(panel=pk, cost=c,
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                OOS_MaxDD=mo["MaxDD"],
                                v2_OOS_CAGR=mo2["CAGR"], v2_OOS_Sharpe=mo2["Sharpe"],
                                v2_OOS_MaxDD=mo2["MaxDD"],
                                v1_OOS_CAGR=mo1["CAGR"], v1_OOS_Sharpe=mo1["Sharpe"],
                                v1_OOS_MaxDD=mo1["MaxDD"],
                                spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                                spy_OOS_MaxDD=mso["MaxDD"],
                                dSharpe_vs_spy=mo["Sharpe"] - mso["Sharpe"],
                                dSharpe_vs_v2=mo["Sharpe"] - mo2["Sharpe"]))

        # ---- the crossings ----
        for which in ("full", "IS", "OOS"):
            for bar in BARS4B:
                cstar, note = crossing(margin_fn("4b", bar, arm, v2, BARS[which], which, None))
                cross_rows.append(dict(panel=pk, window=which, path="4b", bar=bar,
                                       convention="-", c_star=cstar, note=note,
                                       margin_at_10=margin_fn("4b", bar, arm, v2, BARS[which],
                                                              which, None)(10.0)))
            for cv in CONVENTIONS:
                for bar in BARS4A:
                    f = margin_fn("4a", bar, arm, v2, BARS[which], which, cv)
                    cstar, note = crossing(f)
                    cross_rows.append(dict(panel=pk, window=which, path="4a", bar=bar,
                                           convention=cv, c_star=cstar, note=note,
                                           margin_at_10=f(10.0)))

    G = pd.DataFrame(grid_rows)
    X = pd.DataFrame(cross_rows)
    WF = pd.DataFrame(wf_rows)

    # ------------------------------------------------------------------ reporting ----
    say("\n" + "=" * 110)
    say("NAMED GRID — every rung reported (window=full, PROTOCOL's own 4b reading)")
    for pk in PANELS:
        s = G[(G.panel == pk) & (G.window == "full")]
        say(f"\n[{pk}]")
        say(s[["cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "m4b_H1", "m4b_H2", "m4b_OOS",
               "m4b_DD", "m4b_CAGR", "pass4b", "fail4b", "m4a_DD_MATCHED", "pass4a_MATCHED",
               "pass4a_FIXED10", "pass_both_MATCHED"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 110)
    say("CROSSINGS c* (bps) — the rung at which each bar gives way")
    for pk in PANELS:
        for which in ("full", "IS", "OOS"):
            s = X[(X.panel == pk) & (X.window == which)]
            say(f"\n[{pk} / window={which}]")
            say(s[["path", "bar", "convention", "margin_at_10", "c_star", "note"]]
                .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
            live = s[np.isfinite(s.c_star)]
            for path, sub in live.groupby("path"):
                if path == "4a":
                    for cv, s2 in sub.groupby("convention"):
                        b = s2.loc[s2.c_star.idxmin()]
                        say(f"    binding {path}/{cv}: {b['bar']} at c* = {b['c_star']:.2f} bps")
                else:
                    b = sub.loc[sub.c_star.idxmin()]
                    say(f"    binding {path}: {b['bar']} at c* = {b['c_star']:.2f} bps")

    say("\n" + "=" * 110)
    say("HEADLINE — c* of the CANDIDATE (both paths together, MATCHED convention, window=full)")
    head = []
    for pk in PANELS:
        s = X[(X.panel == pk) & (X.window == "full") &
              ((X.path == "4b") | (X.convention == "MATCHED"))]
        live = s[np.isfinite(s.c_star)]
        c4b = live[live.path == "4b"].c_star.min() if (live.path == "4b").any() else np.nan
        c4a = live[live.path == "4a"].c_star.min() if (live.path == "4a").any() else np.nan
        cboth = np.nanmin([c4b, c4a])
        bind = live.loc[live.c_star.idxmin()] if len(live) else None
        head.append(dict(panel=pk, c_star_4b=c4b, c_star_4a=c4a, c_star_both=cboth,
                         binding_bar=f"{bind['path']}_{bind['bar']}" if bind is not None else "-",
                         slack_over_10bps=cboth - 10.0))
        say(f"  {pk}: c*(4b) {c4b:.2f}  c*(4a MATCHED) {c4a:.2f}  -> candidate dies at "
            f"{cboth:.2f} bps on {head[-1]['binding_bar']}; slack over the record's 10-bps rung "
            f"= {cboth - 10.0:.2f} bps")
    HEAD = pd.DataFrame(head)

    say("\n" + "=" * 110)
    say("RULE 8 WALK-FORWARD — OOS (2017-01-01..) at every named rung vs baselines and SPY")
    for pk in PANELS:
        s = WF[WF.panel == pk]
        say(f"\n[{pk}]")
        say(s[["cost", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_Sharpe", "v1_OOS_Sharpe",
               "spy_OOS_Sharpe", "dSharpe_vs_spy", "dSharpe_vs_v2"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        cis = X[(X.panel == pk) & (X.window == "IS") &
                ((X.path == "4b") | (X.convention == "MATCHED"))]
        cis = cis[np.isfinite(cis.c_star)]
        cos = X[(X.panel == pk) & (X.window == "OOS") &
                ((X.path == "4b") | (X.convention == "MATCHED"))]
        cos = cos[np.isfinite(cos.c_star)]
        cis_v = cis.c_star.min() if len(cis) else np.nan
        cos_v = cos.c_star.min() if len(cos) else np.nan
        say(f"    rule-8 on the rung: c* chosen on IS (2009-2016) alone = {cis_v:.2f} bps; the "
            f"OOS window read once gives {cos_v:.2f} bps "
            f"(IS overstates the slack by {cis_v - cos_v:+.2f} bps)")

    # 4b pass/fail on the OOS window at each named rung — the rule-8 verdict per rung
    say("\n  OOS-window 4b verdict per rung (rule 8's own reading):")
    say(G[G.window == "OOS"][["panel", "cost", "CAGR", "Sharpe", "MaxDD", "m4b_CAGR", "m4b_DD",
                              "pass4b", "fail4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 110)
    say("PREDICTIONS")
    for pk in PANELS:
        s = X[(X.panel == pk) & (X.window == "full")]
        b4b = s[(s.path == "4b") & np.isfinite(s.c_star)]
        p1 = b4b.loc[b4b.c_star.idxmin(), "bar"] if len(b4b) else "none"
        c = float(HEAD.loc[HEAD.panel == pk, "c_star_both"].iloc[0])
        dd = s[(s.path == "4a") & (s.bar == "DD") & (s.convention == "MATCHED")].iloc[0]
        m = s[(s.path == "4a") & (s.convention == "MATCHED") & np.isfinite(s.c_star)]
        f = s[(s.path == "4a") & (s.convention == "FIXED10") & np.isfinite(s.c_star)]
        say(f"  [{pk}] P1 binding 4b bar = {p1} ({'HELD' if p1 == 'CAGR' else 'FAILED'})")
        say(f"        P2 c*(candidate) = {c:.2f} bps "
            f"({'HELD' if 10.0 < c < 25.0 else 'FAILED'} vs the pre-registered (10,25))")
        say(f"        P3 4a_DD: c* {dd['c_star'] if np.isfinite(dd['c_star']) else dd['note']} "
            f"-> {'HELD' if not np.isfinite(dd['c_star']) or not (10 <= dd['c_star'] <= 25) else 'FAILED'}")
        mm = m.c_star.min() if len(m) else np.inf
        ff = f.c_star.min() if len(f) else np.inf
        say(f"        P4 binding 4a c*: MATCHED {mm:.2f} vs FIXED10 {ff:.2f} "
            f"({'HELD' if ff < mm else 'FAILED'})")

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    X.to_csv(OUT / f"{STEM}.crossings.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    HEAD.to_csv(OUT / f"{STEM}.headline.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.{{grid,crossings,walkforward,headline}}.csv and .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
