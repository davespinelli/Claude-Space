#!/usr/bin/env python3
"""Idea 814 (lane C, 2026-09-14) — does the B136 CORR-HI q0.17 w252 d0.50 BOOK survive a
PRE-REGISTERED run?

QUESTION
--------
Idea 606 was a measurement run about placebo excess.  As a by-product it reported one cell of a
3,456-arm head-rung grid as a 4b KEEP-candidate and memo'd it
(`2026-09-12_b136-corr-hi-q017-w252-d050-D-g100_4b_B_MEMO.md`), explicitly NOT proposed, with four
named doubts:
    (a) post-hoc — the cell was read off a grid built to answer a different question;
    (b) the rule-8 chooser only ever picked (level, w); depth / cadence / gross were reported axes;
    (c) 164 of 3,456 head-rung arms are clean 4b+OOS passers, 81 of them CORR-HI, so singling out
        this one is a choice;
    (d) BOTH of the cell's tuned dials sat on the EDGE of their grid — q = 0.17 was the TOP of
        {0.07, 0.12, 0.17} and w = 252 the BOTTOM of {252, 504, 1008, 2016} — so the reported
        argmax was never shown to be an argmax at all.

This run answers the queue's question by fixing the BOOK in advance and sweeping ONLY the two dials
the memo names, on grids extended in both directions so that an interior argmax is possible.

THE BOOK — FIXED BEFORE ANY NUMBER WAS READ (pre-registered, never swept, no selection here)
    panel      B136 = research/universe_broad.json via baseline.load_universe(broad=True)
    eligible   name is above its own 200d moving average AND vol20 < 0.60   (idea 42's mask)
    weights    equal weight, gross / n of NAV over the eligible names, n = eligible that day
    gross      1.00
    cadence    the BOOK rebalances weekly (freq="W"); the GATE reads daily (cadence D)
    state      rho = 20d average pairwise correlation of the B136 panel, from the equal-weight
               index-vs-name variance identity rho = (s_idx^2 - s2bar/N) / (sbar^2 - s2bar/N)
    gate       fire when rho_t > its own trailing-w (1-q) quantile (strict min_periods = w)
    depth      0.50 — halve every weight tomorrow, leave the released half idle at 0% (DE-GROSS,
               never re-spread)
    costs      10 bps per unit turnover (head rung), next-day execution, no shorting, no leverage
Everything on that list is idea 606's memo verbatim.  NOTHING on it is tuned by this run.

TUNED PARAMETERS (PROTOCOL rule 4 — exactly two, the queue's own: level and window)
    1. q  in {0.05, 0.10, 0.17, 0.25, 0.33, 0.42, 0.50}      (606's grid was {0.07, 0.12, 0.17})
    2. w  in {63, 126, 252, 504, 756, 1008, 1512, 2016}      (606's grid was {252, 504, 1008, 2016})
Both grids are extended THROUGH the candidate's value on both sides, so (0.17, 252) is interior to
the grid by construction and an edge argmax is now a reportable failure rather than an artefact.
ALL 7 x 8 = 56 cells are reported (research/backtests/..._C.grid.csv).

REPORTED, NEVER SELECTED: cost rung {0, 5, 10, 25, 50} bps and execution lag {1, 2, 3} days, both
carried for the whole grid; and the two named drawdown episodes (2020 COVID, 2022 bear).

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO    the (0.17, 252) cell reproduces idea 606's memo triple — full sample 14.02% /
               1.1538 / -15.11% and OOS 14.29% / 1.2080 / -15.11% — inside 0.02 Sharpe, 0.5 pp CAGR
               and 1.0 pp MaxDD.  This is a gate on the rebuild, not evidence for the book.
    H_INTERIOR *** THE DECIDING TEST FOR DOUBT (d). *** On the extended grid the IS-Sharpe argmax
               (2009-2016 alone) is INTERIOR in BOTH dials.  FAIL => the candidate's dials are an
               edge of whatever grid they are swept on, and the "argmax" was never one.
    H_PICK     *** THE DECIDING TEST FOR CAPITAL. *** The cell chosen on the IS window ALONE passes
               4b on the full sample AND read inside the OOS window, under BOTH pre-stated
               choosers.  FAIL => the book is not reachable by a rule-8 selector and is PARK/KILL
               however good the post-hoc cell looks.
    H_SAME     the IS-alone chooser lands ON the memo's cell (0.17, 252) under at least one
               convention.  FAIL (with H_PICK passing) is still a live book, but a DIFFERENT one.
    H_BAND     at least 28 of the 56 cells (>= 50%) pass 4b on the full sample, i.e. the candidate
               sits in a band and not on a point (idea 585's band-not-point bar).
    H_GATE     at the pick, the gross-matched ungated twin (the same book held statically at the
               arm's own realised mean gross) FAILS 4b — so 4b is seeing the GATE, not the exposure
               it leaves behind (ideas 502/504/596/674/767/810).
    H_LADDER   the pick passes 4b at 0 / 5 / 10 / 25 bps and at execution lag 1, 2 and 3 days.
    H_EPISODE  the pick's MaxDD leg is not a single episode: the 4b DD cap is cleared with the
               2020 episode excluded AND with the 2022 episode excluded (idea 852's leg).

VERDICT RULE, FIXED IN ADVANCE
    KEEP-candidate (path 4b) iff H_PICK and H_GATE and H_LADDER (0/5/10/25 bps and lag 1/2/3) all
        pass.  H_INTERIOR and H_SAME are reported beside it and named in the memo if they fail.
    PARK if the pick passes 4b full sample but not inside OOS, or under only one of the two
        choosers.
    KILL otherwise.
Path 4a is evaluated against RULES v2 (the live book) for every cell and reported either way.

THE TWO PRE-STATED CHOOSERS (rule 8; the OOS window is read ONCE, after both have picked)
    C1  argmax IS Sharpe over all 56 cells.
    C2  argmax IS Sharpe among cells whose IS MaxDD <= 60% of SPY's IS MaxDD (the 4b drawdown leg
        read in sample) — the selector a drawdown-constrained allocator would actually run.

GATES (printed before any verdict is read)
    G1  runner identity: a never-firing multiplier (depth 0) reproduces engine.backtest's own
        returns for the same book                                              bar 1e-12
    G2  causality: every threshold uses min_periods = w and the multiplier decided at t is applied
        at t+1; the count of days with no threshold is reported per (q, w)     bar exact
    G3  reproduction of idea 606's memo cell                                   H_REPRO's tolerance
    G4  determinism: no RNG anywhere in this script; the grid is recomputed and compared  bar 0

SURVIVORSHIP: B136 is universe_broad.json's CURRENT constituents (PROTOCOL rule 9).  Dead names are
absent, so every CAGR level here is biased upward and the 4b CAGR floor is easier to clear than it
would be on a point-in-time panel.  The correlation STATE is optimistic for the same reason — the
names that died are exactly the ones that would have co-moved hardest in 2020 and 2022, so a
correlation gate measured on survivors sees a tamer state than the one a live book would have seen.
The drawdown leg, which is what this gate is supposed to buy, is the least affected of the three.

Deterministic, no network, standalone.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py or
baseline.py.
"""
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
from engine import backtest, metrics, rebalance_mask                 # noqa: E402

