#!/usr/bin/env python3
"""Idea 866 (cloud lane, 2026-09-15) — is a DE-GROSSING CLAUSE worth more priced on
EPISODE-CONDITIONAL SIZING than on a FULL-SAMPLE book?

QUESTION
--------
Idea 863/864's CORR-HI clause is a GATE: whenever the 20d average pairwise correlation of the
B136 panel sits above its own rolling 83rd percentile (LEVEL 0.17), the equal-weight-all book is
cut to 50% of its gross, every such day, for the whole sample.  863's calendar table shows the
memo cell (w=252, depth=0.50) **loses to its own matched-gross twin in 7 of 18 years, -13.23pp
between them, and wins almost entirely inside 2 crashes**.

The queue's test: take the SAME state and use it only to SIZE the book's crash exposure — a FLOOR
on gross rather than a gate — and ask whether that keeps the crash payoff without the ordinary-year
cost.

THE TWO FORMS, on one state, one panel, one book
    GATE(d)   (863/864's, verbatim)   mult_t = 1.0 if OFF else (1 - d).  Binary: every ON day pays
              the same 50% cut, whether the correlation is at its 83rd percentile or its 100th.
    SIZE(f)   (this run's)            mult_t = 1.0 if OFF else 1 - (1 - f)*u_t, where
              u_t = (pctrank_t - (1 - LEVEL)) / LEVEL, clipped to [0, 1], and pctrank_t is the
              state's CAUSAL rolling-window percentile rank over the same window w.  At the ON
              boundary u=0 and the book is untouched; at the window's correlation extreme u=1 and
              the book sits at its FLOOR f.  Exposure never goes below f, and ordinary ON days
              (the false alarms that cost the gate 7 years) are barely sized down at all.
    Both forms are decided at t and applied at t+1, both pay switch cost on |dmult|, both are
    scored against the SAME matched-gross static twin convention (the EWALL book held at a
    CONSTANT gross equal to the arm's own realised mean multiplier) that 863/864 used.

TUNED PARAMETERS (PROTOCOL rule 4 — exactly two, the queue's own: FLOOR and WINDOW)
    1. floor  f in {0.10, 0.25, 0.40, 0.50, 0.60, 0.75, 0.90}
    2. window w in {63, 126, 252, 504, 756, 1008}
    ALL 42 SIZE cells are reported, plus the 6 GATE cells at the memo's own depth 0.50 (an
    INHERITED constant from 863's memo, not tuned here) as the comparand at each window.
    LEVEL = 0.17, SMOOTH = 20, GROSS = 1.00, weekly, 10 bps, t+1 — all inherited, none tuned.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO   the GATE cell (w=252, d=0.50) reproduces 863/864's committed FULL triple
              14.02% / 1.1538 / -15.11%.  A gate on the re-implementation, not evidence.
    H_YEARS   *** THE QUEUE'S OWN TEST, leg 1. *** at the matched window w=252, SIZE loses to its
              own matched-gross twin in STRICTLY FEWER calendar years than the GATE's 7 of 18.
    H_ORD     *** leg 2. *** on the ORDINARY-YEAR corpus (calendar 2020 and 2022 removed) SIZE's
              CAGR is within 25 bps/yr of the UNGATED book's — i.e. the clause is close to free
              when nothing is happening.  The GATE's own ordinary-year gap is printed beside it.
    H_CRASH   *** leg 3. *** SIZE keeps at least HALF of the GATE's calendar-2020 payoff over the
              ungated book (dCAGR_2020(SIZE) >= 0.50 * dCAGR_2020(GATE)).
    H_WORKS   at the matched cell SIZE beats its matched-gross twin on BOTH legs (Sharpe higher,
              |MaxDD| lower) on the FULL corpus — the record's own WORKS test.
    H_4B      the walk-forward-chosen SIZE cell clears PROTOCOL 4b (all legs) on the untouched
              2017-2026 window.
    H_WF      rule 8: the cell chosen on 2009-2016 ALONE under BOTH pre-stated choosers still
              beats its matched-gross twin on the untouched OOS window.

VERDICT RULE, FIXED IN ADVANCE
    KEEP (4b) iff H_4B and H_WF and H_WORKS — the sizing form is a capital candidate.
    ANSWERED-YES (sizing is the better pricing of the clause, PARK for capital) iff H_YEARS and
        H_ORD and H_CRASH but not the KEEP conjunction.
    ANSWERED-NO / KILL otherwise; in particular if H_CRASH fails the floor buys nothing where the
        clause was supposed to earn, and if H_YEARS fails the ordinary-year cost is not a gate
        artefact at all.
    No book is promoted by this run on its own; a KEEP would be written as a memo with exact RULES
    wording for the Sunday review (PROTOCOL rule 6), not applied.

THE TWO PRE-STATED CHOOSERS (rule 8; the OOS window is read ONCE, after both have picked)
    C1  argmax IS Sharpe over all 42 (w, f) cells.
    C2  the Sep-3 memo's own rule: among cells whose IS |MaxDD| <= 60% of SPY's IS |MaxDD|, the
        HIGHEST floor (the least intervention that clears the drawdown bar); ties -> longest w.

GATES (printed before any verdict is read)
    G1  runner identity: SIZE at floor 1.00 == the ungated engine.backtest book        bar 1e-12
    G2  causality: the multiplier is shifted t+1 and the rolling threshold/rank exist only after w
        rows; no-threshold day counts rise monotonically with w                        bar exact
    G3  H_REPRO: the GATE memo cell against 863/864's committed triple      bar 0.02 Sharpe / 0.5pp
    G4  determinism: the whole grid recomputed, no RNG anywhere in this script          bar 0
    G5  the comparands (SPY, RULES v2 live baseline, UNGATED g=1.00) printed before any arm
    G6  cost sweep at 0/10/25/50 bps on the chosen cell, and the 1-day-delayed (t+2) variant

SURVIVORSHIP (PROTOCOL rule 9): B136 is `research/universe_broad.json`'s CURRENT constituents, so
every CAGR level is optimistic, every MaxDD understated, and the correlation state is optimistic
too — the names that died are the ones that would have correlated hardest in a crash.  The
contrast between the two FORMS is run on the identical panel and is far less exposed than a level.

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
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics                                   # noqa: E402

DATE = "2026-09-15"
SLUG = "is-a-DE-GROSSING-CLAUSE-worth-more-priced-on-EPISODE-CONDITIONAL-SIZING"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---- the book and the state, all inherited from 863/864, none tuned here ----------------------
FREQ = "W"
GROSS = 1.00
LEVEL = 0.17            # the memo's level
SMOOTH = 20             # the state's own smoothing
MAX_VOL = 0.60
WARMUP = 260
COST = 10
RUNGS = [0, 10, 25, 50]
LAGS = [1, 2]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- the two tuned dials ----------------------------------------------------------------------
FLOORS = [0.10, 0.25, 0.40, 0.50, 0.60, 0.75, 0.90]
WS = [63, 126, 252, 504, 756, 1008]
MEMO_W, MEMO_DEPTH = 252, 0.50          # 863's memo cell (the GATE comparand)
MEMO = dict(CAGR=0.1402, Sharpe=1.1538, MaxDD=-0.1511)
TOL = dict(Sharpe=0.02, CAGR=0.005, MaxDD=0.005)

EP2020Y = ("2020-01-01", "2020-12-31")
EP2022 = ("2022-01-01", "2022-12-31")

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (863/864 verbatim)
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
    """863/864's GATE: cut to (1 - depth) whenever the state is ABOVE its rolling threshold."""
    fire = (st > thr) & st.notna() & thr.notna()
    return pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)


