#!/usr/bin/env python3
"""Idea 863 (lane C, 2026-09-15) — is the CORR-HI gate worth anything once the 2022 EPISODE
is the only evidence?

QUESTION
--------
Idea 814 priced the B136 CORR-HI candidate episode by episode and found the gate's real work is
lopsided: inside the 2020 COVID episode the book lost -7.26% against SPY's -9.18% (a 1.9 pp edge,
gate on for 72.6% of days), while inside 2022 the book lost -7.24% against SPY's -18.18% (a 10.9 pp
edge, gate on for 51.4% of days).  Essentially all of the clause's visible value is ONE bear market.
The queue's question: price the gate on a corpus with 2022 REMOVED and on 2022 ALONE, each against
the gate's OWN matched-gross twin, and report whether ANY non-2022 evidence for the clause exists.

A gate that only ever beats its matched-gross twin inside one 12-month window is not a market-state
clause — it is a dated bet on one bear market, and a live book cannot be sized on it.

THE BOOK — FIXED BEFORE ANY NUMBER WAS READ (idea 606's memo verbatim, via idea 814; not tuned here)
    panel      B136 = research/universe_broad.json via baseline.load_universe(broad=True)
    eligible   name above its own 200d moving average AND vol20 < 0.60      (idea 42's mask)
    weights    equal weight, gross / n of NAV over the eligible names, n = eligible that day
    gross      1.00
    cadence    the BOOK rebalances weekly (freq="W"); the GATE reads daily
    state      rho = 20d average pairwise correlation of the B136 panel, from the equal-weight
               index-vs-name variance identity
    gate       HI side: fire (de-gross) when rho_t > its own trailing-w (1 - q) quantile,
               strict min_periods = w
    LEVEL      q = 0.17 — the memo's own value, FIXED here, NOT a tuned parameter of this run
    costs      10 bps per unit turnover (head rung), next-day execution, no shorting, no leverage

TUNED PARAMETERS (PROTOCOL rule 4 — exactly two, the queue's own: WINDOW and DEPTH)
    1. w      in {63, 126, 252, 504, 756, 1008, 1512, 2016}     (memo cell w = 252, interior)
    2. depth  in {0.10, 0.25, 0.50, 0.75, 1.00}                 (memo cell depth = 0.50, interior)
ALL 8 x 5 = 40 cells are reported at every corpus (research/backtests/..._C.grid.csv).

THE CORPORA (pre-stated, never tuned; a corpus is a DAY SET, spliced and read as a contiguous
sequence of trading days — idea 814's own convention for its episode leg)
    FULL        the whole scored sample
    EX2022      2022-01-01 .. 2022-12-31 removed              <- where non-2022 evidence must live
    ONLY2022    2022-01-01 .. 2022-12-31 alone                <- the queue's single-episode corpus
    EX2020      2020-02-01 .. 2020-04-30 removed              (reported control, never selected)
    EXBOTH      both episodes removed                          (reported control, never selected)

THE CONTROL AT EVERY CORPUS — the gate's OWN matched-gross twin
    For each (cell, corpus): twin = the SAME book held STATICALLY at the arm's realised mean
    effective gross OVER THAT CORPUS's days, run on the full panel at the ARM'S OWN COST RUNG and
    then read on the same day set.  This is the comparand ideas 502/504/596/674/767/810 and 814
    established: it strips the de-grossing out of the gate and leaves only the TIMING.
    WORKS(cell, corpus) := Sharpe(gated) > Sharpe(twin) AND |MaxDD(gated)| < |MaxDD(twin)|
    — both legs, because the clause's entire published case is that it buys drawdown without
    buying it by simply holding less.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO     the (w=252, depth=0.50) cell reproduces idea 814's FULL-corpus triple
                14.02% / 1.1538 / -15.11% inside 0.02 Sharpe, 0.5 pp CAGR, 1.0 pp MaxDD.
                A gate on the rebuild, not evidence for the book.
    H_PREMISE   the queue's premise: on ONLY2022 the gate WORKS at >= 30 of 40 cells (75%).
    H_NON2022   *** THE DECIDING TEST. *** On EX2022 the gate WORKS at >= 20 of 40 cells (50%).
                FAIL => the clause has no non-2022 evidence at the grid level.
    H_CELL      at the memo's own cell (w=252, depth=0.50) the gate WORKS on EX2022.
    H_4B_EX     the memo cell passes PROTOCOL 4b on EX2022 — bars recomputed from SPY read on the
                SAME day set — both full corpus and inside the EX2022 OOS window.
    H_WF        rule 8: (w, depth) chosen on the IS window 2009-2016 ALONE (which contains no 2022
                by construction, so the chooser is itself non-2022 evidence) WORKS on the EX2022
                OOS corpus AND passes 4b there, under BOTH pre-stated choosers.
    H_LADDER    the EX2022 WORKS verdict at the memo cell holds at 0 / 5 / 10 / 25 bps and at
                execution lag 1 / 2 / 3.

VERDICT RULE, FIXED IN ADVANCE
    KEEP-candidate (path 4b) iff H_NON2022 and H_CELL and H_4B_EX and H_WF.
    PARK            if H_NON2022 passes but any of the 4b legs fails.
    KILL            otherwise — in particular if H_NON2022 fails, in which case the clause is a
                    2022-only object and there is no non-2022 evidence for it.
Path 4a is evaluated against RULES v2 (the live book) at every corpus and reported either way.

THE TWO PRE-STATED CHOOSERS (rule 8; each OOS window is read ONCE, after both have picked)
    C1  argmax IS Sharpe over all 40 cells.
    C2  argmax IS Sharpe among cells whose IS MaxDD <= 60% of SPY's IS MaxDD — the selector a
        drawdown-constrained allocator would actually run (idea 814's C2).

GATES (printed before any verdict is read)
    G1  runner identity: a never-firing multiplier (depth 0) reproduces engine.backtest   bar 1e-12
    G2  causality: min_periods = w, multiplier decided at t applied at t+1; days with no
        threshold reported per w and must rise with w                                     bar exact
    G3  reproduction of idea 814's FULL-corpus cell                              H_REPRO tolerance
    G4  determinism: no RNG; the grid is recomputed and compared                          bar 0
    G5  splice integrity: |EX2022| + |ONLY2022| == |FULL|, and every comparand at a corpus is read
        on exactly the same day set as the arm                                            bar exact

SURVIVORSHIP: B136 is universe_broad.json's CURRENT constituents (PROTOCOL rule 9).  Every CAGR
level here is biased upward and the 4b CAGR floor is easier than on a point-in-time panel.  The
correlation STATE is optimistic for the same reason — the names that died are exactly the ones that
would have co-moved hardest in 2020 and 2022 — so a 2022-free corpus measured on survivors is, if
anything, GENEROUS to the clause: the episodes that remain are tamer than the ones a live book saw.

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
from engine import backtest, metrics                                 # noqa: E402

DATE = "2026-09-15"
SLUG = "is-the-CORR-HI-gate-worth-anything-once-2022-is-the-only-evidence"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ---- the book, fixed in advance --------------------------------------------------------------
FREQ = "W"
GROSS = 1.00
LEVEL = 0.17            # the memo's level — FIXED, not tuned by this run
SMOOTH = 20
MAX_VOL = 0.60
WARMUP = 260
RUNG_HEAD = 10
RUNGS = [0, 5, 10, 25, 50]
LAGS = [1, 2, 3]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- the two tuned dials ----------------------------------------------------------------------
WS = [63, 126, 252, 504, 756, 1008, 1512, 2016]
DEPTHS = [0.10, 0.25, 0.50, 0.75, 1.00]
CAND = (252, 0.50)                       # the memo's own cell, interior in both dials
MEMO = dict(CAGR=0.1402, Sharpe=1.1538, MaxDD=-0.1511)
TOL = dict(Sharpe=0.02, CAGR=0.005, MaxDD=0.010)

EP2022 = ("2022-01-01", "2022-12-31")
EP2020 = ("2020-02-01", "2020-04-30")

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (606/814 verbatim)
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


def gate_mult(st, thr, depth, idx):
    """HI side: fire (de-gross to 1-depth) when the state is ABOVE its threshold; 1.0 wherever the
    threshold does not yet exist, so the gate is silent through its own warm-up."""
    fire = (st > thr) & st.notna() & thr.notna()
    return pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)


def apply_gate(r_base, mult, gross, cost_bps, lag=1):
    """Multiplier decided at t, applied at t+lag, switch cost on |dm| (idea 399's runner)."""
    m_eff = mult.reindex(r_base.index).shift(lag).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def trip(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def bars_4b(spy_r, oos_key):
    """The 4b bars read on ONE corpus: (H1, H2, OOS Sharpe, MaxDD, CAGR) of SPY on that day set."""
    h1, h2 = half_sharpes(spy_r)
    m = metrics(spy_r)
    oos = spy_r[oos_key(spy_r.index)]
    return (h1, h2, metrics(oos)["Sharpe"] if len(oos) > 20 else np.nan, m["MaxDD"], m["CAGR"])


def tests_4b(r, pk, oos_key):
    s1, s2, s_oos, s_dd, s_cagr = pk
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    oos = r[oos_key(r.index)]
    t = {"H1": h1 > s1, "H2": h2 > s2,
         "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
         "CAGR": m["CAGR"] >= 0.70 * s_cagr}
    if not np.isnan(s_oos) and len(oos) > 20:
        t["OOS"] = metrics(oos)["Sharpe"] > s_oos
    return t


def tests_4a(r, bp):
    b1, b2, bdd = bp
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def main():
    t0 = time.time()
    log("=" * 100)
    log(f"IDEA 863 (lane C, {DATE}) — {SLUG}")
    log("=" * 100)
    log(__doc__.split("QUESTION")[0].strip())

    px = load_universe(broad=True)
    start = px.index[WARMUP]
    log(f"\nPanel B136: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}; "
        f"scored sample starts {start.date()} (warm-up {WARMUP} rows).")

    # ---------------- base book at every cost rung, plus the comparands -----------------------
    W = ewall_weights(px, GROSS)
    base_r = {rung: backtest(px, W, cost_bps=rung, freq=FREQ)["returns"].loc[start:]
              for rung in RUNGS}
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]

    idx = base_r[RUNG_HEAD].index
    in_2022 = (idx >= EP2022[0]) & (idx <= EP2022[1])
    in_2020 = (idx >= EP2020[0]) & (idx <= EP2020[1])
    CORPORA = {
        "FULL": pd.Series(True, index=idx),
        "EX2022": pd.Series(~in_2022, index=idx),
        "ONLY2022": pd.Series(in_2022, index=idx),
        "EX2020": pd.Series(~in_2020, index=idx),
        "EXBOTH": pd.Series(~(in_2022 | in_2020), index=idx),
    }
    PRIMARY = ["FULL", "EX2022", "ONLY2022"]     # the queue's own three; the rest are reported

    def oos_key(ix):
        return ix >= OOS_START

    # ---------------- GATES -------------------------------------------------------------------
    st = state_corr(px)
    log("\n" + "-" * 100)
    log("GATES (printed before any verdict)")
    log("-" * 100)
    thr_c = st.rolling(CAND[0], min_periods=CAND[0]).quantile(1 - LEVEL)
    m_never = gate_mult(st, thr_c, 0.0, px.index).loc[start:]
    r_never, _ = apply_gate(base_r[RUNG_HEAD], m_never, GROSS, RUNG_HEAD)
    g1 = float((r_never - base_r[RUNG_HEAD]).abs().max())
    log(f"  G1 runner identity (depth 0 == engine.backtest)      max|d| = {g1:.3e}   "
        f"{'PASS' if g1 < 1e-12 else 'FAIL'}")

    g5a = int(CORPORA["EX2022"].sum() + CORPORA["ONLY2022"].sum()) == len(idx)
    log(f"  G5 splice integrity  |FULL| = {len(idx)}, |EX2022| = {int(CORPORA['EX2022'].sum())}, "
        f"|ONLY2022| = {int(CORPORA['ONLY2022'].sum())}   {'PASS' if g5a else 'FAIL'}")

    # ---------------- corpus-level comparands -------------------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 0 — COMPARANDS AT EVERY CORPUS (10 bps, weekly, t+1)")
    log("-" * 100)
    packs, bases, cmp_rows = {}, {}, []
    for cname, keep in CORPORA.items():
        s_c, v_c, u_c = spy[keep.values], v2[keep.values], base_r[RUNG_HEAD][keep.values]
        packs[cname] = bars_4b(s_c, oos_key)
        h1, h2 = half_sharpes(v_c)
        bases[cname] = (h1, h2, metrics(v_c)["MaxDD"])
        for nm, r in [("SPY", s_c), ("RULES v2", v_c), ("UNGATED g=1.00", u_c)]:
            c, s, d = trip(r)
            cmp_rows.append(dict(corpus=cname, name=nm, days=len(r), CAGR=c, Sharpe=s, MaxDD=d))
        p = packs[cname]
        log(f"\n  {cname:<9} ({len(s_c)} days)")
        for nm, r in [("SPY", s_c), ("RULES v2", v_c), ("UNGATED g=1.00", u_c)]:
            c, s, d = trip(r)
            hh = half_sharpes(r)
            log(f"    {nm:<16} {c:>8.2%} / {s:>7.4f} / {d:>8.2%}   halves "
                f"{hh[0]:.4f} / {hh[1]:.4f}")
        log(f"    4b bars off SPY: H1 > {p[0]:.4f}, H2 > {p[1]:.4f}, OOS Sharpe > {p[2]:.4f}, "
            f"MaxDD >= {0.60 * p[3]:.2%}, CAGR >= {0.70 * p[4]:.2%}")
    pd.DataFrame(cmp_rows).to_csv(f"{OUT}.comparands.csv", index=False)

    # ---------------- the 40-cell grid at every corpus ----------------------------------------
    twin_cache = {}

    def twin_returns(g, rung=RUNG_HEAD):
        """The matched-gross static twin, priced at the SAME cost rung as the arm it answers."""
        k = (round(float(g), 5), rung)
        if k not in twin_cache:
            twin_cache[k] = backtest(px, ewall_weights(px, k[0]), cost_bps=rung,
                                     freq=FREQ)["returns"].loc[start:]
        return twin_cache[k]

    rows, mults = [], {}
    for w, depth in product(WS, DEPTHS):
        thr = st.rolling(w, min_periods=w).quantile(1 - LEVEL)
        mult = gate_mult(st, thr, depth, px.index)
        mults[(w, depth)] = mult
        r, m_eff = apply_gate(base_r[RUNG_HEAD], mult, GROSS, RUNG_HEAD)
        no_thr = int(thr.loc[start:].isna().sum())
        for cname, keep in CORPORA.items():
            kv = keep.values
            r_c, m_c = r[kv], m_eff[kv]
            g_eff = float(m_c.mean() * GROSS)
            tw_c = twin_returns(g_eff)[kv]
            c_g, s_g, d_g = trip(r_c)
            c_t, s_t, d_t = trip(tw_c)
            works = bool(s_g > s_t and abs(d_g) < abs(d_t))
            t4b = tests_4b(r_c, packs[cname], oos_key)
            oos_days = int(oos_key(r_c.index).sum())
            rows.append(dict(
                corpus=cname, w=w, depth=depth, days=len(r_c), no_thr_days=no_thr,
                on_share=float((m_c < 1.0).mean()), mean_gross=g_eff,
                CAGR=c_g, Sharpe=s_g, MaxDD=d_g,
                twin_CAGR=c_t, twin_Sharpe=s_t, twin_MaxDD=d_t,
                d_Sharpe=s_g - s_t, d_CAGR=c_g - c_t, d_MaxDD=abs(d_t) - abs(d_g),
                works=works, sharpe_leg=bool(s_g > s_t), dd_leg=bool(abs(d_g) < abs(d_t)),
                IS_Sharpe=metrics(r_c[r_c.index <= IS_END])["Sharpe"] if (r_c.index <= IS_END).sum() > 20 else np.nan,
                IS_MaxDD=metrics(r_c[r_c.index <= IS_END])["MaxDD"] if (r_c.index <= IS_END).sum() > 20 else np.nan,
                OOS_CAGR=metrics(r_c[oos_key(r_c.index)])["CAGR"] if oos_days > 20 else np.nan,
                OOS_Sharpe=metrics(r_c[oos_key(r_c.index)])["Sharpe"] if oos_days > 20 else np.nan,
                OOS_MaxDD=metrics(r_c[oos_key(r_c.index)])["MaxDD"] if oos_days > 20 else np.nan,
                p4b=all(t4b.values()), p4a=tests_4a(r_c, bases[cname]),
                fail4b=",".join(k for k, v in t4b.items() if not v) or "-"))
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)

    mono = grid[grid.corpus == "FULL"].groupby("w")["no_thr_days"].mean().sort_index()
    g2 = list(mono.values) == sorted(mono.values)
    log(f"\n  G2 causality (min_periods=w; days with no threshold rise with w)   "
        f"{dict(zip(mono.index.astype(int), mono.astype(int)))}   {'PASS' if g2 else 'FAIL'}")

    r_again, _ = apply_gate(base_r[RUNG_HEAD], mults[CAND], GROSS, RUNG_HEAD)
    cand_full = grid[(grid.corpus == "FULL") & (grid.w == CAND[0]) & (grid.depth == CAND[1])].iloc[0]
    g4 = float(abs(metrics(r_again)["Sharpe"] - cand_full["Sharpe"]))
    log(f"  G4 determinism (grid recomputed, no RNG)             |dSharpe| = {g4:.3e}   "
        f"{'PASS' if g4 == 0.0 else 'FAIL'}")

    dev = dict(Sharpe=abs(cand_full["Sharpe"] - MEMO["Sharpe"]),
               CAGR=abs(cand_full["CAGR"] - MEMO["CAGR"]),
               MaxDD=abs(cand_full["MaxDD"] - MEMO["MaxDD"]))
    h_repro = (dev["Sharpe"] <= TOL["Sharpe"] and dev["CAGR"] <= TOL["CAGR"]
               and dev["MaxDD"] <= TOL["MaxDD"])
    log(f"  G3 reproduction of idea 814's FULL cell (w=252, depth=0.50, q=0.17)")
    log(f"     memo {MEMO['CAGR']:.2%} / {MEMO['Sharpe']:.4f} / {MEMO['MaxDD']:.2%}   "
        f"here {cand_full['CAGR']:.2%} / {cand_full['Sharpe']:.4f} / {cand_full['MaxDD']:.2%}")
    log(f"     H_REPRO {'PASS' if h_repro else 'FAIL'}  (dev S {dev['Sharpe']:.4f}, "
        f"CAGR {dev['CAGR']:.4f}, DD {dev['MaxDD']:.4f})")

    # ---------------- SECTION 1 — the grid, corpus by corpus ----------------------------------
    log("\n" + "-" * 100)
    log("SECTION 1 — ALL 40 CELLS AT EVERY CORPUS (rows = w, cols = depth; gated MINUS its own "
        "matched-gross twin)")
    log("-" * 100)
    for cname in CORPORA:
        g = grid[grid.corpus == cname]
        log(f"\n  === {cname} ({int(g['days'].iloc[0])} days) ===")
        for tag, col, fmt in [("gated Sharpe", "Sharpe", "{:.4f}"),
                              ("twin Sharpe", "twin_Sharpe", "{:.4f}"),
                              ("d_Sharpe (gated - twin)", "d_Sharpe", "{:+.4f}"),
                              ("d_MaxDD pp (twin |DD| - gated |DD|, + = gate helps)",
                               "d_MaxDD", "{:+.4f}"),
                              ("d_CAGR (gated - twin)", "d_CAGR", "{:+.4f}")]:
            piv = g.pivot(index="w", columns="depth", values=col)
            log(f"\n    {tag}")
            log("      " + piv.to_string(float_format=lambda x: fmt.format(x)).replace("\n", "\n      "))
        piv = g.pivot(index="w", columns="depth", values="works").replace({True: "W", False: "."})
        log("\n    WORKS map (W = gate beats its matched-gross twin on Sharpe AND on MaxDD)")
        log("      " + piv.to_string().replace("\n", "\n      "))
        nw, ns, nd = int(g["works"].sum()), int(g["sharpe_leg"].sum()), int(g["dd_leg"].sum())
        n4b, n4a = int(g["p4b"].sum()), int(g["p4a"].sum())
        log(f"\n    WORKS {nw}/40   (Sharpe leg alone {ns}/40, MaxDD leg alone {nd}/40)   "
            f"4b {n4b}/40   4a vs RULES v2 {n4a}/40")
        log(f"    failing 4b legs: {g.loc[~g['p4b'], 'fail4b'].value_counts().to_dict()}")

    summary = grid.groupby("corpus").agg(
        WORKS=("works", "sum"), sharpe_leg=("sharpe_leg", "sum"), dd_leg=("dd_leg", "sum"),
        p4b=("p4b", "sum"), p4a=("p4a", "sum"), med_dSharpe=("d_Sharpe", "median"),
        med_dMaxDD=("d_MaxDD", "median"), med_dCAGR=("d_CAGR", "median")).reindex(CORPORA)
    summary.to_csv(f"{OUT}.corpora.csv")
    log("\n  CORPUS SUMMARY (out of 40 cells each)")
    log("    " + summary.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    n_only = int(grid[(grid.corpus == "ONLY2022")]["works"].sum())
    n_ex = int(grid[(grid.corpus == "EX2022")]["works"].sum())
    h_premise = n_only >= 30
    h_non2022 = n_ex >= 20
    log(f"\n  H_PREMISE  (ONLY2022 WORKS >= 30/40): {n_only}/40 -> "
        f"{'PASS' if h_premise else 'FAIL'}")
    log(f"  H_NON2022  (EX2022  WORKS >= 20/40): {n_ex}/40 -> "
        f"{'PASS' if h_non2022 else 'FAIL'}   *** THE DECIDING TEST ***")

    # ---------------- SECTION 2 — the memo cell, corpus by corpus ------------------------------
    log("\n" + "-" * 100)
    log(f"SECTION 2 — THE MEMO'S OWN CELL (w={CAND[0]}, depth={CAND[1]}, q={LEVEL}) AT EVERY CORPUS")
    log("-" * 100)
    cell = grid[(grid.w == CAND[0]) & (grid.depth == CAND[1])].set_index("corpus")
    log(f"  {'corpus':<9} {'days':>5} {'on%':>6} {'gross':>7} | {'GATED CAGR/Sharpe/MaxDD':>30} | "
        f"{'TWIN CAGR/Sharpe/MaxDD':>30} | WORKS  4b")
    for cname in CORPORA:
        rw = cell.loc[cname]
        log(f"  {cname:<9} {int(rw['days']):>5} {rw['on_share']:>6.1%} {rw['mean_gross']:>7.4f} | "
            f"{rw['CAGR']:>9.2%} {rw['Sharpe']:>9.4f} {rw['MaxDD']:>9.2%} | "
            f"{rw['twin_CAGR']:>9.2%} {rw['twin_Sharpe']:>9.4f} {rw['twin_MaxDD']:>9.2%} | "
            f"{'WORKS' if rw['works'] else '  no ':>5}  "
            f"{'PASS' if rw['p4b'] else 'FAIL(' + rw['fail4b'] + ')'}")
    h_cell = bool(cell.loc["EX2022", "works"])
    h_4b_ex = bool(cell.loc["EX2022", "p4b"])
    # 4b read INSIDE the EX2022 OOS window (the corpus's own out-of-sample half)
    keep_ex = CORPORA["EX2022"].values
    r_cell = apply_gate(base_r[RUNG_HEAD], mults[CAND], GROSS, RUNG_HEAD)[0][keep_ex]
    r_cell_oos = r_cell[oos_key(r_cell.index)]
    spy_ex_oos = spy[keep_ex][oos_key(spy[keep_ex].index)]
    pk_oos = (half_sharpes(spy_ex_oos)[0], half_sharpes(spy_ex_oos)[1], np.nan,
              metrics(spy_ex_oos)["MaxDD"], metrics(spy_ex_oos)["CAGR"])
    t_oos = tests_4b(r_cell_oos, pk_oos, lambda ix: np.zeros(len(ix), dtype=bool))
    log(f"\n  memo cell INSIDE the EX2022 OOS window ({len(r_cell_oos)} days): "
        f"{metrics(r_cell_oos)['CAGR']:.2%} / {metrics(r_cell_oos)['Sharpe']:.4f} / "
        f"{metrics(r_cell_oos)['MaxDD']:.2%}   vs SPY {metrics(spy_ex_oos)['CAGR']:.2%} / "
        f"{metrics(spy_ex_oos)['Sharpe']:.4f} / {metrics(spy_ex_oos)['MaxDD']:.2%}")
    log(f"     4b inside EX2022 OOS: "
        f"{'PASS' if all(t_oos.values()) else 'FAIL (' + ','.join(k for k, v in t_oos.items() if not v) + ')'}")
    h_4b_ex = h_4b_ex and all(t_oos.values())
    log(f"  H_CELL  (memo cell WORKS on EX2022): {'PASS' if h_cell else 'FAIL'}")
    log(f"  H_4B_EX (memo cell 4b on EX2022, full AND inside its OOS): "
        f"{'PASS' if h_4b_ex else 'FAIL'}")

    # ---------------- SECTION 3 — rule 8 walk-forward -----------------------------------------
    log("\n" + "-" * 100)
    log("SECTION 3 — RULE 8 WALK-FORWARD ((w, depth) chosen on 2009-2016 ALONE — a window that")
    log("            contains NO 2022 by construction; every OOS window read once)")
    log("-" * 100)
    is_spy = spy[spy.index <= IS_END]
    is_cap = 0.60 * abs(metrics(is_spy)["MaxDD"])
    gF = grid[grid.corpus == "FULL"]
    log(f"  IS {start.date()} -> {IS_END}   OOS {OOS_START} -> {idx[-1].date()}")
    log(f"  C1 = argmax IS Sharpe.  C2 = argmax IS Sharpe s.t. IS MaxDD <= {is_cap:.2%} "
        f"(60% of SPY IS MaxDD {metrics(is_spy)['MaxDD']:.2%}).")
    c1 = gF.loc[gF["IS_Sharpe"].idxmax()]
    elig = gF[gF["IS_MaxDD"].abs() <= is_cap]
    picks = {"C1": c1}
    if len(elig):
        picks["C2"] = elig.loc[elig["IS_Sharpe"].idxmax()]
    log(f"  C2 eligible cells: {len(elig)}/40")

    wf_rows, h_wf_parts = [], []
    for nm, p in picks.items():
        key = (int(p["w"]), float(p["depth"]))
        wi, di = WS.index(key[0]), DEPTHS.index(key[1])
        inter = (0 < wi < len(WS) - 1) and (0 < di < len(DEPTHS) - 1)
        log(f"\n  {nm} picks (w={key[0]}, depth={key[1]})  IS Sharpe {p['IS_Sharpe']:.4f}, "
            f"IS MaxDD {p['IS_MaxDD']:.2%}  —  w index {wi}/{len(WS)-1}, depth index "
            f"{di}/{len(DEPTHS)-1} -> {'INTERIOR' if inter else 'ON THE GRID EDGE'}"
            f"{'   == the memo cell' if key == CAND else ''}")
        r_pick, m_pick = apply_gate(base_r[RUNG_HEAD], mults[key], GROSS, RUNG_HEAD)
        for cname in ["FULL", "EX2022", "ONLY2022"]:
            kv = CORPORA[cname].values
            rc, mc = r_pick[kv], m_pick[kv]
            oos_m = oos_key(rc.index)
            rc_oos = rc[oos_m]
            g_eff_oos = float(mc[oos_m].mean() * GROSS)
            tw_oos = twin_returns(g_eff_oos)[kv][oos_m]
            c_g, s_g, d_g = trip(rc_oos)
            c_t, s_t, d_t = trip(tw_oos)
            works_oos = bool(s_g > s_t and abs(d_g) < abs(d_t))
            spy_c_oos = spy[kv][oos_key(spy[kv].index)]
            v2_c_oos = v2[kv][oos_key(v2[kv].index)]
            pk = (half_sharpes(spy_c_oos)[0], half_sharpes(spy_c_oos)[1], np.nan,
                  metrics(spy_c_oos)["MaxDD"], metrics(spy_c_oos)["CAGR"])
            t = tests_4b(rc_oos, pk, lambda ix: np.zeros(len(ix), dtype=bool))
            bp = (half_sharpes(v2_c_oos)[0], half_sharpes(v2_c_oos)[1], metrics(v2_c_oos)["MaxDD"])
            p4a_oos = tests_4a(rc_oos, bp)
            log(f"     OOS on {cname:<9} ({len(rc_oos)} d)  arm {c_g:>8.2%} / {s_g:>7.4f} / "
                f"{d_g:>8.2%}   twin(g={g_eff_oos:.4f}) {c_t:>8.2%} / {s_t:>7.4f} / {d_t:>8.2%}")
            log(f"        SPY {metrics(spy_c_oos)['CAGR']:>8.2%} / "
                f"{metrics(spy_c_oos)['Sharpe']:>7.4f} / {metrics(spy_c_oos)['MaxDD']:>8.2%}   "
                f"RULES v2 {metrics(v2_c_oos)['CAGR']:>8.2%} / "
                f"{metrics(v2_c_oos)['Sharpe']:>7.4f} / {metrics(v2_c_oos)['MaxDD']:>8.2%}")
            log(f"        WORKS vs twin {'YES' if works_oos else 'NO '}   4b "
                f"{'PASS' if all(t.values()) else 'FAIL (' + ','.join(k for k, v in t.items() if not v) + ')'}"
                f"   4a {'PASS' if p4a_oos else 'FAIL'}")
            if cname == "EX2022":
                h_wf_parts.append(works_oos and all(t.values()))
            wf_rows.append(dict(chooser=nm, w=key[0], depth=key[1], interior=inter, corpus=cname,
                                IS_Sharpe=p["IS_Sharpe"], IS_MaxDD=p["IS_MaxDD"],
                                OOS_days=len(rc_oos), OOS_CAGR=c_g, OOS_Sharpe=s_g, OOS_MaxDD=d_g,
                                twin_gross=g_eff_oos, twin_CAGR=c_t, twin_Sharpe=s_t,
                                twin_MaxDD=d_t, works=works_oos, p4b_oos=all(t.values()),
                                p4a_oos=p4a_oos,
                                fail4b=",".join(k for k, v in t.items() if not v) or "-",
                                spy_CAGR=metrics(spy_c_oos)["CAGR"],
                                spy_Sharpe=metrics(spy_c_oos)["Sharpe"],
                                spy_MaxDD=metrics(spy_c_oos)["MaxDD"],
                                v2_CAGR=metrics(v2_c_oos)["CAGR"],
                                v2_Sharpe=metrics(v2_c_oos)["Sharpe"],
                                v2_MaxDD=metrics(v2_c_oos)["MaxDD"]))
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)
    h_wf = bool(h_wf_parts) and all(h_wf_parts) and len(picks) == 2
    log(f"\n  H_WF (every IS-alone pick WORKS and passes 4b on the EX2022 OOS corpus): "
        f"{'PASS' if h_wf else 'FAIL'}")

    # ---------------- SECTION 4 — cost and lag ladders on the EX2022 verdict -------------------
    log("\n" + "-" * 100)
    log("SECTION 4 — COST AND LAG LADDERS ON THE EX2022 VERDICT (memo cell; reported, never "
        "selected)")
    log("-" * 100)
    kv = CORPORA["EX2022"].values
    lad_rows, h_lad_parts = [], []
    for rung in RUNGS:
        r, m_eff = apply_gate(base_r[rung], mults[CAND], GROSS, rung)
        rc, mc = r[kv], m_eff[kv]
        g_eff = float(mc.mean() * GROSS)
        tw = twin_returns(g_eff, rung)[kv]     # twin priced at the arm's own rung
        c_g, s_g, d_g = trip(rc)
        c_t, s_t, d_t = trip(tw)
        ok = bool(s_g > s_t and abs(d_g) < abs(d_t))
        if rung in (0, 5, 10, 25):
            h_lad_parts.append(ok)
        log(f"  {rung:>2} bps  arm {c_g:>8.2%} / {s_g:>7.4f} / {d_g:>8.2%}   twin {c_t:>8.2%} / "
            f"{s_t:>7.4f} / {d_t:>8.2%}   WORKS {'YES' if ok else 'NO'}")
        lad_rows.append(dict(kind="cost", value=rung, CAGR=c_g, Sharpe=s_g, MaxDD=d_g,
                             twin_Sharpe=s_t, twin_MaxDD=d_t, works=ok))
    for lag in LAGS:
        r, m_eff = apply_gate(base_r[RUNG_HEAD], mults[CAND], GROSS, RUNG_HEAD, lag=lag)
        rc, mc = r[kv], m_eff[kv]
        g_eff = float(mc.mean() * GROSS)
        tw = twin_returns(g_eff)[kv]
        c_g, s_g, d_g = trip(rc)
        c_t, s_t, d_t = trip(tw)
        ok = bool(s_g > s_t and abs(d_g) < abs(d_t))
        h_lad_parts.append(ok)
        log(f"  lag {lag}  arm {c_g:>8.2%} / {s_g:>7.4f} / {d_g:>8.2%}   twin {c_t:>8.2%} / "
            f"{s_t:>7.4f} / {d_t:>8.2%}   WORKS {'YES' if ok else 'NO'}")
        lad_rows.append(dict(kind="lag", value=lag, CAGR=c_g, Sharpe=s_g, MaxDD=d_g,
                             twin_Sharpe=s_t, twin_MaxDD=d_t, works=ok))
    pd.DataFrame(lad_rows).to_csv(f"{OUT}.ladders.csv", index=False)
    h_ladder = all(h_lad_parts)
    log(f"  H_LADDER (EX2022 WORKS at 0/5/10/25 bps and lag 1/2/3): "
        f"{'PASS' if h_ladder else 'FAIL'}")

    # ---------------- SECTION 5 — where the clause's value actually sits -----------------------
    log("\n" + "-" * 100)
    log("SECTION 5 — CALENDAR-YEAR DECOMPOSITION OF THE MEMO CELL vs ITS OWN TWIN (reported)")
    log("-" * 100)
    r_f, m_f = apply_gate(base_r[RUNG_HEAD], mults[CAND], GROSS, RUNG_HEAD)
    g_full = float(m_f.mean() * GROSS)
    tw_f = twin_returns(g_full)
    yr_rows = []
    log(f"  {'year':<6} {'gate on%':>9} {'arm':>9} {'twin':>9} {'arm-twin':>9} {'SPY':>9}")
    for y, sub in r_f.groupby(r_f.index.year):
        a = (1 + sub).prod() - 1
        t_ = (1 + tw_f.loc[sub.index]).prod() - 1
        s_ = (1 + spy.loc[sub.index]).prod() - 1
        on = float((m_f.loc[sub.index] < 1.0).mean())
        log(f"  {y:<6} {on:>9.1%} {a:>+9.2%} {t_:>+9.2%} {a - t_:>+9.2%} {s_:>+9.2%}")
        yr_rows.append(dict(year=int(y), gate_on=on, arm=a, twin=t_, excess=a - t_, spy=s_))
    ydf = pd.DataFrame(yr_rows)
    ydf.to_csv(f"{OUT}.years.csv", index=False)
    pos = ydf[ydf.excess > 0]
    log(f"\n  arm beats its own matched-gross twin in {len(pos)} of {len(ydf)} calendar years; "
        f"total excess {ydf.excess.sum():+.2%}, 2022 alone "
        f"{float(ydf.loc[ydf.year == 2022, 'excess'].iloc[0]):+.2%}, "
        f"ex-2022 {ydf.loc[ydf.year != 2022, 'excess'].sum():+.2%}")

    # ---------------- VERDICT ------------------------------------------------------------------
    log("\n" + "=" * 100)
    log("HYPOTHESES (all pre-registered above; none added after a number was read)")
    log("=" * 100)
    H = [("H_REPRO", h_repro, "the memo cell rebuilds inside tolerance on the FULL corpus"),
         ("H_PREMISE", h_premise, "ONLY2022: the gate WORKS at >= 30 of 40 cells"),
         ("H_NON2022", h_non2022, "EX2022: the gate WORKS at >= 20 of 40 cells  *** DECIDING ***"),
         ("H_CELL", h_cell, "the memo cell WORKS on EX2022"),
         ("H_4B_EX", h_4b_ex, "the memo cell passes 4b on EX2022, full AND inside its OOS"),
         ("H_WF", h_wf, "both IS-alone picks WORK and pass 4b on the EX2022 OOS corpus"),
         ("H_LADDER", h_ladder, "the EX2022 WORKS verdict holds at 0/5/10/25 bps and lag 1/2/3")]
    for nm, ok, desc in H:
        log(f"  {nm:<11} {'PASS' if ok else 'FAIL'}   {desc}")
    pd.DataFrame([dict(hypothesis=n, result="PASS" if o else "FAIL", statement=d)
                  for n, o, d in H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    if h_non2022 and h_cell and h_4b_ex and h_wf:
        verdict = "KEEP-candidate (path 4b)"
    elif h_non2022:
        verdict = "PARK"
    else:
        verdict = "KILL"
    log(f"\n  PRE-REGISTERED VERDICT RULE -> {verdict}")
    log("  (rule, fixed in advance: KEEP iff H_NON2022 and H_CELL and H_4B_EX and H_WF; "
        "PARK if H_NON2022 alone; else KILL.)")
    log("\n  SURVIVORSHIP: B136 is universe_broad.json's CURRENT constituents; every CAGR level is")
    log("  biased upward, the 4b CAGR floor is easier than on a point-in-time panel, and the "
        "correlation")
    log("  state is measured on names that did not die in 2020 or 2022 — which makes the 2022-free")
    log("  corpus GENEROUS to the clause, not harsh.")
    log(f"\nDone in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
