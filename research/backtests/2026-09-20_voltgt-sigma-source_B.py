#!/usr/bin/env python3
"""Idea 1763 (lane B, 2026-09-20): DOES A SPY-SOURCED VOL TARGET REPRODUCE THE VOLTGT016
CANDIDATE WITHOUT INHERITING THE PANEL?

THE DEFECT THIS CLOSES
----------------------
The record's standing vol-target candidate (`2026-09-20_voltgt-panel_KEEP4b_MEMO.md`, idea 1730,
now PARK after idea 1771) scales the book by `g_t = clip(target / sigma_t, 0, 1)` where `sigma_t`
is the realised vol of *the panel's own* unlevered equal-weight portfolio.  Its own memo, point 8,
names the consequence: the target is calibrated on a SURVIVORSHIP-SELECTED panel, so the book
inherits that panel; addendum A2 then found it does not exist on small caps (0 of 96 books clear
4b on SMALL).

A target set on SPY's realised vol does not inherit anything.  It is one public series, identical
for every panel, implementable by anyone, and it removes the circularity of sizing a book by the
volatility of the very names the book selected.  If the SPY-sourced cut reproduces the candidate,
the panel-inheritance caveat is not load-bearing and the RULES wording gets strictly simpler.  If
it does not, the record learns that the candidate's exposure path is a PANEL object and the
caveat is the finding.

THE CONSTRUCTION
----------------
TUNED (2, the protocol maximum; ALL grid points reported):
    target vol   t     {0.08, 0.10, 0.12, 0.16, 0.20}   (the memo's 0.08/0.12/0.16 + 2 rungs)
    sigma SOURCE src   {PANEL, SPY, BLEND}              PANEL = the memo's own construction
                                                        SPY   = sigma of SPY's own daily returns
                                                        BLEND = 0.5 * PANEL + 0.5 * SPY
PUBLISHED, NOT TUNED:
    convention (L, d)  {(20,0) = the memo's cell, (20,1), (10,0), (40,0)}   -- idea 1771's axis,
                       carried as a SENSITIVITY so the answer is not read at one cell only
    panel              {U56, B136, SMALL665}
    cost               {0, 10, 25, 50} bps    (exact: held / turnover do not depend on cost)
CONTROL (not a dial): every book is paired with its OWN realised-mean-gross-matched CONSTANT-GROSS
    twin, solved on the same window.  The twin is what "just buy less of it" looks like; a
    sigma source has to beat that, not cash.
    -> 3 panels x 3 sources x 5 targets x 4 conventions = 180 books, each with a FULL-matched and
       an OOS-matched twin, scored at 4 cost rungs = 720 scored rows.

Execution realism throughout: weights decided at close t, applied t+1 (the engine's shift), weekly
cadence, 10 bps primary cost rung, gross capped at 1.00 (never levered).

PRE-STATED VERDICT RULES (fixed before the run; no tuning-until-it-works)
------------------------------------------------------------------------
V1  REPRODUCTION.  At the memo's own cell (L=20, d=0, t=0.16) on U56 and B136, does src=SPY carry
    the SAME 4b FULL and 4b OOS verdicts as src=PANEL?  If yes, the panel inheritance is not
    load-bearing for the candidate's pass and the simpler wording is available.
V2  PORTABILITY.  src=PANEL clears 4b 0 of 96 times on SMALL (memo addendum A2).  If src=SPY
    clears 4b FULL *and* OOS on SMALL665 at ANY tested rung, the panel inheritance WAS the binding
    defect.  If it clears 0 of N, the SMALL failure is a PANEL-RETURN fact, not a sigma-source
    fact, and this idea's premise is KILLED on its own terms.
V3  RULE 8 IS DECISIVE FOR CAPITAL.  (t, src) chosen on 2009-2016 ONLY; 2017-2026 read ONCE.  If
    no legal IS-only chooser reaches a 4b-OOS-passing cell, nothing here is capital-worthy
    whatever the pass-shares say -- the passing cells are hindsight.
V4  THE TWIN IS THE COMPARAND.  If the matched constant-gross twin clears 4b at least as often as
    the vol-target book, the sigma source is a parameter that buys nothing.
V5  CONVENTION ROBUSTNESS.  Idea 1771 showed the candidate's U56 pass is a property of the cell
    (L=20, d=0): pass-share 0.250 over its 20 convention cells.  Report the same pass-share per
    SOURCE over this run's 4 conventions.  A source is only "more robust" if its pass-share is
    HIGHER than PANEL's on the same panels and rungs.

Run: python research/backtests/2026-09-20_voltgt-sigma-source_B.py
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

DATE, SLUG = "2026-09-20", "voltgt-sigma-source"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, CAD = 260, "W"
GRID_T = [0.08, 0.10, 0.12, 0.16, 0.20]
GRID_SRC = ["PANEL", "SPY", "BLEND"]
GRID_CONV = [(20, 0), (20, 1), (10, 0), (40, 0)]        # (lookback L, staleness d)
COSTS = [0.0, 10.0, 25.0, 50.0]
PRIMARY_COST = 10.0
MEMO_L, MEMO_D, MEMO_T, MEMO_SRC = 20, 0, 0.16, "PANEL"
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
    return b are computed ONCE per panel and shared by every book on it."""
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
    return dict(R=R, E=E, mask=mask, B=B, Upre=Upre, T=T, idx=px.index)


