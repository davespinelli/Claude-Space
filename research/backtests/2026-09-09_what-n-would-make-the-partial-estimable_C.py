#!/usr/bin/env python3
"""Idea 547 - "what-n-would-make-the-partial-estimable" (lane C, 2026-09-09).

The question
------------
Idea 310 found that the within-stratum rank-PARTIAL of a panel characteristic against OOS
Sharpe does not replicate its SIGN across disjoint seed blocks for any of the four
characteristics, while the MARGINAL rank correlation keeps its sign 21-26 of 27 points.  Its
named mechanism is collinearity: median within-stratum rank corr(disp_IS, evol_IS) = +0.6909,
measured at n = 60 panels per stratum -- "the regime where a partial's sign is noise".

Collinearity does not make a partial unestimable, it makes it EXPENSIVE: the partial's sampling
SD is inflated by 1/sqrt(1 - R^2) over the marginal's, so the same sign-replication rate needs a
larger n.  The queue's question is therefore a sample-size question, not a sign question:

    sweep panels-per-stratum n in {30, 60, 120, 240} at ONE fixed stratum and report the
    seed-block SIGN-AGREEMENT CURVE -- the n at which the partial's sign replicates 90% of
    the time, or that it never does.

Design (fixed before any new number was computed)
-------------------------------------------------
FIXED, never varied (inherited resolution, not dials):
    construction  idea 284/293's panel builder VERBATIM -- q * k names drawn from SMALL439,
                  the rest from BSTK100, seed key zlib.crc32("STRAT|{q:.3f}|{sd}"), so seeds
                  0..59 of any (q, k) are idea 293's committed panels bit-for-bit and seeds
                  60..479 are the same generator run further.  Seeds 100..159 coincide with
                  lane B's idea-310 block B by construction; they are the same panels, not a
                  new draw, and are labelled as such in .panels.csv.
    books         CAND10, CAND20, EWall -- all three always reported, none selected on
    outcome       OOS Sharpe (>= 2017-01-01); characteristics measured on IS (<= 2016-12-31)
    statistics    MARGINAL = Spearman rho (idea 546's statistic, the pre-registered comparand)
                  PARTIAL  = rank-partial controlling the OTHER THREE characteristics
                             (idea 284/293's estimator verbatim, "REC" control set)
    chars         breadth, disp, corr, evol -- all four reported, focus disp and evol
    pairs         400 disjoint block pairs per (stratum, n), rng seed 20260909

TUNED PARAMETERS -- exactly two, as the queue specifies:
    1. n        panels per stratum in {30, 60, 120, 240}
    2. stratum  (q = 0.500, k = 40)  PRIMARY -- idea 284's own stratum, and the one whose
                                     corr(disp, evol) = +0.7757 is ABOVE idea 310's +0.6909
                                     median, i.e. the hard case
                (q = 0.250, k = 40)  SECOND  -- idea 293's strongest-ordering cap mix and where
                                     41 of 46 of the record's fresh-block 4b passes sit;
                                     corr(disp, evol) = +0.5474, the easy case
    4 n-rungs x 2 strata x 4 chars x 2 statistics x 3 books = 192 curve points, ALL reported.
    480 panels per stratum x 2 strata = 960 constructed panels, ALL reported.

Pre-registered bars, written before any new number was computed
---------------------------------------------------------------
B1  ESTIMABLE-AT-n.  A (char, statistic, book) is "estimable at n" iff the sign-agreement rate
    between two DISJOINT blocks of n draws is >= 0.90 AND the lower end of its 95% CI is
    >= 0.85.  Reported for every one of the 192 points.
B2  MARGINAL COMPARAND.  The same bar on the marginal.  Idea 310's premise implies the marginal
    is estimable at n = 60 where the partial is not; graded verbatim, both directions.
B3  n*.  The n at which agreement first crosses 0.90.  Inside the ladder by linear interpolation
    in log2(n); beyond it by the normal extrapolation implied by se(n) = c / sqrt(n):
    agreement = p^2 + (1-p)^2 with p = Phi(|mu| / se(n)), so n* = (c * z_p / |mu|)^2 with
    z_p = Phi^-1(0.9472) = 1.6187 (the per-block rate whose pair agreement is 0.90).
    c is FITTED on the observed block-level SD across the ladder (SD * sqrt(n), averaged), |mu|
    is the full-480 pooled estimate.  n* is reported as ">240 (extrapolated N)" whenever the
    ladder itself does not reach the bar; an n* above 480 is an extrapolation and is labelled.
B4  MECHANISM.  Report, per stratum: the rank correlation matrix of the four IS characteristics,
    each char's R^2 on the other three, the observed sd(PARTIAL)/sd(MARGINAL) ratio at each n,
    and the collinearity prediction 1/sqrt(1 - R^2).  The mechanism is "the whole story" iff the
    observed ratio is within 25% of the prediction at every rung.
B5  RULE 8 / PROTOCOL 8 (required, out-of-sample in TWO directions):
    (a) TIME  characteristics are IS-only (<= 2016-12-31) and every book metric read is OOS
        (>= 2017-01-01) -- inherited from the construction.
    (b) DRAW  the direction is FIT on block A (n draws) and APPLIED ONCE to the disjoint block B:
        pick B's extreme panel in the fitted direction, read its OOS book metrics once.  Scored
        against block B's do-nothing anchor (mean OOS Sharpe of the n unseen draws), SPY and
        RULES v2 (the live book, run on the same panel).  50 pairs per point.
B6  BOTH KEEP PATHS on every panel-book (960 x 3) and on every walk-forward pick:
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70% of SPY's.

B7  POST-HOC, ADDED AFTER THE FIRST RUN -- declared as post-hoc, not pre-registered
---------------------------------------------------------------------------------
The first run produced two artefacts of the block device itself, both of which have to be
priced before B1-B3 can be read as an answer, and neither of which was anticipated:

  (i)  the fitted c = sd_block * sqrt(n) FALLS monotonically with n (1.006 -> 0.717 on the
       primary stratum) instead of being flat, in exactly the ratio sqrt(1 - n/N_TOTAL);
  (ii) several agreement rates fall BELOW 0.50 and keep falling with n (disp/CAND10/PARTIAL
       0.460 -> 0.110), which independent blocks cannot do.

Both have one cause: two DISJOINT blocks of n drawn from a fixed pool of N are negatively
dependent, corr = -n/(N - n), reaching -1 at n = N/2 where they are exact complements.  B7
therefore reports, alongside the raw curve and never in place of it:
  B7a  c_inf = sd_block * sqrt(n) / sqrt(1 - n/N)  -- the infinite-pool SE constant, per rung
       and per statistic.  If the FPC is the whole cause, c_inf is flat in n.
  B7b  the analytic same-sign probability of a bivariate normal with mean a = |mu| / (c_inf /
       sqrt(n)) in both legs and correlation r = -n/(N - n), against the observed rate
       (validation), and the same quantity at r = 0 (the INDEPENDENT-block curve, which is what
       "does the sign replicate" actually asks).
  B7c  n*_indep = (c_inf * z_p / |mu|)^2, the independent-block answer to the queue's question.
  B7d  what this costs the record: idea 310's own split-half device (seeds 0-29 vs 30-59) is
       n = 30 of N = 60, i.e. r = -1 EXACTLY, so its published sign-agreement counts are biased
       toward DISagreement.  The exact map from the independent rate to the r = -1 rate is
       published so the record's counts can be restated.

Gates (asserted before any verdict is read)
    G1  the rebuild of stratum (q 0.500, k 40) seeds 0..59 reproduces idea 293's committed
        .panels.csv on all four IS characteristics and all three book OOS Sharpes
        (60 x 7 = 420 cells) to < 1e-9.
    G2  the same 60 draws reproduce idea 284's published within-stratum corr rho
        (-0.3648 / -0.4815 / -0.4708 on CAND10 / CAND20 / EWall) to < 2e-3.
    G3  the same 60 draws reproduce lane B's committed within-stratum rank corr(disp_IS,
        evol_IS): +0.7757 at (k40, q0.500) and +0.5474 at (k40, q0.250), to < 5e-3.  This is
        idea 310's premise made auditable.

SURVIVORSHIP: panels are drawn from SMALL439 and BSTK100, both CURRENT constituents of their
screens, so every panel's return LEVEL is inflated and the KEEP columns inherit that whole.  This
run measures how many DRAWS a within-stratum statistic needs before its sign replicates, which
the bias does not create; but any "estimable" verdict is a within-corpus statement about the
estimator, never a tradable edge.

Deterministic, standalone.  Modifies nothing outside its own outputs.  The 960-panel build is
CACHED to .panels.csv / .keeppaths.csv: if both exist with the expected shape they are read back
instead of rebuilt (the build is a pure function of the committed price caches and the seed key,
so this is a cache, not a state).  Delete them to force a full rebuild.
Outputs: .panels.csv .curve.csv .extrap.csv .collin.csv .fpc.csv .walkforward.csv .keeppaths.csv
         .console.txt .result.md
"""
import json
import math
import sys
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state
from engine import backtest, metrics, rebalance_mask

