#!/usr/bin/env python3
"""QUEUE idea 65 — cadence-sensitivity-as-a-KEEP-test (lane B, 2026-09-06).

Question
--------
Idea 3 observed that `ew-band3` was the only book whose 4b pass survived EVERY
rebalance cadence (dSharpe -0.03..+0.00 across D/W/M) while `top20`'s Sharpe swung
+0.11 and v1's +0.30 across the same axis.  Idea 65 asks whether that observation
should be promoted into a PRE-REGISTERED ROBUSTNESS BAR: "no arm becomes a
KEEP-candidate unless its 4b verdict survives every cadence in {D,W,M,Q}".

Two separable claims are tested, and they are NOT the same claim:

  Q1 (descriptive, the queued ask): re-check the standing 4b candidates — idea 2's
      `top20`, idea 46's `f=0.85`, idea 57's `ew-band3` — against the bar on BOTH
      large-cap universes.  Which of them survive it?

  Q2 (the claim that decides whether the bar is worth adopting): does cadence
      insensitivity measured IN SAMPLE (2009-2016) predict anything OOS (2017-2026)?
      A screening bar earns its place only if the arms it keeps do better out of
      sample than the arms it rejects.  If IS cadence span is uncorrelated with OOS
      outcome, the bar is a tax on the search with no return, and the honest verdict
      is KILL of the bar — even though idea 3's within-sample observation is true.

Design (PROTOCOL rules 1-9)
---------------------------
Universes : research/universe.json (56 names) and research/universe_broad.json (136),
            both fully reported.  Committed caches; no network.
Books     : 12 PRE-EXISTING published constructions, none tuned here.  They are the
            record's own book family, taken as given so the cadence axis is the only
            thing that moves:
            v1, v2-live, top20, top12, top30, ew-all, ew-band3, ew-band5,
            frac55, frac70, frac85, ew-nogate.
Cadences  : {D, W, M, Q} — the axis under test, applied through engine.rebalance_mask.
Costs     : 10 bps (PROTOCOL, verdicts read here) and 25 bps (robustness).  Applied
            analytically, returns(c) = gross - turnover*c/1e4, which is exactly what
            engine.backtest does; asserted below against a real cost_bps=10 run.
Params    : TWO tuned numbers total — (i) the cadence set is enumerated, not tuned;
            (ii) the bar's tolerance TAU on the Sharpe span, pre-registered at 0.05
            with the whole span distribution reported so any other TAU can be read
            off the printed table; (iii) the IS/OOS split is PROTOCOL rule 8, fixed.
Rule 8    : cadence-span computed on 2009-2016 ONLY; 2017-2026 evaluated untouched.
            The chooser is fixed before any OOS number is read.
Baseline  : RULES v2 (live) at weekly, and SPY buy-and-hold, at each cost.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The cadence-vs-cadence comparisons that answer the question are far less
exposed: every arm holds the same names on the same days and differs only in when it
trades.

Deterministic, standalone.  Reads baseline.py / engine.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

GROSS = 0.75
MAX_VOL = 0.60
COSTS = [10, 25]
PROTO_COST = 10
FREQS = ["D", "W", "M", "Q"]
REF_FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TAU = 0.05                      # pre-registered Sharpe-span tolerance for the bar
SCRIPT = "research/backtests/2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.py"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, gate, band=0.03):
    ma = px.rolling(200).mean()
    if gate == "200d":
        return (px > ma).fillna(False)
    if gate == "band":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + band), 1.0)
        raw = raw.mask(px < ma * (1 - band), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "none":
        return px.notna()
    raise ValueError(gate)


def eligible(px, gate, band=0.03):
    return (vol20(px) < MAX_VOL) & trend(px, gate, band)


def w_topn(px, n):
    """Idea 2's book: top-n by the no-vol-scale composite among v1-eligible names,
    GROSS/n each, cash when fewer than n are eligible."""
    rank = composite(px).where(eligible(px, "200d")).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def w_frac(px, f):
    """Idea 46's book: top ceil(f * E_t) eligible names, always GROSS in total."""
    elig = eligible(px, "200d")
    s = score(px, vol_scale=False)[0].where(elig)
    rank = s.rank(axis=1, ascending=False)
    k = np.ceil(f * elig.sum(axis=1).astype(float)).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)


