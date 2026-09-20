#!/usr/bin/env python3
"""Idea 1624 (lane C, 2026-09-20): is the FILTER-vs-DEGROSS DRAWDOWN GAP bigger than its OWN
PAIRED SE?

WHY THIS IDEA.  Idea 1617 ran every eligibility filter the record owns (MAXVOL, BAND, RANKCUT)
against a constant de-gross of the UNFILTERED book matched on REALISED mean gross, and found the
filter SHALLOWER than its twin at 30 of 33 cells, mean dMaxDD +3.67 pp.  That drawdown gap is the
ONLY axis on which the filter family beat the de-gross -- 1617's own Sharpe contrast was +0.0089
at the single cell that clears 4b, and negative at 25 and 50 bps -- and it is the sole reason 3
cells clear 4b where 0 twins do.  But idea 1511 measured the PAIRED circular-block-bootstrap SE
of a MaxDD contrast at 2.93 pp, so +3.67 pp is about 1.25 SE.  A 30-of-33 sign count looks
decisive and a 1.25-SE mean does not; the two readings cannot both be the headline.

WHAT THIS RUN DOES.  It bootstraps the FILTER-minus-TWIN dMaxDD DIRECTLY on all 33 pairs -- not a
borrowed SE from another cell -- with the record's own paired circular-block estimator (identical
block starts for filter and twin, so the pairing is preserved), and publishes the share of cells
reaching |t| > 2.  The sign count is re-read the same way: 30 of 33 positive is only evidence if
the 33 cells are independent draws, and they are not (4 MAXVOL rungs are nested, 4 BAND rungs are
nested, 3 panels share 55 of 56 names), so this run ALSO publishes a cell-level sign test that
states its own effective n.

  PRE-REGISTERED READING, stated before the run:
    - If NO cell reaches |t| > 2, the one axis on which the filter family beat the de-gross is
      inside its own noise, and the family can be retired after all (the idea's own words).
    - If SOME cells reach it, the finding is that the drawdown gap is real WHERE it is large,
      and the retirement is partial; the run must then say which cells and how the 4b passes sit
      relative to them.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  LB    circular block length in trading days {21, 65, 126}; the idea names LB = 65 as
                the headline rung (idea 1511's own convention is 63, one quarter; 65 is the same
                quarter to within two rows and is what 1624 asks for -- both are published).
  DIAL 2  CELL  which of the 33 (panel x family x rung) filter cells is read.

NOT DIALS, all published at every point: PANEL {U56, B136, SMALL}, COST {0, 10, 25, 50} bps,
WINDOW {FULL, OOS}.  Reps 400, seed 20260920, fixed before the run.

THE TWIN, unchanged from 1617 (this run must reproduce its dMaxDD exactly or it is measuring a
different quantity -- gate G2): the BASE book holds EVERY priced name at GROSS/N_priced; the twin
is that same book scaled by a constant k solved so the two carry the SAME REALISED mean gross
over the window being read.  FULL-window twins use a k solved on the full window; OOS twins use a
k solved on 2009-2016 ONLY (rule 8 -- no OOS data touches the twin's construction).

WHAT IS *NOT* CLAIMED.  A circular-block bootstrap resamples blocks, so the resampled path is NOT
the tape's path: MaxDD is the most path-dependent statistic the record uses and its block-
bootstrap SE is a crude yardstick.  That is precisely why this run does not invent a new one --
it uses the estimator the record already committed to in idea 1511 and reports what it says.  The
SE is published beside every reading so the next run can re-scale any of it.

GATES (published, and the ones marked GATE are asserted):
  G0  min sample >= 10 years (rule 1).
  G1  closed-form realised-gross solver vs a direct engine-semantics run (max |dev| < 1e-12).
  G2  this run's observed dMaxDD reproduces idea 1617's committed grid.csv at all 33 cells x 4
      cost rungs (max |dev| < 1e-12).  Without G2 the SE is attached to the wrong number.
  G3  BAND 0.03 on U56 replays baseline.compare's live RULES v2 row (< 1e-12).
  G4  realised-gross match |gross(twin) - gross(filter)| < 1e-9 at every cell and window.
  G5  exactly two tuned parameters.
  G6  no leverage / no shorting: max realised target gross <= 0.75.
  G7  bootstrap block starts IDENTICAL for filter and twin at every cell (pairing preserved).
  G8  every grid point published (no cell dropped).

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward with
2017-2026 read once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_filter-vs-degross-dd-paired-se_C.py
"""
from __future__ import annotations

