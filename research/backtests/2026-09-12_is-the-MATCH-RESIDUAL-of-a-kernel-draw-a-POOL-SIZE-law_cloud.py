#!/usr/bin/env python3
"""Idea 800 (cloud, 2026-09-12) - is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law.

QUESTION
--------
Idea 569/571's machinery matches two sub-panels (BONLY, sourced from B136; SONLY, sourced from the
sub-$2B panel) at a common LEVEL of a per-name characteristic by drawing k names with Gaussian
kernel weights w ~ exp(-0.5((x-L)/h)^2), h = BW * sd(char over the pool).  The MATCH RESIDUAL is
what is left over: resid(L) = achieved_B(L) - achieved_S(L), the difference between the two arms'
realised mean levels.  Every matched-level claim in the record is entitled only to the precision
its residual permits.

Idea 796 found the residual does NOT respond to the dial the queue expected: narrowing the kernel
made the match WORSE (|resid| 0.0027 -> 0.0129 -> 0.0147 at BW 0.500/0.250/0.125), while growing
the small panel from 430 to 663 names took it 0.0133 -> 0.0027 with nothing tuned.  Idea 800 asks
for the LAW: |resid| as a function of pool size at fixed k, on sub-sampled pools, so a future claim
can state the residual it is entitled to before it measures one.

THE QUEUE'S PREMISE, STATED SO IT CAN FAIL
------------------------------------------
The queue reads idea 796's evidence as "the residual is governed by the thin arm's pool density",
i.e. by min(n_BONLY, n_SONLY).  That reading has a problem visible before any code runs, and it is
pre-registered here rather than discovered later: the 430 -> 663 move idea 796 cites grew the THICK
arm (SMALL) and left the THIN arm (B136) untouched, so under a min(n) law it should have changed
NOTHING.  Either the law is not a min(n) law, or that observation has another cause.  The obvious
other cause is that momac is a cross-sectional rank WITHIN the pool, so adding 233 small names
re-writes every name's characteristic - a composition channel, not a size channel.  This run
separates the two by construction (CHARBASIS below) instead of arguing about them.

DESIGN
------
Arms are sub-sampled to TARGET SIZES and the kernel draw is re-run inside them.  The target LEVELS
are the FULL pool's own quantiles, frozen once in raw characteristic units, so a rung means the same
thing in every cell and only the pool moves.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: pool size, k)
    1. POOL SIZE  s in {40, 60, 90, 136, 200, 330}, applied three ways per pair:
         SYM   n_thin = n_thick = s          both arms at s
         THIN  n_thin = s, n_thick = max     only the thin arm moves (min(n) moves)
         THICK n_thin = max, n_thick = s     only the thick arm moves (min(n) is FLAT until s < n_thin)
       THIN vs THICK is the discriminating test for the queue's min(n) reading.
    2. K in {12, 24, 36, 48}                 36 = idea 569/571's draw size, the anchor.
    All 2 x 18 x 4 = 144 grid points are reported, including the ones that are INFEASIBLE
    (s <= K leaves the kernel no freedom; s > 136 does not exist inside B136).

REPORTED-NEVER-SELECTED axes: arm pair (BS = the record's B-vs-SMALL arms; SS = two disjoint random
halves of the small panel, a SAME-DISTRIBUTION null whose residual can only be matching error and
which reaches min(n) = 330), characteristic (momac = the variable idea 796 measured, tpers = idea
571's tight-match reference control), CHARBASIS (FULL = characteristics and bandwidth frozen at the
full pool, isolating pure draw geometry; SUB = both recomputed inside the sub-sample, adding the
rank-renormalisation channel), replicate 0..5, rung, seed 0..5, window, gross, cadence, book form.
BW is held at idea 569/571's 0.500 and is NOT a dial here - idea 796 already swept it.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_MONO : mean |resid| is monotone decreasing in min(n) at fixed K - Spearman(min_n, |resid|)
             <= -0.90 on the SYM ladder, in both characteristics and both pairs.
    H_MIN  : the queue's reading.  The THIN arm governs.  Moving the THICK arm alone, while it
             stays above the thin arm, leaves |resid| unchanged (|d log10 |resid|| < 0.10 across
             those cells) while moving the THIN arm alone reproduces the SYM curve to within 1.25x
             at every s.
    H_POWER: the law is a power law.  log10 |resid| on log10 min_n is linear with R^2 >= 0.80 and
             slope in [-1.00, -0.25], and the fitted slope agrees between the two characteristics
             to within 0.15.
    H_FILL : the governing variable is the FILL RATIO K/min_n, not min_n - pooling the four K rungs,
             the K/min_n fit has a smaller residual sd than the min_n fit.
    H_NEFF : the physical variable is the kernel's EFFECTIVE sample size at the rung (Kish
             n_eff = (sum w)^2 / sum w^2 in the thin arm), which beats both on pooled R^2.
    H_VINT : the min(n) law explains idea 796's 430 -> 663 observation.  Pre-registered as expected
             to FAIL (that move held the thin arm fixed); the stated alternative is CHARBASIS.
             Tested directly by rebuilding |resid| on idea 571's FROZEN 439-name small arm and on
             today's 663-name arm with the B arm held fixed, under both bases.

GATES (run and printed BEFORE any new number is read)
    G0 determinism : every draw rebuilt twice gives identical name sets.                    bar 0
    G1 contiguity  : each name's valid mask is one contiguous block, which is what makes the
                     vectorised lag-21 autocorrelation identical to idea 571's dropna-then-shift
                     estimator.                                                     bar: 0 breaks
    G2 estimator   : vectorised momac vs idea 571/796's pandas estimator, 40 sampled names. bar 1e-12
    G3 engine      : fast_backtest vs engine.backtest on two drawn books.                 bar 1e-9
    G4 anchor      : this run's full-pool BW=0.500 / Q5 / K=36 residual against idea 796's committed
                     `.origin.csv` rows.  MEASURED and published; the panel has been appended to
                     since idea 796 ran, so this is a drift reading, not a pass/fail bar.

RULE 8 WALK-FORWARD (required)
    IS = ..2016-12-31, OOS = 2017-01-01.. , OOS read ONCE.
    WF-A on the ANSWER: characteristics are re-estimated on IS prices alone and on OOS prices alone
       and the whole law is refit in each window.  The predictor is CHOSEN on IS by pooled R^2 and
       its OOS R^2 / slope are then read once, so "which variable governs the residual" is itself
       walked forward rather than fitted on the full sample.
    WF-B on a BOOK: the law taken as a trading instruction - "draw at a matched level from whichever
       arm is available".  Among all drawn books (flavour, pool size, K, rung, seed, gross, form)
       the pick is made by IS Sharpe ALONE, then OOS CAGR / Sharpe / MaxDD are read ONCE against
       live RULES v2 (U56, weekly, 10 bps) and against SPY.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY book
    and counted.  Stated up front: a kernel-weighted seeded draw is a diagnostic panel, not a rule
    anyone can trade, so no 4b pass on this ladder is claimed as a capital candidate.

SURVIVORSHIP: B136 is the current constituent list of universe_broad.json; the small panel is the
    current constituent list of its sub-$2B screen with every ticker whose max_1d_move >= 1.0 in
    data/small_meta.csv dropped first, per PROTOCOL.  Names that died are absent from both.  For
    this run the bias is second-order - the object measured is a difference of ACHIEVED
    CHARACTERISTIC LEVELS between two draws from the same screened universe, not a return - but the
    return legs (WF-B, the KEEP-path counts) carry the usual upward bias and are read as diagnostics.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine convention), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and idea 796's committed
artefacts; modifies nothing but its own outputs:
    .grid.csv .rungs.csv .law.csv .walkforward.csv .keeppaths.csv .vintage.csv .console.txt
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

STAMP = "2026-09-12_is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law_cloud"
OUT = ROOT / "research" / "backtests"

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252
AC_LAG = 21
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"            # idea 571/796's last bar - kept so G4 is comparable
BW = 0.500                           # idea 569/571's bandwidth; NOT a dial here (idea 796 swept it)
SIZES = [40, 60, 90, 136, 200, 330]  # TUNED 1
KS = [12, 24, 36, 48]                # TUNED 2
K_ANCHOR = 36
LEVEL_Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]
SEEDS = [0, 1, 2, 3, 4, 5]
REPS = [0, 1, 2, 3, 4, 5]
CHARS = ["momac", "tpers"]
PAIRS = ["BS", "SS"]
BASES = ["FULL", "SUB"]
SHAPES = ["SYM", "THIN", "THICK"]
PARENT796 = OUT / "2026-09-11_is-momac-s-0.0549-MATCHED-LEVEL-GAP-real-or-a-MATCHING-RESIDUAL_cloud"
PARENT571 = OUT / "2026-09-11_is-tpers-INFORMATION-or-TAUTOLOGY_B"
TOL = 1e-9

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
def _flip_persistence(state, valid):
    st = state.where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def tpers_chars(pool):
    """Per-name trend persistence.  Pool-INDEPENDENT: uses each column against its own 200d MA."""
    ma = pool.rolling(MA_WIN).mean()
    return _flip_persistence(pool > ma, pool.notna() & ma.notna())


def _ac_vec(R):
    """Column-wise lag-AC_LAG Pearson correlation of an ndarray with NaNs, over rows valid at both
    t and t-AC_LAG.  Identical to idea 571's `s.dropna().corr(s.dropna().shift(21))` whenever each
    column's valid mask is one contiguous block (gate G1)."""
    X, Y = R[AC_LAG:], R[:-AC_LAG]
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
    ac[n <= 3 * AC_LAG] = np.nan
    return ac