# ---------------------------------------------------------------- fixed construction constants
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
BAND_V2 = 0.03
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
CHARS = ["breadth", "disp", "corr", "evol"]
BOOKS = ["CAND10", "CAND20", "EWall"]
STATS = ["MARGINAL", "PARTIAL"]

# ---------------------------------------------------------------- the two tuned dials
N_LADDER = [30, 60, 120, 240]
STRATA = [(0.500, 40), (0.250, 40)]           # PRIMARY first
PRIMARY = STRATA[0]
N_TOTAL = 480                                  # 2 x max(N_LADDER), so every rung has 2 disjoint blocks

N_PAIRS = 400                                  # block pairs per (stratum, n)
N_WF = 50                                      # of those pairs, the first 50 carry rule 8
RNG_SEED = 20260909
AGREE_BAR = 0.90
CI_BAR = 0.85
Z_P = 1.6187                                   # Phi^-1(0.9472); 0.9472^2 + 0.0528^2 = 0.900
MECH_TOL = 0.25                                # B4: observed vs predicted SD-inflation ratio

# ---------------------------------------------------------------- gates
G1_TOL = 1e-9
G2_PUB = {"CAND10": -0.3648, "CAND20": -0.4815, "EWall": -0.4708}
G2_TOL = 2e-3
G3_PUB = {(0.500, 40): 0.7757, (0.250, 40): 0.5474}
G3_TOL = 5e-3
SRC293 = (REPO / "research" / "backtests" /
          "2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- estimators (idea 284/293 verbatim)
def rk(v):
    v = pd.Series(np.asarray(v, float)).rank().to_numpy()
    return (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan
    rx, ry = pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def rank_partial(y, x, controls):
    """Idea 284/293's estimator verbatim: rank all, residualise on controls, correlate."""
    Y, X = rk(y), rk(x)
    C = np.column_stack([np.ones(len(Y))] + [rk(c) for c in controls])
    B = np.linalg.pinv(C.T @ C) @ C.T
    ry = Y - C @ (B @ Y)
    rx = X - C @ (B @ X)
    if ry.std() == 0 or rx.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def stat_of(df, char, book, kind):
    y = df[f"{book}_OOS_Sharpe"].to_numpy()
    x = df[f"{char}_IS"].to_numpy()
    if kind == "MARGINAL":
        return spearman(x, y)
    ctrls = [df[f"{c}_IS"].to_numpy() for c in CHARS if c != char]
    return rank_partial(y, x, ctrls)


def r2_on_others(df, char):
    Y = rk(df[f"{char}_IS"].to_numpy())
    C = np.column_stack([np.ones(len(Y))] + [rk(df[f"{c}_IS"].to_numpy())
                                             for c in CHARS if c != char])
    B = np.linalg.pinv(C.T @ C) @ C.T
    e = Y - C @ (B @ Y)
    ss_tot = float(((Y - Y.mean()) ** 2).sum())
    return float(1 - (e @ e) / ss_tot) if ss_tot > 0 else np.nan


# ---------------------------------------------------------------- sources / panels (idea 284/293 verbatim)
def build_sources():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    idx = pxs.index.intersection(px136.index)
    P(f"sources: BSTK{len(b_stk)} large-cap stocks, SMALL{len(s_stk)} small-cap stocks "
      f"({len(bad)} dropped for max_1d_move >= 1.0)")
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")
    return pxs.reindex(idx).ffill(), px136.reindex(idx).ffill(), np.array(sorted(s_stk)), np.array(sorted(b_stk))


def make_panel(pxs_c, pxb_c, small_pool, large_pool, q, k, sd):
    n_s = int(round(q * k))
    n_l = k - n_s
    seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)      # idea 284's key
    rng = np.random.default_rng(seed)
    sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
    lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
    parts = []
    if lc:
        parts.append(pxb_c[lc])
    if sc:
        parts.append(pxs_c[sc])
    p = pd.concat(parts + [pxb_c["SPY"].rename("SPY")], axis=1).dropna(how="all").ffill()
    return p, set(sc) | set(lc)


def eligible_mask(px, tradable, above, vol20):
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, key, elig, n=None):
    if arm == "v2":
        e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        for c in px.columns:
            if c in tradable:
                e[c] = px[c].notna().astype(float)
        ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND_V2), 0.0)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def stat_block(r):
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    return out


