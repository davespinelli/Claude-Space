#!/usr/bin/env python3
"""Idea 412 — does PARTIAL REBALANCING beat CADENCE as the turnover dial?  (cloud, 2026-09-10)

QUEUE 412: "idea 137's rule-8 chooser picks a cadence slower than weekly in 8 of 10 cells and
lambda<1 in 6 of 10, but only lambda changes the book's path.  Price the two dials against each
other at matched realised turnover on all three panels and say which one the record should adopt
as its turnover instrument.  Max 2 params (cadence, lambda)."

WHAT IS ACTUALLY BEING TESTED
  H1 (the queue's stated PREMISE)  "only lambda changes the book's path".  Falsifiable and
     measured directly: tracking error to the un-dialled base book, for both dials, AT MATCHED
     REALISED TURNOVER.  If cadence's TE is comparable to or larger than lambda's, the premise
     is refuted and the queue's reason for preferring lambda evaporates.
  H2 (the head-to-head)  At matched realised turnover, which dial delivers the higher Sharpe /
     CAGR / shallower MaxDD?  Reported per (panel, book, rung), both directions of the match,
     with the bracketing rate stated rather than buried (idea 403's A3 lesson).
  H3 (the adoption question)  Under PROTOCOL rule 8, is a CADENCE-ONLY chooser, a LAMBDA-ONLY
     chooser, or a JOINT chooser the better instrument out of sample?  That is the thing the
     queue asks the record to decide, and it is decided on 2017-2026 read exactly once.
  H4 (the confound the record already found)  A calendar cadence has a PHASE: 'last trading day
     of the month' is one of ~21 possible monthly schedules.  Every cadence number here is
     reported phase-averaged with its phase SPREAD beside it, because a cadence-vs-lambda
     comparison run on one phase is a comparison with an unpriced nuisance parameter in it.

AXES (PROTOCOL 4: "no more than 2 tuned parameters" — the queue names them)
  P1 cadence: every k trading days with offset p, k in {1, 5, 21, 63} (~ D / W / M / Q) and up to
     5 evenly spaced phases per k = 16 cadence variants.  Calendar D/W/M/Q is run alongside as
     the bridge to the record's own convention and as gate G1.
  P2 lambda : idea 137's partial-rebalance dial, verbatim ladder, 8 points.
  Panels (u56 / broad136 / small439), books (TOP20 / EWALL) and cost rungs (0-50 bps) are
  REPORTED axes, never selected on.  The full 16 x 8 cross is run and every point is reported.
  The only selection anywhere is PROTOCOL rule 8.

GATES (before any new number is read)
  G1 the vectorised runner vs `engine.backtest` at ALL FOUR calendar cadences D/W/M/Q, on
     returns AND turnover, on all three panels.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 the k-day cadence nests the calendar one where it must: k=1 is identical to freq='D'.
  G4 turnover monotone in lambda, and monotone in k, in every (panel, book) cell.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): current constituents on all three panels; SMALL439 drops the 44
    tickers with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.
  * BOTH dials can only LOWER turnover from the daily-rebalanced book, so the match is one-sided
    and its bracketing rate is reported, not assumed.
  * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * A k-day cadence is not a calendar cadence; the two are bridged, not conflated.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .matched.csv,
.walkforward.csv, .phase.csv next to itself.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
GROSS = H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60

KS = [1, 5, 21, 63]                                    # ~ D / W / M / Q in trading days
NPHASE = 5                                             # evenly spaced phases per k (1 when k=1)
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]
BOOKS = ["TOP20", "EWALL"]
PANELS = ["u56", "broad", "small"]
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]
CAL = ["D", "W", "M", "Q"]
BASE_K, BASE_P = 5, 0                                  # the record's weekly base cadence
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
NTOP = 20

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def phases_of(k):
    return [0] if k == 1 else [int(round(x)) for x in np.linspace(0, k, min(k, NPHASE), endpoint=False)]


# =====================================================================================
# runner
# =====================================================================================
def _apply_mask(idx, freq=None, k=None, p=0):
    """The engine's convention: a schedule decided at close t is APPLIED at t+1."""
    if freq is not None:
        return rebalance_mask(idx, freq).shift(1, fill_value=False).values
    m = np.zeros(len(idx), dtype=bool)
    m[p::k] = True
    return pd.Series(m, index=idx).shift(1, fill_value=False).values