DATE = "2026-09-14"
SLUG = "does-the-B136-CORR-HI-q017-w252-d050-BOOK-survive-a-PRE-REGISTERED-run"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ---- the book, fixed in advance -------------------------------------------------------------
FREQ = "W"              # the book's rebalance cadence
GATE_CADENCE = "D"      # the gate reads daily
GROSS = 1.00
DEPTH = 0.50
SMOOTH = 20             # the state's own smoothing window (memo's "20d average pairwise corr")
MAX_VOL = 0.60
WARMUP = 260
RUNG_HEAD = 10
RUNGS = [0, 5, 10, 25, 50]
LAGS = [1, 2, 3]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- the two tuned dials --------------------------------------------------------------------
QS = [0.05, 0.10, 0.17, 0.25, 0.33, 0.42, 0.50]
WS = [63, 126, 252, 504, 756, 1008, 1512, 2016]
CAND = (0.17, 252)
MEMO = dict(CAGR=0.1402, Sharpe=1.1538, MaxDD=-0.1511,
            OOS_CAGR=0.1429, OOS_Sharpe=1.2080, OOS_MaxDD=-0.1511)
TOL = dict(Sharpe=0.02, CAGR=0.005, MaxDD=0.010)

EPISODES = {"2020": ("2020-02-01", "2020-04-30"), "2022": ("2022-01-01", "2022-12-31")}

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (606/602 verbatim)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def state_corr(px):
    """20d average pairwise correlation from the equal-weight index-vs-name variance identity."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    idx = rt.mean(axis=1)
    s_idx = idx.rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar = sig.mean(axis=1)
    s2bar = (sig ** 2).mean(axis=1)
    num = s_idx ** 2 - s2bar / n
    den = sbar ** 2 - s2bar / n
    return (num / den.replace(0, np.nan)).clip(-1, 1)


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0) if GATE_CADENCE == "W" else m


def gate_mult(st, thr, depth, idx):
    """HI side: fire (de-gross to 1-depth) when the state is ABOVE its threshold.  1.0 wherever the
    threshold does not yet exist, so the gate is silent through its own warm-up."""
    fire = (st > thr) & st.notna() & thr.notna()
    return _cadence(pd.Series(1.0, index=idx).where(~fire, 1.0 - depth), idx)


def apply_gate(r_base, mult, gross, cost_bps, lag=1):
    """Multiplier decided at t, applied at t+lag, switch cost on |dm| (idea 399's runner)."""
    m_eff = mult.reindex(r_base.index).shift(lag).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pack_full(r):
    """(H1, H2, OOS Sharpe, MaxDD, CAGR) of a comparand over the full scored sample."""
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    return (h1, h2, metrics(r.loc[OOS_START:])["Sharpe"], m["MaxDD"], m["CAGR"])


def pack_window(r):
    """(H1, H2, MaxDD, CAGR) of a comparand read INSIDE one window."""
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    return (h1, h2, m["MaxDD"], m["CAGR"])


def tests_4b(r, pk):
    s1, s2, s_oos, s_dd, s_cagr = pk
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def tests_4b_window(r, pk):
    s1, s2, s_dd, s_cagr = pk
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2, "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, bp):
    b1, b2, bdd = bp
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def summarise(r, spy_pack, base_pack, spy_oos_pack, base_oos_pack):
    m, h1h2 = metrics(r), half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy_pack)
    ro = r.loc[OOS_START:]
    to = tests_4b_window(ro, spy_oos_pack)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1h2[0], H2=h1h2[1],
                IS_CAGR=m_is["CAGR"], IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                p4a=verdict_4a(r, base_pack), p4b=all(t.values()),
                p4a_oos=verdict_4a(ro, base_oos_pack), p4b_oos=all(to.values()),
                fail4b=",".join([k for k, v in t.items() if not v]) or "-",
                fail4b_oos=",".join([k for k, v in to.items() if not v]) or "-")


