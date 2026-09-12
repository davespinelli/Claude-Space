#!/usr/bin/env python3
"""Idea 802 (cloud, 2026-09-12) - is-the-MATCHED-LEVEL-RESIDUAL-a-SEPARATION-law-not-a-SIZE-law.

QUESTION
--------
Idea 569/571's machinery matches two arms at a common LEVEL of a per-name characteristic by drawing
k names with Gaussian kernel weights w ~ exp(-0.5((x-L)/h)^2), h = BW*sd(char over the pool).  The
MATCH RESIDUAL is what is left over: resid(L) = achieved_A(L) - achieved_B(L).  Every matched-level
claim in the record is entitled only to the precision its residual permits.

Idea 800 KILLED the pool-size reading (six pre-registered hypotheses all FAIL; |resid| flat over an
8x span of min(n)) and then found, POST-HOC on six (pair, char) points, that the dimensionless
residual d = |resid|/sd(char) tracks the two arms' standardised mean separation exactly:
Spearman(SMD, d) = +1.000 (BS avol SMD 1.146 -> d 0.4104 against the SS null's 0.009 -> 0.0347).
Six points, three characteristics, two arm pairs - a conjecture, not a law.  This run pre-registers
it and tests it on 13 characteristics and 6 arm pairs, then publishes the SMD -> residual curve so a
matched-level claim can state its entitlement from the arms ALONE, before it draws anything.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: characteristic set, arm pair)
    1. CHARACTERISTIC (13): avol tpers momac beta ivol skew kurt ac1 mdd mafrac dnup mommean trendr2
       momac is the record's variable and the only POOL-DEPENDENT one (a within-pool rank AC);
       the other 12 are per-name functions of that name's own price series.
    2. ARM PAIR (6):
         BS      B136 vs SMALL            the record's own arms (idea 569/571/796/800)
         SS      SMALL halves             same-distribution null, seed 20260912 = idea 800's
         BB      B136 halves              second same-distribution null, at 1/5 the pool size
         VSPLIT  pool split at median avol      separation INDUCED, large on avol
         TSPLIT  pool split at median tpers     separation INDUCED, large on tpers
         MSPLIT  pool split at median mommean   separation INDUCED, large on mommean
       The three induced splits exist to populate the high-SMD end of the curve, which the record's
       own arms never reach, and to make the curve's DOMAIN a measured fact rather than an
       extrapolation.  All 6 x 13 = 78 cells are reported, feasible or not.
    Nothing else is tuned.  BW is held at idea 569/571's 0.500 and k at its 36 (idea 800 swept both
    and found neither governs).  REPORTED-NEVER-SELECTED: rung (9 deciles), kernel seed 0..5,
    re-roll replicate 0..5, window (FULL/IS/OOS), gross, book form, cadence.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_SMD    : the queue's claim.  Spearman(SMD, cell-mean d) >= +0.70 over the feasible cells
               (>= 30 of 78), and the two same-distribution nulls sit in the bottom tertile of d.
    H_LIN    : the law is publishable as a curve.  Pooled rung-level fit of d on SMD has
               R^2 >= 0.50 with slope > 0.
    H_DISP   : the STATED ALTERNATIVE mechanism.  SMD is a whole-arm summary, but a draw happens at
               one rung; the rung-local standardised displacement
               DISP(L) = |L-mean_A|/sd + |L-mean_B|/sd should beat SMD on pooled R^2.  If H_DISP
               wins, the entitlement a claim may quote is a function of its RUNG, not of its arms.
    H_SIZE   : idea 800's kill holds under the new predictor - within SMD tertiles,
               |Spearman(min_n, d)| <= 0.30.
    H_NOISE  : the SMD signal is bigger than the draw noise idea 800 measured - the span of cell-mean
               d across SMD quintiles is >= 3x the median within-cell re-roll sd.
    H_ENTITLE: the curve survives rule 8.  Fit the p90 entitlement on IS-estimated characteristics,
               read it ONCE on OOS-estimated characteristics; every SMD bin's OOS p90 within 1.5x of
               the IS-fitted prediction.

GATES (printed BEFORE any new number is read)
    G0 determinism : every draw rebuilt twice gives identical name sets.                 bar 0
    G1 contiguity  : each name's valid mask is one contiguous block (what makes the vectorised
                     lag-k autocorrelation identical to the pandas estimator).      bar: 0 breaks
    G2 estimator   : vectorised momac vs idea 571/796/800's pandas estimator, 40 names.  bar 1e-12
    G3 parent      : this run's SMD / OVL / d for the six (pair, char) points idea 800 published in
                     its .overlap.csv, rebuilt from scratch here.                        bar 1e-6
                     (SMD and OVL are deterministic given the panel; d involves the same seeded
                     draws, so a mismatch in d alone would be a draw-convention break.)
    G4 engine      : fast_backtest vs engine.backtest on two drawn books.                bar 1e-9

RULE 8 WALK-FORWARD (required)
    IS = ..2016-12-31, OOS = 2017-01-01.., OOS read ONCE.
    WF-A on the ANSWER: every characteristic is re-estimated on IS prices ALONE and on OOS prices
       ALONE, rungs re-frozen per window, and the whole grid re-measured in each.  The predictor is
       CHOSEN on IS by pooled R^2 among {SMD, DISP, min_n, n_eff, 1/OVL} and its OOS R^2 / slope are
       then read once - so "what governs the residual" is itself walked forward.
    WF-B on a BOOK: the law taken as a trading instruction - "draw k names at a matched level".
       Among all drawn books (pair, char, rung, arm, seed, form, gross) the pick is made by IS
       Sharpe ALONE, then OOS CAGR / Sharpe / MaxDD are read ONCE against live RULES v2 (U56,
       weekly, 10 bps) and against SPY.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY book
    and counted.  Stated up front, as idea 800 did: a kernel-weighted seeded draw is a diagnostic
    panel, not a rule anyone can trade, so no 4b pass on this ladder is claimed as a capital
    candidate.

SURVIVORSHIP: B136 is the current constituent list of universe_broad.json; the small panel is the
    current constituent list of its sub-$2B screen with every ticker whose max_1d_move >= 1.0 in
    data/small_meta.csv dropped first, per PROTOCOL.  Names that died are absent from both arms.
    For the LAW the bias is second-order - the object is a difference of achieved CHARACTERISTIC
    LEVELS between two draws from the same screened universe, not a return - but the return legs
    (WF-B, the KEEP-path counts) carry the usual upward bias and are read as diagnostics only.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine convention), no shorting, no leverage.
Deterministic, standalone, no network.  Writes only its own outputs:
    .cells.csv .rungs.csv .law.csv .entitle.csv .walkforward.csv .keeppaths.csv .gates.csv
    .console.txt
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_is-the-MATCHED-LEVEL-RESIDUAL-a-SEPARATION-law-not-a-SIZE-law_cloud"
OUT = ROOT / "research" / "backtests"
PARENT800 = OUT / "2026-09-12_is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law_cloud"

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252
AC_LAG = 21
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"          # idea 571/796/800's last bar - kept so G3 is comparable
BW = 0.500                         # idea 569/571's bandwidth; NOT a dial (idea 796/800 swept it)
K = 36                             # idea 569/571's draw size; NOT a dial (idea 800 swept it)
SEEDS = [0, 1, 2, 3, 4, 5]         # idea 800's seed block
NREP = 6                           # independent re-rolls of the whole seed block (noise bar)
LEVEL_Q = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
BOOK_Q = [0.10, 0.30, 0.50, 0.70, 0.90]    # rungs that also get run as books
SMD_BINS = [0.0, 0.10, 0.20, 0.40, 0.80, 1.60, 99.0]

CHARS = ["avol", "tpers", "momac", "beta", "ivol", "skew", "kurt", "ac1", "mdd", "mafrac",
         "dnup", "mommean", "trendr2"]
PAIRS = ["BS", "SS", "BB", "VSPLIT", "TSPLIT", "MSPLIT"]
SPLIT_CHAR = {"VSPLIT": "avol", "TSPLIT": "tpers", "MSPLIT": "mommean"}

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner (idea 796)
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- characteristics
def _ac_vec(R, lag):
    """Column-wise lag-`lag` Pearson AC of an ndarray with NaNs, over rows valid at t and t-lag.
    Identical to `s.dropna().corr(s.dropna().shift(lag))` when each column's mask is contiguous."""
    X, Y = R[lag:], R[:-lag]
    m = np.isfinite(X) & np.isfinite(Y)
    n = m.sum(0).astype(float)
    Xm = np.where(m, X, 0.0)
    Ym = np.where(m, Y, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        mx, my = Xm.sum(0) / n, Ym.sum(0) / n
        cov = (Xm * Ym).sum(0) / n - mx * my
        vx = (Xm * Xm).sum(0) / n - mx * mx
        vy = (Ym * Ym).sum(0) / n - my * my
        ac = cov / np.sqrt(vx * vy)
    ac[n <= 3 * lag] = np.nan
    return ac


def momac_chars(pool, mom=None):
    """momac = lag-21 AC of the name's 12-1 momentum rank_pct.  POOL-DEPENDENT (rank is
    cross-sectional within the given column set) - idea 571/796/800's variable."""
    if mom is None:
        mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    valid = pool.notna() & mom.notna()
    return pd.Series(_ac_vec(rk.where(valid).to_numpy(dtype=float), AC_LAG), index=pool.columns)


def momac_ref(pool):
    """Idea 571/796/800's estimator, verbatim - the G2 reference."""
    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    v = pool.notna() & mom.notna()
    out = {}
    for c in pool.columns:
        s = rk[c].where(v[c]).dropna()
        out[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    return pd.Series(out, dtype=float)


def tpers_chars(pool):
    """Per-name trend persistence (1 - 200d-MA state flip rate).  Pool-INDEPENDENT."""
    ma = pool.rolling(MA_WIN).mean()
    valid = pool.notna() & ma.notna()
    st = (pool > ma).where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def _col_stats(X, y):
    """Column-wise (n, cov, var_x, var_y) of an (T,N) NaN-bearing matrix against a (T,) vector,
    over the rows where both are finite.  Exact per column - no pairwise/whole-series mixing."""
    Y = np.broadcast_to(np.asarray(y, float)[:, None], X.shape)
    m = np.isfinite(X) & np.isfinite(Y)
    n = m.sum(0).astype(float)
    Xm = np.where(m, X, 0.0)
    Ym = np.where(m, Y, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        mx, my = Xm.sum(0) / n, Ym.sum(0) / n
        cov = (Xm * Ym).sum(0) / n - mx * my
        vx = (Xm * Xm).sum(0) / n - mx * mx
        vy = (Ym * Ym).sum(0) / n - my * my
    cov[n < 60] = np.nan
    return n, cov, vx, vy


def chars_for(pool, spy, want=CHARS):
    """All 13 characteristics on the given price panel.  Everything except momac is a function of
    the name's own series (and SPY for beta/ivol), so only momac moves when the pool moves."""
    R = pool.pct_change()
    sp = spy.reindex(pool.index).pct_change()
    d = {}
    if "avol" in want:
        d["avol"] = R.std() * np.sqrt(252)
    if "tpers" in want:
        d["tpers"] = tpers_chars(pool)
    if "momac" in want:
        d["momac"] = momac_chars(pool)
    if "skew" in want:
        d["skew"] = R.skew()
    if "kurt" in want:
        d["kurt"] = R.kurt()
    if "ac1" in want:
        d["ac1"] = pd.Series(_ac_vec(R.to_numpy(dtype=float), 1), index=pool.columns)
    if "beta" in want or "ivol" in want:
        _, cov, vx, vy = _col_stats(R.to_numpy(dtype=float), sp.to_numpy(dtype=float))
        with np.errstate(invalid="ignore", divide="ignore"):
            beta = cov / vy
            resid_var = np.clip(vx - beta ** 2 * vy, 0.0, None)
        if "beta" in want:
            d["beta"] = pd.Series(beta, index=pool.columns)
        if "ivol" in want:
            d["ivol"] = pd.Series(np.sqrt(resid_var) * np.sqrt(252), index=pool.columns)
    if "mdd" in want:
        d["mdd"] = (pool / pool.cummax() - 1.0).min()
    if "mafrac" in want:
        ma = pool.rolling(MA_WIN).mean()
        v = pool.notna() & ma.notna()
        d["mafrac"] = ((pool > ma) & v).sum() / v.sum().replace(0, np.nan)
    if "dnup" in want:
        dn = R.where(R < 0).std()
        up = R.where(R > 0).std()
        d["dnup"] = dn / up
    if "mommean" in want:
        d["mommean"] = (pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0).mean()
    if "trendr2" in want:
        lp = np.log(pool.where(pool > 0))
        t = np.arange(len(pool), dtype=float)
        _, cov, vx, vy = _col_stats(lp.to_numpy(dtype=float), t)
        with np.errstate(invalid="ignore", divide="ignore"):
            d["trendr2"] = pd.Series((cov ** 2) / (vx * vy), index=pool.columns)
    return pd.DataFrame({c: d[c] for c in want if c in d})


# ------------------------------------------------------------------------- the kernel draw
def kernel_draw(names, x, L, h, k, seed_key):
    """Idea 569/571's scheme with its seed key convention; returns (names, achieved, n_eff)."""
    seed = zlib.crc32(seed_key.encode()) % (2 ** 32)
    rng = np.random.default_rng(seed)
    w = np.exp(-0.5 * ((x - L) / h) ** 2)
    sw = w.sum()
    if not np.isfinite(sw) or sw <= 0:
        return None, np.nan, np.nan
    w = w / sw
    neff = 1.0 / float((w ** 2).sum())
    pick = rng.choice(names, size=k, replace=False, p=w)
    return sorted(pick.tolist()), float(np.mean(x[np.isin(names, pick)])), neff


def reach(x, k):
    v = np.sort(np.asarray(x, float))
    return float(v[:k].mean()), float(v[-k:].mean())


def ols_fit(x, y):
    """Plain OLS of y on x with R^2, residual sd and Spearman.  No logs - the law is a level law."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return dict(n=int(m.sum()), slope=np.nan, icept=np.nan, R2=np.nan, sd_resid=np.nan,
                    spearman=np.nan)
    xx, yy = x[m], y[m]
    b, a = np.polyfit(xx, yy, 1)
    pred = a + b * xx
    ss_res = float(((yy - pred) ** 2).sum())
    ss_tot = float(((yy - yy.mean()) ** 2).sum())
    sp = float(np.corrcoef(pd.Series(xx).rank().to_numpy(),
                           pd.Series(yy).rank().to_numpy())[0, 1]) if m.sum() > 2 else np.nan
    return dict(n=int(m.sum()), slope=float(b), icept=float(a),
                R2=float(1 - ss_res / ss_tot) if ss_tot > 0 else np.nan,
                sd_resid=float(np.std(yy - pred, ddof=1)), spearman=sp)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(x[m]).rank().to_numpy(),
                             pd.Series(y[m]).rank().to_numpy())[0, 1])


def ovl_coef(xa, xb, bins=40):
    lo, hi = float(min(xa.min(), xb.min())), float(max(xa.max(), xb.max()))
    edges = np.linspace(lo, hi, bins + 1)
    ha = np.histogram(xa, bins=edges)[0] / len(xa)
    hb = np.histogram(xb, bins=edges)[0] / len(xb)
    return float(np.minimum(ha, hb).sum())


def arm_pairs(nc, b_ok, s_ok, pool_names):
    """The 6 arm pairs.  Same-distribution nulls use idea 800's seed so SS is literally its SS."""
    out = {}
    out["BS"] = (list(b_ok), list(s_ok), "B", "S")
    rng = np.random.default_rng(20260912)
    sp = list(np.array(s_ok)[rng.permutation(len(s_ok))])
    out["SS"] = (sorted(sp[:len(sp) // 2]), sorted(sp[len(sp) // 2:]), "S1", "S2")
    rng2 = np.random.default_rng(20260912)
    bp = list(np.array(b_ok)[rng2.permutation(len(b_ok))])
    out["BB"] = (sorted(bp[:len(bp) // 2]), sorted(bp[len(bp) // 2:]), "B1", "B2")
    for pair, sc in SPLIT_CHAR.items():
        x = nc[sc].dropna()
        med = float(x.median())
        hi = sorted([n for n in x.index if x[n] > med and n in pool_names])
        lo = sorted([n for n in x.index if x[n] <= med and n in pool_names])
        out[pair] = (hi, lo, f"{sc}HI", f"{sc}LO")
    return out


# --------------------------------------------------------------- the measurement, one window
def measure(nc, pool, arms, levels, tag, nrep=NREP, book_levels=None, book_sets=None):
    """Rung-level residuals for every (pair, char) cell in ONE window.  Returns rung rows."""
    book_levels = book_levels or {}
    rows = []
    for pair, (A, B, la, lb) in arms.items():
        for char in CHARS:
            sd = float(nc[char].std())
            if not np.isfinite(sd) or sd <= 0:
                continue
            h = BW * sd
            xa_all = nc.loc[[n for n in A if n in nc.index], char].dropna()
            xb_all = nc.loc[[n for n in B if n in nc.index], char].dropna()
            if min(len(xa_all), len(xb_all)) <= K:
                rows.append(dict(tag=tag, pair=pair, char=char, level=np.nan, feasible=0,
                                 reason="arm<=k", n_A=len(xa_all), n_B=len(xb_all)))
                continue
            na, xa = np.array(xa_all.index), xa_all.to_numpy(float)
            nb, xb = np.array(xb_all.index), xb_all.to_numpy(float)
            smd = abs(float(xa.mean() - xb.mean())) / sd
            ovl = ovl_coef(xa, xb)
            ra, rb = reach(xa, K), reach(xb, K)
            for L in levels[char]:
                base = dict(tag=tag, pair=pair, char=char, level=L, n_A=len(na), n_B=len(nb),
                            min_n=min(len(na), len(nb)), SMD=smd, OVL=ovl, sd_char=sd,
                            DISP=abs(L - float(xa.mean())) / sd + abs(L - float(xb.mean())) / sd)
                if not (ra[0] <= L <= ra[1] and rb[0] <= L <= rb[1]):
                    rows.append(dict(base, feasible=0, reason="out-of-reach"))
                    continue
                ds, nef = [], {}
                for rep in range(nrep):
                    ach = {}
                    for lab, nm, xx in (("A", na, xa), ("B", nb, xb)):
                        per = []
                        for sdd in SEEDS:
                            key = f"CHAR|{char}|{L:.6f}|{lab}|{sdd}" if rep == 0 else \
                                  f"CHAR|{char}|{L:.6f}|{lab}|{sdd}|rep{rep}|{pair}|{tag}"
                            pick, av, ne = kernel_draw(nm, xx, L, h, K, key)
                            if pick is None:
                                per = None
                                break
                            per.append(av)
                            nef[lab] = ne
                            if (rep == 0 and book_sets is not None and sdd < 2
                                    and L in book_levels.get(char, ())):
                                book_sets[(pair, char, round(L, 6), lab, sdd)] = pick
                        if per is None:
                            ach = None
                            break
                        ach[lab] = float(np.mean(per))
                    if ach is None:
                        break
                    ds.append(abs(ach["A"] - ach["B"]) / sd)
                if not ds:
                    rows.append(dict(base, feasible=0, reason="draw-failed"))
                    continue
                rows.append(dict(base, feasible=1, reason="-", d=ds[0],
                                 d_mean_rep=float(np.mean(ds)),
                                 d_sd_rep=float(np.std(ds, ddof=1)) if len(ds) > 1 else np.nan,
                                 nrep=len(ds),
                                 neff_min=float(min(nef["A"], nef["B"])),
                                 resid_raw=ds[0] * sd))
    return rows


def cell_table(RR):
    """One row per (pair, char): SMD, OVL and the cell's mean/p90 dimensionless residual."""
    F = RR[RR.feasible == 1]
    g = F.groupby(["pair", "char"])
    t = g.agg(SMD=("SMD", "first"), OVL=("OVL", "first"), min_n=("min_n", "first"),
              n_rungs=("d", "size"), d_mean=("d", "mean"), d_p90=("d", lambda s: s.quantile(0.90)),
              d_max=("d", "max"), d_sd_rep=("d_sd_rep", "median"),
              DISP_mean=("DISP", "mean"), sd_char=("sd_char", "first")).reset_index()
    return t


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 802 - is the matched-level MATCH RESIDUAL a SEPARATION law (arms' SMD) rather than the")
    P("#            POOL-SIZE law idea 800 killed?  Pre-registered on 13 chars x 6 arm pairs.")
    P("=" * 118)
    P(f"# PROTOCOL: {COST:.0f} bps per unit turnover, next-day fills, IS <= {IS_END}, "
      f"OOS >= {OOS_START}, sample truncated at {PARENT_END} (idea 571/796/800's last bar).")
    P(f"# TUNED (2): characteristic ({len(CHARS)}) x arm pair ({len(PAIRS)}) = "
      f"{len(CHARS)*len(PAIRS)} cells, all reported.")
    P(f"#            FROZEN: BW {BW:.3f}, k {K}, seeds {SEEDS}, {len(LEVEL_Q)} decile rungs, "
      f"{NREP} re-rolls.")
    P("#            REPORTED-NOT-SELECTED: rung, seed, replicate, window, gross, form, cadence.")
    P("")
    P("PRE-REGISTERED: H_SMD (Spearman(SMD, cell-mean d) >= +0.70, nulls in bottom tertile),")
    P("  H_LIN (pooled rung-level R^2 >= 0.50, slope > 0), H_DISP (the STATED ALTERNATIVE: the")
    P("  rung-local displacement |L-mean_A|/sd + |L-mean_B|/sd beats SMD on pooled R^2),")
    P("  H_SIZE (idea 800's kill holds: |Spearman(min_n, d)| <= 0.30 within SMD tertiles),")
    P("  H_NOISE (SMD span across quintiles >= 3x the median within-cell re-roll sd),")
    P("  H_ENTITLE (p90 curve fit on IS characteristics predicts OOS p90 within 1.5x per bin).")
    P("")

    # ------------------------------------------------------------------ panels
    px56 = load_universe().dropna(how="all").ffill().loc[:PARENT_END]
    px136 = load_universe(broad=True).dropna(how="all").ffill().loc[:PARENT_END]
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = sorted([c for c in pxs.columns if c != "SPY" and c not in bad])
    pxs = pxs.dropna(how="all").ffill().loc[:PARENT_END]
    b_stk = sorted([c for c in px136.columns if c != "SPY"])
    ix = px136.index.intersection(pxs.index)
    pool_all = pd.concat([px136.loc[ix, b_stk], pxs.loc[ix, s_stk]], axis=1).ffill()
    spy = (px136["SPY"] if "SPY" in px136.columns else px56["SPY"]).reindex(ix).ffill()
    P(f"PANELS: B136 {len(b_stk)} tradable, SMALL {len(s_stk)} tradable "
      f"({len(bad)} max_1d_move>=1.0 tickers dropped per PROTOCOL), pool {pool_all.shape[1]} names "
      f"over {len(ix)} bars {ix.min().date()}..{ix.max().date()}")
    P("SURVIVORSHIP: both arms are CURRENT constituents; dead names are absent.  The law's object is")
    P("  a difference of ACHIEVED CHARACTERISTIC LEVELS between two draws from the same screened")
    P("  universe, so the bias is second-order there; the return legs carry the usual bias.")

    # ------------------------------------------------------------------ GATES
    P("")
    P("=" * 118)
    P("GATES")
    P("=" * 118)
    gates = []
    v = pool_all.notna()
    first = v.idxmax()
    gappy = [c for c in pool_all.columns if not bool(v[c].loc[first[c]:].all())]
    if gappy:
        P(f"  G1 contiguity : {len(gappy)} of {pool_all.shape[1]} names carry an interior gap "
          f"({' '.join(gappy)}) -> DROPPED, so the vectorised lag-k AC is exact by construction.")
        pool_all = pool_all.drop(columns=gappy)
        b_stk = [c for c in b_stk if c not in gappy]
        s_stk = [c for c in s_stk if c not in gappy]
    else:
        P(f"  G1 contiguity : 0 of {pool_all.shape[1]} names carry an interior gap -> PASS")
    gates.append(dict(gate="G1_contiguity_dropped", value=len(gappy), bar=0, passed=True))

    nc_full = chars_for(pool_all, spy)
    b_ok = [c for c in b_stk if c in nc_full.index]
    s_ok = [c for c in s_stk if c in nc_full.index]
    LEVELS = {c: [round(float(nc_full[c].quantile(q)), 6) for q in LEVEL_Q] for c in CHARS}
    BOOKL = {c: [round(float(nc_full[c].quantile(q)), 6) for q in BOOK_Q] for c in CHARS}

    samp = sorted(np.random.default_rng(0).choice(np.array(pool_all.columns), 40,
                                                  replace=False).tolist())
    d2 = float(np.nanmax(np.abs(momac_ref(pool_all[samp]) - momac_chars(pool_all[samp]))))
    P(f"  G2 estimator  : max |vectorised momac - idea 571 pandas momac| over 40 names {d2:.3e}"
      f"   bar 1e-12 -> {'PASS' if d2 < 1e-12 else 'FAIL'}")
    gates.append(dict(gate="G2_estimator", value=d2, bar=1e-12, passed=bool(d2 < 1e-12)))

    ARMS = arm_pairs(nc_full, b_ok, s_ok, set(pool_all.columns))
    for pair in PAIRS:
        A, B, la, lb = ARMS[pair]
        P(f"    arms {pair:7s} {la}({len(A)}) vs {lb}({len(B)})")

    # G0 determinism
    x0 = nc_full.loc[b_ok, "momac"].dropna()
    p1, a1, _ = kernel_draw(np.array(x0.index), x0.to_numpy(float), LEVELS["momac"][4],
                            BW * float(nc_full["momac"].std()), K, "G0|momac|mid")
    p2, a2, _ = kernel_draw(np.array(x0.index), x0.to_numpy(float), LEVELS["momac"][4],
                            BW * float(nc_full["momac"].std()), K, "G0|momac|mid")
    g0 = int(p1 != p2) + int(abs(a1 - a2) > 0)
    P(f"  G0 determinism: rebuilt draw differs in {g0} ways   bar 0 -> {'PASS' if g0 == 0 else 'FAIL'}")
    gates.append(dict(gate="G0_determinism", value=g0, bar=0, passed=bool(g0 == 0)))

    # G3: idea 800's six published (pair, char) points
    pfile = Path(f"{PARENT800}.overlap.csv")
    if pfile.exists():
        par = pd.read_csv(pfile)
        worst_smd = worst_ovl = 0.0
        P("  G3 parent     : idea 800's .overlap.csv rebuilt here (SMD / OVL deterministic; d uses")
        P("                  the same seeded draws).  bar 1e-6 on SMD and OVL.")
        P(f"      {'pair':6s} {'char':8s} {'SMD_800':>8s} {'SMD_802':>8s} {'OVL_800':>8s} "
          f"{'OVL_802':>8s} {'d_800':>8s} {'d_802':>8s}")
        for _, pr in par.iterrows():
            A, B, _, _ = ARMS[pr["pair"]]
            c = pr["char"]
            xa = nc_full.loc[[n for n in A if n in nc_full.index], c].dropna().to_numpy(float)
            xb = nc_full.loc[[n for n in B if n in nc_full.index], c].dropna().to_numpy(float)
            sd = float(nc_full[c].std())
            smd = abs(float(xa.mean() - xb.mean())) / sd
            ovl = ovl_coef(xa, xb)
            worst_smd = max(worst_smd, abs(smd - float(pr["SMD"])))
            worst_ovl = max(worst_ovl, abs(ovl - float(pr["OVL"])))
            P(f"      {pr['pair']:6s} {c:8s} {float(pr['SMD']):8.4f} {smd:8.4f} "
              f"{float(pr['OVL']):8.4f} {ovl:8.4f} {float(pr['rel']):8.4f} {'(below)':>8s}")
        P(f"      max |dSMD| {worst_smd:.3e}  max |dOVL| {worst_ovl:.3e}  -> "
          f"{'PASS' if max(worst_smd, worst_ovl) < 1e-6 else 'MEASURED DRIFT (not a pass)'}")
        gates.append(dict(gate="G3_parent_SMD", value=worst_smd, bar=1e-6,
                          passed=bool(worst_smd < 1e-6)))
        gates.append(dict(gate="G3_parent_OVL", value=worst_ovl, bar=1e-6,
                          passed=bool(worst_ovl < 1e-6)))
    else:
        P("  G3 parent     : idea 800's .overlap.csv NOT FOUND -> gate cannot run (stated)")
        gates.append(dict(gate="G3_parent_SMD", value=np.nan, bar=1e-6, passed=False))

    # G4: engine agreement on two drawn books
    bk = kernel_draw(np.array(x0.index), x0.to_numpy(float), LEVELS["momac"][4],
                     BW * float(nc_full["momac"].std()), K, "G4|book")[0]
    sub = pool_all[bk].loc[pool_all.index[260]:]
    wts = 0.75 * sub.notna().div(sub.notna().sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    r_fast = fast_backtest(sub, wts, COST, "W")["returns"]
    r_eng = backtest(sub, wts, cost_bps=COST, freq="W")["returns"]
    d4 = float(np.nanmax(np.abs(r_fast - r_eng)))
    P(f"  G4 engine     : max |fast_backtest - engine.backtest| {d4:.3e}   bar 1e-9 -> "
      f"{'PASS' if d4 < 1e-9 else 'FAIL'}")
    gates.append(dict(gate="G4_engine", value=d4, bar=1e-9, passed=bool(d4 < 1e-9)))
    pd.DataFrame(gates).to_csv(f"{OUT}/{STAMP}.gates.csv", index=False)

    P("")
    P(f"POOL chars (sd, kernel h = {BW:.3f}*sd):")
    for c in CHARS:
        P(f"    {c:8s} usable {int(nc_full[c].notna().sum()):4d} "
          f"(B {int(nc_full.loc[b_ok, c].notna().sum()):3d} / S {int(nc_full.loc[s_ok, c].notna().sum()):3d})"
          f"  sd {float(nc_full[c].std()):9.4f}  h {BW*float(nc_full[c].std()):9.4f}  "
          f"rungs " + " ".join(f"{x:.3f}" for x in LEVELS[c]))
    P("")

    # ------------------------------------------------------------------ FULL-sample grid
    P("=" * 118)
    P("THE GRID - rung-level residuals, FULL sample.  d = |achieved_A - achieved_B| / sd(char).")
    P("=" * 118)
    book_sets: dict = {}
    rows = measure(nc_full, pool_all, ARMS, LEVELS, "FULL", NREP, BOOKL, book_sets)
    RR = pd.DataFrame(rows)
    RR.to_csv(f"{OUT}/{STAMP}.rungs.csv", index=False)
    F = RR[RR.feasible == 1]
    P(f"  {len(RR)} rung rows, {len(F)} FEASIBLE ({len(F)/max(len(RR),1):.0%}); "
      f"{int((RR.feasible==0).sum())} infeasible "
      f"({RR[RR.feasible==0].reason.value_counts().to_dict()})")
    CT = cell_table(RR)
    CT.to_csv(f"{OUT}/{STAMP}.cells.csv", index=False)
    P(f"  {len(CT)} of {len(PAIRS)*len(CHARS)} (pair, char) cells have >=1 feasible rung.")
    P("")
    P("  CELL TABLE (sorted by SMD) - the curve's raw material")
    P(f"  {'pair':7s} {'char':8s} {'SMD':>7s} {'OVL':>6s} {'min_n':>6s} {'rungs':>5s} "
      f"{'d_mean':>8s} {'d_p90':>8s} {'d_sd_rep':>9s} {'DISP':>6s}")
    for _, r in CT.sort_values("SMD").iterrows():
        P(f"  {r['pair']:7s} {r['char']:8s} {r.SMD:7.3f} {r.OVL:6.3f} {int(r.min_n):6d} "
          f"{int(r.n_rungs):5d} {r.d_mean:8.4f} {r.d_p90:8.4f} "
          f"{(r.d_sd_rep if np.isfinite(r.d_sd_rep) else np.nan):9.4f} {r.DISP_mean:6.3f}")
    P("")

    # ------------------------------------------------------------------ H_SMD / H_LIN / H_DISP
    P("=" * 118)
    P("PRE-REGISTERED TESTS")
    P("=" * 118)
    law = []
    sp_cell = spearman(CT.SMD, CT.d_mean)
    terc = CT.d_mean.rank(pct=True)
    nulls = CT[CT.pair.isin(["SS", "BB"])]
    null_bot = float((terc[CT.pair.isin(["SS", "BB"])] <= 1 / 3).mean()) if len(nulls) else np.nan
    h_smd = bool(np.isfinite(sp_cell) and sp_cell >= 0.70)
    P(f"  H_SMD   : Spearman(SMD, cell-mean d) = {sp_cell:+.3f} over {len(CT)} cells "
      f"bar >= +0.70 -> {'PASS' if h_smd else 'FAIL'}")
    P(f"            same-distribution nulls (SS, BB) in the bottom d tertile: "
      f"{null_bot:.0%} of {len(nulls)} cells")
    law.append(dict(test="H_SMD", stat="spearman_cell", value=sp_cell, bar=0.70, passed=h_smd))

    preds = {"SMD": F.SMD, "DISP": F.DISP, "min_n": F.min_n, "neff_min": F.neff_min,
             "inv_OVL": 1.0 / F.OVL.replace(0, np.nan)}
    fits = {k: ols_fit(vv, F.d) for k, vv in preds.items()}
    P("")
    P("  POOLED RUNG-LEVEL FITS of d on each candidate predictor (FULL sample, "
      f"n = {len(F)} feasible rungs)")
    P(f"  {'predictor':10s} {'n':>5s} {'slope':>10s} {'icept':>9s} {'R2':>7s} {'sd_resid':>9s} "
      f"{'spearman':>9s}")
    for k, f in fits.items():
        P(f"  {k:10s} {f['n']:5d} {f['slope']:10.5f} {f['icept']:9.4f} {f['R2']:7.3f} "
          f"{f['sd_resid']:9.4f} {f['spearman']:+9.3f}")
        law.append(dict(test="fit_FULL", stat=k, value=f["R2"], bar=np.nan, passed=np.nan,
                        slope=f["slope"], spearman=f["spearman"]))
    h_lin = bool(fits["SMD"]["R2"] >= 0.50 and fits["SMD"]["slope"] > 0)
    P(f"  H_LIN   : SMD fit R^2 {fits['SMD']['R2']:.3f} (bar 0.50), slope "
      f"{fits['SMD']['slope']:+.5f} (bar > 0) -> {'PASS' if h_lin else 'FAIL'}")
    law.append(dict(test="H_LIN", stat="R2_SMD", value=fits["SMD"]["R2"], bar=0.50, passed=h_lin))
    h_disp = bool(fits["DISP"]["R2"] > fits["SMD"]["R2"])
    P(f"  H_DISP  : rung-local DISP R^2 {fits['DISP']['R2']:.3f} vs SMD {fits['SMD']['R2']:.3f} "
      f"-> {'PASS (DISP governs)' if h_disp else 'FAIL (SMD is not beaten by the rung-local view)'}")
    law.append(dict(test="H_DISP", stat="R2_DISP_minus_R2_SMD",
                    value=fits["DISP"]["R2"] - fits["SMD"]["R2"], bar=0.0, passed=h_disp))
    # two-predictor read: is either one redundant?
    both = ols_fit(F.SMD, F.d)
    mm = np.isfinite(F.SMD) & np.isfinite(F.DISP) & np.isfinite(F.d)
    X = np.column_stack([np.ones(mm.sum()), F.SMD[mm], F.DISP[mm]])
    beta2, *_ = np.linalg.lstsq(X, F.d[mm].to_numpy(float), rcond=None)
    pred2 = X @ beta2
    yy = F.d[mm].to_numpy(float)
    r2_2 = 1 - float(((yy - pred2) ** 2).sum()) / float(((yy - yy.mean()) ** 2).sum())
    P(f"            joint fit d = {beta2[0]:+.4f} {beta2[1]:+.4f}*SMD {beta2[2]:+.4f}*DISP  "
      f"R^2 {r2_2:.3f} (SMD alone {both['R2']:.3f}, DISP alone {fits['DISP']['R2']:.3f}); "
      f"Spearman(SMD, DISP) = {spearman(F.SMD, F.DISP):+.3f}")
    law.append(dict(test="joint", stat="R2_SMD_plus_DISP", value=r2_2, bar=np.nan, passed=np.nan,
                    slope=beta2[1], spearman=beta2[2]))

    # H_SIZE - idea 800's kill, re-tested within SMD tertiles
    P("")
    q = F.SMD.rank(pct=True)
    worst = 0.0
    for lo, hi, nm in ((0.0, 1 / 3, "low"), (1 / 3, 2 / 3, "mid"), (2 / 3, 1.01, "high")):
        g = F[(q > lo) & (q <= hi)]
        s_mn = spearman(g.min_n, g.d)
        s_ne = spearman(g.neff_min, g.d)
        worst = max(worst, abs(s_mn) if np.isfinite(s_mn) else 0.0)
        P(f"  H_SIZE  : SMD tertile {nm:4s} (n {len(g):4d}, SMD "
          f"{g.SMD.min():.3f}..{g.SMD.max():.3f})  Spearman(min_n, d) {s_mn:+.3f}   "
          f"Spearman(n_eff, d) {s_ne:+.3f}")
    h_size = bool(worst <= 0.30)
    P(f"            worst |Spearman(min_n, d)| within tertiles {worst:.3f}  bar <= 0.30 -> "
      f"{'PASS (size still inert)' if h_size else 'FAIL (size is back)'}")
    law.append(dict(test="H_SIZE", stat="worst_abs_spearman_min_n", value=worst, bar=0.30,
                    passed=h_size))

    # H_NOISE
    P("")
    qq = pd.qcut(CT.SMD, 5, labels=False, duplicates="drop")
    bym = CT.groupby(qq).d_mean.mean()
    span = float(bym.max() - bym.min())
    noise = float(np.nanmedian(CT.d_sd_rep))
    h_noise = bool(np.isfinite(noise) and noise > 0 and span >= 3 * noise)
    P(f"  H_NOISE : cell-mean d across SMD quintiles " + " ".join(f"{x:.4f}" for x in bym) +
      f"  span {span:.4f}")
    P(f"            median within-cell re-roll sd {noise:.4f} ({NREP} independent re-rolls of the "
      f"{len(SEEDS)}-seed block)  span/noise {span/noise if noise else np.nan:.2f}x  bar 3x -> "
      f"{'PASS' if h_noise else 'FAIL'}")
    law.append(dict(test="H_NOISE", stat="span_over_noise", value=span / noise if noise else np.nan,
                    bar=3.0, passed=h_noise))

    # ------------------------------------------------------------------ the ENTITLEMENT curve
    P("")
    P("=" * 118)
    P("THE ENTITLEMENT CURVE - what |resid| a matched-level claim may quote, from its ARMS alone")
    P("=" * 118)
    F2 = F.copy()
    F2["bin"] = pd.cut(F2.SMD, SMD_BINS, right=False)
    ent = F2.groupby("bin", observed=True).agg(
        n=("d", "size"), cells=("char", "nunique"), SMD_lo=("SMD", "min"), SMD_hi=("SMD", "max"),
        d_p50=("d", lambda s: s.quantile(0.50)), d_p90=("d", lambda s: s.quantile(0.90)),
        d_max=("d", "max")).reset_index()
    ent.to_csv(f"{OUT}/{STAMP}.entitle.csv", index=False)
    P(f"  {'SMD bin':16s} {'n':>5s} {'chars':>5s} {'SMD range':>15s} {'d p50':>8s} {'d p90':>8s} "
      f"{'d max':>8s}")
    for _, r in ent.iterrows():
        P(f"  {str(r['bin']):16s} {int(r.n):5d} {int(r.cells):5d} "
          f"{r.SMD_lo:7.3f}..{r.SMD_hi:5.3f} {r.d_p50:8.4f} {r.d_p90:8.4f} {r.d_max:8.4f}")
    P("  READ: at an arm separation of SMD, a k=36 / BW=0.500 matched-level draw is entitled to a")
    P("  residual of about d_p90 * sd(char) in raw units, at every reachable rung.  To get raw")
    P("  units for a characteristic, multiply by its sd from the POOL chars table above.")

    # ------------------------------------------------------------------ RULE 8 / WF-A
    P("")
    P("=" * 118)
    P("RULE 8 / WF-A - the LAW walked forward.  Characteristics re-estimated IS-only and OOS-only,")
    P("rungs re-frozen per window, predictor CHOSEN on IS by pooled R^2, OOS read ONCE.")
    P("=" * 118)
    wf = []
    wins = {}
    for wname, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
        pw = pool_all.loc[sl]
        ncw = chars_for(pw, spy.loc[sl])
        bw_ = [c for c in b_ok if c in ncw.index]
        sw_ = [c for c in s_ok if c in ncw.index]
        armw = arm_pairs(ncw, bw_, sw_, set(pw.columns))
        lvw = {c: [round(float(ncw[c].quantile(q)), 6) for q in LEVEL_Q] for c in CHARS}
        rw = pd.DataFrame(measure(ncw, pw, armw, lvw, wname, nrep=1))
        wins[wname] = rw
        P(f"  {wname:4s} window {pw.index.min().date()}..{pw.index.max().date()} "
          f"({len(pw)} bars)  feasible rungs {int((rw.feasible==1).sum())} of {len(rw)}")
    WF = pd.concat([wins["IS"], wins["OOS"]], ignore_index=True)
    WF.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    P("")
    P(f"  {'predictor':10s} {'IS R2':>8s} {'IS slope':>10s} {'OOS R2':>8s} {'OOS slope':>10s} "
      f"{'IS rho':>8s} {'OOS rho':>8s}")
    isf, oof = {}, {}
    for k in ("SMD", "DISP", "min_n", "neff_min", "inv_OVL"):
        out = {}
        for wname in ("IS", "OOS"):
            g = wins[wname]
            g = g[g.feasible == 1]
            x = (1.0 / g.OVL.replace(0, np.nan)) if k == "inv_OVL" else g[k]
            out[wname] = ols_fit(x, g.d)
        isf[k], oof[k] = out["IS"], out["OOS"]
        P(f"  {k:10s} {out['IS']['R2']:8.3f} {out['IS']['slope']:10.5f} {out['OOS']['R2']:8.3f} "
          f"{out['OOS']['slope']:10.5f} {out['IS']['spearman']:+8.3f} {out['OOS']['spearman']:+8.3f}")
    pick = max(isf, key=lambda k: (isf[k]["R2"] if np.isfinite(isf[k]["R2"]) else -9))
    P(f"  WF-A PICK (IS pooled R^2 ALONE): {pick}   IS R^2 {isf[pick]['R2']:.3f} slope "
      f"{isf[pick]['slope']:+.5f}  ->  OOS R^2 {oof[pick]['R2']:.3f} slope "
      f"{oof[pick]['slope']:+.5f}  (read once)")
    law.append(dict(test="WF_A", stat=f"pick={pick}", value=oof[pick]["R2"], bar=np.nan,
                    passed=np.nan, slope=oof[pick]["slope"], spearman=isf[pick]["R2"]))

    # H_ENTITLE: IS-fitted p90 curve read once on OOS
    gi = wins["IS"][wins["IS"].feasible == 1].copy()
    go = wins["OOS"][wins["OOS"].feasible == 1].copy()
    gi["bin"] = pd.cut(gi.SMD, SMD_BINS, right=False)
    go["bin"] = pd.cut(go.SMD, SMD_BINS, right=False)
    pi = gi.groupby("bin", observed=True).d.quantile(0.90)
    po = go.groupby("bin", observed=True).d.quantile(0.90)
    P("")
    P(f"  H_ENTITLE: IS-fitted p90 entitlement read ONCE on OOS-estimated characteristics")
    P(f"  {'SMD bin':16s} {'n_IS':>5s} {'n_OOS':>6s} {'IS p90':>8s} {'OOS p90':>8s} {'ratio':>7s}")
    ratios = []
    for b in pi.index:
        if b not in po.index:
            P(f"  {str(b):16s} {int((gi.bin==b).sum()):5d} {0:6d} {pi[b]:8.4f} {'-':>8s} {'-':>7s}")
            continue
        rt = po[b] / pi[b] if pi[b] > 0 else np.nan
        ratios.append(rt)
        P(f"  {str(b):16s} {int((gi.bin==b).sum()):5d} {int((go.bin==b).sum()):6d} "
          f"{pi[b]:8.4f} {po[b]:8.4f} {rt:7.2f}x")
    h_ent = bool(len(ratios) > 0 and all(np.isfinite(r) and r <= 1.5 for r in ratios))
    P(f"            worst ratio {max(ratios) if ratios else np.nan:.2f}x  bar <= 1.50x in every "
      f"bin -> {'PASS' if h_ent else 'FAIL'}")
    law.append(dict(test="H_ENTITLE", stat="worst_OOS_over_IS_p90",
                    value=max(ratios) if ratios else np.nan, bar=1.50, passed=h_ent))
    pd.DataFrame(law).to_csv(f"{OUT}/{STAMP}.law.csv", index=False)

    # ------------------------------------------------------------------ WF-B books + KEEP paths
    P("")
    P("=" * 118)
    P("RULE 8 / WF-B + KEEP PATHS - every drawn book run as a real book (10 bps, next-day fills).")
    P("=" * 118)
    base_r = fast_backtest(px56, rules_v2_weights(px56), COST, "W")["returns"]
    start = pool_all.index[260]
    idxb = pool_all.loc[start:].index
    b_ret = base_r.reindex(idxb).fillna(0.0)
    spy_ret = spy.pct_change().fillna(0.0).reindex(idxb).fillna(0.0)
    bm, sm = rowify(b_ret), rowify(spy_ret)
    P(f"  comparands over {idxb[0].date()}..{idxb[-1].date()} ({len(idxb)} bars)")
    P(f"    RULES v2 (U56, live) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} MaxDD "
      f"{bm['MaxDD']:.2%} halves {bm['H1']:.3f}/{bm['H2']:.3f} | OOS CAGR {bm['OOS_CAGR']:.2%} "
      f"Sharpe {bm['OOS_Sharpe']:.3f} MaxDD {bm['OOS_MaxDD']:.2%}")
    P(f"    SPY                  CAGR {sm['CAGR']:.2%} Sharpe {sm['Sharpe']:.3f} MaxDD "
      f"{sm['MaxDD']:.2%} halves {sm['H1']:.3f}/{sm['H2']:.3f} | OOS CAGR {sm['OOS_CAGR']:.2%} "
      f"Sharpe {sm['OOS_Sharpe']:.3f} MaxDD {sm['OOS_MaxDD']:.2%}")
    books, seen = [], {}
    for (pair, char, L, arm, sdd), names in book_sets.items():
        full = pool_all[names]
        ma_ok = (full > full.rolling(MA_WIN).mean()).loc[start:]
        sub = full.loc[start:]
        priced = sub.notna()
        for form in ("EWall", "MA-RS"):
            mask = priced if form == "EWall" else (priced & ma_ok)
            nn = mask.sum(axis=1).replace(0, np.nan)
            for g in GROSS:
                key = (tuple(names), form, g)
                if key in seen:
                    rr = seen[key]
                else:
                    w = g * mask.div(nn, axis=0).fillna(0.0)
                    r_ser = fast_backtest(sub, w, COST, "W")["returns"]
                    rr = rowify(r_ser)
                    rr["_4a"] = keep_4a(r_ser, b_ret)
                    rr["_4b"] = fail_4b(r_ser, spy_ret)
                    seen[key] = rr
                books.append(dict(bkey=zlib.crc32(repr(key).encode()), pair=pair, char=char,
                                  level=L, arm=arm, seed=sdd, form=form, gross=g,
                                  keep4a=rr["_4a"], fail4b=rr["_4b"], keep4b=rr["_4b"] == "-",
                                  **{k: v for k, v in rr.items() if not k.startswith("_")}))
    BK = pd.DataFrame(books)
    BK.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    n4a, n4b = int(BK.keep4a.sum()), int(BK.keep4b.sum())
    nboth = int((BK.keep4a & BK.keep4b).sum())
    U = BK.drop_duplicates("bkey")
    P(f"  {len(BK)} books ({BK.pair.nunique()} pairs x {BK.char.nunique()} chars x "
      f"{BK.level.nunique()} rungs x {BK.arm.nunique()} arms x 2 seeds x 2 forms x "
      f"{len(GROSS)} gross); {len(U)} DISTINCT name-set/form/gross books")
    P(f"  KEEP paths over all books: 4a {n4a} ({n4a/len(BK):.1%})   4b {n4b} ({n4b/len(BK):.1%})   "
      f"BOTH {nboth}")
    P(f"  on the {len(U)} distinct books: 4a {int(U.keep4a.sum())}  4b {int(U.keep4b.sum())}  "
      f"BOTH {int((U.keep4a & U.keep4b).sum())}")
    fb = BK.fail4b.value_counts().head(6)
    P("  most common 4b failure sets: " + ", ".join(f"{k} x{v}" for k, v in fb.items()))
    pickb = BK.sort_values("IS_Sharpe", ascending=False).iloc[0]
    P("")
    P("  WF-B pick (IS Sharpe ALONE, OOS read once):")
    P(f"    {pickb.pair}/{pickb.char} rung {pickb.level:.4f} arm {pickb.arm} seed {int(pickb.seed)} "
      f"{pickb.form} g={pickb.gross:.2f}   IS Sharpe {pickb.IS_Sharpe:.3f}")
    P(f"    OOS  CAGR {pickb.OOS_CAGR:.2%}  Sharpe {pickb.OOS_Sharpe:.3f}  MaxDD {pickb.OOS_MaxDD:.2%}"
      f"   vs RULES v2 OOS {bm['OOS_CAGR']:.2%}/{bm['OOS_Sharpe']:.3f}/{bm['OOS_MaxDD']:.2%}"
      f"   vs SPY OOS {sm['OOS_CAGR']:.2%}/{sm['OOS_Sharpe']:.3f}/{sm['OOS_MaxDD']:.2%}")
    P(f"    FULL CAGR {pickb.CAGR:.2%}  Sharpe {pickb.Sharpe:.3f}  MaxDD {pickb.MaxDD:.2%}  "
      f"halves {pickb.H1:.3f}/{pickb.H2:.3f}   4a {bool(pickb.keep4a)}  4b fails [{pickb.fail4b}]")
    nb_beat = int((BK.OOS_Sharpe > bm["OOS_Sharpe"]).sum())
    ns_beat = int((BK.OOS_Sharpe > sm["OOS_Sharpe"]).sum())
    P(f"    books beating RULES v2 OOS Sharpe: {nb_beat} of {len(BK)}; beating SPY OOS Sharpe: "
      f"{ns_beat} of {len(BK)}")
    P("  STATED UP FRONT and unchanged: a kernel-weighted seeded draw is a diagnostic panel, not a")
    P("  tradable rule, so no 4b pass here is claimed as a capital candidate.")

    # ------------------------------------------------------------------ verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    flags = {"H_SMD": h_smd, "H_LIN": h_lin, "H_DISP": h_disp, "H_SIZE": h_size,
             "H_NOISE": h_noise, "H_ENTITLE": h_ent}
    for k, vv in flags.items():
        P(f"  {k:10s} {'PASS' if vv else 'FAIL'}")
    P(f"  ran in {time.time()-t0:.1f}s")
    Path(f"{OUT}/{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    return flags


if __name__ == "__main__":
    main()