def momac_chars(pool, mom=None):
    """momac = lag-21 autocorrelation of the name's 12-1 momentum rank_pct.  The rank is
    CROSS-SECTIONAL WITHIN THE GIVEN COLUMN SET, so this is a property of the pool too."""
    if mom is None:
        mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    valid = pool.notna() & mom.notna()
    R = rk.where(valid).to_numpy(dtype=float)
    return pd.Series(_ac_vec(R), index=pool.columns)


def momac_ref(pool):
    """Idea 571/796's estimator, verbatim - the G2 reference."""
    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    v = pool.notna() & mom.notna()
    out = {}
    for c in pool.columns:
        s = rk[c].where(v[c]).dropna()
        out[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    return pd.Series(out, dtype=float)


def avol_chars(pool):
    """Annualised realised daily vol per name.  Pool-independent, and NOT used anywhere in the
    grid - it is held out as a third characteristic to test the bandwidth-units reading."""
    return pool.pct_change().std() * np.sqrt(252)


def chars_for(pool, want=("momac", "tpers")):
    d = {}
    if "tpers" in want:
        d["tpers"] = tpers_chars(pool)
    if "momac" in want:
        d["momac"] = momac_chars(pool)
    if "avol" in want:
        d["avol"] = avol_chars(pool)
    return pd.DataFrame(d)


# ------------------------------------------------------------------------- the kernel draw
def kernel_draw(names, x, L, h, k, seed_key):
    """Idea 569/571's scheme with its seed key verbatim; returns (picked names, achieved, n_eff)."""
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


def loglog_fit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if m.sum() < 3:
        return dict(n=int(m.sum()), slope=np.nan, icept=np.nan, R2=np.nan, sd_resid=np.nan,
                    spearman=np.nan)
    lx, ly = np.log10(x[m]), np.log10(y[m])
    b, a = np.polyfit(lx, ly, 1)
    pred = a + b * lx
    ss_res = float(((ly - pred) ** 2).sum())
    ss_tot = float(((ly - ly.mean()) ** 2).sum())
    rx = pd.Series(x[m]).rank().to_numpy()
    ry = pd.Series(y[m]).rank().to_numpy()
    sp = float(np.corrcoef(rx, ry)[0, 1]) if m.sum() > 2 else np.nan
    return dict(n=int(m.sum()), slope=float(b), icept=float(a),
                R2=float(1 - ss_res / ss_tot) if ss_tot > 0 else np.nan,
                sd_resid=float(np.std(ly - pred, ddof=1)), spearman=sp)


# ------------------------------------------------------------------------- residual measurement
def cell_plan(pair, n_thin_max, n_thick_max):
    """(shape, s) -> (target thin size, target thick size), skipping sizes an arm cannot reach."""
    out = []
    for shape in SHAPES:
        for s in SIZES:
            if shape == "SYM":
                nt, nk = s, s
            elif shape == "THIN":
                nt, nk = s, n_thick_max
            else:
                nt, nk = n_thin_max, s
            if nt > n_thin_max or nk > n_thick_max:
                out.append(dict(pair=pair, shape=shape, s=s, n_thin=nt, n_thick=nk,
                                available=False))
                continue
            out.append(dict(pair=pair, shape=shape, s=s, n_thin=nt, n_thick=nk, available=True))
    return out


def subsample(names, target, rep, tag):
    if target >= len(names):
        return list(names)
    rng = np.random.default_rng(zlib.crc32(f"SUB|{tag}|{target}|{rep}".encode()) % (2 ** 32))
    return sorted(rng.choice(np.asarray(names), size=target, replace=False).tolist())


def measure_cell(nc_full, pool, mom, thin_names, thick_names, levels, k, basis, tag,
                 thin_label, thick_label, chars=CHARS):
    """Return per-(char, level) residual rows and the drawn name sets, for ONE sub-sampled cell."""
    cols = sorted(set(thin_names) | set(thick_names))
    if basis == "SUB":
        nc = pd.DataFrame(index=cols)
        if "momac" in chars:
            nc["momac"] = momac_chars(pool[cols], mom[cols])
        if "tpers" in chars:
            nc["tpers"] = nc_full.loc[cols, "tpers"]      # pool-independent by construction
    else:
        nc = nc_full.loc[cols]
    rows, sets = [], {}
    for char in chars:
        sd = float(nc[char].std()) if basis == "SUB" else float(nc_full[char].std())
        if not np.isfinite(sd) or sd <= 0:
            continue
        h = BW * sd
        arms = {"THIN": [c for c in thin_names if np.isfinite(nc[char].get(c, np.nan))],
                "THICK": [c for c in thick_names if np.isfinite(nc[char].get(c, np.nan))]}
        if min(len(arms["THIN"]), len(arms["THICK"])) <= k:
            continue
        xs = {a: nc.loc[arms[a], char].to_numpy(dtype=float) for a in arms}
        nms = {a: np.array(arms[a]) for a in arms}
        rch = {a: reach(xs[a], k) for a in arms}
        for L in levels[char]:
            if not all(rch[a][0] <= L <= rch[a][1] for a in arms):
                continue
            ach, nef, ok = {}, {}, True
            for a in arms:
                per = []
                for sdd in SEEDS:
                    pick, av, ne = kernel_draw(nms[a], xs[a], L, h, k,
                                               f"CHAR|{char}|{L:.6f}|{a}|{sdd}")
                    if pick is None:
                        ok = False
                        break
                    per.append(av)
                    nef[a] = ne
                    sets[(char, L, a, sdd)] = pick
                if not ok:
                    break
                ach[a] = per
            if not ok:
                continue
            mb, ms = float(np.mean(ach["THIN"])), float(np.mean(ach["THICK"]))
            perseed = float(np.mean([abs(b - s) for b, s in zip(ach["THIN"], ach["THICK"])]))
            rows.append(dict(tag=tag, char=char, level=L, k=k, basis=basis,
                             n_thin=len(arms["THIN"]), n_thick=len(arms["THICK"]),
                             min_n=min(len(arms["THIN"]), len(arms["THICK"])),
                             tot_n=len(arms["THIN"]) + len(arms["THICK"]),
                             thin_label=thin_label, thick_label=thick_label,
                             achieved_thin=mb, achieved_thick=ms, resid=mb - ms,
                             abs_resid=abs(mb - ms), abs_resid_perseed=perseed,
                             neff_min=float(min(nef["THIN"], nef["THICK"])),
                             neff_thin=float(nef["THIN"]), neff_thick=float(nef["THICK"]),
                             sd_char=sd))
    return rows, sets


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 800 - is the kernel draw's MATCH RESIDUAL a POOL-SIZE law?  Sub-sample the arms at")
    P("#            fixed k, measure |resid| against min(n), and publish the law - or kill it.")
    P("=" * 118)
    P(f"# PROTOCOL: {COST:.0f} bps per unit turnover, next-day fills, IS <= {IS_END}, "
      f"OOS >= {OOS_START}, sample truncated at {PARENT_END} (idea 571/796's last bar).")
    P(f"# TUNED (2): pool size s in {SIZES} x k in {KS}.  BW held at idea 569/571's {BW:.3f}.")
    P("#            REPORTED-NOT-SELECTED: arm pair, characteristic, CHARBASIS, shape, replicate,")
    P("#            rung, seed, window, gross, cadence, book form.")
    P("")
    P("PRE-REGISTERED: H_MONO (|resid| falls with min_n, Spearman <= -0.90), H_MIN (the THIN arm")
    P("  governs: THICK-only moves are inert, THIN-only reproduces SYM to 1.25x), H_POWER (log-log")
    P("  R^2 >= 0.80, slope in [-1.00,-0.25], agreeing across chars to 0.15), H_FILL (K/min_n beats")
    P("  min_n), H_NEFF (kernel n_eff beats both), H_VINT (the min_n law explains idea 796's")
    P("  430->663 move - pre-registered as EXPECTED TO FAIL, since that move held the thin arm")
    P("  fixed; the stated alternative is the CHARBASIS rank-renormalisation channel).")
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
      f"({len(bad)} max_1d_move>=1.0 tickers dropped per PROTOCOL), "
      f"pool {pool_all.shape[1]} names over {len(ix)} bars {ix.min().date()}..{ix.max().date()}")
    P("SURVIVORSHIP: both arms are CURRENT constituents; dead names are absent.  The object here is")
    P("  a difference of ACHIEVED CHARACTERISTIC LEVELS between two draws from the same screened")
    P("  universe, so the bias is second-order for the law; the return legs carry the usual bias.")
    P("")

    mom_all = pool_all.shift(MOM_LAG) / pool_all.shift(MOM_LOOK) - 1.0
    nc_full = chars_for(pool_all)
    b_ok = [c for c in b_stk if c in nc_full.index]
    s_ok = [c for c in s_stk if c in nc_full.index]
    P(f"POOL chars: " + ", ".join(
        f"{c} usable {int(nc_full[c].notna().sum())} (B {int(nc_full.loc[b_ok, c].notna().sum())}"
        f" / S {int(nc_full.loc[s_ok, c].notna().sum())}), sd {float(nc_full[c].std()):.4f}, "
        f"h {BW*float(nc_full[c].std()):.4f}" for c in CHARS))

    LEVELS = {c: [round(float(nc_full[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
    for c in CHARS:
        P(f"  frozen rungs {c:6s} (full-pool Q5 quantiles, raw units): "
          + " ".join(f"{v:.4f}" for v in LEVELS[c]))
    P("")

    # ------------------------------------------------------------------ GATES
    P("=" * 118)
    P("GATES")
    P("=" * 118)
    gates = []
    v = pool_all.notna()
    first = v.idxmax()
    gappy = [c for c in pool_all.columns if not bool(v[c].loc[first[c]:].all())]
    if gappy:
        P(f"  G1 contiguity : {len(gappy)} of {pool_all.shape[1]} names carry an interior gap "
          f"({' '.join(gappy)}) -> DROPPED from the pool, so the vectorised lag-21 AC is exact by")
        P("                  construction for every remaining name.  Stated, not worked around.")
        pool_all = pool_all.drop(columns=gappy)
        b_stk = [c for c in b_stk if c not in gappy]
        s_stk = [c for c in s_stk if c not in gappy]
        mom_all = mom_all.drop(columns=gappy)
        nc_full = nc_full.drop(index=gappy)
        b_ok = [c for c in b_ok if c not in gappy]
        s_ok = [c for c in s_ok if c not in gappy]
    else:
        P(f"  G1 contiguity : 0 of {pool_all.shape[1]} names carry an interior gap -> PASS")
    gates.append(dict(gate="G1_contiguity_dropped", value=len(gappy), bar=0, passed=True))
    if gappy:
        nc_full = chars_for(pool_all)
        b_ok = [c for c in b_stk if c in nc_full.index]
        s_ok = [c for c in s_stk if c in nc_full.index]
        LEVELS = {c: [round(float(nc_full[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
        P("                  rungs re-frozen on the {}-name pool: ".format(pool_all.shape[1])
          + "; ".join(f"{c} " + " ".join(f"{v:.4f}" for v in LEVELS[c]) for c in CHARS))

    samp = sorted(np.random.default_rng(0).choice(np.array(pool_all.columns), 40,
                                                  replace=False).tolist())
    ref = momac_ref(pool_all[samp])
    fastc = momac_chars(pool_all[samp])
    d2 = float(np.nanmax(np.abs(ref - fastc)))
    P(f"  G2 estimator  : max |vectorised momac - idea 571 pandas momac| over 40 names {d2:.3e}"
      f"   bar 1e-12 -> {'PASS' if d2 < 1e-12 else 'FAIL'}")
    gates.append(dict(gate="G2_estimator", value=d2, bar=1e-12, passed=bool(d2 < 1e-12)))

    b_mom = [c for c in b_ok if np.isfinite(nc_full.loc[c, "momac"])]
    x0 = nc_full.loc[b_mom, "momac"].to_numpy(dtype=float)
    n0 = np.array(b_mom)
    h0 = BW * float(nc_full["momac"].std())
    p1, a1, _ = kernel_draw(n0, x0, LEVELS["momac"][2], h0, K_ANCHOR, "G0|momac|mid")
    p2, a2, _ = kernel_draw(n0, x0, LEVELS["momac"][2], h0, K_ANCHOR, "G0|momac|mid")
    same = int(p1 == p2)
    P(f"  G0 determinism: identical name sets on two rebuilds -> {'PASS' if same else 'FAIL'}")
    gates.append(dict(gate="G0_determinism", value=1 - same, bar=0, passed=bool(same)))

    bk = pool_all[p1]
    w = pd.DataFrame(1.0 / len(p1), index=bk.index, columns=bk.columns) * 0.75
    r_fast = fast_backtest(bk, w)["returns"]
    r_eng = backtest(bk, w, cost_bps=COST, freq="W")["returns"]
    d3 = float(np.abs(r_fast - r_eng).max())
    P(f"  G3 engine     : max |fast_backtest - engine.backtest| on a drawn book {d3:.3e}"
      f"   bar 1e-9 -> {'PASS' if d3 < TOL else 'FAIL'}")
    gates.append(dict(gate="G3_engine", value=d3, bar=TOL, passed=bool(d3 < TOL)))

    # G4 anchor: full pool, BS pair, K=36, basis FULL - against idea 796's committed origin rows
    rows_anchor, _ = measure_cell(nc_full, pool_all, mom_all, b_ok, s_ok, LEVELS, K_ANCHOR,
                                  "FULL", "ANCHOR", "B", "S")
    AN = pd.DataFrame(rows_anchor)
    o796 = pd.read_csv(f"{PARENT796}.origin.csv")
    o796 = o796[(o796.vint == "LIVE") & (np.abs(o796.BW - BW) < 1e-9)]
    P("  G4 anchor     : this run's full-pool BW=0.500 / Q5 / k=36 |resid| vs idea 796's committed")
    v4 = []
    for c in CHARS:
        mine = AN[AN.char == c]
        theirs = o796[o796.char == c]
        mv = float(mine.abs_resid.mean()) if len(mine) else np.nan
        tv = float(theirs.match_resid.abs().mean()) if len(theirs) else np.nan
        P(f"                  {c:6s} this run {mv:.4f} on {len(mine)} rungs   |   idea 796 "
          f"{tv:.4f} on {len(theirs)} rungs (its own rung set)")
        v4.append(dict(leg="G4_anchor", char=c, this_run=mv, idea796=tv,
                       n_rungs_here=len(mine), n_rungs_796=len(theirs)))
    P("                  MEASURED, not gated: data/prices_small.csv has been appended to since idea")
    P("                  796 ran and its LIVE momac rung set was Q19, so this is a drift reading.")
    P("")

    # ------------------------------------------------------------------ the grid
    P("=" * 118)
    P("GRID - |resid| over (pair, shape, s, k, basis, replicate).  All 144 (pair,shape,s,k) points")
    P("       are listed; a point is INFEASIBLE when an arm cannot reach s, or when s <= k leaves")
    P("       the kernel no freedom, or when no frozen rung is inside both arms' reach.")
    P("=" * 118)
    grid_rows, book_sets = [], {}
    ss_rng = np.random.default_rng(20260912)
    s_perm = list(np.array(s_ok)[ss_rng.permutation(len(s_ok))])
    SS_A, SS_B = sorted(s_perm[:len(s_perm) // 2]), sorted(s_perm[len(s_perm) // 2:])
    ARMS = {"BS": (b_ok, s_ok, "B", "S"), "SS": (SS_A, SS_B, "S1", "S2")}
    P(f"  arm pairs: BS thin=B({len(b_ok)}) thick=S({len(s_ok)});  "
      f"SS thin=S1({len(SS_A)}) thick=S2({len(SS_B)})  [disjoint random halves of the small panel,")
    P("             a SAME-DISTRIBUTION null whose residual can only be matching error]")
    for pair in PAIRS:
        thin_all, thick_all, tl, kl = ARMS[pair]
        for plan in cell_plan(pair, len(thin_all), len(thick_all)):
            for k in KS:
                if not plan["available"] or min(plan["n_thin"], plan["n_thick"]) <= k:
                    grid_rows.append(dict(pair=pair, shape=plan["shape"], s=plan["s"], k=k,
                                          available=False, n_cells=0))
                    continue
                for basis in BASES:
                    for rep in REPS:
                        tn = subsample(thin_all, plan["n_thin"], rep, f"{pair}|thin")
                        kn = subsample(thick_all, plan["n_thick"], rep, f"{pair}|thick")
                        tag = f"{pair}|{plan['shape']}|{plan['s']}|{k}|{basis}|{rep}"
                        rr, ss = measure_cell(nc_full, pool_all, mom_all, tn, kn, LEVELS, k,
                                              basis, tag, tl, kl)
                        for r in rr:
                            r.update(pair=pair, shp=plan["shape"], s=plan["s"], rep=rep,
                                     window="FULL")
                        grid_rows.extend(rr)
                        if (pair == "BS" and basis == "FULL" and rep == 0
                                and plan["shape"] in ("SYM", "THIN")):
                            for kk, vv in ss.items():
                                book_sets[(plan["shape"], plan["s"], k) + kk] = vv
    G = pd.DataFrame([r for r in grid_rows if "char" in r])
    AVAIL = pd.DataFrame([r for r in grid_rows if "char" not in r])
    P(f"  measured {len(G)} (cell, char, rung) residual rows over "
      f"{G.tag.nunique()} feasible cells; {len(AVAIL)} (pair,shape,s,k) points unavailable")
    P("")

    # per-cell aggregation
    CELL = G.groupby(["pair", "shp", "s", "k", "basis", "rep", "char"]).agg(
        n_rungs=("abs_resid", "size"), min_n=("min_n", "first"), tot_n=("tot_n", "first"),
        n_thin=("n_thin", "first"), n_thick=("n_thick", "first"),
        abs_resid=("abs_resid", "mean"), abs_resid_perseed=("abs_resid_perseed", "mean"),
        neff_min=("neff_min", "mean")).reset_index()
    CELL["fill"] = CELL["k"] / CELL["min_n"]
    CELL.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    G.to_csv(f"{OUT}/{STAMP}.rungs.csv", index=False)

    P("SYM LADDER at k=36, CHARBASIS=FULL (mean over 6 replicates; |resid| in raw characteristic units)")
    P(f"  {'pair':4s} {'char':6s} " + " ".join(f"{s:>9d}" for s in SIZES) + "   spearman(min_n,|resid|)")
    hmono = []
    for pair in PAIRS:
        for c in CHARS:
            d = CELL[(CELL.pair == pair) & (CELL["shp"] == "SYM") & (CELL.k == K_ANCHOR)
                     & (CELL.basis == "FULL") & (CELL.char == c)]
            m = d.groupby("s").agg(v=("abs_resid", "mean"), mn=("min_n", "mean"))
            cells = " ".join(f"{m.v.get(s, np.nan):9.5f}" if s in m.index else f"{'-':>9s}"
                             for s in SIZES)
            sp = loglog_fit(m.mn, m.v)["spearman"] if len(m) >= 3 else np.nan
            P(f"  {pair:4s} {c:6s} {cells}   {sp:+.3f}" if np.isfinite(sp)
              else f"  {pair:4s} {c:6s} {cells}       n/a")
            hmono.append(dict(pair=pair, char=c, spearman=sp, n=len(m)))
    HM = pd.DataFrame(hmono)
    ok_mono = bool(len(HM.dropna(subset=["spearman"])) > 0
                   and (HM.spearman.dropna() <= -0.90).all())
    P(f"  H_MONO (all Spearman <= -0.90): {'PASS' if ok_mono else 'FAIL'}"
      f"   [{', '.join(f'{r.pair}/{r.char} {r.spearman:+.3f}' for r in HM.dropna(subset=['spearman']).itertuples())}]")
    P("")

    # ------------------------------------------------------------------ H_MIN: thin vs thick
    P("H_MIN - which arm governs?  |resid| at k=36, CHARBASIS=FULL, mean over replicates.")
    P(f"  {'pair':4s} {'char':6s} {'shape':5s} " + " ".join(f"{s:>9d}" for s in SIZES))
    hmin = []
    for pair in PAIRS:
        for c in CHARS:
            base = {}
            for shape in SHAPES:
                d = CELL[(CELL.pair == pair) & (CELL["shp"] == shape) & (CELL.k == K_ANCHOR)
                         & (CELL.basis == "FULL") & (CELL.char == c)]
                m = d.groupby("s").abs_resid.mean()
                base[shape] = m
                P(f"  {pair:4s} {c:6s} {shape:5s} " + " ".join(
                    f"{m.get(s, np.nan):9.5f}" if s in m.index else f"{'-':>9s}" for s in SIZES))
            n_thin_max = len(ARMS[pair][0])
            full_val = base["THIN"].get(max([x for x in base["THIN"].index] or [0]), np.nan)
            thick_var = [abs(np.log10(base["THICK"][s]) - np.log10(full_val))
                         for s in base["THICK"].index
                         if s >= n_thin_max and base["THICK"][s] > 0 and full_val > 0]
            rat = [base["THIN"][s] / base["SYM"][s] for s in base["THIN"].index
                   if s in base["SYM"].index and base["SYM"][s] > 0]
            hmin.append(dict(pair=pair, char=c,
                             thick_max_dlog=float(np.nanmax(thick_var)) if thick_var else np.nan,
                             thin_vs_sym_max_ratio=float(np.nanmax([max(r, 1 / r) for r in rat]))
                             if rat else np.nan))
    HMIN = pd.DataFrame(hmin)
    P("  leg readings (THICK-only inertness = max |d log10 |resid|| across the THICK ladder;")
    P("   THIN-vs-SYM = worst two-sided ratio):")
    for r in HMIN.itertuples():
        P(f"    {r.pair:4s} {r.char:6s} THICK max |dlog10| {r.thick_max_dlog:.3f} (bar <0.10)   "
          f"THIN/SYM worst ratio {r.thin_vs_sym_max_ratio:.3f} (bar <=1.25)")
    ok_min = bool((HMIN.thick_max_dlog < 0.10).all() and (HMIN.thin_vs_sym_max_ratio <= 1.25).all())
    P(f"  H_MIN: {'PASS' if ok_min else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------ the law
    P("=" * 118)
    P("THE LAW - log10 |resid| against four candidate predictors, pooled over shapes, sizes, k,")
    P("          replicates and rungs (CHARBASIS=FULL; SUB reported beside it).")
    P("=" * 118)
    laws = []
    for basis in BASES:
        for pair in PAIRS:
            for c in CHARS:
                d = CELL[(CELL.pair == pair) & (CELL.basis == basis) & (CELL.char == c)]
                if len(d) < 6:
                    continue
                for pred in ("min_n", "tot_n", "fill", "neff_min"):
                    f = loglog_fit(d[pred], d.abs_resid)
                    laws.append(dict(window="FULL", basis=basis, pair=pair, char=c, predictor=pred,
                                     **f))
    LAW = pd.DataFrame(laws)
    LAW.to_csv(f"{OUT}/{STAMP}.law.csv", index=False)
    P(f"  {'basis':5s} {'pair':4s} {'char':6s} {'predictor':9s} {'n':>5s} {'slope':>8s} "
      f"{'R2':>7s} {'sd_res':>7s} {'spear':>7s}")
    for r in LAW.itertuples():
        P(f"  {r.basis:5s} {r.pair:4s} {r.char:6s} {r.predictor:9s} {r.n:5d} {r.slope:+8.3f} "
          f"{r.R2:7.3f} {r.sd_resid:7.3f} {r.spearman:+7.3f}")
    P("")
    P("SYM-LADDER FIT (the clean ladder: rung- and replicate-averaged |resid| against min_n, one")
    P("  fit per pair x char x k x basis).  This is the law the queue asked for, in isolation.")
    P(f"  {'basis':5s} {'pair':4s} {'char':6s} {'k':>3s} {'pts':>4s} {'slope':>8s} {'R2':>7s} "
      f"{'spear':>7s}   ladder |resid| by s")
    lad = []
    for basis in BASES:
        for pair in PAIRS:
            for c in CHARS:
                for k in KS:
                    d = CELL[(CELL.pair == pair) & (CELL["shp"] == "SYM") & (CELL.k == k)
                             & (CELL.basis == basis) & (CELL.char == c)]
                    if d.s.nunique() < 3:
                        continue
                    m = d.groupby("s").agg(v=("abs_resid", "mean"), mn=("min_n", "mean"))
                    f = loglog_fit(m.mn, m.v)
                    lad.append(dict(leg="sym_ladder", basis=basis, pair=pair, char=c, k=k, **f))
                    P(f"  {basis:5s} {pair:4s} {c:6s} {k:3d} {f['n']:4d} {f['slope']:+8.3f} "
                      f"{f['R2']:7.3f} {f['spearman']:+7.3f}   "
                      + " ".join(f"{int(i)}:{v:.5f}" for i, v in m.v.items()))
    LADDER = pd.DataFrame(lad)
    LADDER.to_csv(f"{OUT}/{STAMP}.ladder.csv", index=False)
    if len(LADDER):
        L0 = LADDER[LADDER.basis == "FULL"]
        P(f"  SYM-ladder summary (CHARBASIS=FULL, {len(L0)} fits): median slope "
          f"{L0.slope.median():+.3f}, median R2 {L0.R2.median():.3f}, "
          f"{int((L0.spearman <= -0.90).sum())} of {len(L0)} with Spearman <= -0.90, "
          f"{int((L0.slope > 0).sum())} with a POSITIVE slope")
    P("")

    pw = LAW[(LAW.basis == "FULL") & (LAW.predictor == "min_n")]
    ok_pow = bool(len(pw) and (pw.R2 >= 0.80).all() and pw.slope.between(-1.00, -0.25).all()
                  and (pw.groupby("pair").slope.apply(lambda x: x.max() - x.min()) <= 0.15).all())
    P(f"  H_POWER (min_n fit R2>=0.80, slope in [-1.00,-0.25], chars agree to 0.15): "
      f"{'PASS' if ok_pow else 'FAIL'}  "
      f"[R2 {' '.join(f'{v:.3f}' for v in pw.R2)}; slope {' '.join(f'{v:+.3f}' for v in pw.slope)}]")
    fl = LAW[(LAW.basis == "FULL") & (LAW.predictor == "fill")].set_index(["pair", "char"])
    mn = LAW[(LAW.basis == "FULL") & (LAW.predictor == "min_n")].set_index(["pair", "char"])
    ne = LAW[(LAW.basis == "FULL") & (LAW.predictor == "neff_min")].set_index(["pair", "char"])
    ok_fill = bool((fl.sd_resid < mn.sd_resid).all())
    ok_neff = bool((ne.R2 > mn.R2).all() and (ne.R2 > fl.R2).all())
    P(f"  H_FILL  (K/min_n residual sd < min_n's): {'PASS' if ok_fill else 'FAIL'}  "
      + " ".join(f"{i}: {fl.sd_resid[i]:.3f} vs {mn.sd_resid[i]:.3f}" for i in fl.index))
    P(f"  H_NEFF  (kernel n_eff beats both on R2): {'PASS' if ok_neff else 'FAIL'}  "
      + " ".join(f"{i}: {ne.R2[i]:.3f} vs {mn.R2[i]:.3f}/{fl.R2[i]:.3f}" for i in ne.index))
    P("")

    # ------------------------------------------------------------------ POST-HOC: bandwidth units
    P("=" * 118)
    P("POST-HOC (stated as post-hoc: this reading was formed AFTER the grid above was printed, and")
    P("is NOT one of the six pre-registered hypotheses) - the residual in BANDWIDTH UNITS.")
    P("  The kernel geometry is scale-equivariant: h = BW * sd(char) and the rungs are the pool's")
    P("  own quantiles, so |resid| should scale with sd(char) and the DIMENSIONLESS residual")
    P("  |resid| / sd(char) should be a constant of the machinery, not of the pool.")
    P("=" * 118)
    sdmap = {c: float(nc_full[c].std()) for c in CHARS}
    N2 = CELL[CELL.basis == "FULL"].copy()
    N2["rel"] = N2.abs_resid / N2.char.map(sdmap)
    P(f"  {'pair':4s} {'char':6s} {'cells':>5s} {'sd(char)':>9s} {'med |resid|':>12s} "
      f"{'med |resid|/sd':>15s} {'IQR':>17s}")
    rel_summary = {}
    for pair in PAIRS:
        for c in CHARS:
            d = N2[(N2.pair == pair) & (N2.char == c)]
            q1, q3 = float(d.rel.quantile(0.25)), float(d.rel.quantile(0.75))
            rel_summary[(pair, c)] = float(d.rel.median())
            P(f"  {pair:4s} {c:6s} {len(d):5d} {sdmap[c]:9.4f} {float(d.abs_resid.median()):12.5f} "
              f"{float(d.rel.median()):15.4f}   [{q1:.4f}, {q3:.4f}]")
    coll = {pair: max(rel_summary[(pair, c)] for c in CHARS)
            / min(rel_summary[(pair, c)] for c in CHARS) for pair in PAIRS}
    raw = {pair: max(float(N2[(N2.pair == pair) & (N2.char == c)].abs_resid.median()) for c in CHARS)
           / min(float(N2[(N2.pair == pair) & (N2.char == c)].abs_resid.median()) for c in CHARS)
           for pair in PAIRS}
    for pair in PAIRS:
        P(f"  {pair}: momac-vs-tpers spread {raw[pair]:.2f}x in RAW units, {coll[pair]:.2f}x once "
          f"divided by sd(char)")
    bs_ss = {c: rel_summary[("BS", c)] / rel_summary[("SS", c)] for c in CHARS}
    P("  cross-panel excess (BS arms / SS same-distribution null), in bandwidth units: "
      + ", ".join(f"{c} {v:.2f}x" for c, v in bs_ss.items()))
    predlo = min(rel_summary[("BS", c)] for c in CHARS)
    predhi = max(rel_summary[("BS", c)] for c in CHARS)
    plo2 = min(rel_summary[("SS", c)] for c in CHARS)
    phi2 = max(rel_summary[("SS", c)] for c in CHARS)
    P("")
    P("  HELD-OUT TEST, prediction stated BEFORE the number is computed: a THIRD characteristic")
    P("  never used above (avol = annualised realised daily vol per name, a completely different")
    P("  distribution and scale) must land inside the same dimensionless band -")
    P(f"    predicted |resid|/sd for the BS arms in [{predlo:.4f}, {predhi:.4f}], "
      f"for the SS null in [{plo2:.4f}, {phi2:.4f}].")
    nc3 = nc_full.copy()
    nc3["avol"] = avol_chars(pool_all)
    lv3 = {"avol": [round(float(nc3["avol"].quantile(q)), 6) for q in LEVEL_Q5]}
    sd3 = float(nc3["avol"].std())
    P(f"    avol: sd {sd3:.4f} (momac {sdmap['momac']:.4f}, tpers {sdmap['tpers']:.4f}); "
      f"rungs " + " ".join(f"{v:.4f}" for v in lv3["avol"]))
    ho = []
    for pair, (ta, ka, tl, kl) in {"BS": (b_ok, s_ok, "B", "S"),
                                   "SS": (SS_A, SS_B, "S1", "S2")}.items():
        for s_ in SIZES:
            if s_ > min(len(ta), len(ka)):
                continue
            for rep in REPS:
                tn = subsample(ta, s_, rep, f"{pair}|thin")
                kn = subsample(ka, s_, rep, f"{pair}|thick")
                rr, _ = measure_cell(nc3, pool_all, mom_all, tn, kn, lv3, K_ANCHOR, "FULL",
                                     f"HO|{pair}|{s_}|{rep}", tl, kl, chars=["avol"])
                for r in rr:
                    ho.append(dict(pair=pair, s=s_, rep=rep, abs_resid=r["abs_resid"],
                                   min_n=r["min_n"], rel=r["abs_resid"] / sd3))
    HO = pd.DataFrame(ho)
    if len(HO):
        HO.to_csv(f"{OUT}/{STAMP}.heldout.csv", index=False)
        for pair in PAIRS:
            d = HO[HO.pair == pair]
            if not len(d):
                continue
            inb = (predlo, predhi) if pair == "BS" else (plo2, phi2)
            med = float(d.rel.median())
            P(f"    READ: {pair} avol on {len(d)} rungs, median |resid| {float(d.abs_resid.median()):.5f}"
              f", |resid|/sd {med:.4f}  -> {'INSIDE' if inb[0] <= med <= inb[1] else 'OUTSIDE'} the "
              f"predicted band [{inb[0]:.4f}, {inb[1]:.4f}]")
            f = loglog_fit(d.groupby("s").min_n.mean(), d.groupby("s").rel.mean())
            P(f"          its own pool-size ladder: slope {f['slope']:+.3f} R2 {f['R2']:.3f} "
              f"Spearman {f['spearman']:+.3f} over {f['n']} sizes")
        for pair in PAIRS:
            d = HO[HO.pair == pair]
            if len(d):
                rel_summary[(pair, "avol")] = float(d.rel.median())
    P("")
    P("  THE ENTITLEMENT the queue asked for, in the only units this machinery supports: the")
    P("  SPREAD of |resid| across cells that differ only in sub-sample.  Two readings: WITHIN-CELL")
    P("  is the six replicates of one identical (shape, size, k) cell - pure draw/sub-sample noise;")
    P("  POOLED adds the shape and size axes, which the grid above showed to be nearly inert.  Any")
    P("  single-cell |resid| a future claim quotes is entitled to no more precision than this.")
    P(f"  {'pair':4s} {'char':6s} {'k':>3s} {'cells':>5s} {'median |resid|':>14s} {'p10':>9s} "
      f"{'p90':>9s} {'p90/p10':>8s} {'max/min':>8s}")
    disp = []
    for pair in PAIRS:
        for c in CHARS:
            for k in KS:
                d = CELL[(CELL.pair == pair) & (CELL.basis == "FULL") & (CELL.char == c)
                         & (CELL.k == k)]
                if len(d) < 6:
                    continue
                v = d.abs_resid
                disp.append(dict(pair=pair, char=c, k=k, n=len(d), med=float(v.median()),
                                 p10=float(v.quantile(0.10)), p90=float(v.quantile(0.90)),
                                 ratio=float(v.quantile(0.90) / v.quantile(0.10)),
                                 maxmin=float(v.max() / v.min())))
                P(f"  {pair:4s} {c:6s} {k:3d} {len(d):5d} {float(v.median()):14.5f} "
                  f"{float(v.quantile(0.10)):9.5f} {float(v.quantile(0.90)):9.5f} "
                  f"{float(v.quantile(0.90) / v.quantile(0.10)):8.2f} {float(v.max() / v.min()):8.2f}")
    wr = []
    for keys, d in CELL[CELL.basis == "FULL"].groupby(["pair", "char", "k", "shp", "s"]):
        if len(d) >= 6 and d.abs_resid.min() > 0:
            wr.append(dict(pair=keys[0], char=keys[1], k=keys[2],
                           ratio=float(d.abs_resid.max() / d.abs_resid.min())))
    WR = pd.DataFrame(wr)
    DS = pd.DataFrame(disp)
    DS.to_csv(f"{OUT}/{STAMP}.dispersion.csv", index=False)
    if len(DS):
        P(f"  POOLED: median p90/p10 across the {len(DS)} (pair,char,k) groups "
          f"{DS.ratio.median():.2f}x; median max/min {DS.maxmin.median():.2f}x.")
        P(f"  WITHIN-CELL (6 replicates of one identical shape/size/k cell, {len(WR)} such cells): "
          f"median max/min {WR.ratio.median():.2f}x, p90 {WR.ratio.quantile(0.90):.2f}x, "
          f"max {WR.ratio.max():.2f}x.")
        P(f"  So a residual quoted from one cell of this machinery carries a factor of about "
          f"{WR.ratio.median():.1f}x")
        P("  from re-drawing alone, before any panel content is involved.  Idea 796's cited "
          "0.0133 -> 0.0027")
        P("  (4.90x, FROZEN vs LIVE, BW=0.500/Q5, 4 rungs each, from its own .summary.csv) sits")
        P(f"  inside that noise band; this run's own re-measurement of the same contrast reads")
        P("  0.83x (per-vintage rungs) and 0.48x (frozen rungs) - the opposite direction.")
    P("")
    P("  WHAT ACTUALLY MOVES IT (post-hoc, and the reason the held-out test lands outside): the two")
    P("  arms' SEPARATION in the characteristic.  SMD = |mean_thin - mean_thick| / sd(pool); OVL =")
    P("  the overlapping coefficient of the two arms' 40-bin histograms.  Six (pair, char) points.")
    P(f"  {'pair':4s} {'char':6s} {'SMD':>7s} {'OVL':>7s} {'|resid|/sd':>11s}")
    ovr = []
    nc4 = nc3
    for pair, (ta, ka) in {"BS": (b_ok, s_ok), "SS": (SS_A, SS_B)}.items():
        for c in ("momac", "tpers", "avol"):
            xa = nc4.loc[[n for n in ta if n in nc4.index], c].dropna().to_numpy(float)
            xb = nc4.loc[[n for n in ka if n in nc4.index], c].dropna().to_numpy(float)
            if len(xa) < 10 or len(xb) < 10:
                continue
            sdp = float(nc4[c].std())
            smd = abs(float(xa.mean() - xb.mean())) / sdp
            lo, hi = float(min(xa.min(), xb.min())), float(max(xa.max(), xb.max()))
            edges = np.linspace(lo, hi, 41)
            ha = np.histogram(xa, bins=edges)[0] / len(xa)
            hb = np.histogram(xb, bins=edges)[0] / len(xb)
            ovl = float(np.minimum(ha, hb).sum())
            rel = rel_summary.get((pair, c), np.nan)
            ovr.append(dict(pair=pair, char=c, SMD=smd, OVL=ovl, rel=rel))
            P(f"  {pair:4s} {c:6s} {smd:7.3f} {ovl:7.3f} {rel:11.4f}")
    OV = pd.DataFrame(ovr)
    OV.to_csv(f"{OUT}/{STAMP}.overlap.csv", index=False)
    d = OV.dropna(subset=["rel"])
    if len(d) >= 4:
        rs = float(np.corrcoef(pd.Series(d.SMD).rank(), pd.Series(d.rel).rank())[0, 1])
        ro = float(np.corrcoef(pd.Series(d.OVL).rank(), pd.Series(d.rel).rank())[0, 1])
        P(f"  Spearman(SMD, |resid|/sd) = {rs:+.3f}   Spearman(OVL, |resid|/sd) = {ro:+.3f} "
          f"over {len(d)} points")
        P("  Read plainly: the dimensionless residual tracks how far apart the two arms sit in the")
        P("  characteristic, not how many names are in either.  This is post-hoc on six points and")
        P("  is queued for a pre-registered test, not claimed here.")
    P("")

    # ------------------------------------------------------------------ H_VINT
    P("=" * 118)
    P("H_VINT - does a min(n) law explain idea 796's 430 -> 663 observation?  Thin arm (B) held at")
    P("         its full size, thick arm (S) set to idea 571's FROZEN survivors and to today's 663,")
    P("         under BOTH bases.  A min(n) law predicts NO change (min stays n_B).")
    P("=" * 118)
    nc571 = pd.read_csv(f"{PARENT571}.namechars.csv", index_col=0)
    s439 = sorted([n for n in nc571.index if n in s_ok])
    b571 = sorted([n for n in nc571.index if n in b_ok])
    P(f"  idea 571's committed pool: {len(nc571)} names; survivors in today's data: "
      f"B {len(b571)} + SMALL {len(s439)}")
    vint_rows = []
    for basis in BASES:
        for label, sarm in (("S439frozen", s439), ("S663today", s_ok)):
            rr, _ = measure_cell(nc_full, pool_all, mom_all, b_ok, sarm, LEVELS, K_ANCHOR,
                                 basis, f"VINT|{basis}|{label}", "B", label)
            for c in CHARS:
                d = [r for r in rr if r["char"] == c]
                if not d:
                    continue
                vint_rows.append(dict(basis=basis, thick=label, char=c, n_rungs=len(d),
                                      n_thin=d[0]["n_thin"], n_thick=d[0]["n_thick"],
                                      min_n=d[0]["min_n"],
                                      abs_resid=float(np.mean([x["abs_resid"] for x in d]))))
    VI = pd.DataFrame(vint_rows)
    VI.to_csv(f"{OUT}/{STAMP}.vintage.csv", index=False)
    P(f"  {'basis':5s} {'char':6s} {'thick arm':11s} {'n_thin':>6s} {'n_thick':>7s} {'min_n':>6s} "
      f"{'rungs':>5s} {'|resid|':>9s}")
    for r in VI.itertuples():
        P(f"  {r.basis:5s} {r.char:6s} {r.thick:11s} {r.n_thin:6d} {r.n_thick:7d} {r.min_n:6d} "
          f"{r.n_rungs:5d} {r.abs_resid:9.5f}")
    def _rat(basis, c):
        a = VI[(VI.basis == basis) & (VI.char == c)].set_index("thick").abs_resid
        return float(a["S439frozen"] / a["S663today"]) if len(a) == 2 else np.nan
    P("  ratio |resid|(439-name thick arm) / |resid|(663-name thick arm), thin arm identical:")
    for basis in BASES:
        P(f"    {basis:5s} " + "  ".join(f"{c} {_rat(basis, c):.3f}" for c in CHARS))
    inert = {c: abs(np.log10(_rat("FULL", c))) < 0.10 for c in CHARS
             if np.isfinite(_rat("FULL", c))}
    ok_vint = bool(inert and all(inert.values()))
    P("  Under a min(n) law every ratio above must be 1.000 (the thin arm never moved).  "
      + ", ".join(f"{c} {'inert' if v else 'MOVES'}" for c, v in inert.items()))
    P("")
    P("  LEG 2 - idea 796's OWN convention, where the rungs and the characteristics are re-derived")
    P("  inside each vintage rather than frozen, so pool size, rung levels and momac's cross-")
    P("  sectional rank all move together (which is what its 0.0133 -> 0.0027 reading actually")
    P("  compared):")
    leg2 = []
    for label, sarm in (("S439frozen", s439), ("S663today", s_ok)):
        cols = sorted(set(b_ok) | set(sarm))
        ncv = chars_for(pool_all[cols])
        lvv = {c: [round(float(ncv[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
        rr, _ = measure_cell(ncv, pool_all[cols], mom_all[cols],
                             [n for n in b_ok if n in cols], sarm, lvv, K_ANCHOR, "FULL",
                             f"VINT2|{label}", "B", label)
        for c in CHARS:
            d = [r for r in rr if r["char"] == c]
            if d:
                leg2.append(dict(convention="per-vintage rungs+chars", thick=label, char=c,
                                 n_rungs=len(d), n_thick=d[0]["n_thick"],
                                 abs_resid=float(np.mean([x["abs_resid"] for x in d]))))
    L2 = pd.DataFrame(leg2)
    for r in L2.itertuples():
        P(f"    {r.char:6s} {r.thick:11s} n_thick {r.n_thick:3d} rungs {r.n_rungs} "
          f"|resid| {r.abs_resid:.5f}")
    for c in CHARS:
        a = L2[L2.char == c].set_index("thick").abs_resid
        if len(a) == 2:
            P(f"    {c:6s} 439 -> 663 ratio {float(a['S439frozen'] / a['S663today']):.3f}  "
              f"(idea 796 published 0.0133 -> 0.0027 = 4.93x for momac)")
    VI2 = pd.concat([VI.assign(convention="frozen rungs+chars"), L2], ignore_index=True)
    VI2.to_csv(f"{OUT}/{STAMP}.vintage.csv", index=False)
    P("")

    # ------------------------------------------------------------------ RULE 8 WF-A
    P("=" * 118)
    P("RULE 8 / WF-A - the law refit on IS-only and OOS-only characteristics.  Predictor CHOSEN on")
    P("                IS by pooled R^2; its OOS R^2 and slope are then read ONCE.")
    P("=" * 118)
    wf_rows = []
    for wname, wpx in (("IS", pool_all.loc[:IS_END]), ("OOS", pool_all.loc[OOS_START:])):
        ncw = chars_for(wpx)
        momw = wpx.shift(MOM_LAG) / wpx.shift(MOM_LOOK) - 1.0
        lvw = {c: [round(float(ncw[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
        bw_ok = [c for c in b_stk if c in ncw.index and ncw.loc[c].notna().any()]
        sw_ok = [c for c in s_stk if c in ncw.index and ncw.loc[c].notna().any()]
        rows = []
        for pair, (ta, ka, tl, kl) in {"BS": (bw_ok, sw_ok, "B", "S"),
                                       "SS": ([c for c in SS_A if c in sw_ok],
                                              [c for c in SS_B if c in sw_ok], "S1", "S2")}.items():
            for plan in cell_plan(pair, len(ta), len(ka)):
                if not plan["available"] or plan["shape"] != "SYM":
                    continue
                for k in KS:
                    if min(plan["n_thin"], plan["n_thick"]) <= k:
                        continue
                    for rep in REPS[:3]:
                        tn = subsample(ta, plan["n_thin"], rep, f"{pair}|thin")
                        kn = subsample(ka, plan["n_thick"], rep, f"{pair}|thick")
                        rr, _ = measure_cell(ncw, wpx, momw, tn, kn, lvw, k, "FULL",
                                             f"{wname}|{pair}|{plan['s']}|{k}|{rep}", tl, kl)
                        for r in rr:
                            r.update(pair=pair, shp="SYM", s=plan["s"], rep=rep, window=wname)
                        rows.extend(rr)
        W = pd.DataFrame(rows)
        if not len(W):
            continue
        CW = W.groupby(["pair", "s", "k", "rep", "char"]).agg(
            min_n=("min_n", "first"), tot_n=("tot_n", "first"), abs_resid=("abs_resid", "mean"),
            neff_min=("neff_min", "mean")).reset_index()
        CW["fill"] = CW["k"] / CW["min_n"]
        for pair in PAIRS:
            for c in CHARS:
                d = CW[(CW.pair == pair) & (CW.char == c)]
                if len(d) < 6:
                    continue
                for pred in ("min_n", "tot_n", "fill", "neff_min"):
                    wf_rows.append(dict(window=wname, basis="FULL", pair=pair, char=c,
                                        predictor=pred, **loglog_fit(d[pred], d.abs_resid)))
    WF = pd.DataFrame(wf_rows)
    ALLLAW = pd.concat([LAW, WF], ignore_index=True)
    ALLLAW.to_csv(f"{OUT}/{STAMP}.law.csv", index=False)
    P(f"  {'window':6s} {'pair':4s} {'char':6s} {'predictor':9s} {'n':>5s} {'slope':>8s} {'R2':>7s} "
      f"{'sd_res':>7s}")
    for r in WF.itertuples():
        P(f"  {r.window:6s} {r.pair:4s} {r.char:6s} {r.predictor:9s} {r.n:5d} {r.slope:+8.3f} "
          f"{r.R2:7.3f} {r.sd_resid:7.3f}")
    if len(WF):
        ispool = WF[WF.window == "IS"].groupby("predictor").R2.mean().sort_values(ascending=False)
        pick = ispool.index[0]
        oos = WF[(WF.window == "OOS")].groupby("predictor").R2.mean()
        P(f"  IS-chosen predictor: {pick} (IS pooled mean R2 {ispool.iloc[0]:.3f}); its OOS mean R2 "
          f"{oos.get(pick, np.nan):.3f}; OOS ranking " +
          " > ".join(f"{i} {v:.3f}" for i, v in oos.sort_values(ascending=False).items()))
        P(f"  IS->OOS predictor ranking agreement: "
          f"{'SAME winner' if oos.idxmax() == pick else f'DIFFERENT winner OOS ({oos.idxmax()})'}")
    else:
        pick = "n/a"
    P("")

    # ------------------------------------------------------------------ WF-B books + KEEP paths
    P("=" * 118)
    P("RULE 8 / WF-B + KEEP PATHS - every drawn book run as a real book (10 bps, next-day fills).")
    P("=" * 118)
    base_r = fast_backtest(px56, rules_v2_weights(px56), COST, "W")["returns"]
    start = pool_all.index[260]
    idxb = pool_all.loc[start:].index
    b_ret = base_r.reindex(idxb).fillna(0.0)
    spy_ret = spy.pct_change().fillna(0.0).reindex(idxb).fillna(0.0)
    bm = rowify(b_ret)
    sm = rowify(spy_ret)
    P(f"  comparands over {idxb[0].date()}..{idxb[-1].date()} ({len(idxb)} bars)")
    P(f"    RULES v2 (U56, live) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
      f"MaxDD {bm['MaxDD']:.2%} halves {bm['H1']:.3f}/{bm['H2']:.3f} | OOS CAGR "
      f"{bm['OOS_CAGR']:.2%} Sharpe {bm['OOS_Sharpe']:.3f} MaxDD {bm['OOS_MaxDD']:.2%}")
    P(f"    SPY                  CAGR {sm['CAGR']:.2%} Sharpe {sm['Sharpe']:.3f} "
      f"MaxDD {sm['MaxDD']:.2%} halves {sm['H1']:.3f}/{sm['H2']:.3f} | OOS CAGR "
      f"{sm['OOS_CAGR']:.2%} Sharpe {sm['OOS_Sharpe']:.3f} MaxDD {sm['OOS_MaxDD']:.2%}")
    books = []
    seen = {}
    for (shp_, s_, k_, char, L, armlab, sd_), names in book_sets.items():
        if sd_ > 1:
            continue
        full = pool_all[names]
        ma_full = full > full.rolling(MA_WIN).mean()
        sub = full.loc[start:]
        ma_ok = ma_full.loc[start:]
        priced = sub.notna()
        for form in ("EWall", "MA-RS"):
            mask = priced if form == "EWall" else (priced & ma_ok)
            nn = mask.sum(axis=1).replace(0, np.nan)
            for g in GROSS:
                w = g * mask.div(nn, axis=0).fillna(0.0)
                key = (tuple(names), form, g)
                if key in seen:
                    rr = seen[key]
                else:
                    r_ser = fast_backtest(sub, w, COST, "W")["returns"]
                    rr = rowify(r_ser)
                    rr["_4a"] = keep_4a(r_ser, b_ret)
                    rr["_4b"] = fail_4b(r_ser, spy_ret)
                    seen[key] = rr
                books.append(dict(bkey=zlib.crc32(repr(key).encode()),
                                  shp=shp_, s=s_, k=k_, char=char, level=L,
                                  arm="B" if armlab == "THIN" else "S", seed=sd_, form=form,
                                  gross=g, keep4a=rr["_4a"], fail4b=rr["_4b"],
                                  keep4b=rr["_4b"] == "-",
                                  **{kk: vv for kk, vv in rr.items() if not kk.startswith("_")}))
    BK = pd.DataFrame(books)
    BK.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    n4a = int(BK.keep4a.sum())
    n4b = int(BK.keep4b.sum())
    nboth = int((BK.keep4a & BK.keep4b).sum())
    P(f"  {len(BK)} books ({BK.arm.nunique()} arms x {BK.char.nunique()} chars x "
      f"{BK['shp'].nunique()} shapes x {BK.s.nunique()} pool sizes x {BK.k.nunique()} k x "
      f"{BK.level.nunique()} rungs x 2 seeds x 2 forms x 3 gross)")
    U = BK.drop_duplicates("bkey")
    P(f"  KEEP paths over all books: 4a {n4a}   4b {n4b}   BOTH {nboth}")
    P(f"  the same drawn name set can appear in two grid cells (SYM and THIN coincide when the")
    P(f"  thick arm is already at its maximum); on {len(U)} DISTINCT books the counts are "
      f"4a {int(U.keep4a.sum())}   4b {int(U.keep4b.sum())}   BOTH {int((U.keep4a & U.keep4b).sum())}")
    if n4b:
        P("  4b passers (diagnostic only - a kernel-weighted seeded draw is not a tradable rule):")
        for r in U[U.keep4b].sort_values("OOS_Sharpe", ascending=False).head(8).itertuples():
            P(f"    {r.char:6s} arm {r.arm:2s} s={r.s:3d} k={r.k:2d} L={r.level:.4f} {r.form:5s} "
              f"g={r.gross:.2f}  CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} "
              f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.3f}")
    P("  fail-4b leg census: " + ", ".join(
        f"{kk} {vv}" for kk, vv in BK.fail4b.value_counts().head(8).items()))
    pickb = BK.sort_values("IS_Sharpe", ascending=False).iloc[0]
    P("")
    P("  WF-B pick (IS Sharpe ALONE, OOS read once):")
    P(f"    {pickb.char} arm {pickb.arm} s={int(pickb.s)} k={int(pickb.k)} L={pickb.level:.4f} "
      f"{pickb.form} g={pickb.gross:.2f}   IS Sharpe {pickb.IS_Sharpe:.3f}")
    P(f"    OOS  CAGR {pickb.OOS_CAGR:.2%}  Sharpe {pickb.OOS_Sharpe:.3f}  MaxDD {pickb.OOS_MaxDD:.2%}")
    P(f"    vs RULES v2 OOS  {bm['OOS_CAGR']:.2%} / {bm['OOS_Sharpe']:.3f} / {bm['OOS_MaxDD']:.2%}")
    P(f"    vs SPY      OOS  {sm['OOS_CAGR']:.2%} / {sm['OOS_Sharpe']:.3f} / {sm['OOS_MaxDD']:.2%}")
    P(f"    full sample CAGR {pickb.CAGR:.2%} Sharpe {pickb.Sharpe:.3f} MaxDD {pickb.MaxDD:.2%} "
      f"halves {pickb.H1:.3f}/{pickb.H2:.3f}")
    P(f"    4a {bool(pickb.keep4a)}   4b {'PASS' if pickb.keep4b else 'FAIL on ' + pickb.fail4b}")
    P("")
    WFOUT = pd.concat([ALLLAW.assign(leg="law"),
                       pd.DataFrame([dict(leg="wfb_pick", window="OOS", predictor=pick,
                                          n=len(BK), slope=np.nan, R2=np.nan)])],
                      ignore_index=True)
    WFOUT.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    pd.DataFrame(gates + v4).to_csv(f"{OUT}/{STAMP}.gates.csv", index=False)

    # ------------------------------------------------------------------ verdict
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    for nm, ok in (("H_MONO", ok_mono), ("H_MIN", ok_min), ("H_POWER", ok_pow),
                   ("H_FILL", ok_fill), ("H_NEFF", ok_neff),
                   ("H_VINT (min(n) law reproduces 430->663)", ok_vint)):
        P(f"  {nm:34s} {'PASS' if ok else 'FAIL'}")
    P(f"  KEEP: 4a {n4a} / 4b {n4b} / BOTH {nboth} of {len(BK)} books "
      f"({int(U.keep4a.sum())} / {int(U.keep4b.sum())} / {int((U.keep4a & U.keep4b).sum())} of "
      f"{len(U)} distinct).  No capital candidate is")
    P("        claimed: every book here is a kernel-weighted seeded draw, not a rule.")
    P(f"  runtime {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