def w_ew(px, gate, band=0.03):
    e = eligible(px, gate, band).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


BOOKS = {
    "v1":         rules_v1_weights,
    "v2-live":    rules_v2_weights,
    "top12":      lambda px: w_topn(px, 12),
    "top20":      lambda px: w_topn(px, 20),
    "top30":      lambda px: w_topn(px, 30),
    "ew-all":     lambda px: w_ew(px, "200d"),
    "ew-band3":   lambda px: w_ew(px, "band", 0.03),
    "ew-band5":   lambda px: w_ew(px, "band", 0.05),
    "frac55":     lambda px: w_frac(px, 0.55),
    "frac70":     lambda px: w_frac(px, 0.70),
    "frac85":     lambda px: w_frac(px, 0.85),
    "ew-nogate":  lambda px: w_ew(px, "none"),
}
# the three standing 4b candidates the queued ask names
STANDING = {"top20": "idea 2", "frac85": "idea 46", "ew-band3": "idea 57"}


# ---------------------------------------------------------------- metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def sh(r):
    return metrics(r)["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if sh(r_oos) <= sh(spy_oos): bad.append("OOS")
    if abs(dd) > 0.60 * abs(sdd): bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m3(r)
    h1, h2 = halves(r)
    _, _, bdd = m3(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if abs(dd) > abs(bdd): bad.append("DD")
    return bad


def at_cost(g, t, bps):
    return g - t * bps / 1e4


def turn_per_yr(t):
    return t.sum() / (len(t) / 252)


# ---------------------------------------------------------------- run
def main():
    print("=" * 110)
    print("IDEA 65 — cadence-sensitivity as a pre-registered KEEP bar (lane B, 2026-09-06)")
    print(SCRIPT)
    print("=" * 110)

    panels = {}
    for uname, kw in (("u56", dict()), ("broad", dict(broad=True))):
        px = load_universe(**kw)
        # calendar sanity: the index must be trading days only (CHANGELOG 2026-09-04 bug)
        wd = pd.Series(px.index.dayofweek)
        assert (wd < 5).all(), f"{uname}: weekend dates in index"
        panels[uname] = px
        print(f"{uname}: {px.shape[0]} rows x {px.shape[1]} cols, {px.index[0].date()} .. {px.index[-1].date()}")

    # ---------------- harness check: analytic costs == engine costs
    px = panels["u56"]
    chk_g = backtest(px, w_topn(px, 20), cost_bps=0.0, freq="W")
    chk_c = backtest(px, w_topn(px, 20), cost_bps=10.0, freq="W")
    dmax = float((at_cost(chk_g["returns"], chk_g["turnover"], 10) - chk_c["returns"]).abs().max())
    print(f"\nHARNESS analytic-cost identity: max|diff| = {dmax:.3e}  (expected 0.0)")
    assert dmax < 1e-12

    # ---------------- run every (universe, book, cadence) once at zero cost
    raw = {}
    for uname, px in panels.items():
        start = px.index[260]                      # skip warm-up, as baseline.compare does
        spy_full = px["SPY"].pct_change().fillna(0).loc[start:]
        for bname, fn in BOOKS.items():
            w = fn(px)
            for f in FREQS:
                res = backtest(px, w, cost_bps=0.0, freq=f)
                raw[(uname, bname, f)] = (res["returns"].loc[start:], res["turnover"].loc[start:])
        raw[(uname, "SPY", "-")] = (spy_full, pd.Series(0.0, index=spy_full.index))

    # ---------------- reproduction gates vs the published record (u56, W, 10 bps)
    print("\n" + "-" * 110)
    print("REPRODUCTION GATES (universe.json, weekly, 10 bps) — published vs this harness")
    print("-" * 110)
    # The published rows were computed when data/prices.csv ended 2026-09-03; the cache has since
    # gained one trading day.  The gate therefore runs on the RECORD'S OWN sample end, where the
    # reproduction must be exact; the study below uses all available data.
    REC_END = "2026-09-03"
    gates = {"top20": (0.127, 1.093, -0.183, "idea 2"),
             "ew-band3": (0.113, 1.136, -0.151, "idea 57"),
             "ew-all": (0.104, 1.050, -0.159, "idea 3 control")}
    ok = 0
    for b, (pc, ps, pd_, src) in gates.items():
        g, t = raw[("u56", b, "W")]
        r = at_cost(g, t, PROTO_COST).loc[:REC_END]
        c, s, dd = m3(r)
        c2, s2, dd2 = m3(at_cost(g, t, PROTO_COST))
        hit = abs(c - pc) <= 5e-4 and abs(s - ps) <= 5e-4 and abs(dd - pd_) <= 5e-4
        ok += hit
        print(f"  {b:<10} {src:<15} published {pc:.1%}/{ps:.3f}/{pd_:.1%}   "
              f"here@{REC_END} {c:.1%}/{s:.3f}/{dd:.1%} {'MATCH' if hit else 'DIFF'}   "
              f"(full cache {c2:.1%}/{s2:.3f}/{dd2:.1%})")
    print(f"  gates matched: {ok}/{len(gates)}  — the +1 trading day in the cache moves Sharpe by ~0.001")

    # ---------------- full grid
    rows = []
    for uname in panels:
        spy, _ = raw[(uname, "SPY", "-")]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for cost in COSTS:
            base_g, base_t = raw[(uname, "v2-live", REF_FREQ)]
            base = at_cost(base_g, base_t, cost)
            for bname in BOOKS:
                for f in FREQS:
                    g, t = raw[(uname, bname, f)]
                    r = at_cost(g, t, cost)
                    c, s, dd = m3(r)
                    h1, h2 = halves(r)
                    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                    b4a, b4b = fail4a(r, base), fail4b(r, spy, r_oos, spy_oos)
                    rows.append(dict(
                        uni=uname, cost=cost, book=bname, freq=f,
                        CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2,
                        IS=sh(r_is), OOS=sh(r_oos), turn=turn_per_yr(t),
                        pass4a=not b4a, pass4b=not b4b,
                        fail4b=",".join(b4b) or "-"))
    G = pd.DataFrame(rows)
    G.to_csv(ROOT / "research" / "backtests" / "2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.grid.csv", index=False)

    print("\n" + "=" * 110)
    print(f"FULL GRID — {len(G)} points (2 universes x {len(BOOKS)} books x {len(FREQS)} cadences x {len(COSTS)} costs), ALL reported")
    print("=" * 110)
    for uname in panels:
        for cost in COSTS:
            sub = G[(G.uni == uname) & (G.cost == cost)]
            print(f"\n--- {uname} @ {cost} bps " + "-" * 70)
            print(sub[["book", "freq", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS", "OOS", "turn", "pass4a", "pass4b", "fail4b"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- Q1: the bar applied to the standing candidates
    print("\n" + "=" * 110)
    print("Q1 — CADENCE SENSITIVITY OF EVERY BOOK (full-sample), and the bar applied")
    print(f"    bar: 4b verdict must hold at ALL of {FREQS}; span = max-min full-sample Sharpe over cadences")
    print("=" * 110)
    q1 = []
    for (uname, cost, bname), sub in G.groupby(["uni", "cost", "book"], sort=False):
        sub = sub.set_index("freq").loc[FREQS]
        span = sub.Sharpe.max() - sub.Sharpe.min()
        n4b = int(sub.pass4b.sum())
        n4a = int(sub.pass4a.sum())
        dwm = sub.loc[["D", "W", "M"]]
        q1.append(dict(uni=uname, cost=cost, book=bname,
                       W=sub.Sharpe["W"], span=span,
                       span_DWM=dwm.Sharpe.max() - dwm.Sharpe.min(),
                       best=sub.Sharpe.idxmax(), worst=sub.Sharpe.idxmin(),
                       n4b=n4b, n4a=n4a,
                       bar_pass=(n4b == len(FREQS)),
                       bar_DWM=(int(dwm.pass4b.sum()) == 3),
                       W_is_4b=bool(sub.pass4b["W"]),
                       turnW=sub.turn["W"],
                       standing=STANDING.get(bname, "")))
    Q1 = pd.DataFrame(q1)
    print(Q1.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\nStanding 4b candidates against the bar (the queued ask):")
    for b, src in STANDING.items():
        for _, rr in Q1[Q1.book == b].iterrows():
            print(f"  {src:<8} {b:<9} {rr['uni']:<6} @{rr['cost']:>2}bps  weekly Sharpe {rr['W']:.3f}  "
                  f"span(DWMQ) {rr['span']:.3f} ({rr['worst']}->{rr['best']})  span(DWM) {rr['span_DWM']:.3f}  "
                  f"4b passes {rr['n4b']}/4  bar DWMQ: {'SURVIVES' if rr['bar_pass'] else 'FAILS'}  "
                  f"bar DWM: {'SURVIVES' if rr['bar_DWM'] else 'FAILS'}")

    n_w4b = int(Q1.W_is_4b.sum())
    n_bar = int((Q1.W_is_4b & Q1.bar_pass).sum())
    n_dwm = int((Q1.W_is_4b & Q1.bar_DWM).sum())
    print(f"\nAcross all {len(Q1)} (universe, cost, book) arms: {n_w4b} pass 4b at the incumbent weekly cadence; "
          f"the DWMQ bar keeps {n_bar} of them ({n_w4b - n_bar} rejected); the DWM bar (idea 3's own cadence set) "
          f"keeps {n_dwm}.")

    # ---------------- Q2: does IS cadence-insensitivity predict OOS?
    print("\n" + "=" * 110)
    print("Q2 — DOES IN-SAMPLE CADENCE INSENSITIVITY PREDICT OUT-OF-SAMPLE OUTCOME? (rule 8)")
    print("    IS span computed on 2009-2016 ONLY; OOS 2017-2026 read afterwards, untouched.")
    print("=" * 110)
    q2 = []
    for (uname, cost, bname), sub in G.groupby(["uni", "cost", "book"], sort=False):
        sub = sub.set_index("freq").loc[FREQS]
        is_span = sub.IS.max() - sub.IS.min()
        oos_span = sub.OOS.max() - sub.OOS.min()
        spy = raw[(uname, "SPY", "-")][0]
        spy_oos = sh(spy.loc[OOS_START:])
        q2.append(dict(uni=uname, cost=cost, book=bname,
                       IS_span=is_span, OOS_span=oos_span,
                       IS_W=sub.IS["W"], OOS_W=sub.OOS["W"],
                       OOS_mean=sub.OOS.mean(), OOS_min=sub.OOS.min(),
                       turnW=sub.turn["W"],
                       dOOS_vs_SPY=sub.OOS["W"] - spy_oos,
                       OOS_4b_all=int(sub.pass4b.sum()) == len(FREQS)))
    Q2 = pd.DataFrame(q2)
    print(Q2.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    def rank_corr(a, b):
        a, b = pd.Series(a).rank(), pd.Series(b).rank()
        return float(np.corrcoef(a, b)[0, 1])

    print("\nPredictive power of the IS cadence span (lower span = 'more robust' by the proposed bar):")
    for key, lab in ((None, "POOLED"), ("u56", "u56"), ("broad", "broad")):
        sub = Q2 if key is None else Q2[Q2.uni == key]
        for cost in ([None] if key is None else COSTS):
            s2 = sub if cost is None else sub[sub.cost == cost]
            if len(s2) < 4:
                continue
            print(f"  {lab:<7}{'' if cost is None else f'@{cost}bps':<9} n={len(s2):<3} "
                  f"Spearman(IS_span, OOS_W) = {rank_corr(s2.IS_span, s2.OOS_W):+.3f}   "
                  f"Spearman(IS_span, dOOS_vs_SPY) = {rank_corr(s2.IS_span, s2.dOOS_vs_SPY):+.3f}   "
                  f"Spearman(IS_span, OOS_span) = {rank_corr(s2.IS_span, s2.OOS_span):+.3f}")

    med = Q2.IS_span.median()
    lo, hi = Q2[Q2.IS_span <= med], Q2[Q2.IS_span > med]
    print(f"\nMedian split on IS span ({med:.3f}):")
    print(f"  LOW  span (n={len(lo)}): mean OOS_W {lo.OOS_W.mean():.3f}, mean dOOS vs SPY {lo.dOOS_vs_SPY.mean():+.3f}, "
          f"OOS span {lo.OOS_span.mean():.3f}, 4b-all {int(lo.OOS_4b_all.sum())}/{len(lo)}")
    print(f"  HIGH span (n={len(hi)}): mean OOS_W {hi.OOS_W.mean():.3f}, mean dOOS vs SPY {hi.dOOS_vs_SPY.mean():+.3f}, "
          f"OOS span {hi.OOS_span.mean():.3f}, 4b-all {int(hi.OOS_4b_all.sum())}/{len(hi)}")
    d = lo.OOS_W.mean() - hi.OOS_W.mean()
    sd = np.sqrt(lo.OOS_W.var(ddof=1) / len(lo) + hi.OOS_W.var(ddof=1) / len(hi))
    print(f"  difference in mean OOS weekly Sharpe (LOW - HIGH) = {d:+.3f}  (t {d / sd:+.2f})")

    # ------------- Q2c: is the span anything other than turnover, and does it beat IS Sharpe?
    print("\n" + "-" * 110)
    print("Q2c — CONFOUND CHECK.  A high-turnover book is punished hardest by the DAILY arm, so a large")
    print("      cadence span may be nothing but a restatement of turnover, which the record already")
    print("      knows is bad (ideas 273/279).  A screening bar must also add information over the")
    print("      in-sample Sharpe the search already ranks on.")
    print("-" * 110)

    def partial_rank_corr(y, x, z):
        """Spearman(y, x) with z partialled out, on ranks (Gaussian-free, linear residuals)."""
        ry, rx, rz = (pd.Series(v).rank().values for v in (y, x, z))
        def resid(a):
            A = np.column_stack([np.ones_like(rz), rz])
            return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]
        return float(np.corrcoef(resid(ry), resid(rx))[0, 1])

    for key in ("POOLED", "u56", "broad"):
        sub = Q2 if key == "POOLED" else Q2[Q2.uni == key]
        lt = np.log(sub.turnW)
        print(f"  {key:<7} n={len(sub):<3} "
              f"Sp(IS_span, logTurnW) = {rank_corr(sub.IS_span, lt):+.3f}   "
              f"Sp(logTurnW, OOS_W) = {rank_corr(lt, sub.OOS_W):+.3f}   "
              f"Sp(IS_W, OOS_W) = {rank_corr(sub.IS_W, sub.OOS_W):+.3f}")
        print(f"  {'':<7} {'':<6} "
              f"PARTIAL Sp(IS_span, OOS_W | logTurnW) = {partial_rank_corr(sub.OOS_W, sub.IS_span, lt):+.3f}   "
              f"PARTIAL Sp(IS_span, OOS_W | IS_W)     = {partial_rank_corr(sub.OOS_W, sub.IS_span, sub.IS_W):+.3f}")

    # turnover is cost-INVARIANT while the span is not, so the pooled control mixes two
    # different things.  The clean control is inside a single (universe, cost) cell, where
    # the 12 books have 12 distinct turnovers and one cost rung.
    print("\n  Per-cell (n=12 books, one universe, one cost rung) — the clean control:")
    for uname in panels:
        for cost in COSTS:
            sub = Q2[(Q2.uni == uname) & (Q2.cost == cost)]
            lt = np.log(sub.turnW)
            print(f"    {uname:<6}@{cost:>2}bps  Sp(span,OOS) = {rank_corr(sub.IS_span, sub.OOS_W):+.3f}   "
                  f"Sp(logTurn,OOS) = {rank_corr(lt, sub.OOS_W):+.3f}   "
                  f"Sp(span,logTurn) = {rank_corr(sub.IS_span, lt):+.3f}   "
                  f"PARTIAL Sp(span,OOS|logTurn) = {partial_rank_corr(sub.OOS_W, sub.IS_span, lt):+.3f}")

    # head-to-head chooser: rank on IS Sharpe alone vs rank on IS span alone
    print("\n  Head-to-head chooser over the 12 books, selection on 2009-2016 only:")
    for uname in panels:
        spy_oos = sh(raw[(uname, "SPY", "-")][0].loc[OOS_START:])
        for cost in COSTS:
            sub = Q2[(Q2.uni == uname) & (Q2.cost == cost)]
            by_sh = sub.loc[sub.IS_W.idxmax()]
            by_sp = sub.loc[sub.IS_span.idxmin()]
            by_tn = sub.loc[sub.turnW.idxmin()]
            print(f"    {uname:<6}@{cost:>2}bps  IS-Sharpe pick {by_sh.book:<10} OOS {by_sh.OOS_W:.3f} | "
                  f"min-span pick {by_sp.book:<10} OOS {by_sp.OOS_W:.3f} | "
                  f"min-turnover pick {by_tn.book:<10} OOS {by_tn.OOS_W:.3f} | "
                  f"grid-mean OOS {sub.OOS_W.mean():.3f} | SPY {spy_oos:.3f}")

    # ---------------- Q2b: the bar as a chooser (rule 8, decided IS-only)
    print("\n" + "-" * 110)
    print("Q2b — the bar AS A CHOOSER: pick IS-best book per (universe, cost) with and without the bar,")
    print("      then read OOS.  Selection uses 2009-2016 weekly Sharpe only.")
    print("-" * 110)
    for uname in panels:
        spy = raw[(uname, "SPY", "-")][0]
        spy_oos = sh(spy.loc[OOS_START:])
        for cost in COSTS:
            sub = Q2[(Q2.uni == uname) & (Q2.cost == cost)].copy()
            # IS-only cadence-bar: span <= TAU on 2009-2016
            elig = sub[sub.IS_span <= TAU]
            free = sub.loc[sub.IS_W.idxmax()]
            gated = elig.loc[elig.IS_W.idxmax()] if len(elig) else None
            print(f"  {uname} @{cost}bps  unbarred pick: {free.book:<10} IS {free.IS_W:.3f} -> OOS {free.OOS_W:.3f} "
                  f"({free.OOS_W - spy_oos:+.3f} vs SPY {spy_oos:.3f})")
            if gated is None:
                print(f"                barred   pick (TAU={TAU}): NONE — no book qualifies")
            else:
                print(f"                barred   pick (TAU={TAU}): {gated.book:<10} IS {gated.IS_W:.3f} -> OOS {gated.OOS_W:.3f} "
                      f"({gated.OOS_W - spy_oos:+.3f} vs SPY)   worth {gated.OOS_W - free.OOS_W:+.3f} OOS Sharpe "
                      f"({len(elig)}/{len(sub)} books eligible)")
            # threshold-free variant: IS-best among the lowest-span HALF of the books
            half = sub[sub.IS_span <= sub.IS_span.median()]
            hp = half.loc[half.IS_W.idxmax()]
            print(f"                barred   pick (span<=median): {hp.book:<10} IS {hp.IS_W:.3f} -> OOS {hp.OOS_W:.3f} "
                  f"({hp.OOS_W - spy_oos:+.3f} vs SPY)   worth {hp.OOS_W - free.OOS_W:+.3f} OOS Sharpe")

    # ---------------- headline counts
    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)
    print(f"  4a passes : {int(G.pass4a.sum())} of {len(G)} grid points")
    print(f"  4b passes : {int(G.pass4b.sum())} of {len(G)} grid points")
    print(f"  arms (universe,cost,book) whose 4b verdict is cadence-STABLE at all 4 cadences: "
          f"{int((Q1.n4b == 4).sum())} pass-all, {int((Q1.n4b == 0).sum())} fail-all, "
          f"{int(((Q1.n4b > 0) & (Q1.n4b < 4)).sum())} FLIP")
    print(f"  grid CSV  : research/backtests/2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.grid.csv")


if __name__ == "__main__":
    main()
