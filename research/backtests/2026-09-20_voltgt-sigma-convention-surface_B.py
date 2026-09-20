#!/usr/bin/env python3
"""Idea 1771 (lane B, 2026-09-20): IS THE STANDING VOLTGT016 4b OOS PASS DECIDABLE ACROSS THE
SIGMA-CONVENTION SURFACE, OR IS IT A KNIFE-EDGE?

THE DEFECT THIS CLOSES
----------------------
The record has exactly ONE standing KEEP-4b candidate heading for a Sunday review:
`research/backtests/2026-09-20_voltgt-panel_KEEP4b_MEMO.md` (idea 1730, lane cloud).  Its book is
the unlevered equal-weight panel scaled by `g_t = clip(target / sigma_t, 0, 1)`, weekly, 10 bps.
Its U56 4b OOS pass clears the drawdown cap by **0.37 pp** (OOS MaxDD -19.86% against 0.60 x SPY =
-20.23%), and addendum A1 (idea 1715) already flipped that pass to FAIL by computing sigma through
t-1 instead of t -- ONE alternative convention, tested ONCE.

`sigma_t` is not a primitive.  It is a CONVENTION with (at least) two free choices that no rule
wording can avoid making: the LOOKBACK `L` over which realised vol is measured, and the STALENESS
`d` (how many closes back the estimate is read from).  The memo picks `L = 20, d = 0` and says
nothing about either.  The surface those two choices span has never been mapped.  A 4b pass that
holds at one cell of a convention surface is not a property of the BOOK; it is a property of the
CELL, and it is not capital-worthy.

This run maps the surface, publishes the CONVENTION PASS-SHARE beside the verdict (idea 956's
phase pass-share, moved onto the other axis), carries every book's realised-mean-gross-matched
CONSTANT-GROSS twin as a control, and lets rule 8 decide whether any legal IS-only chooser over
(L, d) can reach a 4b-OOS-passing cell at all.

THE CONSTRUCTION
----------------
TUNED (2, the protocol maximum, ALL grid points reported):
    L  lookback for realised vol   {5, 10, 20, 40, 60}
    d  staleness in closes         {0, 1, 2, 5}                       -> 20 convention cells
PUBLISHED, NOT TUNED:
    target vol t   {0.08, 0.10, 0.12, 0.16, 0.20}   (the memo's grid 0.08/0.12/0.16 + 2 rungs)
    panel          {U56, B136, SMALL665}
    cost           {0, 10, 25, 50} bps              (exact: held/turnover do not depend on cost)
CONTROL (not a dial): every VOLTGT book is paired with its OWN constant-gross twin, the same names
    at the same weekly cadence with a CONSTANT gross k solved so the twin carries the SAME REALISED
    MEAN GROSS on the SAME window.  The twin is what "buy less of it" looks like; the VOLTGT book
    has to beat that, not cash.
    -> 20 x 5 x 3 = 300 VOLTGT books + 300 FULL-matched twins + 300 OOS-matched twins, 4 cost rungs.

PRE-STATED VERDICT RULES (fixed before the run; no tuning-until-it-works)
------------------------------------------------------------------------
V1  CONVENTION PASS-SHARE.  If the memo's cell (L=20, d=0) is in a MINORITY (< 0.50) of the 20
    convention cells clearing 4b OOS on U56 at the memo's t=0.16, the pass is CONVENTION-SELECTED
    and the Sunday review should read the candidate as PARK, not KEEP.
V2  If >= 0.75 of convention cells clear 4b OOS on BOTH U56 and B136 at t=0.16, the pass is
    convention-robust and the KEEP-4b candidate stands as written.
V3  RULE 8 IS DECISIVE FOR CAPITAL.  Parameters (L, d) chosen on 2009-2016 ONLY; 2017-2026 read
    ONCE.  If no IS-only chooser reaches a 4b-OOS-passing cell, the candidate is a KILL for capital
    whatever the pass-share says -- the passing cells are hindsight.
V4  THE TWIN IS THE COMPARAND.  If the matched constant-gross twin clears 4b at least as often as
    the VOLTGT book, the vol target is a tuned parameter that buys nothing and the SIMPLER book is
    the better candidate.  That is a finding about what should go to review, not a KEEP.

Run: python research/backtests/2026-09-20_voltgt-sigma-convention-surface_B.py
Deterministic, offline (committed caches only).  RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py are NOT modified by this run (rule 6).
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

DATE, SLUG = "2026-09-20", "voltgt-sigma-convention-surface"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, CAD = 260, "W"
GRID_L = [5, 10, 20, 40, 60]
GRID_D = [0, 1, 2, 5]
GRID_T = [0.08, 0.10, 0.12, 0.16, 0.20]
COSTS = [0.0, 10.0, 25.0, 50.0]
PRIMARY_COST = 10.0
MEMO_L, MEMO_D, MEMO_T = 20, 0, 0.16          # the standing candidate's own cell
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# --------------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book; 4b against SPY.  Returns verdicts + the 4b legs."""
    m = pack(r)
    k4a = bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(L1_H1=bool(m["H1"] > bm["H1"]), L2_H2=bool(m["H2"] > bm["H2"]),
                L4_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L5_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, legs


# --------------------------------------------------------- the shared panel state
def ew_unit(px):
    """Record convention: gross/N over every PRICED name, gated-out weight to CASH."""
    e = px.notna().astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def panel_state(px, freq=CAD):
    """Engine-exact decomposition.  held_t = G_t * u_t with u_t INDEPENDENT of the gross scalar,
    because every book here rebalances to the SAME equal-weight unit vector.  So u and the basket
    return b are computed ONCE per panel and shared by all 600 books on it."""
    R = px.pct_change().fillna(0.0).values
    E = ew_unit(px).shift(1).fillna(0.0).values          # decided t, applied t+1 (engine's shift)
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    T, N = R.shape
    Upre = np.zeros((T, N)); B = np.zeros(T)
    cur = np.zeros(N)
    for i in range(T):
        Upre[i] = cur
        if mask[i] or i == 0:
            cur = E[i]
        b = float(cur @ R[i]); B[i] = b
        cur = cur * (1 + R[i]) / (1 + b) if (1 + b) > 0 else cur
    rb = np.flatnonzero(mask | (np.arange(T) == 0))
    return dict(R=R, E=E, mask=mask, B=B, Upre=Upre, rb=rb, T=T, idx=px.index)


def gross_path(st, gvec):
    """Scalar-only recursion for the realised gross path (no vectors -> used by the twin solve)."""
    B, mask, T = st["B"], st["mask"], st["T"]
    G = np.nan; out = np.empty(T)
    for i in range(T):
        if mask[i] or i == 0:
            G = gvec[i]
        out[i] = G
        tot = 1 + G * B[i]
        if tot > 0:
            G = G * (1 + B[i]) / tot
    return out


def run(st, gvec):
    """Full run: gross return, turnover, realised gross.  Engine-exact (gate G1)."""
    B, mask, E, Upre, T = st["B"], st["mask"], st["E"], st["Upre"], st["T"]
    N = E.shape[1]
    G = np.nan; gross = np.empty(T); turn = np.zeros(T); gr = np.empty(T)
    nanv = np.full(N, np.nan)
    for i in range(T):
        if mask[i] or i == 0:
            held_now = G * Upre[i] if np.isfinite(G) else nanv
            turn[i] = np.abs(gvec[i] * E[i] - held_now).sum()
            G = gvec[i]
        gross[i] = G
        gr[i] = G * B[i]
        tot = 1 + G * B[i]
        if tot > 0:
            G = G * (1 + B[i]) / tot
    return gr, turn, gross


def rets_at(gr, turn, c):
    """Returns at any cost rung, exactly: held and turnover do not depend on cost."""
    return gr - turn * c / 1e4


# --------------------------------------------------------------------- the books
def voltgt_gvec(px, t, L, d):
    """The standing candidate's own construction (verbatim from idea 1730's dev_voltgt), with the
    two convention choices exposed: lookback L and staleness d."""
    base = ew_unit(px)
    pr = (base.shift(1) * px.pct_change()).sum(axis=1)      # unlevered EW panel return
    rv = pr.rolling(L).std() * np.sqrt(252)
    if d:
        rv = rv.shift(d)
    k = (t / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return k.shift(1).fillna(0.0).values                    # engine's decided-t / applied-t+1


def const_gvec(st, k):
    return np.full(st["T"], float(k))


def solve_twin(st, target_mean_gross, sl):
    """Constant gross k whose REALISED mean gross over slice sl matches the VOLTGT book's, to
    machine precision.  mean gross is monotone in k, so plain bisection on [0, 1] (no leverage)."""
    lo, hi = 0.0, 1.0
    f = lambda k: float(np.nanmean(gross_path(st, const_gvec(st, k))[sl])) - target_mean_gross
    if f(hi) < 0:
        return 1.0, f(1.0)                                   # unreachable without leverage
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    k = 0.5 * (lo + hi)
    return k, f(k)


# --------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    mx = px.drop(columns=["SPY"]).pct_change().abs().max()
    keep = [c for c in px.columns if c == "SPY" or mx.get(c, 0.0) < 1.0]
    return px[keep]


def main():
    t_start = time.time()
    say("=" * 108)
    say("IDEA 1771 (lane B, 2026-09-20) — IS THE STANDING VOLTGT016 4b OOS PASS DECIDABLE ACROSS")
    say("THE SIGMA-CONVENTION SURFACE (lookback L x staleness d), OR IS IT A KNIFE-EDGE?")
    say("=" * 108)
    say(__doc__.split("Run:")[0].strip())
    say("=" * 108)

    panels = {}
    for nm, kw in (("U56", {}), ("B136", dict(broad=True))):
        panels[nm] = load_universe(**kw)
    panels["SMALL665"] = small_panel()
    for nm, px in panels.items():
        say(f"  panel {nm:9s} {px.shape[1]:4d} cols x {len(px):5d} days  "
            f"{px.index[0].date()} -> {px.index[-1].date()}")

    rows, wf_rows = [], []
    for pname, px in panels.items():
        say("\n" + "-" * 108)
        say(f"PANEL {pname}")
        say("-" * 108)
        st = panel_state(px)
        i0 = WARMUP
        ioos = int(px.index.searchsorted(pd.Timestamp(OOS_START)))
        iis_end = int(px.index.searchsorted(pd.Timestamp(IS_END), side="right"))
        sl_full, sl_oos, sl_is = slice(i0, None), slice(ioos, None), slice(i0, iis_end)

        spy = px["SPY"].pct_change().fillna(0.0).values
        bm = dict(FULL=pack(spy[sl_full]), OOS=pack(spy[sl_oos]), IS=pack(spy[sl_is]))
        lv = backtest(px, rules_v2_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        v1 = backtest(px, rules_v1_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        live = dict(FULL=pack(lv[sl_full]), OOS=pack(lv[sl_oos]), IS=pack(lv[sl_is]))
        say(f"  SPY   FULL {bm['FULL']['CAGR']:7.2%} / {bm['FULL']['Sharpe']:.4f} / {bm['FULL']['MaxDD']:7.2%}"
            f"   OOS {bm['OOS']['CAGR']:7.2%} / {bm['OOS']['Sharpe']:.4f} / {bm['OOS']['MaxDD']:7.2%}")
        say(f"  LIVE  FULL {live['FULL']['CAGR']:7.2%} / {live['FULL']['Sharpe']:.4f} / {live['FULL']['MaxDD']:7.2%}"
            f"   OOS {live['OOS']['CAGR']:7.2%} / {live['OOS']['Sharpe']:.4f} / {live['OOS']['MaxDD']:7.2%}")
        say(f"  v1    FULL {pack(v1[sl_full])['CAGR']:7.2%} / {pack(v1[sl_full])['Sharpe']:.4f} / {pack(v1[sl_full])['MaxDD']:7.2%}")
        say(f"  4b bars FULL: H1>{bm['FULL']['H1']:.4f} H2>{bm['FULL']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['FULL']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['FULL']['CAGR']:.2%}")
        say(f"  4b bars OOS : H1>{bm['OOS']['H1']:.4f} H2>{bm['OOS']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['OOS']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['OOS']['CAGR']:.2%}")

        # ---- gate G1 (engine exactness) on this panel, at the memo cell
        gv = voltgt_gvec(px, MEMO_T, MEMO_L, MEMO_D)
        gr, turn, gross = run(st, gv)
        W = ew_unit(px).mul(pd.Series(gv, index=px.index).shift(-1).fillna(0.0), axis=0)
        for c in (PRIMARY_COST, 25.0):
            ref = backtest(px, W, cost_bps=c, freq=CAD)["returns"].values[sl_full]
            gate(f"G1 fast_run == engine.backtest [{pname}, {c:.0f}bps]",
                 f"{np.abs(rets_at(gr, turn, c)[sl_full] - ref).max():.3e}", "== 0 (<= 1e-15)",
                 np.abs(rets_at(gr, turn, c)[sl_full] - ref).max() <= 1e-15)

        for t in GRID_T:
            for L in GRID_L:
                for d in GRID_D:
                    gv = voltgt_gvec(px, t, L, d)
                    gr, turn, gross = run(st, gv)
                    mg_f = float(np.nanmean(gross[sl_full])); mg_o = float(np.nanmean(gross[sl_oos]))
                    kf, ef = solve_twin(st, mg_f, sl_full)
                    ko, eo = solve_twin(st, mg_o, sl_oos)
                    tw_f = run(st, const_gvec(st, kf))
                    tw_o = run(st, const_gvec(st, ko))
                    yrs = (len(gr) - i0) / 252
                    for c in COSTS:
                        r = rets_at(gr, turn, c)
                        k4aF, k4bF, mF, legF = keep_paths(r[sl_full], bm["FULL"], live["FULL"])
                        k4aO, k4bO, mO, legO = keep_paths(r[sl_oos], bm["OOS"], live["OOS"])
                        mI = pack(r[sl_is])
                        _, k4bI, _, legI = keep_paths(r[sl_is], bm["IS"], live["IS"])
                        rtf = rets_at(tw_f[0], tw_f[1], c); rto = rets_at(tw_o[0], tw_o[1], c)
                        t4aF, t4bF, tmF, _ = keep_paths(rtf[sl_full], bm["FULL"], live["FULL"])
                        t4aO, t4bO, tmO, _ = keep_paths(rto[sl_oos], bm["OOS"], live["OOS"])
                        rows.append(dict(
                            panel=pname, t=t, L=L, d=d, cost=c,
                            CAGR=mF["CAGR"], Sharpe=mF["Sharpe"], MaxDD=mF["MaxDD"],
                            H1=mF["H1"], H2=mF["H2"],
                            oCAGR=mO["CAGR"], oSharpe=mO["Sharpe"], oMaxDD=mO["MaxDD"],
                            isCAGR=mI["CAGR"], isSharpe=mI["Sharpe"], isMaxDD=mI["MaxDD"],
                            keep4a=k4aF, keep4b=k4bF, keep4a_oos=k4aO, keep4b_oos=k4bO,
                            keep4b_is=k4bI, is_legs=sum(legI.values()),
                            **{f"F_{k}": v for k, v in legF.items()},
                            **{f"O_{k}": v for k, v in legO.items()},
                            mean_gross=mg_f, mean_gross_oos=mg_o,
                            turnover=float(turn[sl_full].sum()) / yrs,
                            twin_k=kf, twin_k_oos=ko, twin_match_err=abs(ef), twin_match_err_oos=abs(eo),
                            twSharpe=tmF["Sharpe"], twMaxDD=tmF["MaxDD"], twCAGR=tmF["CAGR"],
                            twoSharpe=tmO["Sharpe"], twoMaxDD=tmO["MaxDD"], twoCAGR=tmO["CAGR"],
                            tw_keep4a=t4aF, tw_keep4b=t4bF, tw_keep4a_oos=t4aO, tw_keep4b_oos=t4bO,
                            dSharpe=mF["Sharpe"] - tmF["Sharpe"], dMaxDD=mF["MaxDD"] - tmF["MaxDD"],
                            odSharpe=mO["Sharpe"] - tmO["Sharpe"], odMaxDD=mO["MaxDD"] - tmO["MaxDD"],
                        ))
            say(f"  t={t:.2f} done  ({time.time()-t_start:5.1f}s)")

    R = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    R.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"\n  {len(R)} scored rows -> {Path(str(OUT)+'.grid.csv').name}")
    gate("G4 twin realised-mean-gross match (max abs err over all cells)",
         f"{R.twin_match_err.max():.3e} / {R.twin_match_err_oos.max():.3e}", "< 1e-10",
         max(R.twin_match_err.max(), R.twin_match_err_oos.max()) < 1e-10)
    gate("G6 no NaN in scored metrics", int(R[["Sharpe", "oSharpe", "MaxDD", "oMaxDD"]].isna().sum().sum()),
         "== 0", int(R[["Sharpe", "oSharpe", "MaxDD", "oMaxDD"]].isna().sum().sum()) == 0)

    # ---------------- G2/G3: replicate the standing memo and its addendum A1
    say("\n" + "=" * 108)
    say("REPLICATION OF THE STANDING CANDIDATE (idea 1730 memo + idea 1715 addendum A1)")
    say("=" * 108)
    P = lambda pn, t, L, d, c=PRIMARY_COST: R[(R.panel == pn) & (R.t == t) & (R.L == L) & (R.d == d) & (R.cost == c)].iloc[0]
    memo = {("U56", "FULL"): (0.1561, 1.2027, -0.1986), ("U56", "OOS"): (0.1594, 1.2193, -0.1986),
            ("B136", "FULL"): (0.1594, 1.2049, -0.1876), ("B136", "OOS"): (0.1536, 1.1837, -0.1876)}
    worst = 0.0
    for (pn, win), (mc, ms, md) in memo.items():
        r = P(pn, MEMO_T, MEMO_L, MEMO_D)
        got = (r.CAGR, r.Sharpe, r.MaxDD) if win == "FULL" else (r.oCAGR, r.oSharpe, r.oMaxDD)
        dmax = max(abs(got[0] - mc), abs(got[1] - ms), abs(got[2] - md))
        worst = max(worst, dmax)
        say(f"  {pn:5s} {win:4s} memo {mc:7.2%} / {ms:.4f} / {md:7.2%}   "
            f"this run {got[0]:7.2%} / {got[1]:.4f} / {got[2]:7.2%}   max|d| {dmax:.2e}")
    gate("G2 memo replication (idea 1730, 12 published numbers)", f"{worst:.2e}", "<= 5e-4", worst <= 5e-4)
    a1 = P("U56", MEMO_T, MEMO_L, 1)
    say(f"  A1 (idea 1715): U56 t=0.16 L=20 d=1 OOS MaxDD {a1.oMaxDD:.2%} (addendum published -20.77%), "
        f"4b OOS {'PASS' if a1.keep4b_oos else 'FAIL'}")
    gate("G3 addendum A1 replication (d=1 flips U56 4b OOS to FAIL)",
         f"{a1.oMaxDD:.4%} / 4b OOS {'PASS' if a1.keep4b_oos else 'FAIL'}",
         "-20.77% and FAIL", abs(a1.oMaxDD - (-0.2077)) <= 5e-4 and not bool(a1.keep4b_oos))

    # ---------------- the surface
    say("\n" + "=" * 108)
    say(f"THE SIGMA-CONVENTION SURFACE AT THE MEMO'S TARGET t={MEMO_T} AND {PRIMARY_COST:.0f} bps")
    say("(OOS 2017-2026: CAGR / Sharpe / MaxDD, and the 4b OOS verdict.  * = the memo's own cell)")
    say("=" * 108)
    for pn in panels:
        say(f"\n  {pn}")
        say("    " + "L / d".rjust(5) + " " + "  ".join(f"{'d=' + str(d):^30s}" for d in GRID_D))
        for L in GRID_L:
            cells = []
            for d in GRID_D:
                r = P(pn, MEMO_T, L, d)
                star = "*" if (L == MEMO_L and d == MEMO_D) else " "
                cells.append(f"{r.oCAGR:6.2%}/{r.oSharpe:.3f}/{r.oMaxDD:7.2%} "
                             f"{'Y' if r.keep4b_oos else 'n'}{star}")
            say(f"    {L:5d} " + "  ".join(f"{c:^30s}" for c in cells))

    say("\n" + "=" * 108)
    say("CONVENTION PASS-SHARE — the share of the 20 (L, d) convention cells that clears each bar")
    say("=" * 108)
    say(f"  {'panel':9s} {'t':>5s} {'4b FULL':>9s} {'4b OOS':>9s} {'4b BOTH':>9s} {'4a FULL':>9s} "
        f"{'4a OOS':>9s} | {'TWIN 4b FULL':>13s} {'TWIN 4b OOS':>12s}")
    share = []
    for pn in panels:
        for t in GRID_T:
            S = R[(R.panel == pn) & (R.t == t) & (R.cost == PRIMARY_COST)]
            n = len(S)
            rec = dict(panel=pn, t=t, n=n,
                       b4F=S.keep4b.mean(), b4O=S.keep4b_oos.mean(),
                       b4B=(S.keep4b & S.keep4b_oos).mean(),
                       a4F=S.keep4a.mean(), a4O=S.keep4a_oos.mean(),
                       tw4F=S.tw_keep4b.mean(), tw4O=S.tw_keep4b_oos.mean())
            share.append(rec)
            say(f"  {pn:9s} {t:5.2f} {rec['b4F']:9.3f} {rec['b4O']:9.3f} {rec['b4B']:9.3f} "
                f"{rec['a4F']:9.3f} {rec['a4O']:9.3f} | {rec['tw4F']:13.3f} {rec['tw4O']:12.3f}")
    pd.DataFrame(share).to_csv(f"{OUT}.pass_share.csv", index=False)

    say("\n  WHICH 4b LEG FAILS ACROSS THE WHOLE SURFACE (all t x L x d, 10 bps), per panel:")
    for pn in panels:
        S = R[(R.panel == pn) & (R.cost == PRIMARY_COST)]
        fF = {k: float((~S[f"F_{k}"]).mean()) for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR")}
        fO = {k: float((~S[f"O_{k}"]).mean()) for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR")}
        say(f"    {pn:9s} FULL " + " ".join(f"{k} {v:.3f}" for k, v in fF.items()))
        say(f"    {'':9s} OOS  " + " ".join(f"{k} {v:.3f}" for k, v in fO.items()))

    say("\n  COST LADDER (4b OOS pass count over the 100 t x L x d cells, per panel):")
    for pn in panels:
        say(f"    {pn:9s} " + "  ".join(
            f"{c:.0f}bps {int(R[(R.panel==pn)&(R.cost==c)].keep4b_oos.sum()):3d}/100" for c in COSTS))

    # ---------------- the matched twin control
    say("\n" + "=" * 108)
    say("CONTROL — VOLTGT vs ITS OWN REALISED-MEAN-GROSS-MATCHED CONSTANT-GROSS TWIN (10 bps)")
    say("=" * 108)
    say(f"  {'panel':9s} {'mean dSharpe':>13s} {'mean dMaxDD':>12s} {'win share':>10s} | "
        f"{'OOS dSharpe':>12s} {'OOS dMaxDD':>11s} {'OOS win':>8s} | {'4b OOS voltgt':>14s} {'twin':>6s}")
    twin_rows = []
    for pn in panels:
        S = R[(R.panel == pn) & (R.cost == PRIMARY_COST)]
        rec = dict(panel=pn, dSharpe=S.dSharpe.mean(), dMaxDD=S.dMaxDD.mean() * 100,
                   win=(S.dSharpe > 0).mean(), odSharpe=S.odSharpe.mean(),
                   odMaxDD=S.odMaxDD.mean() * 100, owin=(S.odSharpe > 0).mean(),
                   v4b=int(S.keep4b_oos.sum()), t4b=int(S.tw_keep4b_oos.sum()), n=len(S))
        twin_rows.append(rec)
        say(f"  {pn:9s} {rec['dSharpe']:13.4f} {rec['dMaxDD']:11.2f}pp {rec['win']:10.3f} | "
            f"{rec['odSharpe']:12.4f} {rec['odMaxDD']:10.2f}pp {rec['owin']:8.3f} | "
            f"{rec['v4b']:10d}/{rec['n']:d} {rec['t4b']:5d}")
    pd.DataFrame(twin_rows).to_csv(f"{OUT}.twin.csv", index=False)

    # ---------------- rule 8
    say("\n" + "=" * 108)
    say(f"RULE 8 — (L, d) CHOSEN ON {px.index[WARMUP].date()}..{IS_END} ONLY; {OOS_START}..2026 READ ONCE")
    say("=" * 108)
    say("  Choosers, all IS-only and all legal (they see nothing after 2016-12-31):")
    say("    C_ISSHARPE  argmax IS Sharpe")
    say("    C_ISLEGS    max IS 4b-leg count, tie-break on IS Sharpe")
    say("    C_ISDD      argmin IS MaxDD (the leg the memo's margin actually sits on)")
    say("    C_MEMO      the memo's own cell (L=20, d=0), i.e. no choice at all — the control")
    say(f"  Two arms: FIXED t = {MEMO_T} (the candidate's rung) and FREE t (the chooser also picks t).")
    say("")
    say(f"  {'panel':9s} {'arm':6s} {'chooser':11s} {'pick':16s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
        f"{'OOS MaxDD':>10s}  {'4b OOS':>7s} {'4a OOS':>7s}  {'vs SPY':>8s} {'vs LIVE':>8s}")
    for pn in panels:
        Sc = R[(R.panel == pn) & (R.cost == PRIMARY_COST)]
        spy_o = Sc.iloc[0]
        for arm, sub in (("FIXED", Sc[Sc.t == MEMO_T]), ("FREE", Sc)):
            for cname in ("C_ISSHARPE", "C_ISLEGS", "C_ISDD", "C_MEMO"):
                if cname == "C_ISSHARPE":
                    pick = sub.sort_values(["isSharpe"], ascending=False).iloc[0]
                elif cname == "C_ISLEGS":
                    pick = sub.sort_values(["is_legs", "isSharpe"], ascending=False).iloc[0]
                elif cname == "C_ISDD":
                    pick = sub.sort_values(["isMaxDD"], ascending=False).iloc[0]
                else:
                    pk = sub[(sub.L == MEMO_L) & (sub.d == MEMO_D)]
                    pick = pk.sort_values(["isSharpe"], ascending=False).iloc[0]
                wf_rows.append(dict(panel=pn, arm=arm, chooser=cname, t=pick.t, L=pick.L, d=pick.d,
                                    oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                                    keep4b_oos=bool(pick.keep4b_oos), keep4a_oos=bool(pick.keep4a_oos),
                                    twoSharpe=pick.twoSharpe, twoMaxDD=pick.twoMaxDD,
                                    tw_keep4b_oos=bool(pick.tw_keep4b_oos)))
                lbl = f"t{pick.t:.2f} L{int(pick.L)} d{int(pick.d)}"
                say(f"  {pn:9s} {arm:6s} {cname:11s} {lbl:16s} {pick.oCAGR:9.2%} {pick.oSharpe:11.4f} "
                    f"{pick.oMaxDD:10.2%}  {'PASS' if pick.keep4b_oos else 'fail':>7s} "
                    f"{'PASS' if pick.keep4a_oos else 'fail':>7s}  "
                    f"{pick.oSharpe - bm['OOS']['Sharpe']:+8.4f} {pick.oSharpe - live['OOS']['Sharpe']:+8.4f}")
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE 8 TOTALS: 4b OOS {int(WF.keep4b_oos.sum())}/{len(WF)} picks, "
        f"4a OOS {int(WF.keep4a_oos.sum())}/{len(WF)}; the matched TWIN of the same picks clears "
        f"4b OOS {int(WF.tw_keep4b_oos.sum())}/{len(WF)}.")
    real = WF[WF.chooser != "C_MEMO"]
    say(f"  EXCLUDING the no-choice control C_MEMO: 4b OOS {int(real.keep4b_oos.sum())}/{len(real)}, "
        f"4a OOS {int(real.keep4a_oos.sum())}/{len(real)}.")

    # ---------------- verdict against the pre-stated rules
    say("\n" + "=" * 108)
    say("VERDICT AGAINST THE PRE-STATED RULES V1-V4")
    say("=" * 108)
    u56 = R[(R.panel == "U56") & (R.t == MEMO_T) & (R.cost == PRIMARY_COST)]
    b136 = R[(R.panel == "B136") & (R.t == MEMO_T) & (R.cost == PRIMARY_COST)]
    s_u, s_b = u56.keep4b_oos.mean(), b136.keep4b_oos.mean()
    v1 = s_u < 0.50
    v2 = (s_u >= 0.75) and (s_b >= 0.75)
    v3 = int(real.keep4b_oos.sum()) == 0
    v4 = bool(R[R.cost == PRIMARY_COST].tw_keep4b_oos.sum() >= R[R.cost == PRIMARY_COST].keep4b_oos.sum())
    say(f"  V1 convention pass-share, U56 @ t={MEMO_T}: {s_u:.3f} ({int(u56.keep4b_oos.sum())}/20) -> "
        f"{'TRIGGERED (minority -> PARK, not KEEP)' if v1 else 'not triggered'}")
    say(f"  V2 robust on BOTH panels (>=0.75): U56 {s_u:.3f}, B136 {s_b:.3f} -> "
        f"{'TRIGGERED (KEEP stands)' if v2 else 'not triggered'}")
    say(f"  V3 no IS-only chooser reaches a 4b-OOS cell: {int(real.keep4b_oos.sum())}/{len(real)} -> "
        f"{'TRIGGERED (KILL for capital)' if v3 else 'not triggered'}")
    say(f"  V4 twin clears 4b OOS at least as often as VOLTGT: "
        f"{int(R[R.cost==PRIMARY_COST].tw_keep4b_oos.sum())} vs {int(R[R.cost==PRIMARY_COST].keep4b_oos.sum())} -> "
        f"{'TRIGGERED (simpler book is the better candidate)' if v4 else 'not triggered'}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n  GATES {sum(g['pass_'] for g in GATES)}/{len(GATES)}  "
        f"({'ALL PASS' if ok else 'SOME FAILED'})   runtime {time.time()-t_start:.1f}s")
    say("  SURVIVORSHIP: U56 and B136 are CURRENT constituents; SMALL665 is a current sub-$2B screen "
        "(names with max_1d_move >= 1.0 dropped).  Every pass-count above is therefore the OPTIMISTIC read.")
    say("  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are UNTOUCHED by this run (rule 6).")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return R, WF


if __name__ == "__main__":
    main()