def keep_flags(row, spy_row, v2_row):
    a = bool(row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"]
             and row["MaxDD"] >= v2_row["MaxDD"])
    fails = []
    if not row["H1"] > spy_row["H1"]: fails.append("H1")
    if not row["H2"] > spy_row["H2"]: fails.append("H2")
    if not row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]: fails.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(spy_row["MaxDD"]): fails.append("DD")
    if not row["CAGR"] >= 0.70 * spy_row["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), (",".join(fails) if fails else "-")


def panel_chars(px, elig, lo, hi, cols, rbmask):
    start = px.index[260]
    idx = px.loc[start:].index
    idx = idx[idx >= pd.Timestamp(lo)]
    if hi:
        idx = idx[idx <= pd.Timestamp(hi)]
    rb = idx[rbmask.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]
    k = len(cols)
    nel = e.sum(axis=1)
    breadth = float((nel / k).mean())
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    disp = float(r63.where(e).std(axis=1, ddof=0).mean())
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    evol = float(vol20.where(e).mean(axis=1).mean())
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy()
    iu = np.triu_indices(k, 1)
    corr = float(np.nanmean(C[iu])) if k > 1 else np.nan
    return dict(n_elig=float(nel.median()), breadth=breadth, disp=disp, corr=corr, evol=evol)


# ---------------------------------------------------------------- build the 960 panels
def build_all(pxs_c, pxb_c, small_pool, large_pool):
    prows, krows = [], []
    total = len(STRATA) * N_TOTAL
    i = 0
    for (q, k) in STRATA:
        for sd in range(N_TOTAL):
            i += 1
            px, tr = make_panel(pxs_c, pxb_c, small_pool, large_pool, q, k, sd)
            key, above, vol20 = score(px, vol_scale=False)
            elig = eligible_mask(px, tr, above, vol20)
            cols = [c for c in px.columns if c in tr]
            rbm = pd.Series(rebalance_mask(px.index, FREQ), index=px.index)
            cis = panel_chars(px, elig, IS_START, IS_END, cols, rbm)
            rec = dict(panel=f"k{k:02d}~q{q:.3f}~s{sd:03d}", q=q, k=k, seed=sd,
                       block=("IDEA293_0_59" if sd < 60 else
                              ("IDEA310B_100_159" if 100 <= sd < 160 else "FRESH")),
                       n_elig_IS=cis["n_elig"])
            for c in CHARS:
                rec[f"{c}_IS"] = cis[c]

            start = px.index[260]
            spy_row = stat_block(px["SPY"].pct_change().fillna(0.0).loc[start:])
            books = {}
            for arm, nn in [("EWall", None), ("CAND10", 10), ("CAND20", 20), ("v2", None)]:
                w = book_weights(px, tr, "CAND" if arm.startswith("CAND") else arm, key, elig, n=nn)
                r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                books[arm] = stat_block(r)
            v2_row = books["v2"]
            for arm in BOOKS + ["v2"]:
                b = books[arm]
                for f in ("IS_Sharpe", "OOS_Sharpe", "Sharpe", "CAGR", "MaxDD", "H1", "H2",
                          "OOS_CAGR", "OOS_MaxDD"):
                    rec[f"{arm}_{f}"] = b[f]
                a4, b4, fails = keep_flags(b, spy_row, v2_row)
                rec[f"{arm}_keep4a"], rec[f"{arm}_keep4b"] = a4, b4
                krows.append(dict(panel=rec["panel"], q=q, k=k, seed=sd, arm=arm,
                                  **{kk: b[kk] for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                  keep4a=a4, keep4b=b4, fails4b=fails))
            for f in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
                rec[f"SPY_{f}"] = spy_row[f]
            prows.append(rec)
            if i % 60 == 0 or i == total:
                P(f"  ... {i}/{total} panels")
                flush_log()
    return pd.DataFrame(prows), pd.DataFrame(krows)


# ---------------------------------------------------------------- gates
def run_gates(panels):
    P("\n" + "=" * 110)
    P("GATES")
    P("=" * 110)
    ok = True

    src = pd.read_csv(SRC293)
    src = src[src.kind == "k40q0.500"].sort_values("seed").reset_index(drop=True)
    mine = panels[(panels.q == 0.500) & (panels.k == 40) & (panels.seed < 60)].sort_values("seed").reset_index(drop=True)
    cols = [f"{c}_IS" for c in CHARS] + [f"{b}_OOS_Sharpe" for b in BOOKS]
    d = (mine[cols].to_numpy() - src[cols].to_numpy())
    worst = float(np.nanmax(np.abs(d)))
    g1 = (len(src) == 60 and len(mine) == 60 and worst < G1_TOL)
    ok &= g1
    P(f"  G1 rebuild vs idea 293 committed panels.csv, {len(mine)}x{len(cols)} = "
      f"{len(mine) * len(cols)} cells: max |diff| {worst:.3e}  (bar {G1_TOL:.0e})  "
      f"{'PASS' if g1 else 'FAIL'}")

    P("  G2 idea 284's published within-stratum corr rho on the same 60 draws:")
    g2 = True
    for b in BOOKS:
        r = spearman(mine["corr_IS"], mine[f"{b}_OOS_Sharpe"])
        dd = abs(r - G2_PUB[b])
        g2 &= dd < G2_TOL
        P(f"     {b:7s} {r:+.4f}  published {G2_PUB[b]:+.4f}  |diff| {dd:.5f}  "
          f"{'OK' if dd < G2_TOL else 'MISMATCH'}")
    ok &= g2
    P(f"     G2 {'PASS' if g2 else 'FAIL'}")

    P("  G3 idea 310's premise -- lane B's committed rank corr(disp_IS, evol_IS), seeds 0..59:")
    g3 = True
    for (q, k) in STRATA:
        m = panels[(panels.q == q) & (panels.k == k) & (panels.seed < 60)]
        r = spearman(m["disp_IS"], m["evol_IS"])
        dd = abs(r - G3_PUB[(q, k)])
        g3 &= dd < G3_TOL
        P(f"     (q{q:.3f}, k{k}) {r:+.4f}  published {G3_PUB[(q, k)]:+.4f}  |diff| {dd:.5f}  "
          f"{'OK' if dd < G3_TOL else 'MISMATCH'}")
    ok &= g3
    P(f"     G3 {'PASS' if g3 else 'FAIL'}")
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- verdict not readable'}")
    assert ok, "reproduction gates failed"
    return ok


# ---------------------------------------------------------------- block pairs
def pair_index(n, npairs, rng):
    """npairs disjoint (A, B) index pairs of size n drawn from 0..N_TOTAL-1 without replacement."""
    out = []
    for _ in range(npairs):
        perm = rng.permutation(N_TOTAL)
        out.append((perm[:n], perm[n:2 * n]))
    return out


# ---------------------------------------------------------------- B7 analytics (post-hoc)
_SQ2 = math.sqrt(2.0)


def Phi(x):
    x = np.atleast_1d(np.asarray(x, float))
    return np.array([0.5 * (1.0 + math.erf(v / _SQ2)) for v in x.ravel()]).reshape(x.shape)


def same_sign_prob(a, r, ngrid=4001):
    """P(sign(X) == sign(Y)) for (X, Y) bivariate normal, both mean a, unit sd, corr r.

    X = a + Z1, Y = a + Z2.  P(both > 0) = int_{-a}^{inf} phi(z) Phi((a + r z)/sqrt(1-r^2)) dz,
    P(both < 0) = int_{-inf}^{-a} phi(z) Phi((-a - r z)/sqrt(1-r^2)) dz.  r = -1 is the exact
    complement case, where Y = 2a - X and the answer collapses to 2*Phi(|a|) - 1.
    """
    a = float(a)
    if r <= -0.999999:
        return float(max(0.0, 2.0 * Phi(abs(a))[0] - 1.0))
    s = math.sqrt(max(1e-12, 1.0 - r * r))
    hi = np.linspace(-a, -a + 12.0, ngrid)
    lo = np.linspace(-a - 12.0, -a, ngrid)
    ph = lambda z: np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    p_pp = float(np.trapezoid(ph(hi) * Phi((a + r * hi) / s), hi))
    p_mm = float(np.trapezoid(ph(lo) * Phi((-a - r * lo) / s), lo))
    return p_pp + p_mm


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    P(f"tuned dials: n {N_LADDER}, stratum {STRATA}.  Everything else fixed at the record's values.")
    pcache, kcache = Path(f"{OUT}.panels.csv"), Path(f"{OUT}.keeppaths.csv")
    want = len(STRATA) * N_TOTAL
    panels = keeps = None
    if pcache.exists() and kcache.exists():
        p0, k0 = pd.read_csv(pcache), pd.read_csv(kcache)
        if len(p0) == want and len(k0) == want * (len(BOOKS) + 1):
            P(f"panel cache HIT: {len(p0)} panels / {len(k0)} panel-books read back from "
              f"{pcache.name}; the build is a pure function of the committed caches and the "
              f"seed key, so this is a cache, not a state.  Delete it to force a rebuild.")
            panels, keeps = p0, k0
    if panels is None:
        pxs_c, pxb_c, small_pool, large_pool = build_sources()
        P(f"\nbuilding {len(STRATA)} strata x {N_TOTAL} draws = {want} panels "
          f"(4 books each: {BOOKS} + RULES v2)")
        panels, keeps = build_all(pxs_c, pxb_c, small_pool, large_pool)
        panels.to_csv(pcache, index=False)
        keeps.to_csv(kcache, index=False)
    run_gates(panels)

    # ------------------------------------------------------------ B4 mechanism: collinearity
    P("\n" + "=" * 110)
    P("B4 MECHANISM -- what the partial is controlling for (full 480 draws per stratum)")
    P("=" * 110)
    crows = []
    for (q, k) in STRATA:
        d = panels[(panels.q == q) & (panels.k == k)]
        M = pd.DataFrame(index=CHARS, columns=CHARS, dtype=float)
        for a in CHARS:
            for b in CHARS:
                M.loc[a, b] = spearman(d[f"{a}_IS"], d[f"{b}_IS"])
        P(f"\n  stratum (q {q:.3f}, k {k}), n = {len(d)}:  rank correlation of the IS characteristics")
        P(fmt(M))
        for c in CHARS:
            r2 = r2_on_others(d, c)
            crows.append(dict(q=q, k=k, char=c, r2_on_others=r2,
                              vif_sd_ratio=1.0 / np.sqrt(max(1e-12, 1 - r2)),
                              rho_disp_evol=float(M.loc["disp", "evol"])))
        cc = pd.DataFrame([r for r in crows if r["q"] == q and r["k"] == k])
        P(f"  corr(disp, evol) = {M.loc['disp','evol']:+.4f}   R^2 on the other three / predicted "
          f"SD inflation 1/sqrt(1-R^2):")
        P(fmt(cc[["char", "r2_on_others", "vif_sd_ratio"]].set_index("char")))
    collin = pd.DataFrame(crows)
    collin.to_csv(f"{OUT}.collin.csv", index=False)

    # ------------------------------------------------------------ B1/B2 the sign-agreement curve
    P("\n" + "=" * 110)
    P(f"B1/B2 SIGN-AGREEMENT CURVE -- {N_PAIRS} disjoint block pairs per (stratum, n)")
    P("=" * 110)
    rng = np.random.default_rng(RNG_SEED)
    pairs = {}
    for (q, k) in STRATA:
        for n in N_LADDER:
            pairs[(q, k, n)] = pair_index(n, N_PAIRS, rng)

    rows = []
    for (q, k) in STRATA:
        d = panels[(panels.q == q) & (panels.k == k)].sort_values("seed").reset_index(drop=True)
        pooled = {(c, b, s): stat_of(d, c, b, s)
                  for c in CHARS for b in BOOKS for s in STATS}
        for n in N_LADDER:
            for c in CHARS:
                for b in BOOKS:
                    for s in STATS:
                        va, vb = [], []
                        for (ia, ib) in pairs[(q, k, n)]:
                            va.append(stat_of(d.iloc[ia], c, b, s))
                            vb.append(stat_of(d.iloc[ib], c, b, s))
                        va, vb = np.array(va), np.array(vb)
                        ok = np.isfinite(va) & np.isfinite(vb)
                        agree = int(np.sum(np.sign(va[ok]) == np.sign(vb[ok])))
                        m = len(va[ok])
                        lo, hi = wilson(agree, m)
                        allv = np.concatenate([va[ok], vb[ok]])
                        pool_v = pooled[(c, b, s)]
                        # share of blocks whose sign matches the full-480 pooled sign
                        match_pool = float(np.mean(np.sign(allv) == np.sign(pool_v)))
                        rows.append(dict(
                            q=q, k=k, n=n, char=c, book=b, stat=s, pairs=m,
                            agree=agree / m, ci_lo=lo, ci_hi=hi,
                            pooled_rho=pool_v, block_mean=float(allv.mean()),
                            block_sd=float(allv.std(ddof=1)),
                            c_sqrtn=float(allv.std(ddof=1)) * np.sqrt(n),
                            match_pooled_sign=match_pool,
                            estimable=bool(agree / m >= AGREE_BAR and lo >= CI_BAR)))
            P(f"  ... stratum (q {q:.3f}, k {k}) n={n} done")
            flush_log()
    curve = pd.DataFrame(rows)
    curve.to_csv(f"{OUT}.curve.csv", index=False)

    for (q, k) in STRATA:
        P(f"\n--- stratum (q {q:.3f}, k {k}): pairwise SIGN AGREEMENT, all 4 rungs, all reported ---")
        for s in STATS:
            t = curve[(curve.q == q) & (curve.k == k) & (curve["stat"] == s)]
            piv = t.pivot_table(index=["char", "book"], columns="n", values="agree")
            P(f"\n  [{s}] agreement rate by n")
            P(fmt(piv, 3))
            est = t.groupby("n").estimable.sum()
            P(f"  [{s}] estimable (>= {AGREE_BAR:.2f} and CI_lo >= {CI_BAR:.2f}) at n = "
              + ", ".join(f"{n}: {int(est.get(n, 0))}/12" for n in N_LADDER))

    # ------------------------------------------------------------ B3 n*
    P("\n" + "=" * 110)
    P("B3 n* -- the n at which agreement reaches 0.90 (interpolated inside the ladder, "
      "normal-extrapolated beyond)")
    P("=" * 110)
    erows = []
    for (q, k) in STRATA:
        for c in CHARS:
            for b in BOOKS:
                for s in STATS:
                    t = curve[(curve.q == q) & (curve.k == k) & (curve.char == c) &
                              (curve.book == b) & (curve["stat"] == s)].sort_values("n")
                    ag = t.agree.to_numpy()
                    ns = t.n.to_numpy(float)
                    # inside the ladder
                    nstar_in = np.nan
                    for i in range(len(ns)):
                        if ag[i] >= AGREE_BAR:
                            if i == 0:
                                nstar_in = ns[0]
                            else:
                                x0, x1 = np.log2(ns[i - 1]), np.log2(ns[i])
                                y0, y1 = ag[i - 1], ag[i]
                                nstar_in = 2 ** (x0 + (AGREE_BAR - y0) * (x1 - x0) / (y1 - y0)) \
                                    if y1 > y0 else ns[i]
                            break
                    cc = float(np.mean(t.c_sqrtn.to_numpy()))
                    mu = abs(float(t.pooled_rho.iloc[0]))
                    nstar_ex = (cc * Z_P / mu) ** 2 if mu > 0 else np.inf
                    erows.append(dict(q=q, k=k, char=c, book=b, stat=s, pooled_rho=t.pooled_rho.iloc[0],
                                      c_fit=cc, agree_240=ag[-1], nstar_ladder=nstar_in,
                                      nstar_extrap=nstar_ex,
                                      reaches_in_ladder=bool(np.isfinite(nstar_in))))
    extrap = pd.DataFrame(erows)
    extrap.to_csv(f"{OUT}.extrap.csv", index=False)
    for (q, k) in STRATA:
        P(f"\n--- stratum (q {q:.3f}, k {k}) ---")
        t = extrap[(extrap.q == q) & (extrap.k == k)].copy()
        t["nstar"] = np.where(t.reaches_in_ladder, t.nstar_ladder, t.nstar_extrap)
        P(fmt(t[["char", "book", "stat", "pooled_rho", "c_fit", "agree_240",
                 "nstar_ladder", "nstar_extrap"]].set_index(["char", "book", "stat"]), 4))
        for s in STATS:
            u = t[t["stat"] == s]
            P(f"  [{s}] reaches 0.90 inside the ladder: {int(u.reaches_in_ladder.sum())}/12   "
              f"median n* (incl. extrapolation) {u.nstar.median():,.0f}")

    # B4 grading: observed SD ratio vs collinearity prediction
    P("\n--- B4 GRADE: observed sd(PARTIAL)/sd(MARGINAL) vs predicted 1/sqrt(1-R^2) ---")
    mrows = []
    for (q, k) in STRATA:
        for c in CHARS:
            pred = float(collin[(collin.q == q) & (collin.k == k) & (collin.char == c)].vif_sd_ratio.iloc[0])
            for n in N_LADDER:
                sp = curve[(curve.q == q) & (curve.k == k) & (curve.char == c) &
                           (curve.n == n) & (curve["stat"] == "PARTIAL")].block_sd.mean()
                sm = curve[(curve.q == q) & (curve.k == k) & (curve.char == c) &
                           (curve.n == n) & (curve["stat"] == "MARGINAL")].block_sd.mean()
                mrows.append(dict(q=q, k=k, char=c, n=n, sd_partial=sp, sd_marginal=sm,
                                  obs_ratio=sp / sm, pred_ratio=pred,
                                  within_tol=bool(abs(sp / sm - pred) / pred <= MECH_TOL)))
    mech = pd.DataFrame(mrows)
    P(fmt(mech.set_index(["q", "k", "char", "n"]), 4))
    P(f"  B4: observed within {MECH_TOL:.0%} of the collinearity prediction in "
      f"{int(mech.within_tol.sum())}/{len(mech)} cells")

    # ------------------------------------------------------------ B7 post-hoc: the block device
    P("\n" + "=" * 110)
    P("B7 POST-HOC (declared post-hoc, added after the first run; B1-B6 above are unchanged)")
    P("   two DISJOINT blocks of n from a fixed pool of N are negatively dependent, "
      f"corr = -n/(N-n); N = {N_TOTAL}")
    P("=" * 110)
    curve["fpc"] = np.sqrt(1.0 - curve.n / N_TOTAL)
    curve["c_inf"] = curve.block_sd * np.sqrt(curve.n) / curve.fpc
    curve["r_pair"] = -curve.n / (N_TOTAL - curve.n)
    P("\n  B7a  c = sd_block * sqrt(n), RAW and FPC-corrected, mean over the 12 (char, book) "
      "points per rung")
    P(fmt(curve.groupby(["q", "stat", "n"])[["c_sqrtn", "c_inf"]].mean(), 4))
    flat = curve.groupby(["q", "stat"]).c_inf.agg(["mean", "std", "min", "max"])
    P("\n  B7a  is c_inf flat in n?  (if yes, the finite pool is the WHOLE cause of the decline)")
    P(fmt(flat, 4))

    arows = []
    for _, r in curve.iterrows():
        se_inf = r.c_inf / np.sqrt(r.n)
        a = abs(r.pooled_rho) / se_inf if se_inf > 0 else np.nan
        arows.append(dict(q=r.q, n=int(r.n), char=r.char, book=r.book, stat=r["stat"],
                          pooled_rho=r.pooled_rho, a=a, agree_obs=r.agree,
                          agree_pred_pair=same_sign_prob(a, r.r_pair),
                          agree_pred_indep=same_sign_prob(a, 0.0)))
    fpc = pd.DataFrame(arows)
    fpc["err"] = fpc.agree_obs - fpc.agree_pred_pair
    P("\n  B7b  observed vs the analytic complement-pair prediction (validation), and the "
      "INDEPENDENT-block curve")
    P(fmt(fpc.groupby(["q", "stat", "n"])[["agree_obs", "agree_pred_pair", "agree_pred_indep"]]
          .mean(), 4))
    P(f"  B7b  |observed - complement-pair prediction|: mean {fpc.err.abs().mean():.4f}  "
      f"median {fpc.err.abs().median():.4f}  max {fpc.err.abs().max():.4f}  "
      f"(n = {len(fpc)} points)")
    for (q, k) in STRATA:
        for s in STATS:
            t = fpc[(fpc.q == q) & (fpc["stat"] == s)]
            P(f"\n  B7b INDEPENDENT-block agreement, stratum (q {q:.3f}, k {k}) [{s}]")
            P(fmt(t.pivot_table(index=["char", "book"], columns="n", values="agree_pred_indep"), 3))

    # B7c independent-block n*
    nrows = []
    for (q, k) in STRATA:
        for c in CHARS:
            for b in BOOKS:
                for s in STATS:
                    t = curve[(curve.q == q) & (curve.char == c) & (curve.book == b) &
                              (curve["stat"] == s)]
                    cinf = float(t.c_inf.mean())
                    mu = abs(float(t.pooled_rho.iloc[0]))
                    nrows.append(dict(q=q, k=k, char=c, book=b, stat=s, pooled_rho=t.pooled_rho.iloc[0],
                                      c_inf=cinf, nstar_indep=(cinf * Z_P / mu) ** 2 if mu > 0 else np.inf))
    nstar = pd.DataFrame(nrows)
    fpc = fpc.merge(nstar[["q", "char", "book", "stat", "c_inf", "nstar_indep"]],
                    on=["q", "char", "book", "stat"], how="left")
    fpc.to_csv(f"{OUT}.fpc.csv", index=False)
    P("\n  B7c  n*_indep = (c_inf * z_p / |rho_pooled|)^2 -- the queue's question, "
      "independent blocks")
    for (q, k) in STRATA:
        t = nstar[(nstar.q == q) & (nstar.k == k)]
        P(f"\n  stratum (q {q:.3f}, k {k}):")
        P(fmt(t.pivot_table(index=["char", "book"], columns="stat",
                            values="nstar_indep"), 1))
        for s in STATS:
            u = t[t["stat"] == s]
            P(f"    [{s}] median n* {u.nstar_indep.median():,.0f}   "
              f"range {u.nstar_indep.min():,.0f} .. {u.nstar_indep.max():,.0f}   "
              f"<= 240 in {int((u.nstar_indep <= 240).sum())}/12")

    P("\n  B7d  what the complement device costs: the same-sign rate at r = -1 (idea 310's own "
      "split-half, n = 30 of N = 60) against independent blocks, by effect size a = |mu|/se")
    grid = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    P(fmt(pd.DataFrame([dict(a=a, indep=same_sign_prob(a, 0.0), half_pool=same_sign_prob(a, -1 / 3),
                             complement_r_minus1=same_sign_prob(a, -1.0)) for a in grid])
          .set_index("a"), 4))
    P("  B7d  a complement split UNDERSTATES sign replication at every effect size below "
      "a ~ 2, and reports agreement BELOW a coin flip where the independent rate is 0.50.")
    flush_log()

    # ------------------------------------------------------------ B5 rule 8 walk-forward
    P("\n" + "=" * 110)
    P(f"B5 RULE 8 WALK-FORWARD -- direction FIT on block A (n draws), APPLIED ONCE to disjoint "
      f"block B ({N_WF} pairs per point)")
    P("=" * 110)
    wrows = []
    for (q, k) in STRATA:
        d = panels[(panels.q == q) & (panels.k == k)].sort_values("seed").reset_index(drop=True)
        spy = dict(Sharpe=float(d.SPY_Sharpe.iloc[0]), OOS_Sharpe=float(d.SPY_OOS_Sharpe.iloc[0]),
                   OOS_CAGR=float(d.SPY_OOS_CAGR.iloc[0]), OOS_MaxDD=float(d.SPY_OOS_MaxDD.iloc[0]),
                   CAGR=float(d.SPY_CAGR.iloc[0]), MaxDD=float(d.SPY_MaxDD.iloc[0]),
                   H1=float(d.SPY_H1.iloc[0]), H2=float(d.SPY_H2.iloc[0]))
        for n in N_LADDER:
            for c in CHARS:
                for b in BOOKS:
                    for s in STATS:
                        picks, anchors, v2s = [], [], []
                        n4a = n4b = 0
                        pc, pm, pd_ = [], [], []
                        for (ia, ib) in pairs[(q, k, n)][:N_WF]:
                            A, B = d.iloc[ia], d.iloc[ib]
                            sgn = np.sign(stat_of(A, c, b, s))
                            if not np.isfinite(sgn) or sgn == 0:
                                continue
                            x = B[f"{c}_IS"].to_numpy()
                            j = int(np.argmax(x)) if sgn > 0 else int(np.argmin(x))
                            row = B.iloc[j]
                            picks.append(float(row[f"{b}_OOS_Sharpe"]))
                            pc.append(float(row[f"{b}_OOS_CAGR"]))
                            pd_.append(float(row[f"{b}_OOS_MaxDD"]))
                            pm.append(float(row[f"{b}_MaxDD"]))
                            anchors.append(float(B[f"{b}_OOS_Sharpe"].mean()))
                            v2s.append(float(B["v2_OOS_Sharpe"].mean()))
                            n4a += int(bool(row[f"{b}_keep4a"]))
                            n4b += int(bool(row[f"{b}_keep4b"]))
                        if not picks:
                            continue
                        wrows.append(dict(
                            q=q, k=k, n=n, char=c, book=b, stat=s, picks=len(picks),
                            pick_OOS_Sharpe=float(np.mean(picks)),
                            pick_OOS_CAGR=float(np.mean(pc)),
                            pick_OOS_MaxDD=float(np.mean(pd_)),
                            pick_MaxDD=float(np.mean(pm)),
                            anchor_OOS_Sharpe=float(np.mean(anchors)),
                            edge=float(np.mean(picks) - np.mean(anchors)),
                            beat_anchor=float(np.mean(np.array(picks) > np.array(anchors))),
                            v2_OOS_Sharpe=float(np.mean(v2s)),
                            spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                            spy_OOS_MaxDD=spy["OOS_MaxDD"],
                            keep4a=n4a, keep4b=n4b))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for (q, k) in STRATA:
        t = wf[(wf.q == q) & (wf.k == k)]
        P(f"\n--- stratum (q {q:.3f}, k {k}): OOS Sharpe of the pick vs the block's do-nothing anchor ---")
        P(f"  SPY on this calendar: OOS Sharpe {t.spy_OOS_Sharpe.iloc[0]:.4f}  "
          f"OOS CAGR {t.spy_OOS_CAGR.iloc[0]:.4f}  OOS MaxDD {t.spy_OOS_MaxDD.iloc[0]:.4f}")
        for s in STATS:
            u = t[t["stat"] == s]
            P(f"\n  [{s}] mean edge (pick - anchor) by n:")
            P(fmt(u.pivot_table(index=["char", "book"], columns="n", values="edge"), 4))
            P(f"  [{s}] mean pick OOS Sharpe {u.pick_OOS_Sharpe.mean():+.4f}  "
              f"anchor {u.anchor_OOS_Sharpe.mean():+.4f}  edge {u.edge.mean():+.4f}  "
              f"beats anchor {u.beat_anchor.mean():.1%} of picks  |  RULES v2 OOS "
              f"{u.v2_OOS_Sharpe.mean():.4f}  SPY OOS {u.spy_OOS_Sharpe.iloc[0]:.4f}")
            P(f"  [{s}] picks clearing 4a: {int(u.keep4a.sum())}/{int(u.picks.sum())}   "
              f"4b: {int(u.keep4b.sum())}/{int(u.picks.sum())}")

    # ------------------------------------------------------------ B6 KEEP paths, whole corpus
    P("\n" + "=" * 110)
    P("B6 BOTH KEEP PATHS over the whole constructed corpus")
    P("=" * 110)
    kk = keeps[keeps.arm.isin(BOOKS)]
    P(fmt(kk.groupby(["q", "k", "arm"]).agg(n=("panel", "size"), keep4a=("keep4a", "sum"),
                                            keep4b=("keep4b", "sum"),
                                            OOS_Sharpe=("OOS_Sharpe", "mean"),
                                            CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean")), 4))
    both = kk[kk.keep4a & kk.keep4b]
    P(f"  corpus: {len(kk)} panel-books.  4a {int(kk.keep4a.sum())}  4b {int(kk.keep4b.sum())}  "
      f"BOTH {len(both)}")
    P("  4b fail-reason census (first-listed set):")
    P(fmt(kk.fails4b.value_counts().to_frame("count").head(12), 0))
    for (q, k) in STRATA:
        d = panels[(panels.q == q) & (panels.k == k)]
        P(f"  (q {q:.3f}, k {k}) SPY: CAGR {d.SPY_CAGR.iloc[0]:.4f} Sharpe {d.SPY_Sharpe.iloc[0]:.4f} "
          f"MaxDD {d.SPY_MaxDD.iloc[0]:.4f} halves {d.SPY_H1.iloc[0]:.4f}/{d.SPY_H2.iloc[0]:.4f} "
          f"OOS {d.SPY_OOS_Sharpe.iloc[0]:.4f} | RULES v2: Sharpe {d.v2_Sharpe.mean():.4f} "
          f"halves {d.v2_H1.mean():.4f}/{d.v2_H2.mean():.4f} OOS {d.v2_OOS_Sharpe.mean():.4f} "
          f"MaxDD {d.v2_MaxDD.mean():.4f}")

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 110)
    P("VERDICT")
    P("=" * 110)
    q0, k0 = PRIMARY
    prim = curve[(curve.q == q0) & (curve.k == k0)]
    for s in STATS:
        for n in N_LADDER:
            u = prim[(prim["stat"] == s) & (prim.n == n)]
            P(f"  PRIMARY (q {q0:.3f}, k {k0})  [{s}] n={n:3d}: mean agreement {u.agree.mean():.3f} "
              f"(range {u.agree.min():.3f}-{u.agree.max():.3f})  estimable {int(u.estimable.sum())}/12")
    pe = extrap[(extrap.q == q0) & (extrap.k == k0)]
    for s in STATS:
        u = pe[pe["stat"] == s]
        P(f"  PRIMARY [{s}] n* median {u.apply(lambda r: r.nstar_ladder if r.reaches_in_ladder else r.nstar_extrap, axis=1).median():,.0f}   "
          f"reaches inside ladder {int(u.reaches_in_ladder.sum())}/12")
    P("  --- B7c, the answer the queue asked for (INDEPENDENT blocks, post-hoc correction) ---")
    for (q, k) in STRATA:
        for s in STATS:
            u = nstar[(nstar.q == q) & (nstar.k == k) & (nstar["stat"] == s)]
            P(f"  (q {q:.3f}, k {k}) [{s}] n*_indep median {u.nstar_indep.median():,.0f}  "
              f"range {u.nstar_indep.min():,.0f}..{u.nstar_indep.max():,.0f}  "
              f"<= 240 in {int((u.nstar_indep <= 240).sum())}/12  "
              f"<= 60 in {int((u.nstar_indep <= 60).sum())}/12")
    P("  --- B4 grade: does collinearity inflate the partial's SD? ---")
    P(f"  observed sd(PARTIAL)/sd(MARGINAL) range {mech.obs_ratio.min():.4f}..{mech.obs_ratio.max():.4f} "
      f"(mean {mech.obs_ratio.mean():.4f}) against the 1/sqrt(1-R^2) prediction "
      f"{mech.pred_ratio.min():.4f}..{mech.pred_ratio.max():.4f}")
    flush_log()
    return panels, curve, extrap, wf, keeps, mech, collin


if __name__ == "__main__":
    main()
    flush_log()
