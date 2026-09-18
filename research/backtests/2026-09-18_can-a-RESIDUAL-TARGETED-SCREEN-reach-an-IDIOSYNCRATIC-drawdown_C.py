#!/usr/bin/env python3
"""
Idea 1317 (lane C, 2026-09-18) — can a RESIDUAL-TARGETED SCREEN reach an IDIOSYNCRATIC
drawdown where a TOTAL-VOL SCREEN cannot?

THE PREMISE, READ FROM THE RECORD.  Idea 1301 split the SMALL incumbent's own worst
peak-to-trough (368 days, -33.35%) at beta 0.658 into 21.2% systematic / 78.8% RESIDUAL, and
found the residual stream's standalone MaxDD (-44.68%) is nearly twice beta*SPY's (-23.18%).
Idea 1297 showed the EXPOSURE dial cannot reach the -20.23% cap (a gross multiplier scales
both parts by the same k) and 1301 showed SELECTION on (N, H) cannot either (0 of 24 cells).
What NEITHER run touched is the screen itself: the incumbent's only risk filter is
`vol20 < 0.60`, a TOTAL-vol bar that mostly prices the SYSTEMATIC part of a name's variance.
If the binding risk is idiosyncratic, the screen that prices idiosyncratic risk should be the
one that moves the leg.  This run swaps it and measures.

THE SWAP.  For each name i and each trailing WINDOW w, fit beta_i by OLS on that window's
daily returns against SPY and take the residual standard deviation exactly:
    beta = cov(r_i, spy) / var(spy),   resid_var = var(r_i) - cov(r_i, spy)^2 / var(spy)
    RESID_VOL = sqrt(252 * max(resid_var, 0))                       [= sd of r - beta*spy]
Admit name i at t iff it is above its 200d average (unchanged) AND its RESID_VOL sits in the
lowest RESID_MAX fraction of that day's ABOVE-200d, priced, measurable cross-section.  The
percentile is taken over the candidate set the screen actually filters — the above-200d names
— and not over the whole panel, because that is the set whose size has to be matched between
the two arms for the comparison below to mean anything.

MATCHED ADMISSION COUNTS — the control arm, not a dial.  Every RESID cell is run beside a
TOTAL cell that ranks TOTAL_VOL over the SAME window at the SAME percentile.  The screen is
built as "admit the k LOWEST by the statistic, k = floor(p * n_candidates(t))", where
n_candidates(t) is the count of names that are above their 200d average, priced, and have
BOTH statistics that day, with ties broken by a stable first-seen order.  A percentile BAR
would not do: resid_var is clipped at zero and ties at the floor differ between the two
statistics, so a `pct_rank <= p` bar on the whole panel admits up to 18 more ELIGIBLE names on
one arm than the other (measured on this run's first pass; that is why the screen is written
in the count form over the candidate set).  Under this form the two screens admit EXACTLY the
same number of names on every single day — gate G1 asserts max |difference| == 0 — so the only
thing that differs between the two books is WHICH names.  That isolates residual-vs-total from window length,
from admission breadth, and from percentile-vs-absolute bar.  The incumbent's own
`vol20 < 0.60` book is the frozen third arm, and its realised admission share is published
so "matched" is a measured claim, not an assertion.

EXACTLY TWO TUNED PARAMETERS (PROTOCOL rule 4), every grid point reported:
    WINDOW      {63, 126, 252}
    RESID_MAX   {0.5, 0.7, 0.9}     (cross-sectional percentile)
NOT DIALS, reported at every value: SCREEN {RESID, TOTAL, INCUMBENT}, PANEL {U56, B136,
SMALL663}, both KEEP paths at every cell, IS/OOS windows, halves.

EVERYTHING ELSE IS THE FROZEN INCUMBENT: 3-leg composite (21/252, 0/126, 0/63) as the rank
key, above-200d eligibility, N=15, H=126 min-hold, GROSS=0.60, weekly cadence, decide-at-t /
apply-at-t+1 (rule 2), warm-up 260 rows, 10 bps (rule 2's rung).

PROTOCOL: rule 1 (>= 10y, gate G0); rule 2; rule 3 (vs live RULES v2 AND SPY); rule 4 (both
KEEP paths, 2 dials); rule 8 walk-forward — (WINDOW, RESID_MAX) chosen on warm-up..2016-12-31
by argmax IS Sharpe, 2017-2026 read ONCE, run separately for RESID and for the TOTAL control;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

SMALL PANEL (house filter): data/small_meta.csv, drop every ticker with max_1d_move >= 1.0.
SURVIVORSHIP: current constituents of a sub-$2B screen carried back to 2010, so every
absolute level on SMALL is biased UP and any 4b pass there would be an upper bound.  The
RESID-vs-TOTAL difference is read on the SAME names and days, so a common level bias moves
both arms together.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-18_can-a-RESIDUAL-TARGETED-SCREEN-reach-an-IDIOSYNCRATIC-drawdown_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "can-a-RESIDUAL-TARGETED-SCREEN-reach-an-IDIOSYNCRATIC-drawdown"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"          # the incumbent, frozen
WINDOWS = [63, 126, 252]                          # DIAL 1
PCTS = [0.5, 0.7, 0.9]                            # DIAL 2
SCREENS = ["RESID", "TOTAL"]                      # control arm, not a dial
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# committed comparands (replay gates; nothing is tuned on them)
C_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)     # 1215 / 1297 / 1301, U56 incumbent
C_SMALL_DDCAP, C_SMALL_FLOOR = -0.2023, 0.0984              # 1301 / 1297 committed SMALL bars
C_1301_SMALL = dict(CAGR=0.070580, Sharpe=0.5202, MaxDD=-0.333508)   # 1301's house-663 incumbent
C_1301_SHALLOWEST_DD = -0.2869      # 1301's best SELECTION cell on SMALL (N=30/H=63)
C_1297_SMALL_BEST_DD = -0.2243      # 1297's best EXPOSURE cell on SMALL

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")
    return bool(ok)


# ==================================================================== panel machinery
def mech(q):
    """The record's rank key and its two incumbent eligibility inputs."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def vol_pair(q, w):
    """TOTAL and RESIDUAL annualised vol over a trailing window of w days, per name.

    resid_var = var(r) - cov(r, spy)^2 / var(spy)  is exactly the variance of r - beta*spy
    with beta fit by OLS on the same window, so RESID_VOL is the trailing sd the idea asks
    for.  Both statistics require w observations, so they are NaN on identical (t, i) and the
    percentile screens built from them admit the same COUNT every day."""
    r = q.pct_change()
    s = r["SPY"] if "SPY" in r.columns else None
    assert s is not None
    R = r.drop(columns=["SPY"])
    mx = R.rolling(w).mean()
    my = s.rolling(w).mean()
    mxy = R.mul(s, axis=0).rolling(w).mean()
    mxx = (R * R).rolling(w).mean()
    myy = (s * s).rolling(w).mean()
    n = w / (w - 1.0)
    cov = (mxy.sub(mx.mul(my, axis=0))) * n
    var_r = (mxx - mx * mx) * n
    var_s = (myy - my * my) * n
    beta = cov.div(var_s, axis=0)
    resid_var = var_r - cov.pow(2).div(var_s, axis=0)
    tot = np.sqrt(var_r.clip(lower=0) * 252.0)
    res = np.sqrt(resid_var.clip(lower=0) * 252.0)
    return tot, res, beta


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sub = px[invest]
        sc, above, vol20 = mech(sub)
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.above = above
        self.elig_inc = above & (vol20 < MAXVOL)          # the incumbent screen, frozen
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.lo = WARMUP
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.i_ise = int(np.searchsorted(px.index.values, np.datetime64(IS_END), side="right"))
        # the two screens, one matched pair per window, ranked over the ABOVE-200d candidates
        self.screen, self.nvalid = {}, {}
        keep = list(invest) + ["SPY"]
        cand0 = above & self.priced[:, self.iinv]
        BIG = np.iinfo(np.int32).max
        for w in WINDOWS:
            tot, res, _ = vol_pair(px[keep], w)
            T_, K_ = tot.shape
            A, B = tot.values, res.values
            cand = cand0 & np.isfinite(A) & np.isfinite(B)   # identical for both arms (G1b)
            self.nvalid[w] = cand.sum(axis=1)
            for kind, V in (("TOTAL", A), ("RESID", B)):
                X = np.where(cand, V, np.inf)
                order = np.argsort(X, axis=1, kind="stable")     # ties -> first-seen, stable
                pos = np.empty((T_, K_), dtype=np.int32)
                np.put_along_axis(pos, order, np.arange(K_, dtype=np.int32)[None, :], axis=1)
                self.screen[(kind, w)] = np.where(cand, pos, BIG)