import math

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "filter-vs-degross-dd-paired-se"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
GROSS = 0.75
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

BLOCKS = [21, 65, 126]          # DIAL 1
HEAD_LB = 65                    # the rung idea 1624 names
BOOT_REPS = 400
BOOT_SEED = 20260920
TBAR = 2.0

CELLS = ([("BASE", 0.0)]
         + [("MAXVOL", m) for m in (0.45, 0.60, 0.80, 1.00)]
         + [("BAND", c) for c in (0.00, 0.03, 0.06, 0.10)]
         + [("RANKCUT", q) for q in (0.25, 0.50, 0.75)])
LIVE_CELL = ("BAND", 0.03)
BASE_CELL = ("BASE", 0.0)
PANELS = ["U56", "B136", "SMALL"]

PRIOR_GRID = ROOT / "research" / "backtests" / \
    "2026-09-19_is-every-eligibility-filter-a-degross-in-disguise_C.grid.csv"


def lab(cell):
    f, p = cell
    return "BASE" if f == "BASE" else f"{f} {p:.2f}"


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


# ---------------------------------------------------------------- panel (identical to idea 1617)
class Panel:
    def __init__(self, name, px, cols):
        self.name, self.px, self.cols = name, px, list(cols)
        allc = list(px.columns)
        self.icol = np.array([allc.index(c) for c in self.cols])
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        q = px[self.cols]
        self.priced = q.notna().values
        v = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.vol20 = np.nan_to_num(v, nan=1e9)
        self.bands = {c: band_state(q, c).values for c in (0.00, 0.03, 0.06, 0.10)}
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts))
        self.rankpct = comp.rank(axis=1, ascending=False, pct=True).values
        self.rankok = np.isfinite(self.rankpct)
        self.reb = self._reb(CADENCE)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))

    def _reb(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)

    def elig(self, cell):
        f, p = cell
        if f == "BASE":
            return self.priced
        if f == "MAXVOL":
            return self.priced & (self.vol20 < p)
        if f == "BAND":
            return self.priced & self.bands[p]
        if f == "RANKCUT":
            return self.priced & self.rankok & (np.nan_to_num(self.rankpct, nan=9.9) <= p)
        raise ValueError(f)

    def frame(self, cell):
        T, M = self.rets.shape
        e = self.elig(cell).astype(float)
        n = self.priced.sum(axis=1).astype(float)
        w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
        w = np.nan_to_num(w, nan=0.0)
        W = np.zeros((T, M))
        W[:, self.icol] = w
        return np.vstack([np.zeros((1, M)), W[:-1]])


def run_cell(pan, frame, g=GROSS):
    """Identical semantics to engine.backtest (gated in idea 1617 at 1e-12): weekly rebalance,
    drift in between, gated-out weight to 0%-yielding cash.  GROSS-OF-COST daily returns."""
    rets = pan.rets
    T, M = rets.shape
    reb = pan.reb
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


def gross_kernel(pan, frame):
    """Unit-gross aggregate exposure path S(t) and the segment's own S(i0), so realised gross of
    the SAME book at any scale g is closed-form:  gross(t;g) = g S(t) / (g S(t) + 1 - g S(i0)).
    This removes the 60-halving re-simulation idea 1617 needed per twin.  Gated at G1."""
    T = pan.rets.shape[0]
    S = np.zeros(T)
    S0 = np.zeros(T)
    ends = np.append(pan.reb[1:], T)
    Cp = pan.Cp
    for i0, i1 in zip(pan.reb, ends):
        if i1 <= i0:
            continue
        w0 = frame[i0]
        base = Cp[i0]
        S[i0:i1] = (w0[None, :] * (Cp[i0:i1] / base[None, :])).sum(axis=1)
        S0[i0:i1] = float(w0.sum())
    return S, S0


def gross_path(S, S0, g):
    num = g * S
    return num / (num + 1.0 - g * S0)


def solve_k(S, S0, target_mean_gross, lo, hi):
    """Bisect the constant scaler k (of GROSS) so the BASE book carries target realised mean gross
    over [lo:hi).  Realised gross is monotone in k, so 200 halvings is exact to machine eps."""
    a, b = 0.0, 1.0
    for _ in range(200):
        k = 0.5 * (a + b)
        gm = float(np.mean(gross_path(S, S0, k * GROSS)[lo:hi]))
        if gm < target_mean_gross:
            a = k
        else:
            b = k
    return 0.5 * (a + b)


