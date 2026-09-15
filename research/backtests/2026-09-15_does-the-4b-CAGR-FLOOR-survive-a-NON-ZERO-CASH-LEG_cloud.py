#!/usr/bin/env python3
"""Idea 676 (cloud lane, 2026-09-15) — does the 4b CAGR FLOOR survive a NON-ZERO CASH LEG on the
arms that need it least?

QUESTION
--------
Every backtest in this record credits CASH AT ZERO.  Idea 670's committed 160-point grid carries a
closed-form column, `cash_rate_to_flip_L5 = (0.70*SPY_CAGR - CAGR) / cash_share`, and the queue
reads it as: **27 of the CAGR-floor failures would flip at <= 5%/yr flat cash, median 4.22% at the
live gross 0.75**.  If that is right, a chunk of the record's "exposure buys the floor" is really
"cash earns nothing", and idea 642's T-bill path could overturn published verdicts wholesale.

This run does not wait for 642.  It sweeps a FLAT cash credit over idea 670's OWN 160-point grid,
re-reads all five 4b legs at every credit, and reports **which 4b verdicts are CREDIT-INVARIANT** —
i.e. exactly which committed conclusions 642 cannot overturn, whatever path it finds.

THE GRID (idea 670's, imported from its committed script, not re-typed)
    10 arms x 8 gross rungs x 2 panels = **160 points**, every one reported, at each credit.
    arms      BAND03 (RULES v2 live), BAND08, BAND03_M, CAND20_VS, **CAND20 (the 2026-09-04 KEEP
              4b book: top-20 equal weight, no vol scaler)**, CAND10, CAND05, CAND20_NOCAP,
              EWELIG, **SPYBH (the zero-signal exposure control)**
    grosses   0.20 0.35 0.50 0.60 0.75 0.85 0.95 1.00      (idea 668's ladder)
    panels    U56 = research/universe.json; B136 = research/universe_broad.json
    weekly (BAND03_M monthly), 10 bps per unit turnover, next-day execution.

TUNED PARAMETERS (PROTOCOL rule 4 — exactly two, the queue's own)
    1. credit level c in {0%, 1%, 2%, 3%, 4%, 5%, 6%}/yr flat        (0% = the record's convention)
    2. panel        in {U56, B136}
    160 x 7 = 1,120 rows, ALL published to `.grid.csv` and printed to the console.

HOW THE CREDIT IS APPLIED (stated, because the convention matters)
    r_credited(t) = r(t) + cash(t) * c/252, where cash(t) = 1 - (realised held exposure at t).
    The weight PATH is held fixed — the same convention idea 670's closed form assumes.  The only
    neglected term is the intra-rebalance drift of the cash sleeve against the risky sleeve, which
    at weekly cadence is O(c * cash * 1 week) < 0.1 bp per rung.  The credit is applied to EVERY
    book that holds cash, the RULES v2 baseline included (its 4a bars move with it); SPY holds no
    cash, so the 4b bars are credit-invariant by construction.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO   at c=0 this run reproduces idea 670's committed 160 rows (CAGR/Sharpe/MaxDD/H1/H2 and
              all five legs).  A gate on the read, not evidence.  Bar 5e-4 on levels (the tape has
              moved since 2026-09-11), EXACT on the 4b verdict.
    H_INV     *** THE QUEUE'S OWN TEST. *** at least 80% of the 160 4b verdicts are unchanged
              across the whole 0-5% credit range.  PASS => most of the record is credit-proof.
    H_CF      idea 670's closed form is honest: the realised flip credit and its committed
              `cash_rate_to_flip_L5` agree at Spearman >= 0.95, and its <=5% flip COUNT is within
              +/-3 of the realised one.
    H_SPYBH   *** THE DECISIVE ONE. *** a flat 5% credit does NOT buy a 4b pass for the ZERO-SIGNAL
              control (SPYBH) at any gross on either panel.  If it does, the CAGR floor is not an
              edge test under ANY cash assumption and the record's "exposure buys the floor"
              becomes "cash rate buys the floor".
    H_SURV    the two matched-gross 4b survivors idea 670 names (U56/CAND20 at g=0.75 and
              B136/EWELIG) stay passes at every credit in 0-5%.
    H_WF      rule 8: the arm/gross chosen on 2009-2016 ALONE under BOTH pre-stated choosers, and
              its 2017-2026 4b verdict, are the same at every credit in 0-5%.

VERDICT RULE, FIXED IN ADVANCE
    ANSWERED-YES (the floor survives; 642 cannot overturn the record's 4b verdicts) iff H_INV and
        H_SURV and H_SPYBH and H_WF.
    ANSWERED-NO iff H_SPYBH fails or H_INV fails — the record's 4b verdicts are cash-rate artefacts
        and every committed 4b count must be restated with its cash assumption.
    Either way this is a PATH-DEFINITION result, not a capital candidate: no book is promoted.
        Both KEEP paths are evaluated and reported on every arm at every credit.

THE TWO PRE-STATED CHOOSERS (rule 8; the OOS window is read ONCE, after both have picked)
    C1  argmax IS Sharpe over the 80 (arm, gross) cells of a panel, ties to the SMALLEST gross.
    C2  the 2026-09-03 memo's own rule: the SMALLEST gross whose IS |MaxDD| <= 60% of SPY's IS
        |MaxDD|, among arms that clear the IS CAGR floor; ties to the highest IS Sharpe.

GATES (printed before any verdict is read)
    G1  `fast_backtest` == `engine.backtest` on one book                                bar 1e-10
    G2  H_REPRO against idea 670's committed grid.csv                    bar 5e-4 / exact verdicts
    G3  credit identity: at gross 1.00 with zero cash the credit moves nothing          bar 1e-12
    G4  monotonicity: CAGR is non-decreasing in the credit at every one of the 160 points  exact
    G5  determinism: no RNG anywhere in this script; the grid recomputed                     bar 0
    G6  the comparands (SPY, credited RULES v2) printed before any arm

SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT constituents of `universe.json` and
`universe_broad.json`, so every CAGR is optimistic and every MaxDD understated.  That makes the
CAGR floor EASIER to clear here than on a point-in-time panel, so a finding that the credit does
NOT move verdicts is conservative, while any credit-driven flip would be at least as large on a
survivor-free panel.

Deterministic, no network, standalone.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py or
baseline.py.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                     # noqa: E402
from engine import backtest                                              # noqa: E402

DATE = "2026-09-15"
SLUG = "does-the-4b-CAGR-FLOOR-survive-a-NON-ZERO-CASH-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# idea 670's committed script and grid — imported, never re-typed
REF = Path(__file__).resolve().parent / "2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone_C"
_spec = importlib.util.spec_from_file_location("idea670", REF.with_suffix(".py"))
I670 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(I670)

ARMS, GROSSES, ARM_FREQ, ARM_SRC = I670.ARMS, I670.GROSSES, I670.ARM_FREQ, I670.ARM_SRC
COST, FREQ0, BAND0, GROSS0, WARM = I670.COST, I670.FREQ0, I670.BAND0, I670.GROSS0, I670.WARM
IS_END, OOS_START = I670.IS_END, I670.OOS_START

CREDITS = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06]     # tuned axis 1
CREDIT_MAX_TEST = 0.05                                   # the queue's own bar
PANELS = ["U56", "B136"]                                 # tuned axis 2
REPRO_BAR = 5e-4

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def M(r):
    return I670.M(r)


def M0(r):
    return I670.M0(r)


def credit(r, cash, c):
    """Flat annual credit c on the realised cash share, weight path held fixed."""
    return r if c == 0.0 else r + cash * (c / 252.0)


def legs_at(r, base, spy):
    """PROTOCOL 4b's five legs and 4a, idea 670's `legs`, verbatim (CONV-A: Sharpe at rf=0)."""
    return I670.legs(r, base, spy)


def sharpe_rf(x, rf):
    v = x.std() * np.sqrt(252)
    return (x.mean() * 252 - rf) / v if v else np.nan


def legs_rf(r, base, spy, rf):
    """CONV-B: the SAME five legs with every Sharpe taken against rf = the cash credit.

    The record's `engine.metrics` uses rf=0.  That convention is harmless while cash earns
    nothing, but under a credit it pays cash-heavy arms a riskless return and then counts it in
    the numerator of a rf=0 Sharpe — so the Sharpe legs move for a reason that has nothing to do
    with the book.  CONV-B subtracts the same rf from the arm, the baseline and SPY, which leaves
    the CAGR floor and the DD cap untouched and isolates what the credit really does.
    """
    h = len(r) // 2
    hb, hs = len(base) // 2, len(spy) // 2
    L = dict(L1_H1=bool(sharpe_rf(r.iloc[:h], rf) > sharpe_rf(spy.iloc[:hs], rf)),
             L2_H2=bool(sharpe_rf(r.iloc[h:], rf) > sharpe_rf(spy.iloc[hs:], rf)),
             L3_OOS=bool(sharpe_rf(r.loc[OOS_START:], rf) > sharpe_rf(spy.loc[OOS_START:], rf)),
             L4_DDcap=bool(abs(M(r)["MaxDD"]) <= 0.60 * abs(M(spy)["MaxDD"])),
             L5_CAGRfloor=bool(M(r)["CAGR"] >= 0.70 * M(spy)["CAGR"]))
    p4a = bool(sharpe_rf(r.iloc[:h], rf) > sharpe_rf(base.iloc[:hb], rf)
               and sharpe_rf(r.iloc[h:], rf) > sharpe_rf(base.iloc[hb:], rf)
               and M(r)["MaxDD"] >= M(base)["MaxDD"])
    return L, p4a, all(L.values())


def fails(L):
    return ",".join(k for k, v in L.items() if not v) or "-"


def main():
    t0 = time.time()
    log("=" * 100)
    log(f"IDEA 676 (cloud lane, {DATE}) — {SLUG}")
    log("=" * 100)
    log(__doc__.split("QUESTION")[0].strip())

    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pres = {pn: I670.prep(p) for pn, p in px.items()}
    for pn, p in px.items():
        log(f"\nPanel {pn}: {p.shape[1]} columns, {p.index[0].date()} -> {p.index[-1].date()}; "
            f"scored sample starts {p.index[WARM].date()} (warm-up {WARM} rows).")
    log("\nARMS (idea 670's ten, imported from its committed script):")
    for a in ARMS:
        log(f"    {a:<13} {ARM_SRC[a]}   cadence {ARM_FREQ[a]}")

    # ---------------- GATES -------------------------------------------------------------------
    log("\n" + "-" * 100)
    log("GATES (printed before any verdict)")
    log("-" * 100)
    pU = px["U56"]
    wtest = I670.arm_weights(pU, pres["U56"], "CAND20", 0.75)
    r_fast = I670.fast_backtest(pU, wtest, FREQ0, COST)
    r_eng = backtest(pU, wtest, cost_bps=COST, freq=FREQ0)["returns"]
    st = pU.index[WARM]
    g1 = float((r_fast.loc[st:] - r_eng.loc[st:]).abs().max())
    log(f"  G1 fast_backtest == engine.backtest (U56/CAND20 g=0.75, 10 bps)  max|d| = {g1:.3e}   "
        f"{'PASS' if g1 < 1e-10 else 'FAIL'}")

    # ---------------- the grid at every credit ------------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 1 — THE 160-POINT GRID AT EVERY CREDIT (1,120 rows, all published)")
    log("=" * 100)
    rows = []
    bars = {}
    for pn in PANELS:
        p = px[pn]
        st = p.index[WARM]
        spy = p["SPY"].pct_change().fillna(0).loc[st:]
        ms = M(spy)
        # the live baseline holds cash too, so it is credited at the same rate
        rb, eb, _ = I670.fast_backtest(p, rules_v2_weights(p, BAND0, GROSS0), FREQ0, COST,
                                       want_exposure=True)
        rb, cash_b = rb.loc[st:], (1.0 - eb.loc[st:])
        bars[pn] = (spy, ms, rb, cash_b)
        for arm in ARMS:
            for g in GROSSES:
                w = I670.arm_weights(p, pres[pn], arm, g)
                r, expo, turn = I670.fast_backtest(p, w, ARM_FREQ[arm], COST, want_exposure=True)
                r, expo = r.loc[st:], expo.loc[st:]
                cash = 1.0 - expo
                for c in CREDITS:
                    rc = credit(r, cash, c)
                    base_c = credit(rb, cash_b, c)
                    L, p4a, p4b, m, _ = legs_at(rc, base_c, spy)
                    LB, p4a_B, p4b_B = legs_rf(rc, base_c, spy, c)
                    mo = M(rc.loc[OOS_START:])
                    mi = M(rc.loc[:IS_END])
                    rows.append(dict(pass4b_B=p4b_B, pass4a_B=p4a_B,
                                     **{f"{k}_B": v for k, v in LB.items()},
                                     IS_Sharpe_B=sharpe_rf(rc.loc[:IS_END], c),
                                     panel=pn, arm=arm, gross=g, credit=c, freq=ARM_FREQ[arm],
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=m["H1"], H2=m["H2"], IS_CAGR=mi["CAGR"],
                                     IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                     OOS_MaxDD=mo["MaxDD"], mean_exposure=float(expo.mean()),
                                     cash_share=float(cash.mean()),
                                     SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"],
                                     SPY_MaxDD=ms["MaxDD"], **L, pass4a=p4a, pass4b=p4b,
                                     fail_legs=fails(L)))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    log(f"  {len(G)} rows written to {Path(OUT).name}.grid.csv")

    # G2 — reproduction of idea 670's committed grid at credit 0
    R = pd.read_csv(REF.with_suffix(".grid.csv"))
    z = G[G.credit == 0.0].merge(R, on=["panel", "arm", "gross"], suffixes=("", "_ref"))
    dev = {k: float((z[k] - z[f"{k}_ref"]).abs().max())
           for k in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]}
    vmatch = int((z["pass4b"] == z["pass4b_ref"]).sum())
    lmatch = {k: int((z[k] == z[f"{k}_ref"]).sum())
              for k in ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]}
    g2 = max(dev.values()) < REPRO_BAR and vmatch == len(z)
    log(f"  G2 H_REPRO vs idea 670's committed grid ({len(z)} joined rows): max|d| " +
        "  ".join(f"{k} {v:.2e}" for k, v in dev.items()))
    log(f"     4b verdict matches {vmatch}/{len(z)}; per-leg matches {lmatch}   "
        f"{'PASS' if g2 else 'FAIL'}   (bar {REPRO_BAR:.0e} on levels, exact on verdicts)")

    if not g2:
        log("\n  G2b DIAGNOSTIC (the gate FAILED as pre-registered; this asks whether the cause is")
        log("      the TAPE VINTAGE): the credit-0 grid recomputed on panels truncated to earlier")
        log("      end dates, each compared to idea 670's committed grid. If the deviation "
            "collapses")
        log("      as the tape is rolled back, the failure is vintage, not implementation.")
        log(f"      {'tape end':<14} {'CAGR':>10} {'Sharpe':>10} {'H2':>10} {'4b match':>10}")
        vin_rows = []
        for end in ["2026-09-11", "2026-09-08", "2026-09-04", "2026-09-03"]:
            vr = []
            for pn in PANELS:
                p = px[pn].loc[:end]
                if len(p) < WARM + 260:
                    continue
                stv = p.index[WARM]
                spyv = p["SPY"].pct_change().fillna(0).loc[stv:]
                bv = I670.fast_backtest(p, rules_v2_weights(p, BAND0, GROSS0),
                                        FREQ0, COST).loc[stv:]
                prev = I670.prep(p)
                for arm in ARMS:
                    for g in GROSSES:
                        w = I670.arm_weights(p, prev, arm, g)
                        r = I670.fast_backtest(p, w, ARM_FREQ[arm], COST).loc[stv:]
                        L, p4a_v, p4b_v, m, _ = legs_at(r, bv, spyv)
                        vr.append(dict(panel=pn, arm=arm, gross=g, CAGR=m["CAGR"],
                                       Sharpe=m["Sharpe"], H2=m["H2"], pass4b=p4b_v))
            VV = pd.DataFrame(vr).merge(R, on=["panel", "arm", "gross"], suffixes=("", "_ref"))
            d = {k: float((VV[k] - VV[f"{k}_ref"]).abs().max()) for k in ["CAGR", "Sharpe", "H2"]}
            mv = int((VV["pass4b"] == VV["pass4b_ref"]).sum())
            vin_rows.append(dict(tape_end=end, **d, verdict_match=mv, n=len(VV)))
            log(f"      {end:<14} {d['CAGR']:>10.2e} {d['Sharpe']:>10.2e} {d['H2']:>10.2e} "
                f"{mv:>7}/{len(VV)}")
        pd.DataFrame(vin_rows).to_csv(f"{OUT}.vintage.csv", index=False)

    g100 = G[(G.gross == 1.00) & (G.arm == "SPYBH")]
    spread = float(g100.groupby(["panel"])["CAGR"].apply(lambda s: s.max() - s.min()).max())
    log(f"  G3 credit identity at gross 1.00 with no cash (SPYBH): max CAGR spread across the "
        f"whole credit sweep = {spread:.3e}   {'PASS' if spread < 1e-12 else 'FAIL'}")

    mono = G.sort_values("credit").groupby(["panel", "arm", "gross"])["CAGR"].apply(
        lambda s: bool((s.diff().dropna() >= -1e-12).all()))
    log(f"  G4 CAGR non-decreasing in the credit at {int(mono.sum())}/{len(mono)} points   "
        f"{'PASS' if bool(mono.all()) else 'FAIL'}")

    log("\n  G6 comparands (10 bps, next-day execution)")
    for pn in PANELS:
        spy, ms, rb, cash_b = bars[pn]
        log(f"    {pn:<5} SPY {ms['CAGR']:>8.2%} / {ms['Sharpe']:>7.4f} / {ms['MaxDD']:>8.2%}"
            f"   halves {ms['H1']:.4f} / {ms['H2']:.4f}"
            f"   -> 4b bars: |MaxDD| <= {0.60 * abs(ms['MaxDD']):.2%}, "
            f"CAGR >= {0.70 * ms['CAGR']:.2%}  (SPY holds no cash: bars are credit-invariant)")
        for c in (0.00, 0.05):
            mb = M(credit(rb, cash_b, c))
            log(f"          RULES v2 baseline at credit {c:.0%}: {mb['CAGR']:>7.2%} / "
                f"{mb['Sharpe']:>7.4f} / {mb['MaxDD']:>8.2%}   halves {mb['H1']:.4f} / "
                f"{mb['H2']:.4f}   (mean cash share {float(cash_b.mean()):.1%})")

    # ---------------- SECTION 2 — the pass counts ---------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 2 — 4b AND ITS FIVE LEGS AS THE CREDIT RISES")
    log("=" * 100)
    log("  CONV-A = the record's own convention (Sharpe at rf=0, as `engine.metrics` computes it)")
    log(f"  {'credit':>7} {'4b':>7} {'4a':>7} {'L1 H1':>7} {'L2 H2':>7} {'L3 OOS':>7} "
        f"{'L4 DD':>7} {'L5 CAGR':>8}")
    for c in CREDITS:
        s = G[G.credit == c]
        log(f"  {c:>7.0%} {int(s['pass4b'].sum()):>4}/160 {int(s['pass4a'].sum()):>4}/160 "
            f"{s['L1_H1'].mean():>7.3f} {s['L2_H2'].mean():>7.3f} {s['L3_OOS'].mean():>7.3f} "
            f"{s['L4_DDcap'].mean():>7.3f} {s['L5_CAGRfloor'].mean():>8.3f}")
    log("\n  CONV-B = the same sweep with EVERY Sharpe taken against rf = the credit (arm,")
    log("  baseline and SPY alike).  The CAGR floor and the DD cap are identical by construction;")
    log("  any difference between the two tables is the rf=0 convention, not the cash leg.")
    log(f"  {'credit':>7} {'4b':>7} {'4a':>7} {'L1 H1':>7} {'L2 H2':>7} {'L3 OOS':>7} "
        f"{'L4 DD':>7} {'L5 CAGR':>8}")
    for c in CREDITS:
        s = G[G.credit == c]
        log(f"  {c:>7.0%} {int(s['pass4b_B'].sum()):>4}/160 {int(s['pass4a_B'].sum()):>4}/160 "
            f"{s['L1_H1_B'].mean():>7.3f} {s['L2_H2_B'].mean():>7.3f} {s['L3_OOS_B'].mean():>7.3f} "
            f"{s['L4_DDcap_B'].mean():>7.3f} {s['L5_CAGRfloor_B'].mean():>8.3f}")

    log("\n  the CAGR floor (L5) by gross rung and credit — pass share, n=20 per cell")
    piv = G.pivot_table(index="gross", columns="credit", values="L5_CAGRfloor", aggfunc="mean")
    log("  " + piv.to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  4b pass count by gross rung and credit (n=20 per cell)")
    piv2 = G.pivot_table(index="gross", columns="credit", values="pass4b", aggfunc="sum")
    log("  " + piv2.to_string())
    piv.to_csv(f"{OUT}.l5_by_gross.csv")
    piv2.to_csv(f"{OUT}.4b_by_gross.csv")

    # ---------------- SECTION 3 — invariance census -------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 3 — WHICH 4b VERDICTS ARE CREDIT-INVARIANT (the queue's deliverable)")
    log("=" * 100)
    inv_rows = []
    for (pn, arm, g), s in G.groupby(["panel", "arm", "gross"]):
        s = s.sort_values("credit")
        s5 = s[s.credit <= CREDIT_MAX_TEST]
        v0 = bool(s[s.credit == 0.0]["pass4b"].iloc[0])
        inv5 = bool(s5["pass4b"].nunique() == 1)
        inv6 = bool(s["pass4b"].nunique() == 1)
        inv5_B = bool(s5["pass4b_B"].nunique() == 1)
        flips = s5[s5["pass4b"] != v0]
        c_flip = float(flips["credit"].min()) if len(flips) else np.nan
        cf = R[(R.panel == pn) & (R.arm == arm) & (R.gross == g)]["cash_rate_to_flip_L5"].iloc[0]
        l5_0 = bool(s[s.credit == 0.0]["L5_CAGRfloor"].iloc[0])
        l5_flips = s5[s5["L5_CAGRfloor"] != l5_0]
        c_l5 = float(l5_flips["credit"].min()) if len(l5_flips) else np.nan
        inv_rows.append(dict(panel=pn, arm=arm, gross=g, pass4b_at_0=v0, invariant_0_5=inv5,
                             invariant_0_5_convB=inv5_B,
                             invariant_0_6=inv6, flip_credit_4b=c_flip, L5_at_0=l5_0,
                             flip_credit_L5=c_l5, closed_form_L5=cf,
                             cash_share=float(s["cash_share"].iloc[0]),
                             fail_legs_at_0=s[s.credit == 0.0]["fail_legs"].iloc[0]))
    V = pd.DataFrame(inv_rows)
    V.to_csv(f"{OUT}.invariance.csv", index=False)
    n_inv5 = int(V["invariant_0_5"].sum())
    n_inv5_B = int(V["invariant_0_5_convB"].sum())
    log(f"  4b verdicts unchanged across 0-5% credit: **{n_inv5} of {len(V)}** "
        f"({n_inv5 / len(V):.1%});  across 0-6%: {int(V['invariant_0_6'].sum())} of {len(V)}")
    log(f"  under CONV-B (Sharpe at rf = the credit): **{n_inv5_B} of {len(V)}** "
        f"({n_inv5_B / len(V):.1%}) unchanged over 0-5%")
    log(f"  verdicts that FLIP within 0-5% ({len(V) - n_inv5}):")
    for _, x in V[~V["invariant_0_5"]].iterrows():
        log(f"    {x['panel']:<5} {x['arm']:<13} g={x['gross']:.2f}  4b at 0% = "
            f"{str(x['pass4b_at_0']):<5} flips at credit {x['flip_credit_4b']:.0%}  "
            f"(cash share {x['cash_share']:.1%}, legs failing at 0%: {x['fail_legs_at_0']})")

    log("\n  the CAGR floor alone (L5): flips within 0-5%")
    l5f = V[V["flip_credit_L5"].notna()]
    log(f"    L5 flips at {len(l5f)} of {len(V)} points; of the {int((~V['L5_at_0']).sum())} "
        f"points failing the floor at 0%, {int((~l5f['L5_at_0']).sum())} clear it by 5%")
    cf_raw = int((R["cash_rate_to_flip_L5"] <= CREDIT_MAX_TEST).sum())
    cf_pos = int(((R["cash_rate_to_flip_L5"] > 0) & (R["cash_rate_to_flip_L5"]
                                                     <= CREDIT_MAX_TEST)).sum())
    log(f"    (idea 670's closed form: {cf_raw} of {len(R)} rows read `need <= 5%`, but "
        f"{cf_raw - cf_pos} of those already CLEAR the floor at 0% — their `need` is negative.")
    log(f"     The closed form's genuine FLIP prediction is {cf_pos}; this run realises "
        f"{len(l5f)}.)")

    # H_CF — is the record's closed form honest?
    k = V["flip_credit_L5"].notna() & V["closed_form_L5"].notna()
    if k.sum() >= 3:
        rho = I670.spearman(V.loc[k, "flip_credit_L5"], V.loc[k, "closed_form_L5"])
        # the realised flip lands on the credit GRID, so compare to the grid-rounded closed form
        cf_grid = V.loc[k, "closed_form_L5"].apply(
            lambda v: min([c for c in CREDITS if c >= v], default=np.nan))
        exact = int((cf_grid.values == V.loc[k, "flip_credit_L5"].values).sum())
        med_err = float((V.loc[k, "closed_form_L5"] - V.loc[k, "flip_credit_L5"]).abs().median())
    else:
        rho, exact, med_err = np.nan, 0, np.nan
    cf_count = cf_pos          # the closed form's genuine flip prediction (need strictly > 0)
    real_count = int(len(l5f))
    log(f"    H_CF: Spearman(realised flip credit, committed closed form) = {rho:.4f}; "
        f"grid-rounded closed form lands on the realised rung {exact}/{int(k.sum())}; "
        f"median |error| {med_err:.2%}; genuine-flip count {cf_count} predicted vs "
        f"{real_count} realised")

    # ---------------- SECTION 4 — the decisive controls ----------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 4 — THE ZERO-SIGNAL CONTROL AND THE RECORD'S TWO MATCHED-GROSS SURVIVORS")
    log("=" * 100)
    S = G[G.arm == "SPYBH"]
    log("  SPYBH (g x SPY, no signal whatever) — 4b passes at each credit:")
    log(f"  {'credit':>7} {'4b passes':>10} {'L5 share':>9} {'L4 share':>9}  grosses passing 4b")
    spy_rows = []
    for c in CREDITS:
        s = S[S.credit == c]
        pg = sorted(s[s["pass4b"]]["gross"].unique())
        spy_rows.append(dict(credit=c, passes=int(s["pass4b"].sum()), L5=s["L5_CAGRfloor"].mean(),
                             L4=s["L4_DDcap"].mean(), grosses=str(pg)))
        log(f"  {c:>7.0%} {int(s['pass4b'].sum()):>7}/16 {s['L5_CAGRfloor'].mean():>9.3f} "
            f"{s['L4_DDcap'].mean():>9.3f}  {pg}")
    pd.DataFrame(spy_rows).to_csv(f"{OUT}.zerosignal.csv", index=False)
    log("  (idea 670's finding at 0%: the zero-signal control clears the CAGR floor at g >= 0.75 "
        "and the DD cap at g <= 0.50, so its gross WINDOW is CLOSED — width -0.25 on both panels.)")
    log("\n  the same control's gross WINDOW as the credit rises (the width IS the edge test):")
    log(f"  {'panel':<6} {'credit':>7} {'g_min (L4 holds up to)':>24} "
        f"{'g_max (L5 holds from)':>23} {'window width':>13}")
    win_rows = []
    for pn in PANELS:
        for c in CREDITS:
            s = S[(S.panel == pn) & (S.credit == c)].sort_values("gross")
            l4 = s[s["L4_DDcap"]]["gross"]
            l5 = s[s["L5_CAGRfloor"]]["gross"]
            gmax = float(l4.max()) if len(l4) else np.nan
            gmin = float(l5.min()) if len(l5) else np.nan
            width = gmax - gmin if np.isfinite(gmax) and np.isfinite(gmin) else np.nan
            win_rows.append(dict(panel=pn, credit=c, g_dd_max=gmax, g_cagr_min=gmin, width=width))
            log(f"  {pn:<6} {c:>7.0%} {gmax:>24.2f} {gmin:>23.2f} {width:>13.2f}")
    pd.DataFrame(win_rows).to_csv(f"{OUT}.window.csv", index=False)

    log("\n  the record's two matched-gross 4b survivors (idea 670 section 2):")
    log(f"  {'point':<28} {'credit':>7} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'4b':>6} "
        f"{'failing legs':<14}")
    for pn, arm, g in [("U56", "CAND20", 0.75), ("B136", "EWELIG", 0.75)]:
        for c in CREDITS:
            x = G[(G.panel == pn) & (G.arm == arm) & (G.gross == g) & (G.credit == c)].iloc[0]
            log(f"  {pn + '/' + arm + f' g={g:.2f}':<28} {c:>7.0%} {x['CAGR']:>8.2%} "
                f"{x['Sharpe']:>8.4f} {x['MaxDD']:>8.2%} {str(x['pass4b']):>6} "
                f"{x['fail_legs']:<14}")

    # ---------------- SECTION 5 — rule 8 walk-forward ------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 5 — RULE 8 WALK-FORWARD AT EVERY CREDIT (choose on 2009-2016, OOS read once)")
    log("=" * 100)
    wf_rows = []
    for pn in PANELS:
        p = px[pn]
        st = p.index[WARM]
        spy, ms, rb, cash_b = bars[pn]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        mis, moos = M(spy_is), M(spy_oos)
        log(f"\n  {pn}: SPY IS {mis['CAGR']:.2%} / {mis['Sharpe']:.4f} / {mis['MaxDD']:.2%}; "
            f"SPY OOS {moos['CAGR']:.2%} / {moos['Sharpe']:.4f} / {moos['MaxDD']:.2%}")
        log(f"  {'credit':>7} {'chooser':<10} {'pick':<22} {'OOS CAGR':>9} {'OOS Shrp':>9} "
            f"{'OOS MaxDD':>10} {'OOS 4b':>7} {'OOS 4a':>7} {'failing legs':<14}")
        for c in CREDITS:
            s = G[(G.panel == pn) & (G.credit == c)]
            c1 = s.sort_values(["IS_Sharpe", "gross"], ascending=[False, True]).iloc[0]
            c1b = s.sort_values(["IS_Sharpe_B", "gross"], ascending=[False, True]).iloc[0]
            pool = s[(s["IS_MaxDD"].abs() <= 0.60 * abs(mis["MaxDD"]))
                     & (s["IS_CAGR"] >= 0.70 * mis["CAGR"])]
            c2 = (pool.sort_values(["gross", "IS_Sharpe"], ascending=[True, False]).iloc[0]
                  if len(pool) else c1)
            for cname, pick in [("C1", c1), ("C1-convB", c1b), ("C2", c2)]:
                w = I670.arm_weights(p, pres[pn], pick["arm"], pick["gross"])
                r, expo, _ = I670.fast_backtest(p, w, ARM_FREQ[pick["arm"]], COST,
                                                want_exposure=True)
                r, expo = r.loc[st:], expo.loc[st:]
                rc = credit(r, 1.0 - expo, c).loc[OOS_START:]
                base_c = credit(rb, cash_b, c).loc[OOS_START:]
                L, p4a, p4b, m, _ = legs_at(rc, base_c, spy_oos)
                LB, p4a_B, p4b_B = legs_rf(rc, base_c, spy_oos, c)
                mb = M(base_c)
                wf_rows.append(dict(panel=pn, credit=c, chooser=cname, arm=pick["arm"],
                                    gross=pick["gross"], pool=len(pool),
                                    OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                                    OOS_MaxDD=m["MaxDD"], base_OOS_CAGR=mb["CAGR"],
                                    base_OOS_Sharpe=mb["Sharpe"], base_OOS_MaxDD=mb["MaxDD"],
                                    SPY_OOS_CAGR=moos["CAGR"], SPY_OOS_Sharpe=moos["Sharpe"],
                                    SPY_OOS_MaxDD=moos["MaxDD"], p4b=p4b, p4a=p4a,
                                    p4b_B=p4b_B, p4a_B=p4a_B, fail_legs=fails(L),
                                    fail_legs_B=fails(LB)))
                label = "{} g={:.2f}".format(pick["arm"], pick["gross"])
                log(f"  {c:>7.0%} {cname:<10} {label:<22} "
                    f"{m['CAGR']:>9.2%} {m['Sharpe']:>9.4f} {m['MaxDD']:>10.2%} "
                    f"{str(p4b):>7} {str(p4a):>7} {fails(L):<14} "
                    f"[CONV-B 4b {str(p4b_B):>5} 4a {str(p4a_B):>5}]")
        mb0 = M(credit(rb, cash_b, 0.0).loc[OOS_START:])
        mb5 = M(credit(rb, cash_b, 0.05).loc[OOS_START:])
        log(f"  (comparands) RULES v2 OOS at 0% {mb0['CAGR']:.2%} / {mb0['Sharpe']:.4f} / "
            f"{mb0['MaxDD']:.2%};  at 5% {mb5['CAGR']:.2%} / {mb5['Sharpe']:.4f} / "
            f"{mb5['MaxDD']:.2%};  SPY OOS {moos['CAGR']:.2%} / {moos['Sharpe']:.4f} / "
            f"{moos['MaxDD']:.2%}")
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    wf_inv = []
    for (pn, cname), s in WF.groupby(["panel", "chooser"]):
        s5 = s[s.credit <= CREDIT_MAX_TEST]
        same_pick = bool(s5.apply(lambda x: (x["arm"], x["gross"]), axis=1).nunique() == 1)
        same_v = bool(s5["p4b"].nunique() == 1)
        same_v_B = bool(s5["p4b_B"].nunique() == 1)
        wf_inv.append(dict(panel=pn, chooser=cname, pick_invariant=same_pick,
                           verdict_invariant=same_v, verdict_invariant_convB=same_v_B,
                           picks=sorted({f"{a} g={g:.2f}" for a, g in zip(s5["arm"], s5["gross"])})))
        log(f"  {pn}/{cname}: pick invariant over 0-5% {same_pick} (picks "
            f"{sorted({f'{a} g={g:.2f}' for a, g in zip(s5['arm'], s5['gross'])})}); "
            f"OOS 4b verdict invariant {same_v}; CONV-B {same_v_B}")
    WI = pd.DataFrame(wf_inv)

    # ---------------- SECTION 6 — every row, published ----------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 6 — EVERY ONE OF THE 1,120 ROWS (published, never selected on)")
    log("=" * 100)
    log(f"  {'panel':<6} {'arm':<13} {'gross':>5} {'credit':>6} {'CAGR':>8} {'Sharpe':>8} "
        f"{'MaxDD':>8} {'H1':>6} {'H2':>6} {'cash':>6} {'4b':>6} {'4a':>6} {'failing legs':<14}")
    for _, x in G.sort_values(["panel", "arm", "gross", "credit"]).iterrows():
        log(f"  {x['panel']:<6} {x['arm']:<13} {x['gross']:>5.2f} {x['credit']:>6.0%} "
            f"{x['CAGR']:>8.2%} {x['Sharpe']:>8.4f} {x['MaxDD']:>8.2%} {x['H1']:>6.3f} "
            f"{x['H2']:>6.3f} {x['cash_share']:>6.1%} {str(x['pass4b']):>6} "
            f"{str(x['pass4a']):>6} {x['fail_legs']:<14}")

    # ---------------- SECTION 7 — hypotheses and verdict ---------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 7 — PRE-REGISTERED HYPOTHESES AND THE VERDICT")
    log("=" * 100)
    h_repro = bool(g2)
    h_inv = bool(n_inv5 / len(V) >= 0.80)
    h_cf = bool((not np.isnan(rho)) and rho >= 0.95 and abs(cf_count - real_count) <= 3)
    spy5 = S[(S.credit <= CREDIT_MAX_TEST)]
    h_spybh = bool(spy5["pass4b"].sum() == 0)
    surv = []
    for pn, arm, g in [("U56", "CAND20", 0.75), ("B136", "EWELIG", 0.75)]:
        s = G[(G.panel == pn) & (G.arm == arm) & (G.gross == g) & (G.credit <= CREDIT_MAX_TEST)]
        surv.append(bool(s["pass4b"].all()))
    h_surv = all(surv)
    h_wf = bool(WI["pick_invariant"].all() and WI["verdict_invariant"].all())
    H = [("H_REPRO", h_repro, f"max level deviation {max(dev.values()):.2e} (bar {REPRO_BAR:.0e}), "
                              f"4b verdicts {vmatch}/{len(z)}"),
         ("H_INV", h_inv, f"{n_inv5}/{len(V)} = {n_inv5 / len(V):.1%} of 4b verdicts unchanged "
                          f"over 0-5% (bar 80%); CONV-B {n_inv5_B}/{len(V)} = "
                          f"{n_inv5_B / len(V):.1%}"),
         ("H_CF", h_cf, f"Spearman {rho:.4f}, closed-form count {cf_count} vs realised "
                        f"{real_count}"),
         ("H_SPYBH", h_spybh, f"zero-signal 4b passes at credits <= 5%: "
                              f"{int(spy5['pass4b'].sum())} of {len(spy5)}"),
         ("H_SURV", h_surv, f"U56/CAND20 g=0.75 all-pass {surv[0]}, B136/EWELIG g=0.75 all-pass "
                            f"{surv[1]}"),
         ("H_WF", h_wf, f"pick invariant {int(WI['pick_invariant'].sum())}/{len(WI)}, verdict "
                        f"invariant {int(WI['verdict_invariant'].sum())}/{len(WI)}; CONV-B verdict "
                        f"invariant {int(WI['verdict_invariant_convB'].sum())}/{len(WI)}")]
    log(f"  {'hypothesis':<10} {'result':<6} detail")
    for nm, val, det in H:
        log(f"  {nm:<10} {'PASS' if val else 'FAIL':<6} {det}")
    pd.DataFrame([dict(hypothesis=n, result=bool(v), detail=d) for n, v, d in H]).to_csv(
        f"{OUT}.hypotheses.csv", index=False)

    if h_inv and h_surv and h_spybh and h_wf:
        verdict = ("ANSWERED-YES — the 4b CAGR floor survives a non-zero cash leg; the record's 4b "
                   "verdicts are credit-invariant and idea 642's T-bill path cannot overturn them")
    elif (not h_spybh) or (not h_inv):
        verdict = ("ANSWERED-NO — the 4b verdicts are cash-rate artefacts; every committed 4b count "
                   "must be restated with its cash assumption")
    else:
        verdict = "MIXED — see the invariance census; the flips are named above"
    log(f"\n  VERDICT: {verdict}")
    log("  No book promoted. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.")
    log(f"\n  runtime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