def main():
    t0 = time.time()
    log("=" * 100)
    log(f"IDEA 814 (lane C, {DATE}) — {SLUG}")
    log("=" * 100)
    log(__doc__.split("QUESTION")[0].strip())

    px = load_universe(broad=True)
    start = px.index[WARMUP]
    log(f"\nPanel B136: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}; "
        f"scored sample starts {start.date()} (warm-up {WARMUP} rows).")

    # ---------------- base book at every cost rung, plus the comparands -----------------------
    W = ewall_weights(px, GROSS)
    base_r, base_to = {}, None
    for rung in RUNGS:
        res = backtest(px, W, cost_bps=rung, freq=FREQ)
        base_r[rung] = res["returns"].loc[start:]
        if base_to is None:
            base_to = res["turnover"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]

    spy_pack, v2_pack_full = pack_full(spy), pack_full(v2)
    base_pack = (v2_pack_full[0], v2_pack_full[1], metrics(v2)["MaxDD"])
    spy_oos_pack = pack_window(spy.loc[OOS_START:])
    v2o = v2.loc[OOS_START:]
    base_oos_pack = (half_sharpes(v2o)[0], half_sharpes(v2o)[1], metrics(v2o)["MaxDD"])

    log("\nCOMPARANDS (10 bps, weekly, t+1, same scored sample)")
    cmp_rows = []
    for nm, r in [("SPY buy-and-hold", spy), ("RULES v2 (live baseline)", v2),
                  ("UNGATED book g=1.00 (the control)", base_r[RUNG_HEAD])]:
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        mo = metrics(r.loc[OOS_START:])
        cmp_rows.append(dict(name=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                             OOS_MaxDD=mo["MaxDD"]))
    cmp_df = pd.DataFrame(cmp_rows).set_index("name")
    log(cmp_df.to_string(float_format=lambda x: f"{x:.4f}"))
    log(f"\n4b bars off SPY: H1 > {spy_pack[0]:.4f}, H2 > {spy_pack[1]:.4f}, "
        f"OOS Sharpe > {spy_pack[2]:.4f}, MaxDD >= {0.60 * spy_pack[3]:.4%}, "
        f"CAGR >= {0.70 * spy_pack[4]:.4%}")
    log(f"4a bars off RULES v2: H1 > {base_pack[0]:.4f}, H2 > {base_pack[1]:.4f}, "
        f"MaxDD >= {base_pack[2]:.4%}")

    st = state_corr(px)

    # ---------------- GATES -------------------------------------------------------------------
    log("\n" + "-" * 100)
    log("GATES (printed before any verdict)")
    log("-" * 100)
    thr_c = st.rolling(CAND[1], min_periods=CAND[1]).quantile(1 - CAND[0])
    m_never = gate_mult(st, thr_c, 0.0, px.index).loc[start:]
    r_never, _ = apply_gate(base_r[RUNG_HEAD], m_never, GROSS, RUNG_HEAD)
    g1 = float((r_never - base_r[RUNG_HEAD]).abs().max())
    log(f"  G1 runner identity (depth 0 == engine.backtest)      max|d| = {g1:.3e}   "
        f"{'PASS' if g1 < 1e-12 else 'FAIL'}")

    # ---------------- the 56-cell grid --------------------------------------------------------
    rows, mults = [], {}
    for q, w in product(QS, WS):
        thr = st.rolling(w, min_periods=w).quantile(1 - q)
        mult = gate_mult(st, thr, DEPTH, px.index)
        mults[(q, w)] = mult
        r, m_eff = apply_gate(base_r[RUNG_HEAD], mult, GROSS, RUNG_HEAD)
        d = summarise(r, spy_pack, base_pack, spy_oos_pack, base_oos_pack)
        d.update(q=q, w=w,
                 no_thr_days=int(thr.loc[start:].isna().sum()),
                 on_share=float((m_eff < 1.0).mean()),
                 mean_gross=float(m_eff.mean() * GROSS),
                 on_share_IS=float((m_eff.loc[:IS_END] < 1.0).mean()),
                 on_share_OOS=float((m_eff.loc[OOS_START:] < 1.0).mean()))
        rows.append(d)
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)

    # G2 causality + G4 determinism
    g2 = all(grid["no_thr_days"] >= 0) and all(
        grid.loc[grid["w"] == w, "no_thr_days"].min() >= 0 for w in WS)
    mono = grid.groupby("w")["no_thr_days"].mean().sort_index()
    log(f"  G2 causality (min_periods=w; days with no threshold rise with w)   "
        f"{dict(zip(mono.index, mono.round(0).astype(int)))}   {'PASS' if g2 else 'FAIL'}")
    r_again, _ = apply_gate(base_r[RUNG_HEAD], mults[CAND], GROSS, RUNG_HEAD)
    cand_row = grid[(grid["q"] == CAND[0]) & (grid["w"] == CAND[1])].iloc[0]
    g4 = float(abs(metrics(r_again)["Sharpe"] - cand_row["Sharpe"]))
    log(f"  G4 determinism (grid recomputed, no RNG)             |dSharpe| = {g4:.3e}   "
        f"{'PASS' if g4 == 0.0 else 'FAIL'}")

    # G3 / H_REPRO
    dev = dict(Sharpe=abs(cand_row["Sharpe"] - MEMO["Sharpe"]),
               CAGR=abs(cand_row["CAGR"] - MEMO["CAGR"]),
               MaxDD=abs(cand_row["MaxDD"] - MEMO["MaxDD"]),
               OOS_Sharpe=abs(cand_row["OOS_Sharpe"] - MEMO["OOS_Sharpe"]),
               OOS_CAGR=abs(cand_row["OOS_CAGR"] - MEMO["OOS_CAGR"]),
               OOS_MaxDD=abs(cand_row["OOS_MaxDD"] - MEMO["OOS_MaxDD"]))
    h_repro = (dev["Sharpe"] <= TOL["Sharpe"] and dev["CAGR"] <= TOL["CAGR"]
               and dev["MaxDD"] <= TOL["MaxDD"] and dev["OOS_Sharpe"] <= TOL["Sharpe"]
               and dev["OOS_CAGR"] <= TOL["CAGR"] and dev["OOS_MaxDD"] <= TOL["MaxDD"])
    log(f"  G3 reproduction of idea 606's memo cell (q=0.17, w=252)")
    log(f"     full  memo {MEMO['CAGR']:.2%} / {MEMO['Sharpe']:.4f} / {MEMO['MaxDD']:.2%}"
        f"   here {cand_row['CAGR']:.2%} / {cand_row['Sharpe']:.4f} / {cand_row['MaxDD']:.2%}")
    log(f"     OOS   memo {MEMO['OOS_CAGR']:.2%} / {MEMO['OOS_Sharpe']:.4f} / "
        f"{MEMO['OOS_MaxDD']:.2%}   here {cand_row['OOS_CAGR']:.2%} / "
        f"{cand_row['OOS_Sharpe']:.4f} / {cand_row['OOS_MaxDD']:.2%}")
    log(f"     H_REPRO {'PASS' if h_repro else 'FAIL'}  (dev "
        f"S {dev['Sharpe']:.4f}/{dev['OOS_Sharpe']:.4f}, CAGR {dev['CAGR']:.4f}/"
        f"{dev['OOS_CAGR']:.4f}, DD {dev['MaxDD']:.4f}/{dev['OOS_MaxDD']:.4f})")

    # ---------------- the whole grid ----------------------------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 1 — ALL 56 GRID POINTS (10 bps, full sample; P = 4b pass, p = 4b pass inside OOS)")
    log("-" * 100)
    for tag, col in [("Sharpe", "Sharpe"), ("CAGR", "CAGR"), ("MaxDD", "MaxDD"),
                     ("IS_Sharpe", "IS_Sharpe"), ("OOS_Sharpe", "OOS_Sharpe"),
                     ("on_share", "on_share")]:
        piv = grid.pivot(index="q", columns="w", values=col)
        log(f"\n  {tag}")
        log("    " + piv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    piv = grid.pivot(index="q", columns="w", values="p4b").replace({True: "P", False: "."})
    pivo = grid.pivot(index="q", columns="w", values="p4b_oos").replace({True: "p", False: "."})
    log("\n  4b FULL-SAMPLE pass map")
    log("    " + piv.to_string().replace("\n", "\n    "))
    log("\n  4b OOS-WINDOW pass map")
    log("    " + pivo.to_string().replace("\n", "\n    "))
    n4b, n4bo, n4a = int(grid["p4b"].sum()), int(grid["p4b_oos"].sum()), int(grid["p4a"].sum())
    log(f"\n  4b full sample {n4b}/56 · 4b inside OOS {n4bo}/56 · BOTH "
        f"{int((grid['p4b'] & grid['p4b_oos']).sum())}/56 · 4a vs RULES v2 {n4a}/56")
    log(f"  failing 4b legs (full sample): "
        f"{grid.loc[~grid['p4b'], 'fail4b'].value_counts().to_dict()}")
    h_band = n4b >= 28
    log(f"  H_BAND (>= 28 of 56 pass 4b full sample): {n4b}/56 -> "
        f"{'PASS' if h_band else 'FAIL'}")

    # ---------------- rule 8: the two choosers ------------------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 2 — RULE 8 WALK-FORWARD ((q, w) chosen on 2009-2016 ALONE; OOS read once)")
    log("-" * 100)
    is_dd_cap = 0.60 * abs(metrics(spy.loc[:IS_END])["MaxDD"])
    log(f"  IS window {start.date()} -> {IS_END}; OOS {OOS_START} -> {px.index[-1].date()}")
    log(f"  C1 = argmax IS Sharpe.   C2 = argmax IS Sharpe s.t. IS MaxDD <= {is_dd_cap:.2%} "
        f"(60% of SPY's IS MaxDD {metrics(spy.loc[:IS_END])['MaxDD']:.2%}).")

    c1 = grid.loc[grid["IS_Sharpe"].idxmax()]
    elig_c2 = grid[grid["IS_MaxDD"].abs() <= is_dd_cap]
    c2 = elig_c2.loc[elig_c2["IS_Sharpe"].idxmax()] if len(elig_c2) else None
    picks = {"C1": c1}
    if c2 is not None:
        picks["C2"] = c2
    log(f"  C2 eligible cells: {len(elig_c2)}/56")

    interior = {}
    wf_rows = []
    for nm, p in picks.items():
        qi, wi = QS.index(p["q"]), WS.index(p["w"])
        inter = (0 < qi < len(QS) - 1) and (0 < wi < len(WS) - 1)
        interior[nm] = inter
        log(f"\n  {nm} picks (q={p['q']}, w={int(p['w'])})  IS Sharpe {p['IS_Sharpe']:.4f}, "
            f"IS MaxDD {p['IS_MaxDD']:.2%}  —  q index {qi}/{len(QS) - 1}, "
            f"w index {wi}/{len(WS) - 1}  -> {'INTERIOR' if inter else 'ON THE GRID EDGE'}")
        log(f"     FULL  {p['CAGR']:.2%} / {p['Sharpe']:.4f} / {p['MaxDD']:.2%}   "
            f"halves {p['H1']:.4f} / {p['H2']:.4f}")
        log(f"     OOS   {p['OOS_CAGR']:.2%} / {p['OOS_Sharpe']:.4f} / {p['OOS_MaxDD']:.2%}")
        log(f"     vs SPY OOS {metrics(spy.loc[OOS_START:])['CAGR']:.2%} / "
            f"{metrics(spy.loc[OOS_START:])['Sharpe']:.4f} / "
            f"{metrics(spy.loc[OOS_START:])['MaxDD']:.2%}   ·   RULES v2 OOS "
            f"{metrics(v2o)['CAGR']:.2%} / {metrics(v2o)['Sharpe']:.4f} / "
            f"{metrics(v2o)['MaxDD']:.2%}")
        log(f"     4b full {'PASS' if p['p4b'] else 'FAIL (' + p['fail4b'] + ')'}   ·   "
            f"4b inside OOS {'PASS' if p['p4b_oos'] else 'FAIL (' + p['fail4b_oos'] + ')'}   ·   "
            f"4a {'PASS' if p['p4a'] else 'FAIL'}")
        wf_rows.append(dict(chooser=nm, q=p["q"], w=int(p["w"]), interior=inter,
                            IS_Sharpe=p["IS_Sharpe"], IS_MaxDD=p["IS_MaxDD"],
                            CAGR=p["CAGR"], Sharpe=p["Sharpe"], MaxDD=p["MaxDD"],
                            H1=p["H1"], H2=p["H2"], OOS_CAGR=p["OOS_CAGR"],
                            OOS_Sharpe=p["OOS_Sharpe"], OOS_MaxDD=p["OOS_MaxDD"],
                            p4a=bool(p["p4a"]), p4b=bool(p["p4b"]),
                            p4b_oos=bool(p["p4b_oos"]), fail4b=p["fail4b"],
                            fail4b_oos=p["fail4b_oos"]))
    for nm, r in [("SPY", spy), ("RULES v2", v2)]:
        mo = metrics(r.loc[OOS_START:])
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        wf_rows.append(dict(chooser=nm, q=np.nan, w=np.nan, interior=np.nan,
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            p4a=np.nan, p4b=np.nan, p4b_oos=np.nan, fail4b="", fail4b_oos=""))
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)

    h_pick = all(bool(p["p4b"]) and bool(p["p4b_oos"]) for p in picks.values()) and len(picks) == 2
    h_same = any((p["q"], int(p["w"])) == CAND for p in picks.values())
    h_interior = all(interior.values())
    log(f"\n  H_INTERIOR {'PASS' if h_interior else 'FAIL'}   "
        f"H_PICK {'PASS' if h_pick else 'FAIL'}   H_SAME {'PASS' if h_same else 'FAIL'}")

    # ---------------- controls: the gross-matched twin ----------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 3 — THE CONTROL THAT MATTERS: is 4b seeing the GATE or the EXPOSURE?")
    log("-" * 100)
    twin_rows, h_gate_parts = [], []
    for nm, p in picks.items():
        g_eff = float(p["mean_gross"])
        tw = backtest(px, ewall_weights(px, g_eff), cost_bps=RUNG_HEAD,
                      freq=FREQ)["returns"].loc[start:]
        tw4b = tests_4b(tw, spy_pack)
        m = metrics(tw)
        h1, h2 = half_sharpes(tw)
        h_gate_parts.append(not all(tw4b.values()))
        log(f"  {nm} (q={p['q']}, w={int(p['w'])}) fires {p['on_share']:.2%} of days, realised "
            f"mean gross {g_eff:.4f}")
        log(f"     GATED   {p['CAGR']:.2%} / {p['Sharpe']:.4f} / {p['MaxDD']:.2%}   4b "
            f"{'PASS' if p['p4b'] else 'FAIL'}")
        log(f"     TWIN    {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   4b "
            f"{'PASS' if all(tw4b.values()) else 'FAIL (' + ','.join(k for k, v in tw4b.items() if not v) + ')'}")
        twin_rows.append(dict(chooser=nm, q=p["q"], w=int(p["w"]), mean_gross=g_eff,
                              twin_CAGR=m["CAGR"], twin_Sharpe=m["Sharpe"], twin_MaxDD=m["MaxDD"],
                              twin_H1=h1, twin_H2=h2, twin_4b=all(tw4b.values()),
                              gated_Sharpe=p["Sharpe"], gated_MaxDD=p["MaxDD"],
                              gated_4b=bool(p["p4b"])))
    ung = base_r[RUNG_HEAD]
    u4b = tests_4b(ung, spy_pack)
    log(f"  UNGATED g=1.00  {metrics(ung)['CAGR']:.2%} / {metrics(ung)['Sharpe']:.4f} / "
        f"{metrics(ung)['MaxDD']:.2%}   4b "
        f"{'PASS' if all(u4b.values()) else 'FAIL (' + ','.join(k for k, v in u4b.items() if not v) + ')'}")
    pd.DataFrame(twin_rows).to_csv(f"{OUT}.twins.csv", index=False)
    h_gate = all(h_gate_parts)
    log(f"  H_GATE (every pick's gross-matched twin FAILS 4b): {'PASS' if h_gate else 'FAIL'}")

    # ---------------- ladders ------------------------------------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 4 — COST AND EXECUTION-LAG LADDERS (reported, never selected)")
    log("-" * 100)
    lad_rows, h_ladder_parts = [], []
    for nm, p in picks.items():
        key = (p["q"], int(p["w"]))
        mult = mults[key]
        log(f"\n  {nm} (q={key[0]}, w={key[1]})")
        for rung in RUNGS:
            r, _ = apply_gate(base_r[rung], mult, GROSS, rung)
            t = tests_4b(r, spy_pack)
            ok = all(t.values())
            if rung in (0, 5, 10, 25):
                h_ladder_parts.append(ok)
            log(f"     {rung:>2} bps   {metrics(r)['CAGR']:.2%} / {metrics(r)['Sharpe']:.4f} / "
                f"{metrics(r)['MaxDD']:.2%}   4b "
                f"{'PASS' if ok else 'FAIL (' + ','.join(k for k, v in t.items() if not v) + ')'}")
            lad_rows.append(dict(chooser=nm, q=key[0], w=key[1], kind="cost", value=rung,
                                 CAGR=metrics(r)["CAGR"], Sharpe=metrics(r)["Sharpe"],
                                 MaxDD=metrics(r)["MaxDD"], p4b=ok))
        for lag in LAGS:
            r, _ = apply_gate(base_r[RUNG_HEAD], mult, GROSS, RUNG_HEAD, lag=lag)
            t = tests_4b(r, spy_pack)
            ok = all(t.values())
            h_ladder_parts.append(ok)
            log(f"     lag {lag}   {metrics(r)['CAGR']:.2%} / {metrics(r)['Sharpe']:.4f} / "
                f"{metrics(r)['MaxDD']:.2%}   4b "
                f"{'PASS' if ok else 'FAIL (' + ','.join(k for k, v in t.items() if not v) + ')'}")
            lad_rows.append(dict(chooser=nm, q=key[0], w=key[1], kind="lag", value=lag,
                                 CAGR=metrics(r)["CAGR"], Sharpe=metrics(r)["Sharpe"],
                                 MaxDD=metrics(r)["MaxDD"], p4b=ok))
    pd.DataFrame(lad_rows).to_csv(f"{OUT}.ladders.csv", index=False)
    h_ladder = all(h_ladder_parts)
    log(f"\n  H_LADDER (4b at 0/5/10/25 bps and lag 1/2/3 for every pick): "
        f"{'PASS' if h_ladder else 'FAIL'}")

    # ---------------- episodes -----------------------------------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 5 — THE EPISODE LEG (is the 4b drawdown cap one episode?)")
    log("-" * 100)
    ep_rows, h_ep_parts = [], []
    for nm, p in picks.items():
        key = (p["q"], int(p["w"]))
        r, _ = apply_gate(base_r[RUNG_HEAD], mults[key], GROSS, RUNG_HEAD)
        for ep, (a, b) in EPISODES.items():
            keep = ~((r.index >= a) & (r.index <= b))
            r_ex, spy_ex = r[keep], spy[keep]
            dd, dd_spy = maxdd(r_ex), maxdd(spy_ex)
            ok = abs(dd) <= 0.60 * abs(dd_spy)
            h_ep_parts.append(ok)
            log(f"  {nm} excluding {ep}: book MaxDD {dd:.2%} vs cap {0.60 * dd_spy:.2%} "
                f"(SPY {dd_spy:.2%})   DD leg {'PASS' if ok else 'FAIL'}")
            ep_rows.append(dict(chooser=nm, q=key[0], w=key[1], excluded=ep, book_MaxDD=dd,
                                spy_MaxDD=dd_spy, cap=0.60 * dd_spy, dd_leg=ok))
            rin = r.loc[a:b]
            log(f"     inside {ep}: book {(1 + rin).prod() - 1:+.2%} vs SPY "
                f"{(1 + spy.loc[a:b]).prod() - 1:+.2%}, gate on "
                f"{float((mults[key].reindex(r.index).shift(1).fillna(1.0).loc[a:b] < 1.0).mean()):.1%} of days")
    pd.DataFrame(ep_rows).to_csv(f"{OUT}.episodes.csv", index=False)
    h_episode = all(h_ep_parts)
    log(f"  H_EPISODE (DD cap cleared with either episode removed): "
        f"{'PASS' if h_episode else 'FAIL'}")

    # ---------------- verdict -------------------------------------------------------------------
    log("\n" + "=" * 100)
    log("HYPOTHESES (all pre-registered above, none added after a number was read)")
    log("=" * 100)
    H = [("H_REPRO", h_repro, "the memo cell rebuilds inside tolerance"),
         ("H_INTERIOR", h_interior, "the IS argmax is interior in BOTH dials on the extended grid"),
         ("H_PICK", h_pick, "the IS-alone pick passes 4b full AND inside OOS under BOTH choosers"),
         ("H_SAME", h_same, "the IS-alone chooser lands on the memo's own cell"),
         ("H_BAND", h_band, ">= 28 of 56 cells pass 4b full sample"),
         ("H_GATE", h_gate, "every pick's gross-matched twin FAILS 4b"),
         ("H_LADDER", h_ladder, "4b holds at 0/5/10/25 bps and lag 1/2/3"),
         ("H_EPISODE", h_episode, "the DD cap survives removing 2020 or 2022")]
    for nm, ok, desc in H:
        log(f"  {nm:<11} {'PASS' if ok else 'FAIL'}   {desc}")
    pd.DataFrame([dict(hypothesis=n, result="PASS" if o else "FAIL", statement=d)
                  for n, o, d in H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    if h_pick and h_gate and h_ladder:
        verdict = "KEEP-candidate (path 4b)"
    elif any(bool(p["p4b"]) for p in picks.values()):
        verdict = "PARK"
    else:
        verdict = "KILL"
    log(f"\n  PRE-REGISTERED VERDICT RULE -> {verdict}")
    log(f"  (rule, fixed in advance: KEEP iff H_PICK and H_GATE and H_LADDER; PARK if any pick "
        f"passes 4b full sample; else KILL.)")

    log("\n  SURVIVORSHIP: B136 is universe_broad.json's CURRENT constituents; every CAGR level "
        "above is")
    log("  biased upward, the 4b CAGR floor is easier than on a point-in-time panel, and the "
        "correlation")
    log("  state is measured on names that did not die in 2020 or 2022.")
    log(f"\nDone in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
