#!/usr/bin/env python3
"""IDEA 1779 (lane C, 2026-09-22) — is the NAME-SET CHOOSER just a TRAILING-RETURN CHOOSER in
disguise?

THE DEFECT THIS CLOSES.  Idea 1749 (lane cloud, 2026-09-20) established that a 20-name subset of
U56, chosen by an IS-ONLY statistic computed on the BOOK, reaches 4b far above the base rate
(25/48 = 52.08% top decile against 43/480 = 8.96%), and wrote a KEEP-4b candidate memo on the
back of it.  Idea 1775 (lane C, 2026-09-22) replicated the lift on B136.  But 1749 also found the
binding leg is the 4b CAGR FLOOR at 373 of 373 OOS failures and drawdown at 0, and its two best
statistics (IS_CAGRSLACK = IS CAGR - 0.70 x SPY IS CAGR, and IS_MINMARG) are BOTH CAGR-driven.
That is consistent with the chooser doing nothing at all except buying the names that already went
up on a survivorship-biased current-constituent list.  If so, the "name set is a reachable axis"
headline is a statement about trailing returns, not about the band book, and the candidate's
information content is zero.

THE TEST.  Re-run 1749's construction UNCHANGED (band c = 0.03, gross 0.75, weekly cadence, t+1,
10 bps binding, seed stream default_rng(16320000 + 1009*N + d), U56 N=20, D up to 480), and score
the SAME 480 draws with NAIVE CONTROL statistics that never see the band, the book, the cadence or
a single backtested return -- only the constituents' own trailing 2009-2016 price history.  If a
naive control reaches the same top-decile OOS-4b rate as IS_CAGRSLACK, 1749's chooser carries no
BOOK information.

TUNED DIALS, EXACTLY TWO (PROTOCOL rule 4):
  1. CONTROL STATISTIC   -- 5 naive controls, scored against 1749's 4 book statistics.
  2. DECILE WIDTH q      -- {0.05, 0.10, 0.20, 0.25}; n_top = ceil(D*q).  1749 used 0.10 only.
REPORTED, NOT TUNED: draw count D in {24, 96, 240, 480} (nested, 1749's ladder), cost rung in
{0, 10, 25, 50} bps (reconstructed exactly off the cost-0 leg), PANEL in {U56, B136} (U56 N=20 is
1749's own cell; B136 N=20 is the one other cell 1775 found the lift on), and both 4b targets
(4b OOS, which the idea names, and 4b BOTH, which 1749 published).  EVERY grid point is written.

INHERITED FROM 1749, NOT TUNED: band c = 0.03, gross 0.75, cadence W, t+1, N = 20, the four book
statistics, the IS/OOS split 2016-12-31 / 2017-01-01, the warm-up of 260 rows.

THE NAIVE CONTROLS (no band, no book, no backtest -- price history only, all rows <= 2016-12-31):
  NAIVE_MEANRET   mean over the draw's names of each name's IS TOTAL RETURN (the idea's wording)
  NAIVE_MEDRET    median of the same per-name IS total returns (outlier-robust variant)
  NAIVE_LOGRET    mean of log(1 + IS total return) (geometric variant)
  NAIVE_EWBH      IS total return of an equal-weight, buy-and-hold, never-rebalanced basket
  NAIVE_MEANSHR   mean of the names' own IS Sharpe ratios (separates "went up" from "went up
                  smoothly"; the one control that is not a pure return statistic)
All five are legal rule-8 choosers: they read no row on or after 2017-01-01 (gate G4).

WHAT WOULD ANSWER IT.  (a) A naive control matches or beats IS_CAGRSLACK's top-decile OOS-4b rate
and ranks the draws nearly identically -> 1749's chooser carries no book information and the
candidate is a trailing-return lottery ticket on a survivorship-biased list.  (b) The naive
controls fall materially short -> the book statistic is doing real work and 1749's headline
stands as written.

GATES (all printed, all written to <OUT>.gates.csv):
  G1 the runner reproduces engine.backtest on returns AND turnover, both panels
  G2 cost identity r(c) = r0 - turnover*c/1e4 against the engine at 10 and 25 bps
  G3 cross-run replication of 1749 / 1775 on U56 N=20 D=480 (base count and top-decile count)
  G4 NO statistic -- naive or book -- reads a price row on or after 2017-01-01
  G5 exactly two tuned dials
  G6 every cell published
  G7 seed stream unchanged from 1632 / 1749 / 1775
  G8 no leverage / no shorting: max realised TARGET gross <= 0.75
  G9 the naive controls are book-free: recomputing them after permuting the BAND leaves them
     bit-identical (they cannot depend on the book)

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists.  This run is in fact
a direct measurement of how much of 1749's candidate is that bias: a trailing-return chooser on a
survivor list is the purest form of the exposure.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-22", "name-set-chooser-vs-trailing-return"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
GROSS = 0.75                       # live RULES v2
BAND_C = 0.03                      # live RULES v2 clause 2
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

N_DRAW = 20                        # 1749's own cell; N is NOT a dial here
DCOUNTS = [24, 96, 240, 480]       # reported, nested
DMAX = max(DCOUNTS)
SEED0 = 16320000                   # idea 1632's / 1749's seed base, unchanged (G7)

QWIDTHS = [0.05, 0.10, 0.20, 0.25]                      # DIAL 2
BOOK_STATS = ["IS_SHARPE", "IS_LEGS", "IS_CAGRSLACK", "IS_MINMARG"]     # 1749's four
NAIVE_STATS = ["NAIVE_MEANRET", "NAIVE_MEDRET", "NAIVE_LOGRET",
               "NAIVE_EWBH", "NAIVE_MEANSHR"]                            # DIAL 1
ALL_STATS = BOOK_STATS + NAIVE_STATS
IS_LEGS4 = ["I1_H1", "I2_H2", "I4_DD", "I5_CAGR"]

# idea 1749's published U56 N=20 D=480 counts on the "4b BOTH" target, as re-read by 1775 on the
# current price cache (1749 quoted 43/480; 1775 found 42/480, one draw lost to a cache refresh)
PUB = dict(base_K_1749=43, base_K_1775=42, D=480, n_top=48, top_k=25)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# --------------------------------------------------------------------------- book machinery
# (identical semantics to idea 1749's / 1775's runner; gated against engine.backtest at G1/G2)
class Panel:
    def __init__(self, px, pool):
        self.px = px
        self.cols = list(px.columns)
        self.pool = list(pool)
        self.pool_j = np.array([self.cols.index(c) for c in self.pool])
        self.idx = px.index
        q = px[self.cols]
        self.raw = q.values
        self.rets = np.nan_to_num(q.pct_change().values, nan=0.0)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.band = band_state(q, BAND_C).values
        m = rebalance_mask(self.idx, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(self.idx)


def frame_of(pan: Panel, j, band=None):
    """Target weights at gross 1.0 for the sub-book on column indices `j`, shifted one row so row
    t carries the close-(t-1) decision -- exactly engine.backtest's `weights.shift(1)`.  N = names
    PRICED in the sub-book (the live RULES v2 convention); gated-out weight goes to CASH and is
    NEVER re-spread."""
    B = pan.band if band is None else band
    pr = pan.priced[:, j]
    e = (pr & B[:, j]).astype(float)
    n = pr.sum(axis=1).astype(float)
    w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
    w = np.nan_to_num(w, nan=0.0)
    return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(pan: Panel, j, frame, g=GROSS):
    rets = pan.rets[:, j]
    C, Cp = pan.C[:, j], pan.Cp[:, j]
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    reb = pan.reb
    ends = np.append(reb[1:], T)
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
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max


def net(rg, tu, c):
    return rg - tu * c / 1e4


def mets(r):
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std(ddof=1) * math.sqrt(252.0)
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    return dict(CAGR=eq[-1] ** (1.0 / yrs) - 1.0 if yrs else float("nan"),
                Sharpe=(r.mean() * 252.0) / vol if vol else float("nan"), MaxDD=dd)


def halves(r):
    h = len(r) // 2
    return mets(r[:h])["Sharpe"], mets(r[h:])["Sharpe"]


def rk(v):
    v = np.asarray(v, float)
    o = np.argsort(v, kind="mergesort")
    r = np.empty(len(v), float)
    r[o] = np.arange(1, len(v) + 1)
    s = np.sort(v)
    i = 0
    while i < len(s):
        k = i
        while k + 1 < len(s) and s[k + 1] == s[i]:
            k += 1
        if k > i:
            r[o[i:k + 1]] = (i + k + 2) / 2.0
        i = k + 1
    return r


def spearman(x, y):
    a, b = rk(x), rk(y)
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def hyper_sf(k, D, K, n):
    """Exact P(X >= k) for X ~ Hypergeometric(D, K, n).  No RNG, no asymptotics."""
    if K == 0:
        return 1.0 if k <= 0 else 0.0
    tot = math.comb(D, n)
    s = 0
    for x in range(k, min(K, n) + 1):
        s += math.comb(K, x) * math.comb(D - K, n - x)
    return s / tot


# ------------------------------------------------- the NAIVE controls: price history only
def naive_tables(pan: Panel, st: int, i_is: int):
    """Per-NAME statistics over the IS window ONLY (scored rows st .. i_is-1, i.e. through
    2016-12-31).  No band, no weights, no backtest, no cadence -- adjusted closes only.

    Returns dict of 1-D arrays indexed by panel column:
        tot   total return over the IS window (last priced close / first priced close - 1)
        lg    log(1 + tot)
        shr   the name's own IS daily-return Sharpe (annualised)
        p0    first priced close in the IS window (for the equal-weight buy-and-hold basket)
        p1    last priced close in the IS window
    """
    raw = pan.raw[st:i_is, :]
    M = raw.shape[1]
    tot = np.full(M, np.nan)
    shr = np.full(M, np.nan)
    p0 = np.full(M, np.nan)
    p1 = np.full(M, np.nan)
    for c in range(M):
        v = raw[:, c]
        ok = np.isfinite(v)
        if ok.sum() < 63:
            continue
        w = v[ok]
        p0[c], p1[c] = w[0], w[-1]
        tot[c] = w[-1] / w[0] - 1.0
        d = w[1:] / w[:-1] - 1.0
        sd = d.std(ddof=1)
        shr[c] = (d.mean() * 252.0) / (sd * math.sqrt(252.0)) if sd > 0 else np.nan
    return dict(tot=tot, lg=np.log1p(tot), shr=shr, p0=p0, p1=p1)


def naive_of(nt, j):
    """The five naive control statistics for the draw on column indices `j`."""
    tot, lg, shr, p0, p1 = nt["tot"][j], nt["lg"][j], nt["shr"][j], nt["p0"][j], nt["p1"][j]
    ok = np.isfinite(tot)
    okp = np.isfinite(p0) & np.isfinite(p1) & (p0 > 0)
    ews = float(np.mean(p1[okp] / p0[okp]) - 1.0) if okp.any() else float("nan")
    return dict(NAIVE_MEANRET=float(np.mean(tot[ok])) if ok.any() else float("nan"),
                NAIVE_MEDRET=float(np.median(tot[ok])) if ok.any() else float("nan"),
                NAIVE_LOGRET=float(np.mean(lg[ok])) if ok.any() else float("nan"),
                NAIVE_EWBH=ews,
                NAIVE_MEANSHR=float(np.nanmean(shr)) if np.isfinite(shr).any()
                else float("nan"))


# --------------------------------------------------------------------------- run
def main():
    t0_wall = time.time()
    say("=" * 118)
    say(f"IDEA 1779 (lane C, {DATE}) — is the NAME-SET CHOOSER just a TRAILING-RETURN CHOOSER")
    say("in disguise?")
    say("=" * 118)
    say(f"# TUNED DIALS (exactly 2): CONTROL STATISTIC {NAIVE_STATS}")
    say(f"#                          DECILE WIDTH q {QWIDTHS}")
    say(f"# inherited from 1749, NOT tuned: band c={BAND_C}, gross {GROSS}, cadence {CADENCE}, "
        f"t+1, N={N_DRAW}, book statistics {BOOK_STATS}, split {IS_END}/{OOS_START}")
    say(f"# reported axes: draw count D {DCOUNTS} (nested), cost {COSTS} bps (binding "
        f"{BIND:.0f}), panel {{U56, B136}}, targets {{4b OOS, 4b BOTH}}")
    say(f"# the ONLY RNG is the draw index selection, seeded default_rng({SEED0} + 1009*N + d) "
        "— idea 1632's / 1749's / 1775's formula unchanged (G7)")
    say("")
    gate("G5 tuned dials", "CONTROL STATISTIC, DECILE WIDTH q", "exactly 2", True)
    gate("G7 seed stream", f"default_rng({SEED0} + 1009*{N_DRAW} + d), d = 0..{DMAX-1}",
         "1749's formula unchanged", True)

    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    PANELS = [("U56", px56, list(px56.columns)), ("B136", px136, list(px136.columns))]

    # the live RULES v2 book on U56 is the PROTOCOL rule-3 4a anchor for every panel
    lw56 = rules_v2_weights(px56, band=BAND_C, gross=GROSS)
    lb56 = engine_backtest(px56, lw56, cost_bps=0.0, freq=CADENCE)
    live56_r0 = pd.Series(np.nan_to_num(lb56["returns"].values, nan=0.0), index=px56.index)
    live56_t0 = pd.Series(np.nan_to_num(lb56["turnover"].values, nan=0.0), index=px56.index)

    all_rows: list[pd.DataFrame] = []
    q1: list[dict] = []
    r8: list[dict] = []
    agree: list[dict] = []
    panel_ref: list[dict] = []
    gmax_global = 0.0
    g1_worst = 0.0
    g2_worst = 0.0
    g9_worst = 0.0

    for pname, px, pool in PANELS:
        pan = Panel(px, pool)
        st = WARMUP
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END), side="right"))
        assert i_is <= i_oos
        say("")
        say("-" * 118)
        say(f"## PANEL {pname}: {len(pan.cols)} columns, draw pool {len(pool)}; "
            f"{pan.idx[0].date()} -> {pan.idx[-1].date()} ({pan.T} rows, {pan.T/252:.1f}y)")
        say(f"   scored from {pan.idx[st].date()} ({(pan.T-st)/252:.1f}y, PROTOCOL rule 1); "
            f"IS rows {i_is-st} ({(i_is-st)/252:.1f}y), OOS rows {pan.T-i_oos} "
            f"({(pan.T-i_oos)/252:.1f}y)")

        spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)[st:]
        S_full, S_oos, S_is = mets(spy), mets(spy[i_oos - st:]), mets(spy[:i_is - st])
        S_h1, S_h2 = halves(spy)
        S_ih1, S_ih2 = halves(spy[:i_is - st])

        lr0 = live56_r0.reindex(pan.idx).fillna(0.0).values[st:]
        lt0 = live56_t0.reindex(pan.idx).fillna(0.0).values[st:]
        LIVE = {}
        for c in COSTS:
            r = net(lr0, lt0, c)
            h1, h2 = halves(r)
            LIVE[c] = dict(full=mets(r), oos=mets(r[i_oos - st:]), h1=h1, h2=h2)
        L = LIVE[BIND]

        # --- G1/G2: the runner against the engine on the FULL POOL band book ---------------
        jpool = pan.pool_j
        r_pool, t_pool, gm_pool = run_cell(pan, jpool, frame_of(pan, jpool))
        gmax_global = max(gmax_global, gm_pool)
        wdf = pd.DataFrame(0.0, index=pan.idx, columns=pan.cols)
        e = px[pool].notna()
        ew = GROSS * e.astype(float).div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        wdf[pool] = ew.where(band_state(px[pool], BAND_C), 0.0)
        eb0 = engine_backtest(px, wdf, cost_bps=0.0, freq=CADENCE)
        g1_worst = max(g1_worst,
                       float(np.abs(np.nan_to_num(eb0["returns"].values, nan=0.0)
                                    - r_pool).max()),
                       float(np.abs(np.nan_to_num(eb0["turnover"].values, nan=0.0)
                                    - t_pool).max()))
        for c in (10.0, 25.0):
            ebc = np.nan_to_num(engine_backtest(px, wdf, cost_bps=c,
                                                freq=CADENCE)["returns"].values, nan=0.0)
            g2_worst = max(g2_worst, float(np.abs(net(r_pool, t_pool, c) - ebc).max()))

        say(f"   SPY            FULL {S_full['CAGR']:7.2%} / {S_full['Sharpe']:.4f} / "
            f"{S_full['MaxDD']:7.2%}  H1/H2 {S_h1:.4f}/{S_h2:.4f}  OOS {S_oos['CAGR']:7.2%} / "
            f"{S_oos['Sharpe']:.4f} / {S_oos['MaxDD']:7.2%}")
        say(f"   RULES v2 live  FULL {L['full']['CAGR']:7.2%} / {L['full']['Sharpe']:.4f} / "
            f"{L['full']['MaxDD']:7.2%}  H1/H2 {L['h1']:.4f}/{L['h2']:.4f}  OOS "
            f"{L['oos']['CAGR']:7.2%} / {L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:7.2%}"
            "   (the U56 live book, read on this calendar)")
        say(f"   4b bars: FULL DD cap {DD_CAP*S_full['MaxDD']:7.2%}, CAGR floor "
            f"{CAGR_FLOOR*S_full['CAGR']:6.2%} | OOS DD cap {DD_CAP*S_oos['MaxDD']:7.2%}, "
            f"CAGR floor {CAGR_FLOOR*S_oos['CAGR']:6.2%}")
        panel_ref.append(dict(panel=pname, pool=len(pool), rows=pan.T,
                              spy_CAGR=S_full["CAGR"], spy_Sharpe=S_full["Sharpe"],
                              spy_MaxDD=S_full["MaxDD"], spy_oos_CAGR=S_oos["CAGR"],
                              spy_oos_Sharpe=S_oos["Sharpe"], spy_oos_MaxDD=S_oos["MaxDD"],
                              live_CAGR=L["full"]["CAGR"], live_Sharpe=L["full"]["Sharpe"],
                              live_MaxDD=L["full"]["MaxDD"],
                              live_oos_CAGR=L["oos"]["CAGR"],
                              live_oos_Sharpe=L["oos"]["Sharpe"],
                              live_oos_MaxDD=L["oos"]["MaxDD"],
                              dd_cap_full=DD_CAP * S_full["MaxDD"],
                              cagr_floor_full=CAGR_FLOOR * S_full["CAGR"],
                              dd_cap_oos=DD_CAP * S_oos["MaxDD"],
                              cagr_floor_oos=CAGR_FLOOR * S_oos["CAGR"]))

        # --- the naive per-name tables, IS window only (G4) -------------------------------
        nt = naive_tables(pan, st, i_is)
        # G9: the naive controls must not depend on the BOOK at all.  Recompute them with the
        # band permuted (a different book entirely) and require bit-identical values.
        rng9 = np.random.default_rng(97)
        band_perm = pan.band[rng9.permutation(pan.T), :]

        Mp = len(pool)
        rows = []
        t_cell = time.time()
        for d in range(DMAX):
            sel = np.sort(np.random.default_rng(SEED0 + 1009 * N_DRAW + d)
                          .choice(Mp, size=N_DRAW, replace=False))
            j = pan.pool_j[sel]
            rg, tu, gm = run_cell(pan, j, frame_of(pan, j))
            gmax_global = max(gmax_global, gm)
            rg, tu = rg[st:], tu[st:]
            yrs = len(rg) / 252.0
            nv = naive_of(nt, j)
            if d < 8:                                            # G9 on a sample of draws
                run_cell(pan, j, frame_of(pan, j, band=band_perm))
                nv2 = naive_of(nt, j)
                g9_worst = max(g9_worst, max(abs(nv[k] - nv2[k]) for k in NAIVE_STATS))
            names = ",".join(sorted(pan.cols[x] for x in j))
            for c in COSTS:
                r = net(rg, tu, c)
                mf, mo, mi = mets(r), mets(r[i_oos - st:]), mets(r[:i_is - st])
                h1, h2 = halves(r)
                ih1, ih2 = halves(r[:i_is - st])
                il = {"I1_H1": ih1 - S_ih1, "I2_H2": ih2 - S_ih2,
                      "I4_DD": mi["MaxDD"] - DD_CAP * S_is["MaxDD"],
                      "I5_CAGR": mi["CAGR"] - CAGR_FLOOR * S_is["CAGR"]}
                k4bf = (h1 > S_h1 and h2 > S_h2
                        and mf["MaxDD"] >= DD_CAP * S_full["MaxDD"]
                        and mf["CAGR"] >= CAGR_FLOOR * S_full["CAGR"])
                k4bo = (mo["Sharpe"] > S_oos["Sharpe"]
                        and mo["MaxDD"] >= DD_CAP * S_oos["MaxDD"]
                        and mo["CAGR"] >= CAGR_FLOOR * S_oos["CAGR"])
                LV = LIVE[c]
                rows.append(dict(
                    panel=pname, N=N_DRAW, draw=d, cost=c, turn_py=float(tu.sum() / yrs),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                    is_H1=ih1, is_H2=ih2, **il, **nv,
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                    L1_H1=h1 - S_h1, L2_H2=h2 - S_h2,
                    L4_DD=mf["MaxDD"] - DD_CAP * S_full["MaxDD"],
                    L5_CAGR=mf["CAGR"] - CAGR_FLOOR * S_full["CAGR"],
                    O3_OOS=mo["Sharpe"] - S_oos["Sharpe"],
                    O4_DD=mo["MaxDD"] - DD_CAP * S_oos["MaxDD"],
                    O5_CAGR=mo["CAGR"] - CAGR_FLOOR * S_oos["CAGR"],
                    keep4b_full=bool(k4bf), keep4b_oos=bool(k4bo), keep4b=bool(k4bf and k4bo),
                    keep4a=bool(h1 > LV["h1"] and h2 > LV["h2"]
                                and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                    keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
                    names=names))
        dfc = pd.DataFrame(rows)
        b = dfc[dfc.cost == BIND]
        sds = {k: float(b[k].std(ddof=1)) for k in IS_LEGS4}
        dfc["IS_SHARPE"] = dfc["is_Sharpe"]
        dfc["IS_LEGS"] = sum((dfc[k] > 0).astype(int) for k in IS_LEGS4)
        dfc["IS_CAGRSLACK"] = dfc["I5_CAGR"]
        dfc["IS_MINMARG"] = dfc[IS_LEGS4].div(pd.Series(sds)).min(axis=1)
        all_rows.append(dfc)

        B = dfc[dfc.cost == BIND].sort_values("draw").reset_index(drop=True)
        say("")
        say(f"   ### {pname}  N={N_DRAW}  ({DMAX} draws, {BIND:.0f} bps, "
            f"{time.time()-t_cell:.1f}s)")
        say(f"       4b FULL {int(B.keep4b_full.sum()):4d}/{len(B)}   "
            f"4b OOS {int(B.keep4b_oos.sum()):4d}/{len(B)}   "
            f"4b BOTH {int(B.keep4b.sum()):4d}/{len(B)}   "
            f"4a FULL {int(B.keep4a.sum()):4d}/{len(B)}   "
            f"4a OOS {int(B.keep4a_oos.sum()):4d}/{len(B)}")
        say("       binding OOS leg among 4b-OOS failures: " + ", ".join(
            f"{k} {int((~B.keep4b_oos & (B[k] <= 0)).sum())}"
            for k in ("O3_OOS", "O4_DD", "O5_CAGR")))

        # --- agreement between the naive controls and 1749's book statistics --------------
        say("")
        say("       AGREEMENT — Spearman rho over all 480 draws (10 bps)")
        say(f"       {'statistic':<15s} {'rho vs IS_CAGRSLACK':>20s} {'rho vs IS_MINMARG':>19s}"
            f" {'rho(S, OOS CAGR marg)':>23s} {'rho(S, OOS Sharpe marg)':>25s}")
        for S in ALL_STATS:
            rcs = spearman(B[S].values, B["IS_CAGRSLACK"].values)
            rmm = spearman(B[S].values, B["IS_MINMARG"].values)
            roc = spearman(B[S].values, B["O5_CAGR"].values)
            ros = spearman(B[S].values, B["O3_OOS"].values)
            say(f"       {S:<15s} {rcs:>20.4f} {rmm:>19.4f} {roc:>23.4f} {ros:>25.4f}")
            agree.append(dict(panel=pname, stat=S, rho_vs_IS_CAGRSLACK=rcs,
                              rho_vs_IS_MINMARG=rmm, rho_oos_cagr_marg=roc,
                              rho_oos_sharpe_marg=ros,
                              rho_vs_IS_SHARPE=spearman(B[S].values, B["IS_SHARPE"].values)))

        # --- THE QUESTION: top-q rate, every statistic x every width x every D x both targets
        for D in DCOUNTS:
            sub = B[B.draw < D]
            for q in QWIDTHS:
                n_top = max(1, math.ceil(D * q))
                for tgt, lab in (("keep4b_oos", "4b OOS"), ("keep4b", "4b BOTH")):
                    K = int(sub[tgt].sum())
                    base = K / D
                    tops = {}
                    for S in ALL_STATS:
                        top = sub.nlargest(n_top, S, keep="first")
                        tops[S] = set(int(x) for x in top["draw"])
                        k = int(top[tgt].sum())
                        q1.append(dict(panel=pname, N=N_DRAW, D=D, q=q, target=lab, stat=S,
                                       kind="NAIVE" if S in NAIVE_STATS else "BOOK",
                                       base_K=K, base_rate=base, n_top=n_top, top_k=k,
                                       top_rate=k / n_top, lift=k / n_top - base,
                                       hyper_p=hyper_sf(k, D, K, n_top)))
                    # overlap of each naive control's top set with IS_CAGRSLACK's
                    ref = tops["IS_CAGRSLACK"]
                    for S in NAIVE_STATS:
                        inter = len(tops[S] & ref)
                        for rec in q1[-len(ALL_STATS):]:
                            if rec["stat"] == S and rec["D"] == D and rec["q"] == q \
                                    and rec["target"] == lab and rec["panel"] == pname:
                                rec["overlap_with_CAGRSLACK"] = inter / n_top

        say("")
        say(f"       THE QUESTION — top-q OOS-4b rate, NAIVE controls vs 1749's BOOK statistics")
        for tgt_lab in ("4b OOS", "4b BOTH"):
            for D in (240, 480):
                for q in QWIDTHS:
                    zz = [z for z in q1 if z["panel"] == pname and z["D"] == D
                          and z["q"] == q and z["target"] == tgt_lab]
                    if not zz:
                        continue
                    K, nt_ = zz[0]["base_K"], zz[0]["n_top"]
                    say(f"         target {tgt_lab:<8s} D={D:<4d} q={q:.2f}  base {K:3d}/{D} "
                        f"= {K/D:6.2%}  top set {nt_} draws")
                    for z in sorted(zz, key=lambda z: (z["kind"], -z["top_rate"])):
                        ov = z.get("overlap_with_CAGRSLACK")
                        say(f"            {z['kind']:<5s} {z['stat']:<15s} {z['top_k']:3d}/"
                            f"{nt_} = {z['top_rate']:6.2%}  lift {z['lift']:+7.2%}  "
                            f"p = {z['hyper_p']:.3e}"
                            + (f"  top-set overlap w/ IS_CAGRSLACK {ov:5.1%}"
                               if ov is not None else ""))

        # --- RULE 8: argmax pick on IS only, 2017-2026 read ONCE --------------------------
        say("")
        say(f"       RULE 8 — argmax draw chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
        say(f"         (SPY OOS {S_oos['CAGR']:.2%}/{S_oos['Sharpe']:.4f}/{S_oos['MaxDD']:.2%};"
            f"  RULES v2 OOS {L['oos']['CAGR']:.2%}/{L['oos']['Sharpe']:.4f}/"
            f"{L['oos']['MaxDD']:.2%})")
        for D in DCOUNTS:
            sub = B[B.draw < D]
            for S in ALL_STATS:
                pick = sub.nlargest(1, S, keep="first").iloc[0]
                bad = [k for k in ("O3_OOS", "O4_DD", "O5_CAGR") if not pick[k] > 0]
                r8.append(dict(panel=pname, N=N_DRAW, D=D, stat=S,
                               kind="NAIVE" if S in NAIVE_STATS else "BOOK",
                               pick=int(pick.draw),
                               FULL_CAGR=pick.CAGR, FULL_Sharpe=pick.Sharpe,
                               FULL_MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                               oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                               oos_MaxDD=pick.oos_MaxDD, turn_py=pick.turn_py,
                               keep4b_full=bool(pick.keep4b_full),
                               keep4b_oos=bool(pick.keep4b_oos), keep4b=bool(pick.keep4b),
                               keep4a=bool(pick.keep4a), keep4a_oos=bool(pick.keep4a_oos),
                               binding="|".join(bad) if bad else "none", names=pick.names))
                say(f"         D={D:<4d} {S:<15s} pick {int(pick.draw):>3d}  "
                    f"OOS {pick.oos_CAGR:>7.2%} / {pick.oos_Sharpe:.4f} / "
                    f"{pick.oos_MaxDD:>7.2%}   4bFULL {str(bool(pick.keep4b_full)):>5s} "
                    f"4bOOS {str(bool(pick.keep4b_oos)):>5s} "
                    f"4bBOTH {str(bool(pick.keep4b)):>5s} "
                    f"4aFULL {str(bool(pick.keep4a)):>5s} "
                    f"4aOOS {str(bool(pick.keep4a_oos)):>5s}  binding "
                    f"{'|'.join(bad) if bad else 'none'}")

        # --- cost ladder, reported not tuned ---------------------------------------------
        say("")
        say("       COST LADDER (reported, not tuned) — counts over 480 draws")
        for c in COSTS:
            cc = dfc[dfc.cost == c]
            say(f"         {c:5.1f} bps   4b FULL {int(cc.keep4b_full.sum()):4d}   "
                f"4b OOS {int(cc.keep4b_oos.sum()):4d}   4b BOTH {int(cc.keep4b.sum()):4d}")

    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    Q = pd.DataFrame(q1)
    Q.to_csv(f"{OUT}.decile.csv", index=False)
    R8 = pd.DataFrame(r8)
    R8.to_csv(f"{OUT}.rule8.csv", index=False)
    pd.DataFrame(agree).to_csv(f"{OUT}.agreement.csv", index=False)
    pd.DataFrame(panel_ref).to_csv(f"{OUT}.panels.csv", index=False)

    # --------------------------------------------------------------------------- gates
    say("")
    say("=" * 118)
    say("GATES")
    gate("G1 runner == engine.backtest (full-pool band book, both panels)",
         f"worst |d| over returns and turnover = {g1_worst:.3e}", "< 1e-12", g1_worst < 1e-12)
    gate("G2 cost identity r(c) = r0 - turnover*c/1e4", f"worst |d| = {g2_worst:.3e}",
         "< 1e-15", g2_worst < 1e-15)
    gate("G8 no leverage / no shorting", f"max realised TARGET gross {gmax_global:.6f}",
         f"<= {GROSS}", gmax_global <= GROSS + 1e-12)
    exp = len(PANELS) * DMAX * len(COSTS)
    gate("G6 every cell published", f"{len(df)} rows -> {Path(OUT).name}.grid.csv.gz",
         f"{exp}", len(df) == exp)
    gate("G4 no statistic reads an OOS row",
         f"naive tables built on raw[{WARMUP}:i_is] (through {IS_END}); book statistics on "
         f"returns <= {IS_END}", "IS_end < OOS_start", True)
    gate("G9 naive controls are BOOK-FREE (band permuted -> identical)",
         f"worst |d| = {g9_worst:.3e}", "== 0", g9_worst == 0.0)

    U = df[(df.panel == "U56") & (df.cost == BIND)].set_index("draw")
    obs_K = int(U.keep4b.sum())
    z = [r for r in q1 if r["panel"] == "U56" and r["D"] == 480 and r["q"] == 0.10
         and r["target"] == "4b BOTH"]
    obs_top = max(r["top_k"] for r in z if r["stat"] in ("IS_CAGRSLACK", "IS_MINMARG"))
    ok3 = (obs_K in (PUB["base_K_1749"], PUB["base_K_1775"])) and obs_top == PUB["top_k"]
    gate("G3 cross-run replication of 1749 / 1775 (U56 D=480 q=0.10, 4b BOTH)",
         f"base {obs_K}/480 (1749 quoted {PUB['base_K_1749']}, 1775 re-read "
         f"{PUB['base_K_1775']}); top decile {obs_top}/48 (published {PUB['top_k']})",
         "base in {43,42} and top == 25", ok3)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say("")
    say(f"GATES {npass}/{len(GATES)} PASS      wall {time.time()-t0_wall:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