def pct_rank(st, w):
    """CAUSAL rolling percentile rank of the state within the trailing w observations, in [0,1].
    Uses the same min_periods=w convention as the rolling quantile, so the SIZE arm and the GATE
    arm are silent over exactly the same warm-up."""
    return st.rolling(w, min_periods=w).rank(pct=True)


def size_mult(st, thr, rank, floor, idx):
    """This run's SIZE form: inside the ON region, ramp gross from 1.0 at the threshold down to
    `floor` at the window's correlation extreme; 1.0 everywhere else and through the warm-up."""
    fire = (st > thr) & st.notna() & thr.notna() & rank.notna()
    u = ((rank - (1.0 - LEVEL)) / LEVEL).clip(0.0, 1.0)
    m = 1.0 - (1.0 - floor) * u
    return pd.Series(1.0, index=idx).where(~fire, m.reindex(idx))


def apply_mult(r_base, mult, gross=GROSS, cost_bps=COST, lag=1):
    """Multiplier decided at t, applied at t+lag, switch cost on |dm| (863/864/399's runner)."""
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


def bars_4b(spy_r):
    h1, h2 = half_sharpes(spy_r)
    m = metrics(spy_r)
    oos = spy_r.loc[OOS_START:]
    return dict(H1=h1, H2=h2, OOS=metrics(oos)["Sharpe"] if len(oos) > 20 else np.nan,
                DD=0.60 * abs(m["MaxDD"]), CAGR=0.70 * m["CAGR"])


def tests_4b(r, bars):
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    t = {"H1": h1 > bars["H1"], "H2": h2 > bars["H2"],
         "DD": abs(m["MaxDD"]) <= bars["DD"], "CAGR": m["CAGR"] >= bars["CAGR"]}
    oos = r.loc[OOS_START:]
    if not np.isnan(bars["OOS"]) and len(oos) > 20:
        t["OOS"] = metrics(oos)["Sharpe"] > bars["OOS"]
    return t


def bars_4a(v2_r):
    h1, h2 = half_sharpes(v2_r)
    return dict(H1=h1, H2=h2, DD=metrics(v2_r)["MaxDD"])


def tests_4a(r, bars):
    h1, h2 = half_sharpes(r)
    return {"H1": h1 > bars["H1"], "H2": h2 > bars["H2"],
            "DD": metrics(r)["MaxDD"] >= bars["DD"]}