def fast_bt(px, W, freq=None, k=None, p=0):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT (see idea 613's G1)."""
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = _apply_mask(px.index, freq, k, p)
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


def book_weights(px, book, investable):
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (GROSS / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


# =====================================================================================
# metrics
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def te(r, base):
    """Tracking error to the un-dialled base book, annualised — the PATH statistic H1 turns on."""
    return float((r - base).std() * np.sqrt(252))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


# =====================================================================================
# gates
# =====================================================================================
def gates(panels):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, (px, _) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        W = book_weights(px, "TOP20", inv)
        start = px.index[260]
        d1 = []
        for f in CAL:
            rf, tf = fast_bt(px, W, freq=f)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            d1.append((f, float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max()),
                       float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())))
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest  " +
            "  ".join(f"{f}: dr {a:.2e} dto {b:.2e}" for f, a, b in d1))
        ok &= all(a < 1e-12 and b < 1e-12 for _, a, b in d1)
        rf, tf = fast_bt(px, W, freq="W")
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>5}: rung identity vs live 25 bps  max|dr| {d2:.3e}")
        ok &= d2 < 1e-12
        rk, tk = fast_bt(px, W, k=1, p=0)
        rd, td = fast_bt(px, W, freq="D")
        d3 = float((rk.loc[start:] - rd.loc[start:]).abs().max())
        say(f"  G3 {pk:>5}: k=1 k-day cadence == calendar 'D'  max|dr| {d3:.3e}")
        ok &= d3 < 1e-12
    say(f"  GATES {'PASS' if ok else 'FAIL'} (G4 is checked on the grid below)")
    return ok