def elig_for(pan, kind, w=None, p=None):
    """Admit the k LOWEST candidates by the screen's statistic, k = floor(p * n_candidates(t)),
    the candidate set being the above-200d, priced, measurable names.  Both arms share that set,
    so both admit exactly k names on every day."""
    if kind == "INCUMBENT":
        return pan.elig_inc
    k = np.floor(p * pan.nvalid[w]).astype(np.int64)
    return pan.screen[(kind, w)] < k[:, None]


# ==================================================================== the book
def build1(pan, elig, N=I_N, H=I_H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight.  Identical to idea 1301's builder
    except that the eligibility mask is passed in rather than frozen."""
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_const(pan, frame, g=I_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def dd_episode(r):
    e = np.cumprod(1 + np.asarray(r, float))
    dd = e / np.maximum.accumulate(e) - 1.0
    j = int(np.argmin(dd))
    i = int(np.argmax(e[: j + 1]))
    return i, j, float(dd[j])


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def annturn(tu):
    return float(np.sum(tu) * 252.0 / len(tu)) if len(tu) else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def decompose(r, spy):
    """Exact additive split of the worst peak-to-trough episode into beta*SPY and residual."""
    r = np.asarray(r, float)
    s = np.asarray(spy, float)
    b, a = np.polyfit(s, r, 1)
    beta_only = b * s
    idio = r - beta_only
    i, j, depth = dd_episode(r)
    seg = slice(i + 1, j + 1)
    tot = r[seg].sum()
    sy, id_ = beta_only[seg].sum(), idio[seg].sum()
    return dict(beta=float(b), R2=float(np.corrcoef(r, s)[0, 1] ** 2),
                MaxDD_book=mdd(r), MaxDD_beta_spy=mdd(beta_only), MaxDD_idio=mdd(idio),
                ep_days=int(j - i), ep_depth=depth,
                ep_share_beta_spy=float(sy / tot) if tot else np.nan,
                ep_share_idio=float(id_ / tot) if tot else np.nan,
                ep_sum_r=float(tot), ep_sum_beta_spy=float(sy), ep_sum_idio=float(id_))


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1317 (lane C, 2026-09-18) — can a RESIDUAL-TARGETED SCREEN reach an")
    say("IDIOSYNCRATIC drawdown where a TOTAL-VOL SCREEN cannot?")
    say("=" * 100)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    say(f"  SMALL filter (house rule): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable of {len(pxS.columns)-1} priced")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances, "
            f"{len(p.invest)} names, OOS from row {p.i_oos}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ---------------------------------------------------------------- benchmarks per panel
    say("")
    say("-" * 100)
    say("BENCHMARKS (rule 3) — SPY and the LIVE RULES v2 book, per panel, full and OOS")
    say("-" * 100)
    bm, live, bm_oos, live_oos = {}, {}, {}, {}
    for p in panels:
        lo = p.lo
        spy = p.spy[lo:]
        bm[p.name] = bmpack(spy)
        bres = backtest(p.px, rules_v2_weights(p.px), cost_bps=COST, freq="W")
        lr = bres["returns"].fillna(0.0).values[lo:]
        live[p.name] = bmpack(lr)
        o = p.i_oos - lo
        bm_oos[p.name] = bmpack(spy[o:])
        live_oos[p.name] = bmpack(lr[o:])
        say(f"  {p.name:9s} SPY  {bm[p.name]['CAGR']:7.2%} / {bm[p.name]['Sharpe']:.4f} / "
            f"{bm[p.name]['MaxDD']:7.2%}  (H1 {bm[p.name]['H1']:.4f} H2 {bm[p.name]['H2']:.4f}) "
            f"| 4b cap {DD_CAP*bm[p.name]['MaxDD']:7.2%} floor {CAGR_FLOOR*bm[p.name]['CAGR']:6.2%}")
        say(f"  {p.name:9s} v2   {live[p.name]['CAGR']:7.2%} / {live[p.name]['Sharpe']:.4f} / "
            f"{live[p.name]['MaxDD']:7.2%}  (H1 {live[p.name]['H1']:.4f} H2 {live[p.name]['H2']:.4f})")
        say(f"  {p.name:9s} OOS  SPY {bm_oos[p.name]['CAGR']:7.2%} / "
            f"{bm_oos[p.name]['Sharpe']:.4f} / {bm_oos[p.name]['MaxDD']:7.2%} | "
            f"v2 {live_oos[p.name]['CAGR']:7.2%} / {live_oos[p.name]['Sharpe']:.4f} / "
            f"{live_oos[p.name]['MaxDD']:7.2%}")

    # ---------------------------------------------------------------- admission census
    say("")
    say("-" * 100)
    say("ADMISSION COUNTS — is 'matched' a measured claim?  (post-warm-up daily mean of "
        "admitted names, and of the incumbent's own bar)")
    say("-" * 100)
    adm = []
    for p in panels:
        lo = p.lo
        pr = p.priced[:, p.iinv]
        inc = (p.elig_inc & pr)[lo:].sum(axis=1)
        # the incumbent's screen as a share of the ABOVE-200d set it filters
        ab = (p.above & pr)[lo:].sum(axis=1)
        share = float(np.nanmean(np.where(ab > 0, inc / np.maximum(ab, 1), np.nan)))
        say(f"  {p.name:9s} INCUMBENT vol20<{MAXVOL}: mean {inc.mean():7.1f} names/day "
            f"admitted of {ab.mean():7.1f} above-200d ({share:.3f} of them)")
        adm.append(dict(panel=p.name, screen="INCUMBENT", window=np.nan, pct=np.nan,
                        mean_admitted=float(inc.mean()), mean_above=float(ab.mean()),
                        share_of_above=share))
        for w in WINDOWS:
            for q in PCTS:
                counts = {}
                for kind in SCREENS:
                    e = elig_for(p, kind, w, q)
                    counts[kind] = (e & pr)[lo:].sum(axis=1)
                    adm.append(dict(panel=p.name, screen=kind, window=w, pct=q,
                                    mean_admitted=float(counts[kind].mean()),
                                    mean_above=float(ab.mean()),
                                    share_of_above=float(np.nanmean(np.where(
                                        ab > 0, counts[kind] / np.maximum(ab, 1), np.nan)))))
                d = int(np.abs(counts["RESID"] - counts["TOTAL"]).max())
                say(f"  {p.name:9s} w={w:3d} p={q:.1f}: RESID {counts['RESID'].mean():7.1f} "
                    f"TOTAL {counts['TOTAL'].mean():7.1f} names/day  "
                    f"max |daily count difference| = {d}")
    A = pd.DataFrame(adm)
    A.to_csv(f"{OUT}.admissions.csv", index=False)
    worst_gap = 0
    for p in panels:
        pr = p.priced[:, p.iinv]
        for w in WINDOWS:
            for q in PCTS:
                cr = (elig_for(p, "RESID", w, q) & pr)[p.lo:].sum(axis=1)
                ct = (elig_for(p, "TOTAL", w, q) & pr)[p.lo:].sum(axis=1)
                worst_gap = max(worst_gap, int(np.abs(cr - ct).max()))
    gate("G1 RESID and TOTAL screens admit MATCHED counts on every day and every cell",
         f"max |count difference| = {worst_gap}", "== 0", worst_gap == 0)
    BIG = np.iinfo(np.int32).max
    same_cand = all(bool(((p.screen[("RESID", w)] < BIG) == (p.screen[("TOTAL", w)] < BIG)).all())
                    for p in panels for w in WINDOWS)
    gate("G1b the two arms share the same candidate set on every (day, name)",
         same_cand, "True", same_cand)

    # ---------------------------------------------------------------- the grid
    say("")
    say("-" * 100)
    say(f"THE GRID — SCREEN {SCREENS} x WINDOW {WINDOWS} x RESID_MAX {PCTS}, plus the FROZEN "
        f"INCUMBENT arm,")
    say(f"at N={I_N} H={I_H} gross={I_G} cadence={I_C} {COST:.0f} bps on "
        f"{len(panels)} panels  ({(len(SCREENS)*len(WINDOWS)*len(PCTS)+1)*len(panels)} books)")
    say("-" * 100)
    rows, series = [], {}

    def add(p, kind, w, q, r, tu):
        h1, h2 = halves(r)
        m = triple(r)
        lv, b = live[p.name], bm[p.name]
        lo, o = p.lo, p.i_oos - p.lo
        ris, ros = r[: p.i_ise - lo], r[o:]
        mo = triple(ros)
        b4 = bm_oos[p.name]
        k4a = bool(h1 > lv["H1"] and h2 > lv["H2"] and m["MaxDD"] >= lv["MaxDD"])
        k4b = bool(h1 > b["H1"] and h2 > b["H2"]
                   and m["MaxDD"] >= DD_CAP * b["MaxDD"]
                   and m["CAGR"] >= CAGR_FLOOR * b["CAGR"])
        k4b_oos = bool(mo["Sharpe"] > b4["Sharpe"]
                       and mo["MaxDD"] >= DD_CAP * b4["MaxDD"]
                       and mo["CAGR"] >= CAGR_FLOOR * b4["CAGR"])
        rows.append(dict(
            panel=p.name, screen=kind, window=w, pct=q, N=I_N, H=I_H, gross=I_G,
            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
            turn=annturn(tu[lo:]),
            IS_Sharpe=sharpe(ris), IS_CAGR=cagr(ris), IS_MaxDD=mdd(ris),
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            dd_cap=DD_CAP * b["MaxDD"], cagr_floor=CAGR_FLOOR * b["CAGR"],
            oos_dd_cap=DD_CAP * b4["MaxDD"], oos_cagr_floor=CAGR_FLOOR * b4["CAGR"],
            keep4a=k4a, keep4b_full=k4b, keep4b_oos=k4b_oos,
            keep4b_both=bool(k4b and k4b_oos)))
        series[(p.name, kind, w, q)] = r

    for p in panels:
        gr, tu = run_const(p, build1(p, elig_for(p, "INCUMBENT")), I_G)
        add(p, "INCUMBENT", np.nan, np.nan, at_cost(gr, tu)[p.lo:], tu)
        for kind in SCREENS:
            for w in WINDOWS:
                for q in PCTS:
                    gr, tu = run_const(p, build1(p, elig_for(p, kind, w, q)), I_G)
                    add(p, kind, w, q, at_cost(gr, tu)[p.lo:], tu)
        say(f"  {p.name}: {1 + len(SCREENS)*len(WINDOWS)*len(PCTS)} books built")
    G = pd.DataFrame(rows)
    for p in panels:
        anc = G[(G.panel == p.name) & (G.screen == "INCUMBENT")].iloc[0]
        m = G.panel == p.name
        G.loc[m, "dMaxDD_pp"] = (G.loc[m, "MaxDD"] - anc["MaxDD"]) * 100
        G.loc[m, "dCAGR_pp"] = (G.loc[m, "CAGR"] - anc["CAGR"]) * 100
        G.loc[m, "dSharpe"] = G.loc[m, "Sharpe"] - anc["Sharpe"]
        with np.errstate(divide="ignore", invalid="ignore"):
            G.loc[m, "price"] = G.loc[m, "dMaxDD_pp"] / (-G.loc[m, "dCAGR_pp"])
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------------- replay gates
    say("")
    say("-" * 100)
    say("REPLAY GATES against committed numbers (nothing is tuned on them)")
    say("-" * 100)
    aU = G[(G.panel == "U56") & (G.screen == "INCUMBENT")].iloc[0]
    dU = max(abs(aU.CAGR - C_U56["CAGR"]), abs(aU.Sharpe - C_U56["Sharpe"]),
             abs(aU.MaxDD - C_U56["MaxDD"]))
    gate("G2 U56 incumbent replays 1215/1297/1301's 13.66% / 1.1706 / -16.38%",
         f"{aU.CAGR:.4%} / {aU.Sharpe:.4f} / {aU.MaxDD:.4%} (max|dev| {dU:.2e})",
         "max|dev| <= 5e-3", dU <= 5e-3)
    aS = G[(G.panel == "SMALL663") & (G.screen == "INCUMBENT")].iloc[0]
    dS = max(abs(aS.CAGR - C_1301_SMALL["CAGR"]), abs(aS.Sharpe - C_1301_SMALL["Sharpe"]),
             abs(aS.MaxDD - C_1301_SMALL["MaxDD"]))
    gate("G3 SMALL663 incumbent replays 1301's 7.0580% / 0.5202 / -33.3508%",
         f"{aS.CAGR:.4%} / {aS.Sharpe:.4f} / {aS.MaxDD:.4%} (max|dev| {dS:.2e})",
         "max|dev| <= 5e-3", dS <= 5e-3)
    capS = DD_CAP * bm["SMALL663"]["MaxDD"]
    flS = CAGR_FLOOR * bm["SMALL663"]["CAGR"]
    gate("G4 SMALL 4b DD cap replays the record's -20.23%", f"{capS:.4%}",
         "|dev| <= 2e-3", abs(capS - C_SMALL_DDCAP) <= 2e-3)
    gate("G5 SMALL 4b CAGR floor replays the record's 9.84%", f"{flS:.4%}",
         "|dev| <= 2e-3", abs(flS - C_SMALL_FLOOR) <= 2e-3)
    # the residual statistic is exactly the sd of r - beta*spy (checked directly on one name)
    nm = [c for c in pxU.columns if c != "SPY"][0]     # U56: full history, no gaps
    tot, res, beta = vol_pair(pxU[[nm, "SPY"]], 126)
    rr = pxU[[nm, "SPY"]].pct_change()
    t_ = 2000
    seg = rr.iloc[t_ - 126 + 1: t_ + 1]
    b_ = np.polyfit(seg["SPY"].values, seg[nm].values, 1)[0]
    e_ = seg[nm].values - b_ * seg["SPY"].values
    direct = float(np.std(e_, ddof=1) * np.sqrt(252))
    got = float(res.iloc[t_, 0])
    gate(f"G6 RESID_VOL == sd(r - beta*SPY) directly ({nm}, w=126, row {t_})",
         f"{got:.8f} vs {direct:.8f} (|dev| {abs(got-direct):.2e})",
         "|dev| <= 1e-8", abs(got - direct) <= 1e-8)

    # ---------------------------------------------------------------- every cell
    for p in panels:
        say("")
        say(f"  ===== {p.name} — EVERY cell (cap {DD_CAP*bm[p.name]['MaxDD']:.2%}, "
            f"floor {CAGR_FLOOR*bm[p.name]['CAGR']:.2%}) =====")
        sub = G[G.panel == p.name]
        say("    screen    w   p |    CAGR   Sharpe    MaxDD |     H1     H2 |  turn | "
            " 4a  4bF 4bO | dMaxDD dCAGR")
        for _, x in sub.iterrows():
            w_ = "  -" if not np.isfinite(x.window) else f"{int(x.window):3d}"
            p_ = "  - " if not np.isfinite(x.pct) else f"{x.pct:.1f}"
            say(f"    {x.screen:9s} {w_} {p_} | {x.CAGR:7.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} | "
                f"{x.H1:6.3f} {x.H2:6.3f} | {x.turn:5.2f} | "
                f"{'Y' if x.keep4a else '.':>3s} {'Y' if x.keep4b_full else '.':>4s} "
                f"{'Y' if x.keep4b_oos else '.':>4s} | {x.dMaxDD_pp:6.2f} {x.dCAGR_pp:6.2f}")

    # ---------------------------------------------------------------- the queue's question
    say("")
    say("-" * 100)
    say("THE QUEUE'S QUESTION — does the RESIDUAL screen reach SMALL's -20.23% cap, and does "
        "it beat the TOTAL screen at MATCHED admission?")
    say("-" * 100)
    sub = G[(G.panel == "SMALL663") & (G.screen == "RESID")]
    subt = G[(G.panel == "SMALL663") & (G.screen == "TOTAL")]
    say(f"  RESID cells on SMALL663: MaxDD {sub.MaxDD.min():.2%} .. {sub.MaxDD.max():.2%} "
        f"(cap {capS:.2%}); CAGR {sub.CAGR.min():.2%} .. {sub.CAGR.max():.2%} (floor {flS:.2%})")
    say(f"  TOTAL cells on SMALL663: MaxDD {subt.MaxDD.min():.2%} .. {subt.MaxDD.max():.2%}; "
        f"CAGR {subt.CAGR.min():.2%} .. {subt.CAGR.max():.2%}")
    say(f"  INCUMBENT on SMALL663:   MaxDD {aS.MaxDD:.2%}, CAGR {aS.CAGR:.2%}")
    nd_r = int((sub.MaxDD >= capS).sum())
    nb_r = int(((sub.MaxDD >= capS) & (sub.CAGR >= flS)).sum())
    nd_t = int((subt.MaxDD >= capS).sum())
    say(f"  RESID cells clearing the DD cap: {nd_r} of {len(sub)}; cap AND floor: {nb_r}")
    say(f"  TOTAL cells clearing the DD cap: {nd_t} of {len(subt)}")
    best_r = sub.loc[sub.MaxDD.idxmax()]
    say(f"  shallowest RESID cell w={int(best_r.window)} p={best_r.pct:.1f}: "
        f"MaxDD {best_r.MaxDD:.2%} (misses cap by {100*(capS-best_r.MaxDD):.2f} pp), "
        f"CAGR {best_r.CAGR:.2%}, Sharpe {best_r.Sharpe:.4f}")
    say(f"  COMPARANDS on SMALL: 1301's best SELECTION cell {C_1301_SHALLOWEST_DD:.2%}, "
        f"1297's best EXPOSURE cell {C_1297_SMALL_BEST_DD:.2%}, cap {capS:.2%}")
    # head-to-head at matched admission, every (panel, w, p)
    say("")
    say("  HEAD-TO-HEAD at MATCHED admission (RESID minus TOTAL, same w and p, same day count):")
    hh = []
    for p in panels:
        for w in WINDOWS:
            for q in PCTS:
                r_ = G[(G.panel == p.name) & (G.screen == "RESID") & (G.window == w)
                       & (G.pct == q)].iloc[0]
                t_ = G[(G.panel == p.name) & (G.screen == "TOTAL") & (G.window == w)
                       & (G.pct == q)].iloc[0]
                hh.append(dict(panel=p.name, window=w, pct=q,
                               dMaxDD_pp=100 * (r_.MaxDD - t_.MaxDD),
                               dCAGR_pp=100 * (r_.CAGR - t_.CAGR),
                               dSharpe=r_.Sharpe - t_.Sharpe,
                               dOOS_Sharpe=r_.OOS_Sharpe - t_.OOS_Sharpe,
                               resid_MaxDD=r_.MaxDD, total_MaxDD=t_.MaxDD,
                               resid_CAGR=r_.CAGR, total_CAGR=t_.CAGR))
    HH = pd.DataFrame(hh)
    HH.to_csv(f"{OUT}.headtohead.csv", index=False)
    for p in panels:
        s = HH[HH.panel == p.name]
        say(f"    {p.name:9s} RESID shallower than TOTAL in {int((s.dMaxDD_pp>0).sum())} of "
            f"{len(s)} cells; median dMaxDD {s.dMaxDD_pp.median():+.2f} pp, "
            f"median dCAGR {s.dCAGR_pp.median():+.2f} pp, "
            f"median dSharpe {s.dSharpe.median():+.4f}")
    win = int((HH.dMaxDD_pp > 0).sum())
    gate("G7 RESID beats TOTAL on drawdown at matched admission (all panels, 27 cells)",
         f"{win} of {len(HH)}", "reported either way", True)

    # ---------------------------------------------------------------- mechanism check
    say("")
    say("-" * 100)
    say("MECHANISM — does the screen actually cut the RESIDUAL part of the drawdown?")
    say("  (exact additive split of each book's OWN worst episode, r = beta*SPY + residual)")
    say("-" * 100)
    drows = []
    for p in panels:
        spy = p.spy[p.lo:]
        books = [("INCUMBENT", np.nan, np.nan)]
        srp = G[(G.panel == p.name) & (G.screen == "RESID")]
        srt = G[(G.panel == p.name) & (G.screen == "TOTAL")]
        b_ = srp.loc[srp.MaxDD.idxmax()]
        t_ = srt.loc[srt.MaxDD.idxmax()]
        books += [("RESID", b_.window, b_.pct), ("TOTAL", t_.window, t_.pct)]
        for kind, w, q in books:
            key = (p.name, kind, w if kind == "INCUMBENT" else int(w),
                   q if kind == "INCUMBENT" else float(q))
            r = series[(p.name, kind, np.nan, np.nan)] if kind == "INCUMBENT" \
                else series[(p.name, kind, int(w), float(q))]
            d = decompose(r, spy)
            d.update(panel=p.name, screen=kind,
                     window=np.nan if kind == "INCUMBENT" else int(w),
                     pct=np.nan if kind == "INCUMBENT" else float(q))
            drows.append(d)
            lab = kind if kind == "INCUMBENT" else f"{kind} w={int(w)} p={q:.1f} (shallowest)"
            say(f"  {p.name:9s} {lab:32s} beta {d['beta']:.3f} R2 {d['R2']:.3f} | "
                f"book MaxDD {d['MaxDD_book']:7.2%} = beta*SPY {d['MaxDD_beta_spy']:7.2%} / "
                f"resid {d['MaxDD_idio']:7.2%}")
            say(f"  {'':9s} {'':32s} worst episode {d['ep_days']:4d}d {d['ep_depth']:7.2%}: "
                f"{d['ep_share_beta_spy']:6.1%} systematic / {d['ep_share_idio']:6.1%} residual")
    D = pd.DataFrame(drows)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    d0 = D[(D.panel == "SMALL663") & (D.screen == "INCUMBENT")].iloc[0]
    gate("G8 SMALL episode split is exact (beta*SPY + residual == sum r)",
         f"{abs(d0.ep_sum_beta_spy + d0.ep_sum_idio - d0.ep_sum_r):.2e}", "<= 1e-12",
         abs(d0.ep_sum_beta_spy + d0.ep_sum_idio - d0.ep_sum_r) <= 1e-12)
    gate("G9 SMALL incumbent episode replays 1301's 78.8% residual share",
         f"{d0.ep_share_idio:.4f}", "|dev| <= 0.01", abs(d0.ep_share_idio - 0.788) <= 0.01)

    # ---------------------------------------------------------------- rule 8 walk-forward
    say("")
    say("-" * 100)
    say(f"RULE 8 WALK-FORWARD — (WINDOW, RESID_MAX) by argmax IS Sharpe on warm-up..{IS_END}; "
        f"{OOS_START}.. read ONCE")
    say("  (run separately for RESID and for the matched TOTAL control; ties -> lower window, "
        "then lower pct)")
    say("-" * 100)
    wf = []
    for p in panels:
        anc = G[(G.panel == p.name) & (G.screen == "INCUMBENT")].iloc[0]
        b4, l4 = bm_oos[p.name], live_oos[p.name]
        say(f"  {p.name}")
        say(f"    OOS SPY     {b4['CAGR']:7.2%} / {b4['Sharpe']:.4f} / {b4['MaxDD']:7.2%}"
            f"   cap {DD_CAP*b4['MaxDD']:.2%} floor {CAGR_FLOOR*b4['CAGR']:.2%}")
        say(f"    OOS v2      {l4['CAGR']:7.2%} / {l4['Sharpe']:.4f} / {l4['MaxDD']:7.2%}")
        say(f"    OOS anchor  {anc.OOS_CAGR:7.2%} / {anc.OOS_Sharpe:.4f} / {anc.OOS_MaxDD:7.2%}"
            f"   (the FROZEN incumbent screen)")
        for kind in SCREENS:
            sub = G[(G.panel == p.name) & (G.screen == kind)].sort_values(
                ["window", "pct"], kind="stable")
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
            legs = dict(
                L_OOS_S=bool(pick.OOS_Sharpe > b4["Sharpe"]),
                L_OOS_DD=bool(pick.OOS_MaxDD >= DD_CAP * b4["MaxDD"]),
                L_OOS_CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b4["CAGR"]),
                L_H1=bool(pick.H1 > bm[p.name]["H1"]), L_H2=bool(pick.H2 > bm[p.name]["H2"]),
                L_FULL_DD=bool(pick.MaxDD >= DD_CAP * bm[p.name]["MaxDD"]),
                L_FULL_CAGR=bool(pick.CAGR >= CAGR_FLOOR * bm[p.name]["CAGR"]))
            wf.append(dict(panel=p.name, screen=kind, pick_window=int(pick.window),
                           pick_pct=float(pick.pct), IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           anc_OOS_CAGR=anc.OOS_CAGR, anc_OOS_Sharpe=anc.OOS_Sharpe,
                           anc_OOS_MaxDD=anc.OOS_MaxDD,
                           spy_OOS_CAGR=b4["CAGR"], spy_OOS_Sharpe=b4["Sharpe"],
                           spy_OOS_MaxDD=b4["MaxDD"],
                           v2_OOS_CAGR=l4["CAGR"], v2_OOS_Sharpe=l4["Sharpe"],
                           v2_OOS_MaxDD=l4["MaxDD"],
                           best_OOS_window=int(best_oos.window), best_OOS_pct=float(best_oos.pct),
                           best_OOS_Sharpe=best_oos.OOS_Sharpe,
                           d_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                           keep4a=bool(pick.keep4a), keep4b_full=bool(pick.keep4b_full),
                           keep4b_oos=bool(pick.keep4b_oos),
                           keep4b_both=bool(pick.keep4b_full and pick.keep4b_oos), **legs))
            say(f"    {kind:6s} pick w={int(pick.window):3d} p={pick.pct:.1f} "
                f"(IS Sharpe {pick.IS_Sharpe:.4f})  OOS {pick.OOS_CAGR:7.2%} / "
                f"{pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}  "
                f"(pick - anchor Sharpe {pick.OOS_Sharpe - anc.OOS_Sharpe:+.4f})")
            say(f"    {'':6s} legs {legs} -> 4a {bool(pick.keep4a)}, "
                f"4b full {bool(pick.keep4b_full)}, 4b OOS {bool(pick.keep4b_oos)}, "
                f"4b BOTH {bool(pick.keep4b_full and pick.keep4b_oos)}")
            say(f"    {'':6s} (unselectable bound: best OOS cell w={int(best_oos.window)} "
                f"p={best_oos.pct:.1f} at {best_oos.OOS_Sharpe:.4f})")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G10 rule 8 run for both screens on every panel, 2017-2026 read once",
         f"{len(W)} rows", f"== {len(panels)*len(SCREENS)}", len(W) == len(panels) * len(SCREENS))

    # ---------------------------------------------------------------- summary
    say("")
    say("-" * 100)
    say("SUMMARY — 4a / 4b full / 4b OOS / 4b BOTH, by panel and screen (9 cells each, "
        "INCUMBENT is 1)")
    say("-" * 100)
    for p in panels:
        for kind in ["INCUMBENT"] + SCREENS:
            s = G[(G.panel == p.name) & (G.screen == kind)]
            say(f"  {p.name:9s} {kind:9s} n={len(s):2d}  4a {int(s.keep4a.sum()):2d}  "
                f"4b full {int(s.keep4b_full.sum()):2d}  4b OOS {int(s.keep4b_oos.sum()):2d}  "
                f"4b BOTH {int(s.keep4b_both.sum()):2d}")
    gate("G11 4a passes over all books", int(G.keep4a.sum()), "reported either way", True)
    gate("G12 4b BOTH passes over all books", int(G.keep4b_both.sum()),
         "reported either way", True)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