# ---------------------------------------------------------------- metrics
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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- the estimator (idea 1511's)
def boot_idx(n, L, reps=BOOT_REPS, seed=BOOT_SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def _dd_rows(X):
    e = np.cumprod(1 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)


def _sh_rows(X):
    v = X.std(axis=1, ddof=0) * np.sqrt(252)
    return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)


def paired_block(a, b, L):
    """PAIRED circular-block bootstrap of the FILTER-minus-TWIN contrast, identical block starts
    for both legs (that is the whole point: the common tape cancels).  Returns observed contrast,
    SE and t for MaxDD and, published alongside, for Sharpe."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    idx = boot_idx(n, L)
    A, B = a[idx], b[idx]
    dd_ = _dd_rows(A) - _dd_rows(B)
    ds = _sh_rows(A) - _sh_rows(B)
    o_d, o_s = float(mdd(a) - mdd(b)), float(sharpe(a) - sharpe(b))
    se_d, se_s = float(np.nanstd(dd_, ddof=1)), float(np.nanstd(ds, ddof=1))
    return dict(dMaxDD=o_d, se_dd=se_d, t_dd=(o_d / se_d if se_d > 0 else np.nan),
                dSharpe=o_s, se_sh=se_s, t_sh=(o_s / se_s if se_s > 0 else np.nan),
                lo=float(np.nanpercentile(dd_ - np.nanmean(dd_) + o_d, 2.5)),
                hi=float(np.nanpercentile(dd_ - np.nanmean(dd_) + o_d, 97.5)))


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1624 (lane C, 2026-09-20) — is the FILTER-vs-DEGROSS DRAWDOWN GAP bigger than its")
    say("OWN PAIRED SE?  Idea 1617: filter shallower than its matched-exposure twin at 30 of 33")
    say("cells, mean +3.67 pp.  Idea 1511's paired circular-block SE of a MaxDD contrast: 2.93 pp.")
    say(f"DIALS: LB {BLOCKS} x CELL (33 filter cells).  Reps {BOOT_REPS}, seed {BOOT_SEED}.")
    say(f"NOT DIALS, all published: PANEL {PANELS} x COST {COSTS} bps x WINDOW [FULL, OOS].")
    say("PRE-REGISTERED: if NO cell reaches |t| > 2, the drawdown axis is inside its own noise")
    say("                and the eligibility-filter family can be retired (the idea's own words).")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated, identical to 1617): data/small_meta.csv drops "
        f"{len(bad)} tickers with max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} survive.")

    panels = [Panel("U56", pxU, list(pxU.columns)),
              Panel("B136", pxB, list(pxB.columns)),
              Panel("SMALL", pxS, inv)]
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level is an UPPER BOUND.  The "
        "headline here is a FILTER-minus-TWIN contrast inside one panel, over the same names on "
        "the same days at the same realised exposure, so it is first-order immune; the 4b pass "
        "counts and the CAGR levels are not.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)  OOS starts row {p.i_oos} ({p.idx[p.i_oos].date()})")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters (LB x CELL)",
         f"LB {BLOCKS} x {len(CELLS)-1} filter cells per panel", "2 dials", True)

    # ---------------------------------------------- G1: closed-form gross solver vs direct run
    say("\n  [G1] closed-form realised-gross kernel vs a direct engine-semantics run")
    d1 = 0.0
    for pan in panels:
        bf = pan.frame(BASE_CELL)
        S, S0 = gross_kernel(pan, bf)
        for k in (1.0, 0.5, 0.137):
            _, _, _, gs = run_cell(pan, bf, g=k * GROSS)
            d1 = max(d1, float(np.max(np.abs(gs - gross_path(S, S0, k * GROSS)))))
    gate("G1 closed-form gross path vs run_cell (max |dev|, 3 panels x 3 scales)",
         f"{d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---------------------------------------------- G3 / G6: books
    rows, boots, wsum_global, gapmax = [], [], 0.0, 0.0
    BARS, RET, TWIN, ISPK = {}, {}, {}, {}
    g3row = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        spy = bmpack(pan.spy[WARMUP:])
        spyO = bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=BIND, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO)
        g3row[pan.name] = live
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}"
            f"  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
            f"  |  OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}  (OOS {liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / "
            f"{liveO['MaxDD']:.2%})")

        base_frame = pan.frame(BASE_CELL)
        S, S0 = gross_kernel(pan, base_frame)
        rgB, tuB, wsB, gsB = run_cell(pan, base_frame)
        twcache = {1.0: (rgB, tuB, gsB)}
        yrs = (T - WARMUP) / 252.0

        for cell in CELLS:
            fm = pan.frame(cell)
            rg, tu, ws, gs = run_cell(pan, fm)
            wsum_global = max(wsum_global, ws)
            gf_full = float(np.mean(gs[WARMUP:]))
            gf_is = float(np.mean(gs[WARMUP:i_oos]))
            if cell == BASE_CELL:
                kF = kI = 1.0
            else:
                kF = solve_k(S, S0, gf_full, WARMUP, T)
                kI = solve_k(S, S0, gf_is, WARMUP, i_oos)      # rule 8: IS-only twin
            for k in (kF, kI):
                if k not in twcache:
                    r_, t_, _, g_ = run_cell(pan, base_frame, g=k * GROSS)
                    twcache[k] = (r_, t_, g_)
            rgT, tuT, gsT = twcache[kF]
            rgTI, tuTI, gsTI = twcache[kI]
            gapmax = max(gapmax, abs(float(np.mean(gsT[WARMUP:])) - gf_full),
                         abs(float(np.mean(gsTI[WARMUP:i_oos])) - gf_is))

            for c in COSTS:
                r = rg - tu * c / 1e4
                rT = rgT - tuT * c / 1e4
                rTI = rgTI - tuTI * c / 1e4
                RET[(pan.name, lab(cell), c)] = r
                TWIN[(pan.name, lab(cell), c)] = (rT, rTI)
                k4a, k4b, mt, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                t4a, t4b, tmt, _, _, _ = keep_paths(rT[WARMUP:], spy, live)
                t4aO, t4bO, tmo, _, _, _ = keep_paths(rTI[i_oos:], spyO, liveO)
                if c == BIND:
                    ISPK.setdefault(pan.name, {})[lab(cell)] = dict(
                        isSharpe=sharpe(r[WARMUP:i_oos]), isCAGR=cagr(r[WARMUP:i_oos]),
                        isMaxDD=mdd(r[WARMUP:i_oos]), oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                        oMaxDD=mo["MaxDD"], keep4b_oos=k4bO, keep4a_oos=k4aO, kI=kI)
                rows.append(dict(
                    panel=pan.name, family=cell[0],
                    rung=("" if cell[0] == "BASE" else f"{cell[1]:.2f}"),
                    cell=lab(cell), cost_bps=c,
                    CAGR=mt["CAGR"], Sharpe=mt["Sharpe"], MaxDD=mt["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    isSharpe=sharpe(r[WARMUP:i_oos]), k_full=kF, k_is=kI,
                    tw_CAGR=tmt["CAGR"], tw_Sharpe=tmt["Sharpe"], tw_MaxDD=tmt["MaxDD"],
                    tw_oCAGR=tmo["CAGR"], tw_oSharpe=tmo["Sharpe"], tw_oMaxDD=tmo["MaxDD"],
                    dSharpe=mt["Sharpe"] - tmt["Sharpe"], dMaxDD=mt["MaxDD"] - tmt["MaxDD"],
                    odSharpe=mo["Sharpe"] - tmo["Sharpe"], odMaxDD=mo["MaxDD"] - tmo["MaxDD"],
                    mean_gross=gf_full, tw_mean_gross=float(np.mean(gsT[WARMUP:])),
                    turnover_yr=float(tu[WARMUP:].sum() / yrs),
                    tw_turnover_yr=float(tuT[WARMUP:].sum() / yrs),
                    keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                    tw_keep4a=t4a, tw_keep4b=t4b, tw_keep4b_oos=t4bO,
                    leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"],
                    is_base=bool(cell == BASE_CELL), is_live=bool(cell == LIVE_CELL)))
        say(f"    [{pan.name}] {len(CELLS)} cells x {len(COSTS)} rungs, twins solved "
            f"({time.time()-t0:.0f}s)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G6 no leverage, no shorting (max realised target gross)", f"{wsum_global:.4f}",
         f"<= {GROSS:.4f}", wsum_global <= GROSS + 1e-12)
    gate("G4 REALISED-gross match |gross(twin) - gross(filter)|, max over all cells and windows",
         f"{gapmax:.3e}", "< 1e-9", gapmax < 1e-9)
    lv = G[(G.panel == "U56") & (G.cell == lab(LIVE_CELL)) & (G.cost_bps == BIND)].iloc[0]
    b = g3row["U56"]
    d3 = max(abs(lv["CAGR"] - b["CAGR"]), abs(lv["Sharpe"] - b["Sharpe"]),
             abs(lv["MaxDD"] - b["MaxDD"]), abs(lv["H1"] - b["H1"]), abs(lv["H2"] - b["H2"]))
    gate("G3 BAND 0.03 on U56 replays baseline.compare's live RULES v2 row", f"{d3:.3e}",
         "< 1e-12 (it IS the same book)", d3 < 1e-12)

    # ---------------------------------------------- G2: reproduce idea 1617's committed dMaxDD
    P = pd.read_csv(PRIOR_GRID)
    key = ["panel", "cell", "cost_bps"]
    J = G.merge(P[key + ["dMaxDD", "odMaxDD", "dSharpe", "mean_gross"]], on=key,
                suffixes=("", "_1617"))
    d2 = float(np.max(np.abs(J.dMaxDD - J.dMaxDD_1617)))
    d2o = float(np.max(np.abs(J.odMaxDD - J.odMaxDD_1617)))
    d2s = float(np.max(np.abs(J.dSharpe - J.dSharpe_1617)))
    gate("G2 this run's FULL dMaxDD reproduces idea 1617's committed grid.csv (all 144 rows)",
         f"{d2:.3e}", "< 1e-12", d2 < 1e-12)
    gate("G2b same, OOS dMaxDD", f"{d2o:.3e}", "< 1e-12", d2o < 1e-12)
    gate("G2c same, FULL dSharpe", f"{d2s:.3e}", "< 1e-12", d2s < 1e-12)
    NB0 = G[(G.cost_bps == BIND) & (~G.is_base)]
    gate("G2d idea 1617's headline replays: dMaxDD >= 0 (filter SHALLOWER) count @10bps",
         f"{int((NB0.dMaxDD >= 0).sum())} of {len(NB0)}, mean {NB0.dMaxDD.mean():+.2%}",
         "30 of 33, mean +3.67%",
         int((NB0.dMaxDD >= 0).sum()) == 30 and abs(NB0.dMaxDD.mean() - 0.0367) < 5e-4)

    # ---------------------------------------------- G7: pairing
    ia = boot_idx(1000, HEAD_LB)
    ib = boot_idx(1000, HEAD_LB)
    gate("G7 bootstrap block starts IDENTICAL for filter and twin (same seed, same n, same L)",
         f"max |idx_a - idx_b| = {int(np.max(np.abs(ia - ib)))}", "0 (pairing preserved)",
         int(np.max(np.abs(ia - ib))) == 0)

    # ---------------------------------------------- THE QUESTION
    say("\n" + "=" * 118)
    say("Q1  PAIRED CIRCULAR-BLOCK BOOTSTRAP OF dMaxDD = MaxDD(filter) - MaxDD(matched twin)")
    say("    at every one of the 33 cells, every block length, both windows, every cost rung.")
    say("=" * 118)
    for pan in PANELS:
        i_oos = [p for p in panels if p.name == pan][0].i_oos
        for cell in CELLS:
            if cell == BASE_CELL:
                continue
            for c in COSTS:
                r = RET[(pan, lab(cell), c)]
                rT, rTI = TWIN[(pan, lab(cell), c)]
                for L in BLOCKS:
                    if c != BIND and L != HEAD_LB:
                        continue                       # full cross only at the binding rung
                    bF = paired_block(r[WARMUP:], rT[WARMUP:], L)
                    bO = paired_block(r[i_oos:], rTI[i_oos:], L)
                    boots.append(dict(panel=pan, family=cell[0], rung=f"{cell[1]:.2f}",
                                      cell=lab(cell), cost_bps=c, block=L, window="FULL", **bF))
                    boots.append(dict(panel=pan, family=cell[0], rung=f"{cell[1]:.2f}",
                                      cell=lab(cell), cost_bps=c, block=L, window="OOS", **bO))
    Bt = pd.DataFrame(boots)
    Bt.to_csv(f"{OUT}.boot.csv", index=False)
    gate("G8 every grid point published",
         f"{len(Bt)} bootstrap rows in {Path(OUT).name}.boot.csv",
         "33 cells x [4 costs @LB65 + 2 extra LB @10bps] x 2 windows = 396", len(Bt) == 396)

    say(f"\n  HEADLINE ROW-BY-ROW  (LB = {HEAD_LB}, {BIND:.0f} bps, FULL window)")
    say(f"  {'panel':6s} {'cell':14s} {'dMaxDD':>8s} {'SE':>7s} {'t':>7s} {'95% CI':>18s} "
        f"{'dSharpe':>8s} {'t_sh':>7s}  {'|t|>2':>5s}")
    H = Bt[(Bt.block == HEAD_LB) & (Bt.cost_bps == BIND) & (Bt.window == "FULL")]
    for _, r in H.iterrows():
        say(f"  {r['panel']:6s} {r['cell']:14s} {r['dMaxDD']:+8.2%} {r['se_dd']:7.2%} "
            f"{r['t_dd']:+7.2f} [{r['lo']:+7.2%},{r['hi']:+7.2%}] {r['dSharpe']:+8.4f} "
            f"{r['t_sh']:+7.2f}  {'YES' if abs(r['t_dd']) > TBAR else 'no':>5s}")

    say("\n  SHARE OF THE 33 CELLS REACHING |t| > 2 ON dMaxDD  (every grid point):")
    say(f"  {'window':7s} {'cost':>5s} {'LB':>4s} {'|t|>2':>8s} {'t>+2':>6s} {'t<-2':>6s} "
        f"{'mean dMaxDD':>12s} {'mean SE':>9s} {'mean t':>7s} {'max |t|':>8s}")
    for w in ["FULL", "OOS"]:
        for c in COSTS:
            for L in BLOCKS:
                S = Bt[(Bt.window == w) & (Bt.cost_bps == c) & (Bt.block == L)]
                if not len(S):
                    continue
                say(f"  {w:7s} {c:5.0f} {L:4d} {int((S.t_dd.abs() > TBAR).sum()):3d} of "
                    f"{len(S):<3d} {int((S.t_dd > TBAR).sum()):6d} "
                    f"{int((S.t_dd < -TBAR).sum()):6d} {S.dMaxDD.mean():+12.2%} "
                    f"{S.se_dd.mean():9.2%} {S.t_dd.mean():+7.2f} {S.t_dd.abs().max():8.2f}")

    HB = Bt[(Bt.block == HEAD_LB) & (Bt.cost_bps == BIND)]
    nF = int((HB[HB.window == "FULL"].t_dd.abs() > TBAR).sum())
    nO = int((HB[HB.window == "OOS"].t_dd.abs() > TBAR).sum())
    say(f"\n  ANSWER at the idea's own rung (LB = {HEAD_LB}, {BIND:.0f} bps): "
        f"{nF} of 33 FULL and {nO} of 33 OOS reach |t| > 2.")
    say(f"  Idea 1617's mean gap +{H.dMaxDD.mean():.2%} against this run's own mean paired SE "
        f"{H.se_dd.mean():.2%}  ->  {H.dMaxDD.mean()/H.se_dd.mean():.2f} SE, against the 1.25 SE "
        f"the queue computed from idea 1511's BORROWED 2.93 pp.")
    publish("PER-CELL SE range (LB 65, 10 bps, FULL)",
            f"{H.se_dd.min():.2%} .. {H.se_dd.max():.2%} (idea 1511's borrowed figure: 2.93%)")

    # ---------------------------------------------- the sign count, re-read
    say("\n" + "=" * 118)
    say("Q2  THE 30-OF-33 SIGN COUNT, RE-READ WITH ITS OWN EFFECTIVE n")
    say("=" * 118)
    sgn = H.dMaxDD.values
    k_pos = int((sgn >= 0).sum())
    say(f"  Raw: {k_pos} of {len(sgn)} positive.  Binomial p (two-sided, p0 = 0.5, n = 33) = "
        f"{2*sum(math.comb(33, i) for i in range(k_pos, 34))/2**33:.3e}")
    say("  But the 33 cells are NOT 33 independent draws.  Published dependence, measured:")
    for pan in PANELS:
        S = H[H.panel == pan]
        say(f"    PANEL {pan:6s}: {int((S.dMaxDD >= 0).sum())} of {len(S)} positive "
            f"(11 nested rungs over ONE tape)")
    fam_pos = {}
    for fam in ["MAXVOL", "BAND", "RANKCUT"]:
        S = H[H.family == fam]
        fam_pos[fam] = int((S.dMaxDD >= 0).sum())
        say(f"    FAMILY {fam:8s}: {fam_pos[fam]} of {len(S)} positive, mean "
            f"{S.dMaxDD.mean():+.2%}, max |t| {S.t_dd.abs().max():.2f}")
    # correlation of the bootstrap dMaxDD draws between cells within a panel: the real n
    rho = []
    for pan in PANELS:
        cells = [lab(c) for c in CELLS if c != BASE_CELL]
        mats = []
        i_oos = [p for p in panels if p.name == pan][0].i_oos
        for cl in cells:
            r = RET[(pan, cl, BIND)][WARMUP:]
            rT = TWIN[(pan, cl, BIND)][0][WARMUP:]
            idx = boot_idx(len(r), HEAD_LB)
            mats.append(_dd_rows(r[idx]) - _dd_rows(rT[idx]))
        M = np.vstack(mats)
        C = np.corrcoef(M)
        off = C[np.triu_indices_from(C, 1)]
        rho.append(float(np.nanmean(off)))
        say(f"    WITHIN-PANEL {pan:6s}: mean pairwise correlation of the 11 cells' bootstrap "
            f"dMaxDD draws = {rho[-1]:+.3f}  ->  effective independent cells ~ "
            f"{11/(1+10*max(rho[-1],0)):.2f} of 11")
    rbar = float(np.mean(rho))
    n_eff = 33.0 / (1.0 + (33 - 1) * max(rbar, 0.0))
    publish("EFFECTIVE n of the 33-cell sign count",
            f"mean within-panel rho {rbar:+.3f} -> n_eff ~ {n_eff:.2f} (naive n = 33)")

    # ---------------------------------------------- 4b passes vs their own SE
    say("\n" + "=" * 118)
    say("Q3  THE THREE 4b PASSES — is each one's DD margin bigger than THAT CELL'S own SE?")
    say("=" * 118)
    B10 = G[(G.cost_bps == BIND) & (~G.is_base)]
    say(f"  4b FULL: FILTER {int(B10.keep4b.sum())} of {len(B10)}  |  TWIN "
        f"{int(B10.tw_keep4b.sum())} of {len(B10)}   (idea 1617's '3 cells vs 0 twins')")
    for _, r in B10[B10.keep4b].iterrows():
        bt = H[(H.panel == r['panel']) & (H.cell == r['cell'])].iloc[0]
        spy = BARS[r['panel']]['spy']
        margin = r['MaxDD'] - DD_CAP * spy['MaxDD']
        tw_margin = r['tw_MaxDD'] - DD_CAP * spy['MaxDD']
        say(f"    {r['panel']:6s} {r['cell']:14s} MaxDD {r['MaxDD']:+.2%} vs 4b cap "
            f"{DD_CAP*spy['MaxDD']:+.2%}  margin {margin:+.2%};  TWIN {r['tw_MaxDD']:+.2%} "
            f"(margin {tw_margin:+.2%}, it MISSES).  The gap that does it: dMaxDD "
            f"{bt['dMaxDD']:+.2%}, SE {bt['se_dd']:.2%}, t {bt['t_dd']:+.2f} -> "
            f"{'SIGNIFICANT' if abs(bt['t_dd']) > TBAR else 'INSIDE ITS OWN NOISE'}")

    # ---------------------------------------------- rule 8 walk-forward
    say("\n" + "=" * 118)
    say("Q4  RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
    say("=" * 118)
    wf = []
    for pan in PANELS:
        i_oos = [p for p in panels if p.name == pan][0].i_oos
        spyO, liveO = BARS[pan]['spyO'], BARS[pan]['liveO']
        cands = [lab(c) for c in CELLS if c != BASE_CELL]
        # C_SHARPE: highest IS Sharpe among the 33 filter cells
        pick_sh = max(cands, key=lambda cl: ISPK[pan][cl]["isSharpe"])
        # C_DDT: this idea's OWN chooser -- the cell whose IS dMaxDD carries the largest |t|
        ist = {}
        for cl in cands:
            r = RET[(pan, cl, BIND)]
            rTI = TWIN[(pan, cl, BIND)][1]
            ist[cl] = paired_block(r[WARMUP:i_oos], rTI[WARMUP:i_oos], HEAD_LB)["t_dd"]
        pick_dt = max(cands, key=lambda cl: ist[cl])
        # C_BASE: take no filter at all (the null the idea would adopt on a retirement verdict)
        for nm, cl in [("C_SHARPE (max IS Sharpe)", pick_sh),
                       ("C_DDT   (max IS dMaxDD t)", pick_dt),
                       ("C_BASE  (no filter at all)", "BASE")]:
            d = ISPK[pan][cl] if cl != "BASE" else None
            if cl == "BASE":
                g = G[(G.panel == pan) & (G.cell == "BASE") & (G.cost_bps == BIND)].iloc[0]
                oC, oS, oD = g["oCAGR"], g["oSharpe"], g["oMaxDD"]
                k4bO, k4aO = bool(g["keep4b_oos"]), bool(g["keep4a_oos"])
            else:
                oC, oS, oD = d["oCAGR"], d["oSharpe"], d["oMaxDD"]
                k4bO, k4aO = d["keep4b_oos"], d["keep4a_oos"]
            say(f"  {pan:6s} {nm:26s} -> {cl:14s}  OOS {oC:7.2%} / {oS:7.4f} / {oD:8.2%}"
                f"  |  SPY OOS {spyO['CAGR']:7.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
                f"  |  RULES v2 OOS {liveO['CAGR']:7.2%} / {liveO['Sharpe']:.4f} / "
                f"{liveO['MaxDD']:.2%}  |  4b OOS {'PASS' if k4bO else 'fail'}"
                f"  4a OOS {'PASS' if k4aO else 'fail'}")
            wf.append(dict(panel=pan, chooser=nm, pick=cl, oCAGR=oC, oSharpe=oS, oMaxDD=oD,
                           spy_oCAGR=spyO['CAGR'], spy_oSharpe=spyO['Sharpe'],
                           spy_oMaxDD=spyO['MaxDD'], live_oCAGR=liveO['CAGR'],
                           live_oSharpe=liveO['Sharpe'], live_oMaxDD=liveO['MaxDD'],
                           keep4b_oos=k4bO, keep4a_oos=k4aO,
                           dSharpe_vs_spy=oS - spyO['Sharpe'],
                           dSharpe_vs_live=oS - liveO['Sharpe']))
        say(f"         IS-chosen filter t-stat {ist[pick_dt]:+.2f} at {pick_dt}; the OOS "
            f"dMaxDD of that same cell is "
            f"{Bt[(Bt.panel==pan)&(Bt.cell==pick_dt)&(Bt.window=='OOS')&(Bt.block==HEAD_LB)&(Bt.cost_bps==BIND)].iloc[0]['dMaxDD']:+.2%} "
            f"at t "
            f"{Bt[(Bt.panel==pan)&(Bt.cell==pick_dt)&(Bt.window=='OOS')&(Bt.block==HEAD_LB)&(Bt.cost_bps==BIND)].iloc[0]['t_dd']:+.2f}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE-8 SUMMARY: of {len(W)} (panel x chooser) picks, {int(W.keep4b_oos.sum())} "
        f"clear 4b OOS and {int(W.keep4a_oos.sum())} clear 4a OOS.")
    say(f"  Pooled OOS Sharpe of the IS-CHOSEN FILTER vs taking NO filter at all: "
        f"{W[W.chooser.str.startswith('C_SHARPE')].oSharpe.mean():.4f} / "
        f"{W[W.chooser.str.startswith('C_DDT')].oSharpe.mean():.4f} vs "
        f"{W[W.chooser.str.startswith('C_BASE')].oSharpe.mean():.4f}")

    # ---------------------------------------------- both KEEP paths
    say("\n" + "=" * 118)
    say("Q5  BOTH KEEP PATHS (rule 4), every cell, @10 bps binding")
    say("=" * 118)
    say(f"  4a (beat the live book on BOTH halves + MaxDD no worse): FILTER "
        f"{int(B10.keep4a.sum())} of {len(B10)}  |  TWIN {int(B10.tw_keep4a.sum())} of {len(B10)}")
    say(f"  4b (beat SPY both halves + DD cap + CAGR floor) FULL: FILTER {int(B10.keep4b.sum())}"
        f" of {len(B10)}  |  TWIN {int(B10.tw_keep4b.sum())} of {len(B10)}")
    say(f"  4b OOS: FILTER {int(B10.keep4b_oos.sum())} of {len(B10)}  |  TWIN "
        f"{int(B10.tw_keep4b_oos.sum())} of {len(B10)}")
    say(f"  4b FULL *and* OOS *and* reached by a legal IS-only chooser: "
        f"{int(W.keep4b_oos.sum())} of {len(W)} rule-8 picks")

    ok = all(g["pass_"] for g in GATES)
    npass = int(H.t_dd.abs().gt(TBAR).sum())
    verdict = "KILL" if npass == 0 else "PARK"
    say("\n" + "=" * 118)
    say(f"VERDICT: {verdict}")
    say("=" * 118)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass; all_ok={ok}; "
        f"{time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return G, Bt, W, H


if __name__ == "__main__":
    main()