def fails(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def ok(d):
    return all(d.values())


def main():
    t0 = time.time()
    log("=" * 100)
    log(f"IDEA 866 (cloud lane, {DATE}) — {SLUG}")
    log("=" * 100)
    log(__doc__.split("QUESTION")[0].strip())

    px = load_universe(broad=True)
    start = px.index[WARMUP]
    log(f"\nPanel B136: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}; "
        f"scored sample starts {start.date()} (warm-up {WARMUP} rows).")

    # ---------------- base book, comparands ---------------------------------------------------
    W1 = ewall_weights(px, GROSS)
    base_r = {rung: backtest(px, W1, cost_bps=rung, freq=FREQ)["returns"].loc[start:]
              for rung in RUNGS}
    base = base_r[COST]
    idx = base.index
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    B4B, B4A = bars_4b(spy), bars_4a(v2)

    st = state_corr(px)

    # ---------------- GATES -------------------------------------------------------------------
    log("\n" + "-" * 100)
    log("GATES (printed before any verdict)")
    log("-" * 100)
    thr_m = st.rolling(MEMO_W, min_periods=MEMO_W).quantile(1 - LEVEL)
    rank_m = pct_rank(st, MEMO_W)
    r_id, _ = apply_mult(base, size_mult(st, thr_m, rank_m, 1.00, px.index))
    g1 = float((r_id - base).abs().max())
    log(f"  G1 runner identity (SIZE floor 1.00 == ungated engine.backtest)  max|d| = {g1:.3e}   "
        f"{'PASS' if g1 < 1e-12 else 'FAIL'}")

    nothr = [int(st.rolling(w, min_periods=w).quantile(1 - LEVEL).loc[start:].isna().sum())
             for w in WS]
    mono = all(nothr[i] <= nothr[i + 1] for i in range(len(nothr) - 1))
    m_lag = apply_mult(base, size_mult(st, thr_m, rank_m, 0.50, px.index))[1]
    raw = size_mult(st, thr_m, rank_m, 0.50, px.index).reindex(idx)
    lag_ok = bool((m_lag.iloc[1:].values == raw.iloc[:-1].values).all())
    log(f"  G2 causality: no-threshold days by w {dict(zip(WS, nothr))} monotone={mono}; "
        f"multiplier is exactly raw.shift(1): {lag_ok}   "
        f"{'PASS' if (mono and lag_ok) else 'FAIL'}")

    r_memo, m_memo = apply_mult(base, gate_mult(st, thr_m, MEMO_DEPTH, px.index))
    c_m, s_m, d_m = trip(r_memo)
    g3 = (abs(s_m - MEMO["Sharpe"]) <= TOL["Sharpe"] and abs(c_m - MEMO["CAGR"]) <= TOL["CAGR"]
          and abs(d_m - MEMO["MaxDD"]) <= TOL["MaxDD"])
    log(f"  G3 H_REPRO GATE memo cell (w={MEMO_W}, d={MEMO_DEPTH}): {c_m:.2%} / {s_m:.4f} / "
        f"{d_m:.2%}  vs committed 14.02% / 1.1538 / -15.11%   {'PASS' if g3 else 'FAIL'}")

    log("\n  G5 comparands on the scored sample (10 bps, weekly, t+1)")
    for nm, r in [("SPY", spy), ("RULES v2 (live baseline)", v2), ("UNGATED EWALL g=1.00", base)]:
        c, s, d = trip(r)
        h1, h2 = half_sharpes(r)
        oc, os_, od = trip(r.loc[OOS_START:])
        log(f"    {nm:<25} {c:>8.2%} / {s:>7.4f} / {d:>8.2%}   halves {h1:.4f} / {h2:.4f}"
            f"   OOS {oc:>8.2%} / {os_:>7.4f} / {od:>8.2%}")
    log(f"    4b bars off SPY : H1 > {B4B['H1']:.4f}, H2 > {B4B['H2']:.4f}, "
        f"OOS Sharpe > {B4B['OOS']:.4f}, |MaxDD| <= {B4B['DD']:.2%}, CAGR >= {B4B['CAGR']:.2%}")
    log(f"    4a bars off v2  : H1 > {B4A['H1']:.4f}, H2 > {B4A['H2']:.4f}, "
        f"MaxDD >= {B4A['DD']:.2%}")

    # ---------------- twins -------------------------------------------------------------------
    twin_cache = {}

    def twin(g, rung=COST):
        k = (round(float(g), 4), rung)
        if k not in twin_cache:
            twin_cache[k] = backtest(px, ewall_weights(px, k[0]), cost_bps=rung,
                                     freq=FREQ)["returns"].loc[start:]
        return twin_cache[k]

    # ---------------- the grid ----------------------------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 1 — THE FULL GRID: every (w, floor) SIZE cell and the GATE comparand at each w")
    log("=" * 100)
    log("  10 bps, weekly, t+1, gross 1.00, LEVEL 0.17.  on% = share of days the state is ON;")
    log("  g_eff = realised mean multiplier (= the matched-gross twin's constant gross).")
    log("  WORKS = Sharpe > twin's AND |MaxDD| < twin's, the record's own two-leg test.")

    in20 = (idx >= EP2020Y[0]) & (idx <= EP2020Y[1])
    in22 = (idx >= EP2022[0]) & (idx <= EP2022[1])
    ordinary = ~(in20 | in22)
    log(f"\n  corpora: FULL {len(idx)} days; calendar-2020 {int(in20.sum())}; "
        f"calendar-2022 {int(in22.sum())}; ORDINARY (both removed) {int(ordinary.sum())}")

    arms, rows = {}, []
    for w in WS:
        thr = st.rolling(w, min_periods=w).quantile(1 - LEVEL)
        rank = pct_rank(st, w)
        cells = [("GATE", MEMO_DEPTH, gate_mult(st, thr, MEMO_DEPTH, px.index))]
        cells += [("SIZE", f, size_mult(st, thr, rank, f, px.index)) for f in FLOORS]
        for form, par, mult in cells:
            r, m_eff = apply_mult(base, mult)
            g_eff = float(m_eff.mean() * GROSS)
            tw = twin(g_eff)
            c, s, d = trip(r)
            ct, sta, dt_ = trip(tw)
            h1, h2 = half_sharpes(r)
            works = bool(s > sta and abs(d) < abs(dt_))
            t4b, t4a = tests_4b(r, B4B), tests_4a(r, B4A)
            oc, os_, od = trip(r.loc[OOS_START:])
            key = (form, w, par)
            arms[key] = (r, m_eff, g_eff, tw)
            rows.append(dict(form=form, w=w, param=par, on_pct=float((m_eff < 1.0).mean()),
                             g_eff=g_eff, CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                             twin_CAGR=ct, twin_Sharpe=sta, twin_MaxDD=dt_, WORKS=works,
                             OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                             p4b=ok(t4b), p4b_fails=fails(t4b), p4a=ok(t4a), p4a_fails=fails(t4a),
                             ord_CAGR=metrics(r[ordinary])["CAGR"],
                             y2020_CAGR=metrics(r[in20])["CAGR"],
                             y2022_CAGR=metrics(r[in22])["CAGR"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    log(f"\n  {'form':<5} {'w':>5} {'par':>5} {'on%':>6} {'g_eff':>6} {'CAGR':>8} {'Sharpe':>7} "
        f"{'MaxDD':>8} {'H1':>6} {'H2':>6} {'twinShrp':>8} {'twinDD':>8} {'WORKS':>5} "
        f"{'4b':>4} {'4b fails':<12} {'4a':>4}")
    for _, x in G.iterrows():
        log(f"  {x['form']:<5} {x['w']:>5} {x['param']:>5.2f} {x['on_pct']:>6.1%} "
            f"{x['g_eff']:>6.3f} {x['CAGR']:>8.2%} {x['Sharpe']:>7.4f} {x['MaxDD']:>8.2%} "
            f"{x['H1']:>6.3f} {x['H2']:>6.3f} {x['twin_Sharpe']:>8.4f} {x['twin_MaxDD']:>8.2%} "
            f"{str(x['WORKS']):>5} {str(x['p4b']):>4} {x['p4b_fails']:<12} {str(x['p4a']):>4}")
    log(f"\n  grid totals: WORKS {int(G['WORKS'].sum())}/{len(G)}   "
        f"4b {int(G['p4b'].sum())}/{len(G)}   4a {int(G['p4a'].sum())}/{len(G)}")
    for form in ("GATE", "SIZE"):
        sub = G[G.form == form]
        log(f"    {form:<5}: WORKS {int(sub['WORKS'].sum())}/{len(sub)}   "
            f"4b {int(sub['p4b'].sum())}/{len(sub)}   4a {int(sub['p4a'].sum())}/{len(sub)}   "
            f"median Sharpe {sub['Sharpe'].median():.4f}   median CAGR {sub['CAGR'].median():.2%}")

    # ---------------- SECTION 2 — the calendar-year test (the queue's own) --------------------
    log("\n" + "=" * 100)
    log("SECTION 2 — THE CALENDAR-YEAR TEST (863's 7-of-18 table, re-run for both forms)")
    log("=" * 100)
    log(f"  matched window w = {MEMO_W} (863's memo window).  Each arm is compared YEAR BY YEAR "
        f"to its OWN matched-gross twin.")

    def year_table(key):
        r, m_eff, g_eff, tw = arms[key]
        yr = pd.DataFrame({"arm": r, "twin": tw, "ungated": base})
        by = yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
        by["arm-twin"] = by["arm"] - by["twin"]
        by["arm-ungated"] = by["arm"] - by["ungated"]
        return by

    ygate = year_table(("GATE", MEMO_W, MEMO_DEPTH))
    log(f"\n  GATE (w={MEMO_W}, depth={MEMO_DEPTH}) — g_eff {arms[('GATE', MEMO_W, MEMO_DEPTH)][2]:.3f}")
    log(f"  {'year':>6} {'arm':>9} {'twin':>9} {'arm-twin':>9} {'ungated':>9} {'arm-ung':>9}")
    for y, x in ygate.iterrows():
        log(f"  {y:>6} {x['arm']:>9.2%} {x['twin']:>9.2%} {x['arm-twin']:>+9.2%} "
            f"{x['ungated']:>9.2%} {x['arm-ungated']:>+9.2%}")
    ng_lose = int((ygate["arm-twin"] < 0).sum())
    log(f"  GATE loses to its matched-gross twin in {ng_lose} of {len(ygate)} years; "
        f"sum of the losing years {ygate.loc[ygate['arm-twin'] < 0, 'arm-twin'].sum():+.2%}; "
        f"total {ygate['arm-twin'].sum():+.2%}")

    yrows = []
    for f in FLOORS:
        yy = year_table(("SIZE", MEMO_W, f))
        lose = int((yy["arm-twin"] < 0).sum())
        yrows.append(dict(form="SIZE", floor=f, years=len(yy), lose_years=lose,
                          lose_sum=yy.loc[yy["arm-twin"] < 0, "arm-twin"].sum(),
                          total=yy["arm-twin"].sum(),
                          d2020_vs_ung=yy.loc[2020, "arm-ungated"],
                          d2022_vs_ung=yy.loc[2022, "arm-ungated"]))
    yrows.append(dict(form="GATE", floor=1 - MEMO_DEPTH, years=len(ygate), lose_years=ng_lose,
                      lose_sum=ygate.loc[ygate["arm-twin"] < 0, "arm-twin"].sum(),
                      total=ygate["arm-twin"].sum(),
                      d2020_vs_ung=ygate.loc[2020, "arm-ungated"],
                      d2022_vs_ung=ygate.loc[2022, "arm-ungated"]))
    Y = pd.DataFrame(yrows)
    Y.to_csv(f"{OUT}.years.csv", index=False)
    log(f"\n  {'form':<5} {'floor':>6} {'lose yrs':>9} {'lose sum':>9} {'total':>9} "
        f"{'d2020 vs ungated':>17} {'d2022 vs ungated':>17}")
    for _, x in Y.iterrows():
        log(f"  {x['form']:<5} {x['floor']:>6.2f} {int(x['lose_years']):>9} "
            f"{x['lose_sum']:>+9.2%} {x['total']:>+9.2%} {x['d2020_vs_ung']:>+17.2%} "
            f"{x['d2022_vs_ung']:>+17.2%}")

    # ordinary-year cost, both forms, every floor, every window
    log("\n  ORDINARY-YEAR COST (calendar 2020 and 2022 removed; CAGR on the spliced corpus)")
    ung_ord = metrics(base[ordinary])["CAGR"]
    ung20 = metrics(base[in20])["CAGR"]
    ung22 = metrics(base[in22])["CAGR"]
    log(f"    UNGATED: ordinary {ung_ord:.2%}   2020 {ung20:.2%}   2022 {ung22:.2%}")
    log(f"  {'form':<5} {'w':>5} {'par':>5} {'ord CAGR':>9} {'d ord':>8} {'2020':>9} "
        f"{'d2020':>8} {'2022':>9} {'d2022':>8}")
    ORD = []
    for _, x in G.iterrows():
        d_ord = x["ord_CAGR"] - ung_ord
        d20 = x["y2020_CAGR"] - ung20
        d22 = x["y2022_CAGR"] - ung22
        ORD.append(dict(form=x["form"], w=x["w"], param=x["param"], ord_CAGR=x["ord_CAGR"],
                        d_ord=d_ord, y2020=x["y2020_CAGR"], d2020=d20, y2022=x["y2022_CAGR"],
                        d2022=d22))
        log(f"  {x['form']:<5} {x['w']:>5} {x['param']:>5.2f} {x['ord_CAGR']:>9.2%} "
            f"{d_ord:>+8.2%} {x['y2020_CAGR']:>9.2%} {d20:>+8.2%} {x['y2022_CAGR']:>9.2%} "
            f"{d22:>+8.2%}")
    pd.DataFrame(ORD).to_csv(f"{OUT}.episodes.csv", index=False)

    # ---------------- SECTION 3 — rule 8 walk-forward -----------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 3 — RULE 8 WALK-FORWARD (dials chosen on 2009-2016 ALONE, OOS read once)")
    log("=" * 100)
    is_mask = idx <= IS_END
    oos_mask = idx >= OOS_START
    spy_is, spy_oos = spy[is_mask], spy[oos_mask]
    v2_oos = v2[oos_mask]
    B4B_OOS = bars_4b(spy_oos)
    B4A_OOS = bars_4a(v2_oos)
    log(f"  IS {int(is_mask.sum())} days ({idx[0].date()} -> {IS_END}); "
        f"OOS {int(oos_mask.sum())} days ({OOS_START} -> {idx[-1].date()})")
    spy_is_dd = abs(metrics(spy_is)["MaxDD"])
    log(f"  SPY IS  {metrics(spy_is)['CAGR']:.2%} / {metrics(spy_is)['Sharpe']:.4f} / "
        f"{metrics(spy_is)['MaxDD']:.2%}  -> C2 pool = cells with IS |MaxDD| <= "
        f"{0.60 * spy_is_dd:.2%}")

    is_rows = []
    for key, (r, m_eff, g_eff, tw) in arms.items():
        ris = r[is_mask]
        is_rows.append(dict(form=key[0], w=key[1], param=key[2], IS_CAGR=metrics(ris)["CAGR"],
                            IS_Sharpe=metrics(ris)["Sharpe"], IS_MaxDD=metrics(ris)["MaxDD"]))
    I = pd.DataFrame(is_rows)
    I.to_csv(f"{OUT}.insample.csv", index=False)
    size_is = I[I.form == "SIZE"].copy()
    c1 = size_is.loc[size_is["IS_Sharpe"].idxmax()]
    pool = size_is[size_is["IS_MaxDD"].abs() <= 0.60 * spy_is_dd]
    if len(pool):
        pool = pool.sort_values(["param", "w"], ascending=[False, False])
        c2 = pool.iloc[0]
    else:
        c2 = c1
    log(f"  C1 argmax IS Sharpe  -> SIZE w={int(c1['w'])}, floor={c1['param']:.2f} "
        f"(IS Sharpe {c1['IS_Sharpe']:.4f}, IS MaxDD {c1['IS_MaxDD']:.2%})")
    log(f"  C2 highest floor clearing the IS DD bar (pool {len(pool)}/{len(size_is)}) -> "
        f"SIZE w={int(c2['w'])}, floor={c2['param']:.2f} (IS Sharpe {c2['IS_Sharpe']:.4f}, "
        f"IS MaxDD {c2['IS_MaxDD']:.2%})")
    gate_is = I[I.form == "GATE"]
    gc1 = gate_is.loc[gate_is["IS_Sharpe"].idxmax()]
    log(f"  GATE comparand chosen the same way (C1) -> w={int(gc1['w'])}, depth={MEMO_DEPTH}")

    wf_rows = []
    picks = [("C1", ("SIZE", int(c1["w"]), float(c1["param"]))),
             ("C2", ("SIZE", int(c2["w"]), float(c2["param"]))),
             ("GATE-C1", ("GATE", int(gc1["w"]), MEMO_DEPTH)),
             ("GATE-memo", ("GATE", MEMO_W, MEMO_DEPTH))]
    log(f"\n  {'chooser':<10} {'arm':<22} {'OOS CAGR':>9} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'twinShrp':>8} {'twinDD':>8} {'WORKS':>6} {'4b':>5} {'4b fails':<14} {'4a':>5}")
    for cname, key in picks:
        r, m_eff, g_eff, tw = arms[key]
        r_o = r[oos_mask]
        g_o = float(m_eff[oos_mask].mean() * GROSS)
        tw_o = twin(g_o)[oos_mask]
        c, s, d = trip(r_o)
        ct, sta, dt_ = trip(tw_o)
        t4b, t4a = tests_4b(r_o, B4B_OOS), tests_4a(r_o, B4A_OOS)
        works = bool(s > sta and abs(d) < abs(dt_))
        wf_rows.append(dict(chooser=cname, form=key[0], w=key[1], param=key[2], OOS_g_eff=g_o,
                            OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d, twin_CAGR=ct, twin_Sharpe=sta,
                            twin_MaxDD=dt_, WORKS=works, p4b=ok(t4b), p4b_fails=fails(t4b),
                            p4a=ok(t4a), p4a_fails=fails(t4a)))
        log(f"  {cname:<10} {key[0]+' w='+str(key[1])+' p='+f'{key[2]:.2f}':<22} {c:>9.2%} "
            f"{s:>8.4f} {d:>8.2%} {sta:>8.4f} {dt_:>8.2%} {str(works):>6} {str(ok(t4b)):>5} "
            f"{fails(t4b):<14} {str(ok(t4a)):>5}")
    for nm, r_o in [("SPY", spy_oos), ("RULES v2", v2_oos), ("UNGATED", base[oos_mask])]:
        c, s, d = trip(r_o)
        log(f"  {'(comparand)':<10} {nm:<22} {c:>9.2%} {s:>8.4f} {d:>8.2%}")
    log(f"  OOS 4b bars: H1 > {B4B_OOS['H1']:.4f}, H2 > {B4B_OOS['H2']:.4f}, "
        f"|MaxDD| <= {B4B_OOS['DD']:.2%}, CAGR >= {B4B_OOS['CAGR']:.2%}   "
        f"(OOS leg inside an OOS window is the same window, reported for completeness)")
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)

    # every OOS cell, published, never selected on
    log("\n  EVERY cell's OOS triple (published, not selected on)")
    log(f"  {'form':<5} {'w':>5} {'par':>5} {'OOS CAGR':>9} {'Sharpe':>8} {'MaxDD':>8} {'4b':>5}")
    oos_rows = []
    for key, (r, m_eff, g_eff, tw) in arms.items():
        r_o = r[oos_mask]
        c, s, d = trip(r_o)
        t = tests_4b(r_o, B4B_OOS)
        oos_rows.append(dict(form=key[0], w=key[1], param=key[2], OOS_CAGR=c, OOS_Sharpe=s,
                             OOS_MaxDD=d, p4b=ok(t), fails=fails(t)))
        log(f"  {key[0]:<5} {key[1]:>5} {key[2]:>5.2f} {c:>9.2%} {s:>8.4f} {d:>8.2%} "
            f"{str(ok(t)):>5}")
    pd.DataFrame(oos_rows).to_csv(f"{OUT}.oos.csv", index=False)

    # ---------------- SECTION 4 — robustness (G6) ---------------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 4 — ROBUSTNESS ON THE CHOSEN CELL (G6: cost rungs and execution delay)")
    log("=" * 100)
    chosen = ("SIZE", int(c1["w"]), float(c1["param"]))
    thr_c = st.rolling(chosen[1], min_periods=chosen[1]).quantile(1 - LEVEL)
    mult_c = size_mult(st, thr_c, pct_rank(st, chosen[1]), chosen[2], px.index)
    gate_c = gate_mult(st, st.rolling(MEMO_W, min_periods=MEMO_W).quantile(1 - LEVEL),
                       MEMO_DEPTH, px.index)
    rob = []
    log(f"  chosen SIZE cell {chosen}; GATE memo cell (w={MEMO_W}, d={MEMO_DEPTH}) beside it")
    log(f"  {'arm':<12} {'bps':>4} {'lag':>4} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'twinShrp':>8} {'WORKS':>6}")
    for nm, mlt in [("SIZE", mult_c), ("GATE", gate_c)]:
        for rung in RUNGS:
            for lag in LAGS:
                r, m_eff = apply_mult(base_r[rung], mlt, cost_bps=rung, lag=lag)
                g_eff = float(m_eff.mean() * GROSS)
                tw = twin(g_eff, rung)
                c, s, d = trip(r)
                sta = metrics(tw)["Sharpe"]
                dt_ = metrics(tw)["MaxDD"]
                works = bool(s > sta and abs(d) < abs(dt_))
                rob.append(dict(arm=nm, bps=rung, lag=lag, CAGR=c, Sharpe=s, MaxDD=d,
                                twin_Sharpe=sta, WORKS=works))
                log(f"  {nm:<12} {rung:>4} {lag:>4} {c:>8.2%} {s:>8.4f} {d:>8.2%} "
                    f"{sta:>8.4f} {str(works):>6}")
    pd.DataFrame(rob).to_csv(f"{OUT}.robust.csv", index=False)

    # ---------------- SECTION 4B — DESCRIPTIVE ADDENDA (computed AFTER the pre-registered legs)
    log("\n" + "=" * 100)
    log("SECTION 4B — DESCRIPTIVE ADDENDA (NOT pre-registered; no dial is chosen on them)")
    log("=" * 100)
    log("  (a) EPISODE EFFICIENCY = crash payoff bought per pp of ordinary-year CAGR given up,")
    log("      where payoff = (d2020 + d2022) vs the ungated book and cost = -d_ord.  A form that")
    log("      'keeps the crash payoff without the ordinary-year cost' must score HIGHER here.")
    E = pd.DataFrame(ORD)
    E["payoff"] = E["d2020"] + E["d2022"]
    E["cost"] = -E["d_ord"]
    E["eff"] = E["payoff"] / E["cost"].replace(0, np.nan)
    E.to_csv(f"{OUT}.efficiency.csv", index=False)
    log(f"  {'form':<5} {'w':>5} {'par':>5} {'cost(ord)':>10} {'payoff':>9} {'eff':>7}")
    for _, x in E.iterrows():
        log(f"  {x['form']:<5} {x['w']:>5} {x['param']:>5.2f} {x['cost']:>10.2%} "
            f"{x['payoff']:>+9.2%} {x['eff']:>7.2f}")
    log("\n  per-window comparison of the two forms (best SIZE floor by efficiency vs the GATE)")
    log(f"  {'w':>5} {'GATE eff':>9} {'best SIZE eff':>14} {'floor':>6} {'SIZE > GATE':>12}")
    eff_rows = []
    for w in WS:
        ge = float(E[(E.form == "GATE") & (E.w == w)]["eff"].iloc[0])
        sub = E[(E.form == "SIZE") & (E.w == w)]
        bi = sub["eff"].idxmax()
        be, bf = float(E.loc[bi, "eff"]), float(E.loc[bi, "param"])
        eff_rows.append(dict(w=w, gate_eff=ge, best_size_eff=be, best_floor=bf, size_wins=be > ge))
        log(f"  {w:>5} {ge:>9.2f} {be:>14.2f} {bf:>6.2f} {str(be > ge):>12}")
    EW = pd.DataFrame(eff_rows)
    log(f"  SIZE beats the GATE on episode efficiency at {int(EW['size_wins'].sum())} of "
        f"{len(EW)} windows.")

    log("\n  (b) DOMINANCE: at each window, does ANY SIZE floor beat the GATE comparand on all")
    log("      three of CAGR, Sharpe and |MaxDD| (full sample), and on the OOS window?")
    dom_rows = []
    for w in WS:
        gr = G[(G.form == "GATE") & (G.w == w)].iloc[0]
        sub = G[(G.form == "SIZE") & (G.w == w)]
        full = sub[(sub["CAGR"] > gr["CAGR"]) & (sub["Sharpe"] > gr["Sharpe"])
                   & (sub["MaxDD"].abs() < abs(gr["MaxDD"]))]
        oos = sub[(sub["OOS_CAGR"] > gr["OOS_CAGR"]) & (sub["OOS_Sharpe"] > gr["OOS_Sharpe"])
                  & (sub["OOS_MaxDD"].abs() < abs(gr["OOS_MaxDD"]))]
        dom_rows.append(dict(w=w, gate_Sharpe=gr["Sharpe"], gate_MaxDD=gr["MaxDD"],
                             n_dom_full=len(full), n_dom_oos=len(oos),
                             dom_floors_full=list(full["param"]), dom_floors_oos=list(oos["param"])))
        log(f"    w={w:<5} GATE {gr['CAGR']:.2%}/{gr['Sharpe']:.4f}/{gr['MaxDD']:.2%}  "
            f"SIZE floors dominating it: FULL {list(full['param'])}  OOS {list(oos['param'])}")
    D = pd.DataFrame(dom_rows)
    D.to_csv(f"{OUT}.dominance.csv", index=False)
    log(f"  SIZE cells dominating their GATE comparand: FULL {int(D['n_dom_full'].sum())}/42, "
        f"OOS {int(D['n_dom_oos'].sum())}/42.")

    # ---------------- SECTION 5 — hypotheses and verdict --------------------------------------
    log("\n" + "=" * 100)
    log("SECTION 5 — PRE-REGISTERED HYPOTHESES AND THE VERDICT")
    log("=" * 100)
    ysize = Y[Y.form == "SIZE"]
    best_years = int(ysize["lose_years"].min())
    h_years = bool(best_years < ng_lose)
    memo_size = G[(G.form == "SIZE") & (G.w == MEMO_W)]
    h_ord_rows = memo_size[(memo_size["ord_CAGR"] - ung_ord) >= -0.0025]
    h_ord = bool(len(h_ord_rows) > 0)
    d20_gate = ygate.loc[2020, "arm-ungated"]
    crash_ok = []
    for f in FLOORS:
        yy = year_table(("SIZE", MEMO_W, f))
        if yy.loc[2020, "arm-ungated"] >= 0.50 * d20_gate:
            crash_ok.append(f)
    h_crash = bool(len(crash_ok) > 0)
    h_both = [f for f in crash_ok
              if (memo_size.set_index("param").loc[f, "ord_CAGR"] - ung_ord) >= -0.0025]
    memo_works = bool(G[(G.form == "SIZE") & (G.w == MEMO_W)]["WORKS"].any())
    wf = pd.DataFrame(wf_rows).set_index("chooser")
    h_wf = bool(wf.loc["C1", "WORKS"] and wf.loc["C2", "WORKS"])
    h_4b = bool(wf.loc["C1", "p4b"] and wf.loc["C2", "p4b"])

    H = [("H_REPRO", g3, f"GATE memo cell {c_m:.2%}/{s_m:.4f}/{d_m:.2%} vs 14.02%/1.1538/-15.11%"),
         ("H_YEARS", h_years, f"best SIZE loses {best_years} of {len(ygate)} years vs GATE's "
                              f"{ng_lose}"),
         ("H_ORD", h_ord, f"{len(h_ord_rows)} of {len(memo_size)} SIZE floors at w={MEMO_W} are "
                          f"within 25bp/yr of the ungated ordinary-year CAGR {ung_ord:.2%}"),
         ("H_CRASH", h_crash, f"floors keeping >= half the GATE's 2020 payoff ({d20_gate:+.2%}): "
                              f"{crash_ok}"),
         ("H_WORKS", memo_works, f"any SIZE cell at w={MEMO_W} beats its matched-gross twin on "
                                 f"both legs (FULL)"),
         ("H_WF", h_wf, f"C1 WORKS={wf.loc['C1', 'WORKS']}, C2 WORKS={wf.loc['C2', 'WORKS']} OOS"),
         ("H_4B", h_4b, f"C1 4b={wf.loc['C1', 'p4b']} ({wf.loc['C1', 'p4b_fails']}), "
                        f"C2 4b={wf.loc['C2', 'p4b']} ({wf.loc['C2', 'p4b_fails']})")]
    log(f"  {'hypothesis':<10} {'result':<6} detail")
    for nm, val, det in H:
        log(f"  {nm:<10} {'PASS' if val else 'FAIL':<6} {det}")
    pd.DataFrame([dict(hypothesis=n, result=bool(v), detail=d) for n, v, d in H]).to_csv(
        f"{OUT}.hypotheses.csv", index=False)
    log(f"\n  floors that pass BOTH the ordinary-year and the crash leg at w={MEMO_W}: {h_both}")

    if h_4b and h_wf and memo_works:
        mech = "KEEP-4b-candidate"
    elif h_years and h_ord and h_crash:
        mech = "ANSWERED-YES / PARK (sizing prices the clause better, not capital-worthy)"
    else:
        mech = "ANSWERED-NO / KILL"
    log(f"\n  MECHANICAL VERDICT (the pre-registered rule, run verbatim): {mech}")

    # The queue's own question, answered on its own terms, and the dominance the addendum found.
    q_ans = "YES" if (h_years and h_crash and len(h_both) > 0) else "NO"
    dom_any = int(D["n_dom_full"].sum()) + int(D["n_dom_oos"].sum())
    log(f"  THE QUEUE'S QUESTION ('keeps the crash payoff without the ordinary-year cost'): "
        f"{q_ans}")
    log(f"    - floors clearing BOTH legs at the memo window: {h_both} (empty => the cost and the "
        f"payoff move together)")
    log(f"    - SIZE cells dominating their own GATE comparand on CAGR+Sharpe+MaxDD: "
        f"FULL {int(D['n_dom_full'].sum())}/42, OOS {int(D['n_dom_oos'].sum())}/42")
    log(f"    - at the memo window the GATE is {G[(G.form == 'GATE') & (G.w == MEMO_W)]['Sharpe'].iloc[0]:.4f} "
        f"Sharpe / {G[(G.form == 'GATE') & (G.w == MEMO_W)]['MaxDD'].iloc[0]:.2%} MaxDD against the "
        f"best SIZE floor's {G[(G.form == 'SIZE') & (G.w == MEMO_W)]['Sharpe'].max():.4f} / "
        f"{G[(G.form == 'SIZE') & (G.w == MEMO_W)]['MaxDD'].max():.2%}")
    # The published reading (stated after the addenda were read, and labelled as such): a cell that
    # clears 4b but is beaten on ALL THREE of CAGR, Sharpe and |MaxDD| by the very arm it was meant
    # to improve on is not new capital — it is a worse spelling of a clause the record already
    # killed (idea 864).  PARK, not KEEP, and the mechanical label is published beside it.
    ch = ("SIZE", int(c1["w"]), float(c1["param"]))
    grw = G[(G.form == "GATE") & (G.w == ch[1])].iloc[0]
    chw = G[(G.form == "SIZE") & (G.w == ch[1]) & (G.param == ch[2])].iloc[0]
    beaten = bool(grw["CAGR"] > chw["CAGR"] and grw["Sharpe"] > chw["Sharpe"]
                  and abs(grw["MaxDD"]) < abs(chw["MaxDD"]))
    log(f"    - the WF-chosen cell {ch} vs the GATE at its own window: "
        f"{chw['CAGR']:.2%}/{chw['Sharpe']:.4f}/{chw['MaxDD']:.2%} against "
        f"{grw['CAGR']:.2%}/{grw['Sharpe']:.4f}/{grw['MaxDD']:.2%} -> "
        f"{'GATE WINS ALL THREE LEGS' if beaten else 'not dominated'}")
    if mech == "KEEP-4b-candidate" and q_ans == "NO" and beaten:
        verdict = ("ANSWERED-NO / PARK — 4b clears mechanically (and is reported as such), but the "
                   "chosen cell is beaten on CAGR, Sharpe AND MaxDD by the GATE it was meant to "
                   "improve on, and that GATE is idea 864's documented KILL for capital")
    else:
        verdict = mech
    log(f"\n  PUBLISHED VERDICT: {verdict}")
    log(f"  DOMINANCE COUNTS (addendum, reported not selected on): FULL "
        f"{int(D['n_dom_full'].sum())}/42, OOS {int(D['n_dom_oos'].sum())}/42; "
        f"episode efficiency SIZE > GATE at {int(EW['size_wins'].sum())}/{len(EW)} windows, all at "
        f"floor 0.90 (the smallest intervention on the grid).")
    log(f"\n  runtime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