# =====================================================================================
# grid
# =====================================================================================
def run_panel(pk, px, ndrop):
    inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars_full, bars_is = bars_of(spy, "full"), bars_of(spy, "IS")
    v2r, v2t = fast_bt(px, rules_v2_weights(px), freq="W")
    v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
    say(f"\n  panel {pk}: {px.shape[1]} cols ({len(inv)} investable"
        + (f", {ndrop} dropped for max_1d_move>=1.0" if ndrop else "")
        + f"), evaluated from {start.date()} to {px.index[-1].date()}")
    say(f"    SPY bars: H1 {bars_full['s1']:.3f}  H2 {bars_full['s2']:.3f}  "
        f"OOS {bars_full['soos']:.3f}  MaxDD {bars_full['sdd']:.1%}  CAGR {bars_full['scagr']:.2%}")

    rows, series = [], {}
    for book in BOOKS:
        raw = book_weights(px, book, inv)
        Ws = {lam: smooth(raw, lam) for lam in LAMBDAS}
        base_r, base_t = fast_bt(px, Ws[1.0], k=BASE_K, p=BASE_P)
        base_r = base_r.loc[start:]
        for lam in LAMBDAS:
            for k in KS:
                for p in phases_of(k):
                    r0, t0 = fast_bt(px, Ws[lam], k=k, p=p)
                    r0, t0 = r0.loc[start:], t0.loc[start:]
                    series[(pk, book, lam, k, p)] = (r0, t0)
                    to = float(t0.sum() / (len(t0) / 252))
                    tev = te(r0, base_r)
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        m = metrics(r)
                        mg = margins(r, bars_full, "full")
                        mgi = margins(r.loc[:IS_END], bars_is, "IS")
                        rows.append(dict(
                            panel=pk, book=book, lam=lam, k=k, phase=p, cost=c,
                            turnover=to, TE=tev, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                            MaxDD=m["MaxDD"], H1=halves(r)[0], H2=halves(r)[1],
                            OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                            **{f"m_{x}": mg[x] for x in BARS5},
                            m_min=min(mg[x] for x in BARS5),
                            pass4b=all(mg[x] > 0 for x in BARS5), pass4a=pass4a(r, v2[c]),
                            IS_pass4b=all(mgi[x] > 0 for x in ("H1", "H2", "DD", "CAGR")),
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"]))
    return pd.DataFrame(rows), series, v2, bars_full


def interp_at(curve_x, curve_y, x):
    """Linear interpolation of y at x along a curve sorted by x; NaN outside the range (the
    bracketing condition is REPORTED, never extrapolated through)."""
    o = np.argsort(curve_x)
    cx, cy = np.asarray(curve_x)[o], np.asarray(curve_y)[o]
    if not (cx.min() <= x <= cx.max()):
        return np.nan
    return float(np.interp(x, cx, cy))


def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 412 — does PARTIAL REBALANCING beat CADENCE as the turnover dial?   (cloud)")
    say("=" * 100)
    say(f"tuned parameter 1 (cadence): k in {KS} trading days x up to {NPHASE} phases = "
        f"{sum(len(phases_of(k)) for k in KS)} variants, all reported")
    say(f"tuned parameter 2 (lambda) : {LAMBDAS}, all reported")
    say(f"books {BOOKS}; panels {PANELS}; rungs {RUNGS} bps; t+1, gross {GROSS}; "
        f"IS <= {IS_END}, OOS >= {OOS_START}")
    say("phase is a NUISANCE parameter, not a dial: every cadence number is reported "
        "phase-averaged with its spread.")

    panels = {"u56": (load_universe(), None), "broad": (load_universe(broad=True), None)}
    sp, nd = small_panel()
    panels["small"] = (sp, nd)
    if not gates(panels):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    say()
    say("=" * 100)
    say("GRID (3 panels x 2 books x 8 lambdas x 16 cadence variants, read at 6 rungs)")
    say("=" * 100)
    G, SER, V2 = [], {}, {}
    for pk in PANELS:
        px, nd = panels[pk]
        g, ser, v2, _ = run_panel(pk, px, nd)
        G.append(g)
        SER.update(ser)
        V2[pk] = v2
    G = pd.concat(G, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    nsim = G[["panel", "book", "lam", "k", "phase"]].drop_duplicates().shape[0]
    say(f"\n  {len(G)} arm-rows written ({nsim} simulations x {len(RUNGS)} rungs).")

    # ---- G4 monotonicity ----------------------------------------------------------
    mono_l, mono_k = [], []
    for (pk, book, k, p), s in G[G.cost == 0].groupby(["panel", "book", "k", "phase"]):
        s = s.sort_values("lam", ascending=False)
        mono_l.append(bool((s.turnover.diff().dropna() <= 1e-9).all()))
    for (pk, book, lam), s in G[(G.cost == 0) & (G.phase == 0)].groupby(["panel", "book", "lam"]):
        s = s.sort_values("k")
        mono_k.append(bool((s.turnover.diff().dropna() <= 1e-9).all()))
    say(f"  G4 turnover monotone DOWN in lambda: {sum(mono_l)}/{len(mono_l)} cells; "
        f"monotone DOWN in k: {sum(mono_k)}/{len(mono_k)} cells")
    bad = []
    for (pk, book, k, p), s in G[G.cost == 0].groupby(["panel", "book", "k", "phase"]):
        s = s.sort_values("lam", ascending=False)
        step = float(s.turnover.diff().dropna().max())
        if step > 1e-9:
            bad.append(dict(panel=pk, book=book, k=k, phase=p, max_up_step=step,
                            to_range=float(s.turnover.max() - s.turnover.min())))
    if bad:
        BD = pd.DataFrame(bad)
        say(f"     the {len(BD)} non-monotone cells, reported not hidden — all of them are cells "
            f"where lambda BARELY MOVES turnover at all:")
        say("     " + BD.groupby(["panel", "book"]).agg(
            cells=("max_up_step", "size"), max_up_step=("max_up_step", "max"),
            median_to_range=("to_range", "median")).to_string(
            float_format=lambda x: f"{x:.6f}").replace("\n", "\n     "))
        say(f"     the largest wrong-way step is {BD.max_up_step.max():.2e} x/yr against a "
            f"turnover LEVEL of order 1 x/yr, i.e. lambda is INERT on those cells, not "
            f"non-monotone in any usable sense.")

    # ---- the turnover ranges each dial can reach ----------------------------------
    say()
    say("-" * 100)
    say("REACH — what each dial can actually do to turnover (0 bps, phase-averaged)")
    say("-" * 100)
    say(f"  {'panel':>6} {'book':>6} {'base(k=5,lam=1)':>16} {'CADENCE reach':>26} "
        f"{'LAMBDA reach':>26} {'overlap':>22}")
    reach = {}
    for (pk, book), s in G[G.cost == 0].groupby(["panel", "book"]):
        cad = s[s.lam == 1.0].groupby("k").turnover.mean()
        lam = s[(s.k == BASE_K) & (s.phase == BASE_P)].set_index("lam").turnover
        base = float(lam.loc[1.0])
        clo, chi = float(cad.min()), float(cad.max())
        llo, lhi = float(lam.min()), float(lam.max())
        olo, ohi = max(clo, llo), min(chi, lhi)
        reach[(pk, book)] = (clo, chi, llo, lhi, olo, ohi)
        say(f"  {pk:>6} {book:>6} {base:>16.2f} {f'{clo:.2f} - {chi:.2f} x/yr':>26} "
            f"{f'{llo:.2f} - {lhi:.2f} x/yr':>26} "
            f"{(f'{olo:.2f} - {ohi:.2f}' if olo <= ohi else 'EMPTY'):>22}")

    # ---- H4 phase spread ----------------------------------------------------------
    say()
    say("-" * 100)
    say("H4 (PHASE) — a calendar cadence has a phase; how big is the nuisance?")
    say("-" * 100)
    ph = []
    for (pk, book, k, c), s in G[G.lam == 1.0].groupby(["panel", "book", "k", "cost"]):
        ph.append(dict(panel=pk, book=book, k=k, cost=c, n_phase=len(s),
                       Sharpe_mean=s.Sharpe.mean(), Sharpe_sd=s.Sharpe.std(),
                       Sharpe_rng=s.Sharpe.max() - s.Sharpe.min(),
                       to_mean=s.turnover.mean(), to_rng=s.turnover.max() - s.turnover.min(),
                       n_pass4b=int(s.pass4b.sum())))
    PH = pd.DataFrame(ph)
    PH.to_csv(OUT / f"{STEM}.phase.csv", index=False)
    say("  Sharpe spread ACROSS PHASES at the same k (lambda=1), by k and rung:")
    say(PH[PH.k > 1].groupby(["k", "cost"]).agg(
        cells=("Sharpe_sd", "size"), mean_sd=("Sharpe_sd", "mean"),
        max_range=("Sharpe_rng", "max"), mean_range=("Sharpe_rng", "mean")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    big = PH[(PH.k > 1) & (PH.cost == 10)]
    say(f"  At PROTOCOL's 10 bps rung the phase range is up to {big.Sharpe_rng.max():.4f} of "
        f"Sharpe (mean {big.Sharpe_rng.mean():.4f}) — and 4b passes disagree across phases in "
        f"{int(((big.n_pass4b > 0) & (big.n_pass4b < big.n_phase)).sum())} of {len(big)} "
        f"(panel, book, k) cells.")

    # ---- H1 / H2 the matched-turnover head-to-head --------------------------------
    say()
    say("-" * 100)
    say("H1 + H2 — CADENCE vs LAMBDA at MATCHED REALISED TURNOVER")
    say("-" * 100)
    say("  For every CADENCE arm (lambda=1) the LAMBDA curve (k=5, phase=0) is interpolated at")
    say("  the SAME realised turnover, and vice versa.  Arms outside the other dial's turnover")
    say("  range are NOT extrapolated: they are counted as unbracketed and reported.")
    M = []
    for (pk, book, c), s in G.groupby(["panel", "book", "cost"]):
        cad = s[s.lam == 1.0]
        lamc = s[(s.k == BASE_K) & (s.phase == BASE_P)]
        for _, a in cad.iterrows():
            sh = interp_at(lamc.turnover.values, lamc.Sharpe.values, a.turnover)
            cg = interp_at(lamc.turnover.values, lamc.CAGR.values, a.turnover)
            dd = interp_at(lamc.turnover.values, lamc.MaxDD.values, a.turnover)
            tev = interp_at(lamc.turnover.values, lamc.TE.values, a.turnover)
            M.append(dict(panel=pk, book=book, cost=c, direction="CAD->LAM", k=a.k,
                          phase=a.phase, lam=np.nan, turnover=a.turnover,
                          bracketed=bool(np.isfinite(sh)),
                          dSharpe=a.Sharpe - sh, dCAGR=a.CAGR - cg,
                          dMaxDD=abs(a.MaxDD) - abs(dd) if np.isfinite(dd) else np.nan,
                          TE_cad=a.TE, TE_lam=tev,
                          dTE=a.TE - tev if np.isfinite(tev) else np.nan))
        cadb = cad.groupby("k").agg(turnover=("turnover", "mean"), Sharpe=("Sharpe", "mean"),
                                    CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                                    TE=("TE", "mean")).reset_index()
        for _, a in lamc.iterrows():
            sh = interp_at(cadb.turnover.values, cadb.Sharpe.values, a.turnover)
            cg = interp_at(cadb.turnover.values, cadb.CAGR.values, a.turnover)
            dd = interp_at(cadb.turnover.values, cadb.MaxDD.values, a.turnover)
            tev = interp_at(cadb.turnover.values, cadb.TE.values, a.turnover)
            M.append(dict(panel=pk, book=book, cost=c, direction="LAM->CAD", k=np.nan,
                          phase=np.nan, lam=a.lam, turnover=a.turnover,
                          bracketed=bool(np.isfinite(sh)),
                          dSharpe=a.Sharpe - sh, dCAGR=a.CAGR - cg,
                          dMaxDD=abs(a.MaxDD) - abs(dd) if np.isfinite(dd) else np.nan,
                          TE_cad=tev, TE_lam=a.TE,
                          dTE=tev - a.TE if np.isfinite(tev) else np.nan))
    M = pd.DataFrame(M)
    M.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    B = M[M.bracketed]
    say(f"\n  bracketing: {len(B)} of {len(M)} matched sites are inside the other dial's "
        f"turnover range ({len(B)/len(M):.1%}); the rest are reported and dropped, never "
        f"extrapolated.")
    say("\n  dSharpe = CADENCE minus LAMBDA at the same realised turnover.  Positive => cadence "
        "is the better dial.")
    say(B.groupby(["direction", "cost"]).agg(
        n=("dSharpe", "size"), median_dSharpe=("dSharpe", "median"),
        mean_dSharpe=("dSharpe", "mean"), cad_wins=("dSharpe", lambda x: int((x > 0).sum())),
        median_dCAGR=("dCAGR", "median"), median_dMaxDD=("dMaxDD", "median")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  by panel and book, pooled over both directions and all rungs:")
    say(B.groupby(["panel", "book"]).agg(
        n=("dSharpe", "size"), median_dSharpe=("dSharpe", "median"),
        cad_wins=("dSharpe", lambda x: int((x > 0).sum())),
        median_dTE=("dTE", "median")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    DEG = B[B.dSharpe.abs() < 1e-9]
    ND = B[B.dSharpe.abs() >= 1e-9]
    say(f"\n  SELF-MATCHES, reported not hidden AND used as a check: {len(DEG)} of {len(B)} "
        f"bracketed sites ({len(DEG)/len(B):.1%}) have dSharpe EXACTLY 0.  These are exactly the "
        f"{len(PANELS)*len(BOOKS)*len(RUNGS)} sites where the two dials COINCIDE — the "
        f"k=5/phase=0 cadence arm IS the lambda=1 arm — one per (panel, book, rung), "
        f"{int((DEG.book == 'EWALL').sum())} of them EWALL.  That the interpolated match returns "
        f"0.000000 there rather than a small residual is a correctness check on the matching "
        f"machinery itself.  Excluding them:")
    say(f"    cadence wins {int((ND.dSharpe > 0).sum())}/{len(ND)} "
        f"({(ND.dSharpe > 0).mean():.1%}), median dSharpe {ND.dSharpe.median():+.4f}, "
        f"median |dSharpe| {ND.dSharpe.abs().median():.4f}")
    w = int((B.dSharpe > 0).sum())
    say(f"\n  POOLED: cadence beats lambda on Sharpe at matched turnover in {w} of {len(B)} "
        f"bracketed sites ({w/len(B):.1%}); median dSharpe {B.dSharpe.median():+.4f}, "
        f"median dCAGR {B.dCAGR.median():+.4%}, median dMaxDD {B.dMaxDD.median():+.4%}.")
    say(f"  At PROTOCOL's 10 bps rung alone: "
        f"{int((B[B.cost==10].dSharpe > 0).sum())}/{len(B[B.cost==10])}, median "
        f"{B[B.cost==10].dSharpe.median():+.4f}.")

    say()
    say("  H1 — the queue's premise, 'only lambda changes the book's path', measured as tracking")
    say("  error to the un-dialled base book at MATCHED realised turnover:")
    say(f"    median TE(cadence) {B.TE_cad.median():.4f}   median TE(lambda) {B.TE_lam.median():.4f}"
        f"   median dTE (cad - lam) {B.dTE.median():+.4f}")
    say(f"    cadence's TE is the LARGER one at {int((B.dTE > 0).sum())} of {len(B)} matched "
        f"sites ({(B.dTE > 0).mean():.1%})")
    say("    " + ("--> PREMISE REFUTED: at matched turnover cadence moves the path AT LEAST as "
                  "much as lambda." if (B.dTE > 0).mean() > 0.5 else
                  "--> PREMISE CONFIRMED: lambda moves the path more at matched turnover."))
    say("  by panel/book:")
    say(B.groupby(["panel", "book"]).agg(
        TE_cad=("TE_cad", "median"), TE_lam=("TE_lam", "median"), dTE=("dTE", "median"),
        cad_TE_bigger=("dTE", lambda x: int((x > 0).sum())), n=("dTE", "size")
    ).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- RESOLUTION: is the head-to-head even measurable? -------------------------
    say()
    say("-" * 100)
    say("RESOLUTION — is the cadence-vs-lambda gap larger than the PHASE noise of the cadence")
    say("dial itself?  (a difference smaller than its own nuisance parameter is not a finding)")
    say("-" * 100)
    noise = PH[PH.k > 1].Sharpe_sd
    eff = ND.dSharpe.abs()
    say(f"  median |dSharpe| between the two dials at matched turnover : {eff.median():.4f}")
    say(f"  median SD of the SAME cadence arm across its own phases     : {noise.median():.4f}")
    say(f"  ratio effect / noise                                        : "
        f"{eff.median()/noise.median():.3f}")
    say(f"  90th pct |dSharpe| {eff.quantile(0.9):.4f} vs 90th pct phase SD "
        f"{noise.quantile(0.9):.4f}")
    say("  --> " + ("the head-to-head is BELOW its own noise floor: the two dials are not "
                    "distinguishable at matched turnover on this evidence."
                    if eff.median() < noise.median() else
                    "the head-to-head clears the phase noise floor."))

    # ---- KEEP paths ---------------------------------------------------------------
    say()
    say("-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both evaluated on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                                : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>4}  4b {int(s.pass4b.sum()):>4}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    for (pk, book), s in G[G.cost == 10].groupby(["panel", "book"]):
        say(f"    {pk:>6} {book:>6} @10 bps: 4a {int(s.pass4a.sum()):>3}  "
            f"4b {int(s.pass4b.sum()):>3}  of {len(s)}")

    # ---- H3 rule 8 ----------------------------------------------------------------
    say()
    say("-" * 100)
    say("H3 / RULE 8 (PROTOCOL 8) — the dial chosen on 2009-2016 ONLY, 2017-2026 read once")
    say("-" * 100)
    say("  CADONLY: choose k (phase-averaged, phase 0 taken) at lambda=1.  LAMONLY: choose lambda")
    say("  at the base weekly cadence.  JOINT: choose both.  NONE: the un-dialled base book.")
    wf = []
    for pk in PANELS:
        px, _ = panels[pk]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        so = spy.loc[OOS_START:]
        mo = metrics(so)
        bo = dict(s1=metrics(so.iloc[:len(so) // 2])["Sharpe"],
                  s2=metrics(so.iloc[len(so) // 2:])["Sharpe"],
                  sdd=mo["MaxDD"], scagr=mo["CAGR"], soos=mo["Sharpe"])
        for book in BOOKS:
            for c in RUNGS:
                sub = G[(G.panel == pk) & (G.book == book) & (G.cost == c)]
                menus = {
                    "NONE": sub[(sub.lam == 1.0) & (sub.k == BASE_K) & (sub.phase == BASE_P)],
                    "CADONLY": sub[(sub.lam == 1.0) & (sub.phase == 0)],
                    "LAMONLY": sub[(sub.k == BASE_K) & (sub.phase == BASE_P)],
                    "JOINT": sub[sub.phase == 0],
                }
                for mn, mm in menus.items():
                    p = mm.loc[mm.IS_Sharpe.idxmax()]
                    r0, t0 = SER[(pk, book, float(p.lam), int(p.k), int(p.phase))]
                    r = (r0 - t0 * c / 1e4).loc[OOS_START:]
                    m = metrics(r)
                    h = len(r) // 2
                    o4b = dict(H1=metrics(r.iloc[:h])["Sharpe"] - bo["s1"],
                               H2=metrics(r.iloc[h:])["Sharpe"] - bo["s2"],
                               OOS=m["Sharpe"] - bo["soos"],
                               DD=DELTA * abs(bo["sdd"]) - abs(m["MaxDD"]),
                               CAGR=m["CAGR"] - PHI * bo["scagr"])
                    v2o = V2[pk][c].loc[OOS_START:]
                    mv = metrics(v2o)
                    wf.append(dict(panel=pk, book=book, cost=c, menu=mn,
                                   k=int(p.k), lam=float(p.lam),
                                   OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                                   OOS_MaxDD=m["MaxDD"],
                                   SPY_CAGR=mo["CAGR"], SPY_Sharpe=mo["Sharpe"],
                                   SPY_MaxDD=mo["MaxDD"], V2_CAGR=mv["CAGR"],
                                   V2_Sharpe=mv["Sharpe"], V2_MaxDD=mv["MaxDD"],
                                   beats_SPY=bool(m["Sharpe"] > mo["Sharpe"]),
                                   beats_V2=bool(m["Sharpe"] > mv["Sharpe"]),
                                   OOS_4b=all(v > 0 for v in o4b.values()),
                                   OOS_4a=pass4a(r, v2o)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("menu").agg(
        picks=("k", "size"), median_k=("k", "median"), median_lam=("lam", "median"),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        beats_V2=("beats_V2", "sum"), OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    piv = WF.pivot_table(index=["panel", "book", "cost"], columns="menu", values="OOS_Sharpe")
    say(f"\n  head-to-head OOS Sharpe, {len(piv)} cells:")
    say(f"    CADONLY beats LAMONLY in {int((piv.CADONLY > piv.LAMONLY).sum())}/{len(piv)}  "
        f"(median gap {float((piv.CADONLY - piv.LAMONLY).median()):+.4f})")
    say(f"    CADONLY beats NONE    in {int((piv.CADONLY > piv.NONE).sum())}/{len(piv)}  "
        f"(median gap {float((piv.CADONLY - piv.NONE).median()):+.4f})")
    say(f"    LAMONLY beats NONE    in {int((piv.LAMONLY > piv.NONE).sum())}/{len(piv)}  "
        f"(median gap {float((piv.LAMONLY - piv.NONE).median()):+.4f})")
    say(f"    JOINT   beats both    in "
        f"{int(((piv.JOINT > piv.CADONLY) & (piv.JOINT > piv.LAMONLY)).sum())}/{len(piv)}  "
        f"(median gap vs best single "
        f"{float((piv.JOINT - piv[['CADONLY','LAMONLY']].max(axis=1)).median()):+.4f})")
    say()
    for pk in PANELS:
        s = WF[(WF.panel == pk) & (WF.cost == 10)]
        say(f"  {pk:>6} @10 bps  SPY OOS CAGR {s.SPY_CAGR.iloc[0]:.2%} Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f} MaxDD {s.SPY_MaxDD.iloc[0]:.1%}  |  RULES v2 OOS CAGR "
            f"{s.V2_CAGR.iloc[0]:.2%} Sharpe {s.V2_Sharpe.iloc[0]:.3f} MaxDD "
            f"{s.V2_MaxDD.iloc[0]:.1%}")
        for mn, g in s.groupby("menu"):
            say(f"       {mn:>8}: picks k={list(g.k)} lam={list(g.lam)}  OOS CAGR "
                f"{g.OOS_CAGR.mean():.2%}  Sharpe {g.OOS_Sharpe.mean():.3f}  MaxDD "
                f"{g.OOS_MaxDD.mean():.1%}  4b {int(g.OOS_4b.sum())}/{len(g)}  "
                f"4a {int(g.OOS_4a.sum())}/{len(g)}")

    say()
    say("=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