def gross_path(st, gvec):
    """Scalar-only recursion for the realised gross path (used by the twin solve)."""
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
def sigma_series(px, src, L, d):
    """The realised annualised vol the target is divided by, per SOURCE.

    PANEL : vol of the unlevered equal-weight panel return  (the memo's construction, verbatim)
    SPY   : vol of SPY's own daily return                   (panel-independent, public series)
    BLEND : 0.5 * PANEL + 0.5 * SPY
    """
    base = ew_unit(px)
    pr = (base.shift(1) * px.pct_change()).sum(axis=1)          # unlevered EW panel return
    rv_panel = pr.rolling(L).std() * np.sqrt(252)
    rv_spy = px["SPY"].pct_change().rolling(L).std() * np.sqrt(252)
    rv = {"PANEL": rv_panel, "SPY": rv_spy,
          "BLEND": 0.5 * rv_panel + 0.5 * rv_spy}[src]
    return rv.shift(d) if d else rv


def voltgt_gvec(px, t, src, L, d):
    """g_t = clip(t / sigma_t, 0, 1), decided at t and applied at t+1 (the engine's shift)."""
    rv = sigma_series(px, src, L, d)
    k = (t / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return k.shift(1).fillna(0.0).values


def const_gvec(st, k):
    return np.full(st["T"], float(k))


def solve_twin(st, target_mean_gross, sl):
    """Constant gross k whose REALISED mean gross over slice sl matches the book's, to machine
    precision.  mean gross is monotone in k, so plain bisection on [0, 1] (no leverage)."""
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
    say("=" * 110)
    say("IDEA 1763 (lane B, 2026-09-20) — DOES A SPY-SOURCED VOL TARGET REPRODUCE THE VOLTGT016")
    say("CANDIDATE WITHOUT INHERITING THE PANEL?")
    say("=" * 110)
    say(__doc__.split("Run:")[0].strip())
    say("=" * 110)

    panels = {}
    for nm, kw in (("U56", {}), ("B136", dict(broad=True))):
        panels[nm] = load_universe(**kw)
    panels["SMALL665"] = small_panel()
    for nm, px in panels.items():
        say(f"  panel {nm:9s} {px.shape[1]:4d} cols x {len(px):5d} days  "
            f"{px.index[0].date()} -> {px.index[-1].date()}")

    # ---- G5: the SPY-sourced scalar is literally panel-independent (that is the whole claim)
    say("\n  PANEL-INDEPENDENCE OF THE SPY-SOURCED SCALAR (gate G5)")
    ref = pd.Series(voltgt_gvec(panels["U56"], MEMO_T, "SPY", MEMO_L, MEMO_D), index=panels["U56"].index)
    worst_src = 0.0

    def post_warmup(a, b):
        """Common trading days at or after BOTH panels' warm-up day (each panel's own index[260]).
        Before that one panel's rolling window is still empty, which is a warm-up fact, not a
        panel-dependence fact."""
        c = a.index.intersection(b.index)
        t0 = max(a.index[WARMUP], b.index[WARMUP])
        return c[c >= t0]

    dev = {}
    for nm in ("B136", "SMALL665"):
        g = pd.Series(voltgt_gvec(panels[nm], MEMO_T, "SPY", MEMO_L, MEMO_D), index=panels[nm].index)
        common = post_warmup(panels["U56"], panels[nm])
        dmax = float((ref.loc[common] - g.loc[common]).abs().max())
        dev[nm] = dmax
        worst_src = max(worst_src, dmax)
        say(f"    U56 vs {nm:9s}: {len(common)} common post-warm-up days "
            f"({common[0].date()}..{common[-1].date()}), max|d g_t| {dmax:.3e}")
    # SMALL665 draws its SPY benchmark column from data/prices.csv, the same file U56 does, so the
    # scalar must agree to machine precision.  B136 draws SPY from data/prices_broad.csv, a SECOND
    # committed cache whose SPY column is NOT byte-identical to prices.csv's -- so its residual is a
    # CACHE fact, not a panel-dependence fact, and G5b proves that by re-sourcing it.
    gate("G5a SPY-sourced g_t identical U56 vs SMALL665 (same SPY cache)", f"{dev['SMALL665']:.3e}",
         "== 0 (<= 1e-12)", dev["SMALL665"] <= 1e-12)
    dspy = float((panels["U56"]["SPY"] - panels["B136"]["SPY"]).abs().max())
    dspyr = float((panels["U56"]["SPY"].pct_change() - panels["B136"]["SPY"].pct_change()).abs().max())
    bx = panels["B136"].drop(columns=["SPY"]).join(panels["U56"]["SPY"])[panels["B136"].columns]
    g_rs = pd.Series(voltgt_gvec(bx, MEMO_T, "SPY", MEMO_L, MEMO_D), index=bx.index)
    common = post_warmup(panels["U56"], bx)
    d_rs = float((ref.loc[common] - g_rs.loc[common]).abs().max())
    say(f"    U56 vs B136 re-sourced onto data/prices.csv's SPY: max|d g_t| {d_rs:.3e}")
    publish("committed caches' own SPY disagreement (prices.csv vs prices_broad.csv)",
            f"max|d price| ${dspy:.4f}, max|d daily return| {dspyr:.3e}  -> the U56-vs-B136 "
            f"g_t residual of {dev['B136']:.3e} is a CACHE artefact")
    gate("G5b U56-vs-B136 SPY-sourced g_t residual is a CACHE artefact (re-source and it vanishes)",
         f"{d_rs:.3e} (was {dev['B136']:.3e})", "== 0 (<= 1e-12)", d_rs <= 1e-12)
    # and the corresponding PANEL-sourced dispersion, for contrast (published, not a gate)
    refp = pd.Series(voltgt_gvec(panels["U56"], MEMO_T, "PANEL", MEMO_L, MEMO_D), index=panels["U56"].index)
    for nm in ("B136", "SMALL665"):
        g = pd.Series(voltgt_gvec(panels[nm], MEMO_T, "PANEL", MEMO_L, MEMO_D), index=panels[nm].index)
        common = post_warmup(panels["U56"], panels[nm])
        publish(f"PANEL-sourced g_t dispersion U56 vs {nm} (same post-warm-up days)",
                f"max|d| {float((refp.loc[common]-g.loc[common]).abs().max()):.4f}, "
                f"mean|d| {float((refp.loc[common]-g.loc[common]).abs().mean()):.4f}")

    rows, wf_rows = [], []
    for pname, px in panels.items():
        say("\n" + "-" * 110)
        say(f"PANEL {pname}")
        say("-" * 110)
        st = panel_state(px)
        i0 = WARMUP
        ioos = int(px.index.searchsorted(pd.Timestamp(OOS_START)))
        iis_end = int(px.index.searchsorted(pd.Timestamp(IS_END), side="right"))
        sl_full, sl_oos, sl_is = slice(i0, None), slice(ioos, None), slice(i0, iis_end)

        spy = px["SPY"].pct_change().fillna(0.0).values
        bm = dict(FULL=pack(spy[sl_full]), OOS=pack(spy[sl_oos]), IS=pack(spy[sl_is]))
        lv = backtest(px, rules_v2_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        v1r = backtest(px, rules_v1_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        live = dict(FULL=pack(lv[sl_full]), OOS=pack(lv[sl_oos]), IS=pack(lv[sl_is]))
        say(f"  SPY   FULL {bm['FULL']['CAGR']:7.2%} / {bm['FULL']['Sharpe']:.4f} / {bm['FULL']['MaxDD']:7.2%}"
            f"   OOS {bm['OOS']['CAGR']:7.2%} / {bm['OOS']['Sharpe']:.4f} / {bm['OOS']['MaxDD']:7.2%}")
        say(f"  LIVE  FULL {live['FULL']['CAGR']:7.2%} / {live['FULL']['Sharpe']:.4f} / {live['FULL']['MaxDD']:7.2%}"
            f"   OOS {live['OOS']['CAGR']:7.2%} / {live['OOS']['Sharpe']:.4f} / {live['OOS']['MaxDD']:7.2%}")
        say(f"  v1    FULL {pack(v1r[sl_full])['CAGR']:7.2%} / {pack(v1r[sl_full])['Sharpe']:.4f} / "
            f"{pack(v1r[sl_full])['MaxDD']:7.2%}")
        say(f"  4b bars FULL: H1>{bm['FULL']['H1']:.4f} H2>{bm['FULL']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['FULL']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['FULL']['CAGR']:.2%}")
        say(f"  4b bars OOS : H1>{bm['OOS']['H1']:.4f} H2>{bm['OOS']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['OOS']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['OOS']['CAGR']:.2%}")

        # how correlated are the two sigma series on this panel? (published; it is the mechanism)
        s_p = sigma_series(px, "PANEL", MEMO_L, MEMO_D)
        s_s = sigma_series(px, "SPY", MEMO_L, MEMO_D)
        ok = s_p.notna() & s_s.notna()
        publish(f"sigma corr(PANEL, SPY) [{pname}, L20 d0]",
                f"pearson {float(s_p[ok].corr(s_s[ok])):.4f}, "
                f"spearman {float(s_p[ok].rank().corr(s_s[ok].rank())):.4f}, "
                f"mean PANEL {float(s_p[ok].mean()):.4f} vs SPY {float(s_s[ok].mean()):.4f}, "
                f"ratio {float((s_p[ok]/s_s[ok]).mean()):.4f}")

        # ---- gate G1 (engine exactness) on this panel, at the memo cell
        gv = voltgt_gvec(px, MEMO_T, MEMO_SRC, MEMO_L, MEMO_D)
        gr, turn, gross = run(st, gv)
        W = ew_unit(px).mul(pd.Series(gv, index=px.index).shift(-1).fillna(0.0), axis=0)
        for c in (PRIMARY_COST, 25.0):
            refr = backtest(px, W, cost_bps=c, freq=CAD)["returns"].values[sl_full]
            dmax = float(np.abs(rets_at(gr, turn, c)[sl_full] - refr).max())
            gate(f"G1 fast_run == engine.backtest [{pname}, {c:.0f}bps]", f"{dmax:.3e}",
                 "== 0 (<= 1e-15)", dmax <= 1e-15)

        for src in GRID_SRC:
            for t in GRID_T:
                for (L, d) in GRID_CONV:
                    gv = voltgt_gvec(px, t, src, L, d)
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
                            panel=pname, src=src, t=t, L=L, d=d, cost=c,
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
                            twin_k=kf, twin_k_oos=ko,
                            twin_match_err=abs(ef), twin_match_err_oos=abs(eo),
                            twSharpe=tmF["Sharpe"], twMaxDD=tmF["MaxDD"], twCAGR=tmF["CAGR"],
                            twoSharpe=tmO["Sharpe"], twoMaxDD=tmO["MaxDD"], twoCAGR=tmO["CAGR"],
                            tw_keep4a=t4aF, tw_keep4b=t4bF,
                            tw_keep4a_oos=t4aO, tw_keep4b_oos=t4bO,
                            dSharpe=mF["Sharpe"] - tmF["Sharpe"], dMaxDD=mF["MaxDD"] - tmF["MaxDD"],
                            odSharpe=mO["Sharpe"] - tmO["Sharpe"], odMaxDD=mO["MaxDD"] - tmO["MaxDD"],
                        ))
            say(f"  src={src:6s} done  ({time.time()-t_start:6.1f}s)")

    R = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    R.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"\n  {len(R)} scored rows -> {Path(str(OUT)+'.grid.csv').name}")
    gate("G4 twin realised-mean-gross match (max abs err over all cells)",
         f"{R.twin_match_err.max():.3e} / {R.twin_match_err_oos.max():.3e}", "< 1e-10",
         max(R.twin_match_err.max(), R.twin_match_err_oos.max()) < 1e-10)
    nan_n = int(R[["Sharpe", "oSharpe", "MaxDD", "oMaxDD"]].isna().sum().sum())
    gate("G6 no NaN in scored metrics", nan_n, "== 0", nan_n == 0)

    # ---------------- G2/G3/G7: replicate the standing memo, its addendum A1 and A2
    say("\n" + "=" * 110)
    say("REPLICATION OF THE STANDING CANDIDATE (idea 1730 memo, idea 1715 addenda A1 and A2)")
    say("=" * 110)
    P = lambda pn, src, t, L, d, c=PRIMARY_COST: R[(R.panel == pn) & (R.src == src) & (R.t == t) &
                                                   (R.L == L) & (R.d == d) & (R.cost == c)].iloc[0]
    memo = {("U56", "FULL"): (0.1561, 1.2027, -0.1986), ("U56", "OOS"): (0.1594, 1.2193, -0.1986),
            ("B136", "FULL"): (0.1594, 1.2049, -0.1876), ("B136", "OOS"): (0.1536, 1.1837, -0.1876)}
    worst = 0.0
    for (pn, win), (mc, ms, md) in memo.items():
        r = P(pn, MEMO_SRC, MEMO_T, MEMO_L, MEMO_D)
        got = (r.CAGR, r.Sharpe, r.MaxDD) if win == "FULL" else (r.oCAGR, r.oSharpe, r.oMaxDD)
        dmax = max(abs(got[0] - mc), abs(got[1] - ms), abs(got[2] - md))
        worst = max(worst, dmax)
        say(f"  {pn:5s} {win:4s} memo {mc:7.2%} / {ms:.4f} / {md:7.2%}   "
            f"this run {got[0]:7.2%} / {got[1]:.4f} / {got[2]:7.2%}   max|d| {dmax:.2e}")
    gate("G2 memo replication (idea 1730, 12 published numbers)", f"{worst:.2e}", "<= 5e-4",
         worst <= 5e-4)
    a1 = P("U56", MEMO_SRC, MEMO_T, MEMO_L, 1)
    say(f"  A1 (idea 1715): U56 PANEL t=0.16 L=20 d=1 OOS MaxDD {a1.oMaxDD:.2%} "
        f"(addendum published -20.77%), 4b OOS {'PASS' if a1.keep4b_oos else 'FAIL'}")
    gate("G3 addendum A1 replication (d=1 flips U56 4b OOS to FAIL)",
         f"{a1.oMaxDD:.4%} / 4b OOS {'PASS' if a1.keep4b_oos else 'FAIL'}",
         "-20.77% and FAIL", abs(a1.oMaxDD - (-0.2077)) <= 5e-4 and not bool(a1.keep4b_oos))
    sm_panel = R[(R.panel == "SMALL665") & (R.src == "PANEL") & (R.cost == PRIMARY_COST)]
    n_sm = int((sm_panel.keep4b | sm_panel.keep4b_oos).sum())
    gate("G7 addendum A2 replication (PANEL-sourced clears 4b 0 times on SMALL665)",
         f"{n_sm}/{len(sm_panel)}", "== 0", n_sm == 0)

    # ---------------- the source surface
    say("\n" + "=" * 110)
    say(f"THE SIGMA-SOURCE SURFACE AT THE MEMO'S CONVENTION (L=20, d=0) AND {PRIMARY_COST:.0f} bps")
    say("(FULL and OOS 2017-2026: CAGR / Sharpe / MaxDD, 4b verdict.  * = the memo's own cell)")
    say("=" * 110)
    for pn in panels:
        say(f"\n  {pn}")
        say(f"    {'src':6s} {'t':>5s} | {'FULL CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1/H2':>13s} "
            f"{'4b':>4s} {'4a':>4s} | {'OOS CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'4b':>4s} {'4a':>4s} "
            f"| {'gross':>6s} {'turn':>5s}")
        for src in GRID_SRC:
            for t in GRID_T:
                r = P(pn, src, t, MEMO_L, MEMO_D)
                star = "*" if (src == MEMO_SRC and t == MEMO_T) else " "
                say(f"    {src:6s} {t:5.2f}{star}| {r.CAGR:9.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} "
                    f"{r.H1:6.3f}/{r.H2:6.3f} {'Y' if r.keep4b else 'n':>4s} {'Y' if r.keep4a else 'n':>4s} "
                    f"| {r.oCAGR:8.2%} {r.oSharpe:7.4f} {r.oMaxDD:8.2%} "
                    f"{'Y' if r.keep4b_oos else 'n':>4s} {'Y' if r.keep4a_oos else 'n':>4s} "
                    f"| {r.mean_gross:6.3f} {r.turnover:5.2f}")

    say("\n" + "=" * 110)
    say("PASS-SHARE BY SOURCE — over the 4 published conventions (L,d) at each (panel, t), 10 bps")
    say("=" * 110)
    say(f"  {'panel':9s} {'src':6s} {'t':>5s} {'n':>3s} {'4b FULL':>8s} {'4b OOS':>8s} {'4b BOTH':>8s} "
        f"{'4a FULL':>8s} {'4a OOS':>8s} | {'TWIN 4b F':>10s} {'TWIN 4b O':>10s}")
    share = []
    for pn in panels:
        for src in GRID_SRC:
            for t in GRID_T:
                S = R[(R.panel == pn) & (R.src == src) & (R.t == t) & (R.cost == PRIMARY_COST)]
                rec = dict(panel=pn, src=src, t=t, n=len(S),
                           b4F=S.keep4b.mean(), b4O=S.keep4b_oos.mean(),
                           b4B=(S.keep4b & S.keep4b_oos).mean(),
                           a4F=S.keep4a.mean(), a4O=S.keep4a_oos.mean(),
                           tw4F=S.tw_keep4b.mean(), tw4O=S.tw_keep4b_oos.mean())
                share.append(rec)
                say(f"  {pn:9s} {src:6s} {t:5.2f} {rec['n']:3d} {rec['b4F']:8.3f} {rec['b4O']:8.3f} "
                    f"{rec['b4B']:8.3f} {rec['a4F']:8.3f} {rec['a4O']:8.3f} | "
                    f"{rec['tw4F']:10.3f} {rec['tw4O']:10.3f}")
    pd.DataFrame(share).to_csv(f"{OUT}.pass_share.csv", index=False)

    say("\n  SOURCE TOTALS (all panels x targets x conventions, 10 bps):")
    say(f"    {'src':6s} {'n':>4s} {'4b FULL':>8s} {'4b OOS':>8s} {'4b BOTH':>8s} {'4a OOS':>8s} "
        f"{'mean gross':>11s} {'mean turn':>10s}")
    for src in GRID_SRC:
        S = R[(R.src == src) & (R.cost == PRIMARY_COST)]
        say(f"    {src:6s} {len(S):4d} {S.keep4b.mean():8.3f} {S.keep4b_oos.mean():8.3f} "
            f"{(S.keep4b & S.keep4b_oos).mean():8.3f} {S.keep4a_oos.mean():8.3f} "
            f"{S.mean_gross.mean():11.3f} {S.turnover.mean():10.2f}")
    say("\n  U56 + B136 ONLY (the panels the candidate lives on):")
    for src in GRID_SRC:
        S = R[(R.src == src) & (R.cost == PRIMARY_COST) & (R.panel != "SMALL665")]
        say(f"    {src:6s} {len(S):4d} {S.keep4b.mean():8.3f} {S.keep4b_oos.mean():8.3f} "
            f"{(S.keep4b & S.keep4b_oos).mean():8.3f} {S.keep4a_oos.mean():8.3f}")

    say("\n  WHICH 4b LEG FAILS, per panel x source (all t x conventions, 10 bps):")
    for pn in panels:
        for src in GRID_SRC:
            S = R[(R.panel == pn) & (R.src == src) & (R.cost == PRIMARY_COST)]
            fF = {k: float((~S[f"F_{k}"]).mean()) for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR")}
            fO = {k: float((~S[f"O_{k}"]).mean()) for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR")}
            say(f"    {pn:9s} {src:6s} FULL " + " ".join(f"{k} {v:.3f}" for k, v in fF.items())
                + "   OOS " + " ".join(f"{k} {v:.3f}" for k, v in fO.items()))

    say("\n  COST LADDER (4b OOS pass count over the 20 t x convention cells, per panel x source):")
    for pn in panels:
        for src in GRID_SRC:
            say(f"    {pn:9s} {src:6s} " + "  ".join(
                f"{c:.0f}bps {int(R[(R.panel==pn)&(R.src==src)&(R.cost==c)].keep4b_oos.sum()):2d}/20"
                for c in COSTS))

    # ---------------- the matched twin control
    say("\n" + "=" * 110)
    say("CONTROL — EACH BOOK vs ITS OWN REALISED-MEAN-GROSS-MATCHED CONSTANT-GROSS TWIN (10 bps)")
    say("=" * 110)
    say(f"  {'panel':9s} {'src':6s} {'dSharpe':>9s} {'dMaxDD':>9s} {'win':>6s} | {'OOS dSharpe':>12s} "
        f"{'OOS dMaxDD':>11s} {'OOS win':>8s} | {'4b OOS book':>12s} {'twin':>5s}")
    twin_rows = []
    for pn in panels:
        for src in GRID_SRC:
            S = R[(R.panel == pn) & (R.src == src) & (R.cost == PRIMARY_COST)]
            rec = dict(panel=pn, src=src, dSharpe=S.dSharpe.mean(), dMaxDD=S.dMaxDD.mean() * 100,
                       win=(S.dSharpe > 0).mean(), odSharpe=S.odSharpe.mean(),
                       odMaxDD=S.odMaxDD.mean() * 100, owin=(S.odSharpe > 0).mean(),
                       v4b=int(S.keep4b_oos.sum()), t4b=int(S.tw_keep4b_oos.sum()), n=len(S))
            twin_rows.append(rec)
            say(f"  {pn:9s} {src:6s} {rec['dSharpe']:9.4f} {rec['dMaxDD']:8.2f}pp {rec['win']:6.3f} | "
                f"{rec['odSharpe']:12.4f} {rec['odMaxDD']:10.2f}pp {rec['owin']:8.3f} | "
                f"{rec['v4b']:8d}/{rec['n']:d} {rec['t4b']:5d}")
    pd.DataFrame(twin_rows).to_csv(f"{OUT}.twin.csv", index=False)

    # ---------------- rule 8
    say("\n" + "=" * 110)
    say(f"RULE 8 — (t, src) CHOSEN ON 2009..{IS_END} ONLY; {OOS_START}..2026 READ ONCE")
    say("=" * 110)
    say("  Choosers, all IS-only and all legal (they see nothing after 2016-12-31):")
    say("    C_ISSHARPE  argmax IS Sharpe")
    say("    C_ISLEGS    max IS 4b-leg count, tie-break on IS Sharpe")
    say("    C_ISDD      argmin IS MaxDD (the leg the candidate's margin sits on)")
    say("    C_MEMO      the memo's own cell (src=PANEL, t=0.16), i.e. no choice at all — control")
    say("  Arms: FIXEDCONV chooses (t, src) at the memo convention (L=20, d=0);")
    say("        FREECONV  chooses (t, src, L, d) jointly — the honest 4-dial read;")
    say("        SRC=<x>   chooses t ONLY inside one source, at the memo convention.")
    say("")
    say(f"  {'panel':9s} {'arm':10s} {'chooser':11s} {'pick':22s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
        f"{'OOS MaxDD':>10s}  {'4b OOS':>7s} {'4a OOS':>7s}  {'vs SPY':>8s} {'vs LIVE':>8s}")

    def choose(sub, cname):
        if cname == "C_ISSHARPE":
            return sub.sort_values(["isSharpe"], ascending=False).iloc[0]
        if cname == "C_ISLEGS":
            return sub.sort_values(["is_legs", "isSharpe"], ascending=False).iloc[0]
        if cname == "C_ISDD":
            return sub.sort_values(["isMaxDD"], ascending=False).iloc[0]
        pk = sub[(sub.src == MEMO_SRC) & (sub.t == MEMO_T)]
        return pk.sort_values(["isSharpe"], ascending=False).iloc[0]

    for pn in panels:
        Sc = R[(R.panel == pn) & (R.cost == PRIMARY_COST)]
        conv0 = Sc[(Sc.L == MEMO_L) & (Sc.d == MEMO_D)]
        spy_o = dict(Sharpe=np.nan)
        arms = [("FIXEDCONV", conv0), ("FREECONV", Sc)]
        arms += [(f"SRC={s}", conv0[conv0.src == s]) for s in GRID_SRC]
        for arm, sub in arms:
            cnames = ("C_ISSHARPE", "C_ISLEGS", "C_ISDD", "C_MEMO") if arm in ("FIXEDCONV", "FREECONV") \
                else ("C_ISSHARPE", "C_ISDD")
            for cname in cnames:
                pick = choose(sub, cname)
                wf_rows.append(dict(panel=pn, arm=arm, chooser=cname, src=pick.src, t=pick.t,
                                    L=pick.L, d=pick.d, isSharpe=pick.isSharpe,
                                    oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                                    keep4b_oos=bool(pick.keep4b_oos),
                                    keep4a_oos=bool(pick.keep4a_oos),
                                    twoSharpe=pick.twoSharpe, twoMaxDD=pick.twoMaxDD,
                                    tw_keep4b_oos=bool(pick.tw_keep4b_oos)))
                lbl = f"{pick.src} t{pick.t:.2f} L{int(pick.L)} d{int(pick.d)}"
                bmo = pack(panels[pn]["SPY"].pct_change().fillna(0.0).values[
                    int(panels[pn].index.searchsorted(pd.Timestamp(OOS_START))):])
                lvo = pack(backtest(panels[pn], rules_v2_weights(panels[pn]), cost_bps=PRIMARY_COST,
                                    freq=CAD)["returns"].values[
                    int(panels[pn].index.searchsorted(pd.Timestamp(OOS_START))):])
                say(f"  {pn:9s} {arm:10s} {cname:11s} {lbl:22s} {pick.oCAGR:9.2%} {pick.oSharpe:11.4f} "
                    f"{pick.oMaxDD:10.2%}  {'PASS' if pick.keep4b_oos else 'fail':>7s} "
                    f"{'PASS' if pick.keep4a_oos else 'fail':>7s}  "
                    f"{pick.oSharpe - bmo['Sharpe']:+8.4f} {pick.oSharpe - lvo['Sharpe']:+8.4f}")
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE 8 TOTALS: 4b OOS {int(WF.keep4b_oos.sum())}/{len(WF)} picks, "
        f"4a OOS {int(WF.keep4a_oos.sum())}/{len(WF)}; the matched TWIN of the same picks clears "
        f"4b OOS {int(WF.tw_keep4b_oos.sum())}/{len(WF)}.")
    real = WF[WF.chooser != "C_MEMO"]
    say(f"  EXCLUDING the no-choice control C_MEMO: 4b OOS {int(real.keep4b_oos.sum())}/{len(real)}, "
        f"4a OOS {int(real.keep4a_oos.sum())}/{len(real)}.")
    say("  Which SOURCE does a free chooser buy? " + ", ".join(
        f"{s} {int((WF[WF.arm.isin(['FIXEDCONV','FREECONV']) & (WF.chooser!='C_MEMO')].src == s).sum())}"
        for s in GRID_SRC))

    # ---------------- verdict against the pre-stated rules
    say("\n" + "=" * 110)
    say("VERDICT AGAINST THE PRE-STATED RULES V1-V5")
    say("=" * 110)
    v1_tbl = []
    for pn in ("U56", "B136"):
        rp = P(pn, "PANEL", MEMO_T, MEMO_L, MEMO_D); rs = P(pn, "SPY", MEMO_T, MEMO_L, MEMO_D)
        same = (bool(rp.keep4b) == bool(rs.keep4b)) and (bool(rp.keep4b_oos) == bool(rs.keep4b_oos))
        v1_tbl.append(same)
        say(f"  V1 {pn:5s} @ t=0.16 L20 d0:  PANEL 4b FULL {'Y' if rp.keep4b else 'n'} OOS "
            f"{'Y' if rp.keep4b_oos else 'n'} ({rp.oCAGR:.2%}/{rp.oSharpe:.4f}/{rp.oMaxDD:.2%})   "
            f"SPY 4b FULL {'Y' if rs.keep4b else 'n'} OOS {'Y' if rs.keep4b_oos else 'n'} "
            f"({rs.oCAGR:.2%}/{rs.oSharpe:.4f}/{rs.oMaxDD:.2%})  -> "
            f"{'REPRODUCES' if same else 'DOES NOT REPRODUCE'}")
    v1 = all(v1_tbl)
    sm = R[(R.panel == "SMALL665") & (R.src != "PANEL") & (R.cost == PRIMARY_COST)]
    sm_both = int((sm.keep4b & sm.keep4b_oos).sum())
    v2 = sm_both > 0
    say(f"  V2 SMALL665 with a non-PANEL sigma source: 4b FULL and OOS together "
        f"{sm_both}/{len(sm)} -> {'TRIGGERED (the panel inheritance WAS the defect)' if v2 else 'NOT triggered (SMALL failure is a PANEL-RETURN fact; premise KILLED)'}")
    v3 = int(real.keep4b_oos.sum()) == 0
    say(f"  V3 no legal IS-only chooser reaches a 4b-OOS cell: {int(real.keep4b_oos.sum())}/{len(real)} -> "
        f"{'TRIGGERED (nothing here is capital-worthy)' if v3 else 'not triggered'}")
    Rp = R[R.cost == PRIMARY_COST]
    v4 = bool(Rp.tw_keep4b_oos.sum() >= Rp.keep4b_oos.sum())
    say(f"  V4 twin clears 4b OOS at least as often as the book: {int(Rp.tw_keep4b_oos.sum())} vs "
        f"{int(Rp.keep4b_oos.sum())} -> "
        f"{'TRIGGERED (the sigma source buys nothing)' if v4 else 'not triggered'}")
    sh = {s: float(Rp[(Rp.src == s) & (Rp.panel != 'SMALL665')].keep4b_oos.mean()) for s in GRID_SRC}
    v5 = sh["SPY"] > sh["PANEL"]
    say(f"  V5 convention+rung pass-share on U56+B136, 4b OOS: " +
        ", ".join(f"{s} {sh[s]:.3f}" for s in GRID_SRC) +
        f" -> SPY {'MORE' if v5 else 'NOT more'} robust than PANEL")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n  GATES {sum(g['pass_'] for g in GATES)}/{len(GATES)}  "
        f"({'ALL PASS' if ok else 'SOME FAILED'})   runtime {time.time()-t_start:.1f}s")
    say("  SURVIVORSHIP: U56 and B136 are CURRENT constituents; SMALL665 is a current sub-$2B "
        "screen (names with max_1d_move >= 1.0 dropped).  Every pass-count above is the OPTIMISTIC read.")
    say("  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are UNTOUCHED by this run (rule 6).")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return R, WF


if __name__ == "__main__":
    main()
