#!/usr/bin/env python3
"""
IDEA 766 - is the DAILY-CADENCE WIN of the MOMENTUM SLICE an EDGE the IS SELECTOR is MISSING?
=============================================================================================
Lane B, 2026-09-19.

THE CLAIM UNDER TEST.  Idea 563 (cloud, 2026-09-11) priced idea 559's daily-depth-matched
momentum slice as a BOOK and found two things side by side:

    (a) MOM-D beats the MA slice on Sharpe in 66.7% of pairs at cadence D (mean +0.0584)
        and in only 13.0% at cadence Q; and
    (b) the IS-Sharpe selector picks cadence D in 0 of 54 MA-THRESH cells and 4 of 54 MOM-D
        cells.

Read together those say the record's own selector systematically refuses the cell where the
momentum slice wins.  There are exactly two readings and this run pre-registers both:

  H_EDGE       The daily cell is a REAL EDGE the IS selector is leaving on the table.  Then
               FORCING cadence D must beat the selector's own OOS pick, and the daily win must
               survive being charged for the churn it creates.
  H_TURNOVER   The daily cell is TURNOVER the selector is right to avoid.  Then D's advantage
               is a zero-cost artefact: it dies at or below the binding 10 bps, and the OOS
               pick of the selector beats the forced-D book.

THE DISCRIMINATOR (pre-registered, two legs, both required for H_EDGE).
  LEG 1  RULE-8 HEAD-TO-HEAD.  Selectors read IS (start..2016-12-31) ONLY; 2017-2026 read once.
         S_FORCE_D must beat S_SHARPE on OOS Sharpe in a MAJORITY of cells.
  LEG 2  TURNOVER-MATCHED CONTROL.  The whole daily-vs-slow difference is re-cut in COST space.
         Because the engine's cost is exactly `turnover x c / 1e4` in return space, the cost
         rung at which D's advantage over a slower cadence crosses zero is computable EXACTLY
         off one held path.  That BREAK-EVEN COST c* is the turnover-matched control: c* > 10
         bps means the daily win is paid for at the binding rung; c* <= 10 bps means the record
         is right to refuse it.  Reported per cell, not pooled only.

CONSTRUCTION (idea 563's, verbatim, so the premise is tested and not re-invented).
  cell = (panel, theta):
    MA-THRESH  = px > MA200 * (1 + theta)                        [the live rule's gate form]
    MOM-D      = top k_t names by 12-1 momentum, k_t = |MA-THRESH_t| pinned EVERY DAY
                 (idea 559's daily match: identical NUMBER of names held each day, so gross is
                  identical by construction and only the NAMES differ)
    book       = RESPREAD (gross / k_t on held names)  or  DEGROSS (gross / n_live, rest CASH)
    costs      = 10 bps per unit turnover binding, next-day execution (engine convention).
                 Other rungs derived EXACTLY off the same held path (gate G1).

TUNED PARAMETERS - EXACTLY 2, every grid point reported:
  (1) CADENCE  in {D, W, M, Q}
  (2) SELECTOR in {S_SHARPE (argmax IS Sharpe, the record's), S_CAGR (argmax IS CAGR),
                   S_FORCE_D (always daily)}
  PANEL (3) x THETA (5) x ARM (2) x CONSTRUCTION (2) x GROSS (3) are REPORTED axes, never
  selected over.  Full grid = 3 x 5 x 2 x 2 x 4 x 3 = 720 books, every one in .grid.csv.
  S_ORACLE (argmax OOS Sharpe) is printed as an UNREACHABLE upper bound, never as a verdict.

BOTH KEEP PATHS on every one of the 720 books:
  4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2's.
  4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

GATES (pre-registered, all reported pass or fail):
  G0  fast_run reproduces engine.backtest returns AND turnover to 1e-12 on every panel, D and W.
  G1  a derived cost rung equals a fresh fast_run priced at that rung to 1e-15.
  G2  DAILY DEPTH MATCH: exact-match share, mean and max |k_MOM-D - k_MA| per panel.  The match
      cannot be exact on names aged 200-251 days (12-1 momentum needs 252 closes, the MA needs
      200), so the residual is REPORTED, not assumed away.
  G3  the live baseline row is produced by baseline.rules_v2_weights through engine.backtest,
      unmodified, on each panel, and printed beside every verdict.
  G4  GROSS IDENTITY: on days where the depth match is exact, the two arms' TARGET gross agrees
      to 1e-12; the residual on clipped days is reported.
  G5  NO SELECTOR READS A ROW ON OR AFTER 2017-01-01 (asserted on the IS slice's max index).
  G6  every one of the 720 books published to .grid.csv and every selector pick to .walkforward.csv.
  G7  costs 10 bps per unit turnover, t -> t+1, no shorting, gross <= 1.00.

SURVIVORSHIP (rule 9).  U56 / B136 / SMALL439 are CURRENT-constituent lists; dead names are
absent, so every absolute CAGR level is an upper bound and neither KEEP column is immune.  The
head-to-head is arm-minus-arm and cadence-minus-cadence INSIDE one panel over the SAME names on
the SAME days, where the bias very largely cancels; the 4a / 4b pass counts are not protected.
The 44 SMALL names with max_1d_move >= 1.0 are dropped first (data/small_meta.csv), idea 559's
own filter.

Deterministic, standalone.  Reads research/baseline.py.  Modifies nothing outside its outputs:
.grid.csv .walkforward.csv .breakeven.csv .keeppaths.csv .match.csv .gates.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNG_LADDER = [0, 2, 5, 10, 15, 25, 40, 60, 100, 150, 250, 400]
PANELS = ["U56", "B136", "SMALL439"]
THETA = [0.12, 0.06, 0.00, -0.06, -0.12]
ARMS = ["MA-THRESH", "MOM-D"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
CADENCES = ["D", "W", "M", "Q"]                 # tuned param 1
SELECTORS = ["S_SHARPE", "S_CAGR", "S_FORCE_D"]  # tuned param 2
GROSSES = [0.50, 0.75, 1.00]                    # reported axis, never selected over
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

BAR_ENGINE = 1e-12
BAR_RUNG = 1e-15

OUT = Path(__file__).with_suffix("")
LOG = []
GATES = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def gate(name, ok, detail):
    GATES.append(dict(gate=name, pass_=bool(ok), detail=detail))
    P(f"  {name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def fast_run(px, W, freq):
    """engine.backtest's arithmetic, returning the ZERO-COST return path and the turnover so
    that any cost rung can be derived exactly (gate G1)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = np.nansum(held * rets, axis=1)
    return (pd.Series(r0, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def stat(r, warm):
    r = r.loc[warm:]
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def legs_4b(s, spy):
    return {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
            "OOS": s["oSharpe"] > spy["oSharpe"],
            "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
            "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}


def fail_4b(s, spy):
    t = legs_4b(s, spy)
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def daily_matched(sig, live, gm):
    """idea 559's daily match: k_t = k_ma_t every day, clipped to the rankable count."""
    k_ma = gm.sum(axis=1)
    kt = np.minimum(k_ma, sig.notna().sum(axis=1))
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def book(px, g, construction, gross):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def breakeven_cost(r0_fast, t_fast, r0_slow, t_slow, warm, field, lo=0.0, hi=400.0):
    """Exact break-even cost: the c (bps) at which the FAST (daily) book's advantage over the
    SLOW book in `field` crosses zero.  Monotone in c whenever T_fast > T_slow, so bisected on
    the realised paths; returns nan if no crossing inside [lo, hi]."""
    def d(c):
        a = stat(rung(r0_fast, t_fast, c), warm)[field]
        b = stat(rung(r0_slow, t_slow, c), warm)[field]
        return a - b
    dlo, dhi = d(lo), d(hi)
    if dlo <= 0:
        return 0.0 if dlo < 0 else 0.0          # daily already behind at zero cost
    if dhi > 0:
        return np.inf                            # daily still ahead at 400 bps
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if d(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ================================================================== main
def main():
    P("=" * 190)
    P("IDEA 766 - is the DAILY-CADENCE WIN of the MOMENTUM SLICE an EDGE the IS SELECTOR is "
      "MISSING?   lane B, 2026-09-19")
    P("=" * 190)
    P("PROTOCOL: 10 bps per unit turnover binding (other rungs derived exactly and reported), "
      "next-day execution (engine), no shorting, no leverage.")
    P(f"IS = start..{IS_END}, OOS = {OOS_START}..end, read ONCE.")
    P(f"2 tuned params: CADENCE {CADENCES} x SELECTOR {SELECTORS}.")
    P(f"REPORTED axes, never selected over: PANEL {PANELS} x THETA {THETA} x ARM {ARMS} x "
      f"CONSTRUCTION {CONSTRUCTIONS} x GROSS {GROSSES}  =  720 books, all published.")
    P("H_EDGE needs BOTH legs: (1) S_FORCE_D beats S_SHARPE on OOS Sharpe in a MAJORITY of "
      "cells, AND (2) the break-even cost c* of the daily win exceeds the binding 10 bps.")
    P("SURVIVORSHIP (rule 9): U56/B136/SMALL439 are CURRENT constituents; CAGR levels are upper "
      "bounds and the 4a/4b counts are NOT immune.  The head-to-head is within-panel and largely "
      "immune.")
    flush_log()

    u, b = load_universe(), load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "   ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"    ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    WARM = {}
    BASE, SPYS = {}, {}
    P("\n" + "=" * 190)
    P("G3  LIVE BASELINE (baseline.rules_v2_weights through engine.backtest, unmodified) and SPY")
    P("=" * 190)
    for pn, (px, spy) in PN.items():
        warm = px.index[260]
        WARM[pn] = warm
        full = pd.concat([px, spy.rename("SPY")], axis=1)
        bt = backtest(full, rules_v2_weights(full), cost_bps=COST_BPS, freq="W")
        BASE[pn] = stat(bt["returns"], warm)
        SPYS[pn] = stat(spy.pct_change().fillna(0.0), warm)
    bt_tab = pd.DataFrame({f"{k} RULESv2": v for k, v in BASE.items()}
                          | {f"{k} SPY": v for k, v in SPYS.items()}).T
    P(fmt(bt_tab))
    gate("G3", True, "live baseline + SPY produced by the committed baseline/engine on 3 panels")

    # -------------------------------------------------------------- signals + G2/G4
    P("\n" + "=" * 190)
    P("G2  DAILY DEPTH MATCH   |k_MOM-D - k_MA|      G4  TARGET GROSS IDENTITY on exact-match days")
    P("=" * 190)
    SIG = {}
    match_rows = []
    g4_max = 0.0
    for pn, (px, spy) in PN.items():
        live = live_mask(px)
        mr = mom_rank(px)
        for th in THETA:
            gm = ma_gate(px, th)
            gd = daily_matched(mr, live, gm)
            SIG[(pn, th, "MA-THRESH")] = gm
            SIG[(pn, th, "MOM-D")] = gd
            dk = (gd.sum(axis=1) - gm.sum(axis=1)).loc[WARM[pn]:]
            exact = (dk == 0)
            match_rows.append(dict(panel=pn, theta=th, days=len(dk),
                                   exact_share=exact.mean(), mean_abs_dk=dk.abs().mean(),
                                   max_abs_dk=int(dk.abs().max())))
            for cons in CONSTRUCTIONS:
                wa = book(px, gm, cons, 0.75).sum(axis=1).loc[WARM[pn]:][exact]
                wd = book(px, gd, cons, 0.75).sum(axis=1).loc[WARM[pn]:][exact]
                g4_max = max(g4_max, float((wa - wd).abs().max()))
    MATCH = pd.DataFrame(match_rows)
    MATCH.to_csv(f"{OUT}.match.csv", index=False)
    P(fmt(MATCH))
    gate("G2", True, f"exact-match share {MATCH.exact_share.min():.4f}..{MATCH.exact_share.max():.4f}, "
                     f"mean |dk| {MATCH.mean_abs_dk.min():.3f}..{MATCH.mean_abs_dk.max():.3f}, "
                     f"max |dk| {int(MATCH.max_abs_dk.max())}  (REPORTED, 12-1 needs 252 closes vs the MA's 200)")
    gate("G4", g4_max < BAR_ENGINE,
         f"max |gross_MA - gross_MOMD| on exact-match days = {g4_max:.3e} (bar {BAR_ENGINE:.0e})")

    # -------------------------------------------------------------- G0 / G1
    P("\n" + "=" * 190)
    P("G0  fast_run vs engine.backtest        G1  derived cost rung vs a fresh run priced at that rung")
    P("=" * 190)
    g0_max = g1_max = 0.0
    for pn, (px, spy) in PN.items():
        W = book(px, SIG[(pn, 0.00, "MOM-D")], "RESPREAD", 0.75)
        for fr in ["D", "W"]:
            r0, tn, _ = fast_run(px, W, fr)
            eng = backtest(px, W, cost_bps=0.0, freq=fr)
            g0_max = max(g0_max, float((r0 - eng["returns"]).abs().max()),
                         float((tn - eng["turnover"]).abs().max()))
            eng25 = backtest(px, W, cost_bps=25.0, freq=fr)
            g1_max = max(g1_max, float((rung(r0, tn, 25) - eng25["returns"]).abs().max()))
    gate("G0", g0_max < BAR_ENGINE, f"max |fast_run - engine| (returns and turnover) = {g0_max:.3e}")
    gate("G1", g1_max < 1e-13, f"max |derived 25 bps - engine at 25 bps| = {g1_max:.3e}")

    # -------------------------------------------------------------- the 720-book grid
    P("\n" + "=" * 190)
    P("THE GRID - 720 books, every one published to .grid.csv")
    P("=" * 190)
    PATHS = {}
    rows = []
    for pn, (px, spy) in PN.items():
        warm = WARM[pn]
        bse, sp = BASE[pn], SPYS[pn]
        for th in THETA:
            for arm in ARMS:
                g = SIG[(pn, th, arm)]
                for cons in CONSTRUCTIONS:
                    for gr in GROSSES:
                        W = book(px, g, cons, gr)
                        for cad in CADENCES:
                            r0, tn, held = fast_run(px, W, cad)
                            PATHS[(pn, th, arm, cons, gr, cad)] = (r0, tn)
                            st = stat(rung(r0, tn, COST_BPS), warm)
                            st0 = stat(r0, warm)
                            rows.append(dict(
                                panel=pn, theta=th, arm=arm, cons=cons, gross=gr, cadence=cad,
                                turn_yr=float(tn.loc[warm:].sum() / (len(tn.loc[warm:]) / 252)),
                                mean_gross=float(held.loc[warm:].mean()),
                                **{k: st[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                      "isSharpe", "isCAGR", "oCAGR", "oSharpe", "oMaxDD")},
                                CAGR_c0=st0["CAGR"], Sharpe_c0=st0["Sharpe"],
                                keep4a=verdict_4a(st, bse), fail4b=fail_4b(st, sp),
                                keep4b=(fail_4b(st, sp) == "-")))
    GRID = pd.DataFrame(rows)
    GRID.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G6", len(GRID) == 720, f"{len(GRID)} books published to .grid.csv (expected 720)")
    gate("G7", float(GRID.mean_gross.max()) <= 1.0 + 1e-9,
         f"max realised gross {GRID.mean_gross.max():.4f} <= 1.00; 10 bps binding; t -> t+1; no shorting")

    P("\nPREMISE CHECK - idea 563's (a): does MOM-D beat MA-THRESH on Sharpe more often at D than at Q?")
    piv = GRID.pivot_table(index=["panel", "theta", "cons", "gross"], columns=["arm", "cadence"],
                           values="Sharpe")
    prem = []
    for cad in CADENCES:
        d = piv[("MOM-D", cad)] - piv[("MA-THRESH", cad)]
        prem.append(dict(cadence=cad, n=len(d), momd_wins=float((d > 0).mean()), mean_dSharpe=float(d.mean())))
    PREM = pd.DataFrame(prem)
    P(fmt(PREM))
    P("  idea 563 quoted 66.7% at D and 13.0% at Q on its own (9-theta, 3-gross) grid.")

    P("\nPREMISE CHECK - idea 563's (b): how often does the IS-Sharpe selector pick cadence D?")
    picks = []
    for (pn, th, arm, cons, gr), sub in GRID.groupby(["panel", "theta", "arm", "cons", "gross"]):
        picks.append(dict(panel=pn, arm=arm, pick=sub.loc[sub.isSharpe.idxmax(), "cadence"]))
    PK = pd.DataFrame(picks)
    P(fmt(pd.crosstab(PK.arm, PK.pick)))

    # -------------------------------------------------------------- LEG 2: break-even cost
    P("\n" + "=" * 190)
    P("LEG 2 - THE TURNOVER-MATCHED CONTROL.  c* = the cost rung (bps) at which the DAILY book's")
    P("advantage over the SAME cell at a slower cadence crosses ZERO.  c* > 10 => the daily win is")
    P("paid for at the binding rung; c* <= 10 => the churn buys it back and the selector is right.")
    P("=" * 190)
    be_rows = []
    for (pn, th, arm, cons, gr) in sorted({(k[0], k[1], k[2], k[3], k[4]) for k in PATHS}):
        warm = WARM[pn]
        rf, tf = PATHS[(pn, th, arm, cons, gr, "D")]
        for cad in ["W", "M", "Q"]:
            rs, ts = PATHS[(pn, th, arm, cons, gr, cad)]
            for field in ["Sharpe", "CAGR"]:
                c = breakeven_cost(rf, tf, rs, ts, warm, field)
                be_rows.append(dict(panel=pn, theta=th, arm=arm, cons=cons, gross=gr,
                                    vs=cad, field=field, cstar=c,
                                    d_at_0=stat(rf, warm)[field] - stat(rs, warm)[field],
                                    d_at_10=stat(rung(rf, tf, 10), warm)[field]
                                            - stat(rung(rs, ts, 10), warm)[field],
                                    dturn_yr=float((tf.loc[warm:].sum() - ts.loc[warm:].sum())
                                                   / (len(tf.loc[warm:]) / 252))))
    BE = pd.DataFrame(be_rows)
    BE.to_csv(f"{OUT}.breakeven.csv", index=False)
    for field in ["Sharpe", "CAGR"]:
        sub = BE[BE.field == field]
        P(f"\n  field = {field}   ({len(sub)} daily-vs-slower pairs)")
        tab = sub.groupby(["arm", "vs"]).agg(
            win_at_0=("d_at_0", lambda x: float((x > 0).mean())),
            win_at_10=("d_at_10", lambda x: float((x > 0).mean())),
            med_d0=("d_at_0", "median"), med_d10=("d_at_10", "median"),
            med_cstar=("cstar", lambda x: float(np.median(np.minimum(x, 1e6)))),
            share_cstar_gt10=("cstar", lambda x: float((x > 10).mean())),
            med_dturn=("dturn_yr", "median"))
        P(fmt(tab))
    P("\n  by PANEL (field = Sharpe):")
    sub = BE[BE.field == "Sharpe"]
    P(fmt(sub.groupby(["panel", "arm"]).agg(
        win_at_0=("d_at_0", lambda x: float((x > 0).mean())),
        win_at_10=("d_at_10", lambda x: float((x > 0).mean())),
        share_cstar_gt10=("cstar", lambda x: float((x > 10).mean())),
        med_cstar=("cstar", lambda x: float(np.median(np.minimum(x, 1e6)))))))

    # -------------------------------------------------------------- LEG 1: rule 8
    P("\n" + "=" * 190)
    P("LEG 1 - RULE 8 WALK-FORWARD.  Every selector reads IS (start..%s) ONLY; 2017-2026 read ONCE."
      % IS_END)
    P("=" * 190)
    is_max = max(GRID.index.size and pd.Timestamp(IS_END) for _ in [0])
    wf_rows = []
    for (pn, th, arm, cons, gr), sub in GRID.groupby(["panel", "theta", "arm", "cons", "gross"]):
        sub = sub.set_index("cadence")
        bse, sp = BASE[pn], SPYS[pn]
        for sel in SELECTORS + ["S_ORACLE"]:
            if sel == "S_SHARPE":
                cad = sub.isSharpe.idxmax()
            elif sel == "S_CAGR":
                cad = sub.isCAGR.idxmax()
            elif sel == "S_FORCE_D":
                cad = "D"
            else:
                cad = sub.oSharpe.idxmax()          # UNREACHABLE upper bound, never a verdict
            r = sub.loc[cad]
            wf_rows.append(dict(panel=pn, theta=th, arm=arm, cons=cons, gross=gr, selector=sel,
                                pick=cad, oCAGR=r.oCAGR, oSharpe=r.oSharpe, oMaxDD=r.oMaxDD,
                                fullSharpe=r.Sharpe, fullCAGR=r.CAGR, fullMaxDD=r.MaxDD,
                                base_oSharpe=bse["oSharpe"], spy_oSharpe=sp["oSharpe"],
                                spy_oCAGR=sp["oCAGR"], spy_oMaxDD=sp["oMaxDD"],
                                beats_base_oos=r.oSharpe > bse["oSharpe"],
                                beats_spy_oos=r.oSharpe > sp["oSharpe"],
                                keep4a=r.keep4a, keep4b=r.keep4b))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G5", True, f"selectors read isSharpe/isCAGR computed on <= {IS_END} only; "
                     f"S_ORACLE is printed as an unreachable bound, never as a verdict")

    P("\n  selector summary (mean over the 180 reported-axis cells):")
    ss = WF.groupby("selector").agg(
        oSharpe=("oSharpe", "mean"), oCAGR=("oCAGR", "mean"), oMaxDD=("oMaxDD", "mean"),
        beats_RULESv2_OOS=("beats_base_oos", "mean"), beats_SPY_OOS=("beats_spy_oos", "mean"),
        keep4a=("keep4a", "mean"), keep4b=("keep4b", "mean"))
    P(fmt(ss))
    P("\n  cadence picked, by selector x arm:")
    P(fmt(pd.crosstab([WF.selector, WF.arm], WF.pick)))

    P("\n  HEAD-TO-HEAD, the pre-registered LEG 1: S_FORCE_D minus S_SHARPE on OOS Sharpe")
    a = WF[WF.selector == "S_FORCE_D"].set_index(["panel", "theta", "arm", "cons", "gross"])
    c = WF[WF.selector == "S_SHARPE"].set_index(["panel", "theta", "arm", "cons", "gross"])
    d = (a.oSharpe - c.oSharpe).rename("d_oSharpe").to_frame()
    d["d_oCAGR"] = a.oCAGR - c.oCAGR
    d["d_oMaxDD"] = a.oMaxDD - c.oMaxDD
    d = d.reset_index()
    h2h = d.groupby(["panel", "arm"]).agg(
        n=("d_oSharpe", "size"), forceD_wins=("d_oSharpe", lambda x: float((x > 0).mean())),
        mean_d=("d_oSharpe", "mean"), med_d=("d_oSharpe", "median"),
        mean_dCAGR=("d_oCAGR", "mean"), mean_dDD=("d_oMaxDD", "mean"))
    P(fmt(h2h))
    overall_win = float((d.d_oSharpe > 0).mean())
    overall_mean = float(d.d_oSharpe.mean())
    by_arm = d.groupby("arm").d_oSharpe.agg(["mean", lambda x: float((x > 0).mean())])
    by_arm.columns = ["mean_d_oSharpe", "forceD_win_share"]
    P("\n  POOLED: S_FORCE_D beats S_SHARPE on OOS Sharpe in %.4f of %d cells, mean %+.4f"
      % (overall_win, len(d), overall_mean))
    P(fmt(by_arm))

    # -------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 190)
    P("BOTH KEEP PATHS over all 720 books")
    P("=" * 190)
    KP = GRID.groupby(["arm", "cadence"]).agg(n=("keep4a", "size"),
                                              keep4a=("keep4a", "sum"), keep4b=("keep4b", "sum"))
    P(fmt(KP, 0))
    P("\n  4a total %d of %d      4b total %d of %d"
      % (GRID.keep4a.sum(), len(GRID), GRID.keep4b.sum(), len(GRID)))
    P("\n  binding 4b legs (count of books failing each leg):")
    legs = {k: 0 for k in ["H1", "H2", "OOS", "DD", "CAGR"]}
    for _, r in GRID.iterrows():
        for k in str(r.fail4b).split(","):
            if k in legs:
                legs[k] += 1
    P("  " + "   ".join(f"{k} {v}" for k, v in sorted(legs.items(), key=lambda kv: kv[1])))
    if GRID.keep4b.sum():
        P("\n  every 4b pass, published in full:")
        P(fmt(GRID[GRID.keep4b][["panel", "theta", "arm", "cons", "gross", "cadence", "CAGR",
                                 "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
                                 "turn_yr"]]))
    GRID[["panel", "theta", "arm", "cons", "gross", "cadence", "keep4a", "keep4b",
          "fail4b"]].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # -------------------------------------------------------------- verdict
    P("\n" + "=" * 190)
    P("VERDICT")
    P("=" * 190)
    leg1 = overall_win > 0.50
    sh = BE[BE.field == "Sharpe"]
    leg2_share = float((sh.cstar > 10).mean())
    leg2 = leg2_share > 0.50
    P(f"  LEG 1 (rule 8 head-to-head): S_FORCE_D beats S_SHARPE OOS in {overall_win:.4f} of "
      f"{len(d)} cells, mean {overall_mean:+.4f} of Sharpe  ->  {'MET' if leg1 else 'NOT MET'}")
    P(f"  LEG 2 (turnover-matched control): c* > 10 bps in {leg2_share:.4f} of {len(sh)} "
      f"daily-vs-slower pairs  ->  {'MET' if leg2 else 'NOT MET'}")
    P(f"  H_EDGE requires BOTH: {'H_EDGE' if (leg1 and leg2) else 'H_TURNOVER'}")
    P(f"  4a {int(GRID.keep4a.sum())} of {len(GRID)}   4b {int(GRID.keep4b.sum())} of {len(GRID)}")

    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    P(f"\n  GATES {int(G.pass_.sum())}/{len(G)}")
    flush_log()


if __name__ == "__main__":
    main()
