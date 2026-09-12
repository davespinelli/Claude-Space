#!/usr/bin/env python3
"""Idea 838 (lane B, 2026-09-12) — what is the SHORTEST SUB-WINDOW at which a BOOK-vs-SPY
SHARPE COMPARISON can be CALLED?

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 832 measured, on the record's 12 committed 4b
passes, that 0.9858 of 18-month (378d) book-vs-SPY sub-block Sharpe comparisons sit INSIDE their
own two-sided 95% noise band, and that even 30-month blocks only get the inside share to 0.9649
— i.e. PROTOCOL 4b's both-halves clause is, on a three-year window, a comparison the data cannot
make.  Idea 839 then showed the same corpus's next-window sign is never positively informative.
What neither run did is LOCATE the length at which the comparison becomes callable.  The queue
asks for that length as a PROTOCOL-grade constant, with its null beside it.  This run sweeps it.

WHAT "CALLABLE" MEANS HERE (declared before any number).  A single (book vs SPY) Sharpe
comparison over a block of L trading days is CALLED if the difference of the two Sharpe ratios
lies OUTSIDE its own two-sided 95% band under the stated null; it is UNCALLABLE (inside) if it
does not.  `inside_share` is the fraction of a cell's blocks that are uncallable, so it is the
share of the record's own sub-window verdicts that are coin flips.  The MINIMUM CALLABLE LENGTH
L* of a cell is the smallest swept L whose inside_share < 0.50 — the queue's own bar.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  BLOCK LENGTH L   — swept over 15 rungs, 126d (6 months, the queue's floor) to the full
                         scored sample as ONE block.  Every rung reported for every book.
  P2  NULL             — ANALYTIC (Memmel 2003's correction to Jobson-Korkie for the difference
                         of two correlated Sharpe ratios), BOOTSTRAP (paired stationary block
                         bootstrap, block 21d) and PERM (paired 21d-block label-swap
                         permutation).  All three reported at every rung they are computed on.
Tiling (OVERLAP21 / OVERLAP63 / DISJOINT), claim set (MEMO8/MEMO12) and cost rung
{0, 10, 25} bps are REPORTED-NOT-SELECTED.  No book dial is tuned: every book runs at the gross,
band, n and cadence its own committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C6 carried verbatim from ideas 831/832 so the
censuses stay comparable; C7-C10 are this run's own):
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest, weights
      decided at close t applied at t+1, the book's own cadence); blocks are SLICES of it.
  C2  A comparison is always book-vs-SPY over the SAME block, on the book's own panel's SPY.
  C3  Sharpe is engine's: mean*252 / (sd(ddof=1)*sqrt(252)).  Annualisation cancels in z.
  C4  Warm-up: blocks start at each panel's px.index[260], as baseline.compare does.
  C5  A block must lie wholly inside the sample.
  C6  A book is scored against its own panel's SPY column.
  C7  ANALYTIC band: V = (1/T)(2 - 2rho + 0.5(SRa^2 + SRb^2) - SRa SRb rho^2) on DAILY returns,
      z = (SRa - SRb)/sqrt(V), inside iff |z| < 1.96.  This is idea 832's C8, unchanged.
  C8  BOOTSTRAP band: paired stationary block bootstrap of the two series TOGETHER (block 21d,
      400 reps, fixed seed), sd of the resampled (SRa - SRb); inside iff |d| < 1.96 * sd.
  C9  PERM band: for each 21d block of the pair, swap the two series' labels with probability
      0.5 (400 draws, fixed seed) — exchangeable under the equal-distribution null — and take the
      two-sided 97.5th percentile of |null d|; inside iff |d_obs| <= that percentile.
  C10 Tilings: OVERLAP21/OVERLAP63 start a block at every 21st/63rd index from warm-up;
      DISJOINT tiles from warm-up at stride L so every day is used at most once (idea 839 showed
      overlapping reads change the NUMBER even when they keep the sign, so DISJOINT is reported
      beside them at every rung).

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_CROSS   a finite minimum callable length EXISTS: the pooled MEMO12 inside_share drops below
            0.50 at some swept L <= the full sample, under the ANALYTIC null at 10 bps.
  H_CONST   the length is a CONSTANT in the sense the queue asks for: the per-book L* over the
            12 committed passes spans at most a factor of 2.0 (max L* / min L* <= 2.0).
  H_MONO    inside_share is monotone non-increasing in L at every one of the 12 books.
  H_NULL    the three nulls agree: at every book, the L* they give differ by at most one rung.
  H_TILE    the overlap lesson does not bite here: OVERLAP21 and DISJOINT give the same L*
            within one rung at every book.
  H_WF      (rule 8, on this run's own tuned axes) the L chosen on IS blocks only (ending
            2016-12-31) is also the OOS crossing rung, and |OOS inside_share - IS inside_share|
            <= 0.10 there.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp (prices are re-cached daily).
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05%.
  G3  this run's noise machinery reproduces idea 832's COMMITTED inside-share table on ITS OWN
      block set (the k-way splits of 756d/1260d windows at s=21 over MEMO12): 0.9858, 0.9908,
      0.9821, 0.9649, 0.9845, 0.9888, bar |d| <= 0.0200 on every one of the six.
  G4  the vectorised window metrics reproduce engine.metrics exactly (bar 1e-10) on 200
      fixed-seed random windows.
  G5  the ANALYTIC band reproduces the paired stationary block bootstrap on 60 sampled blocks:
      median analytic_sd / bootstrap_sd inside [0.75, 1.25]  (idea 832's G6, re-run).
  G6  the swept L* agrees with the CLOSED FORM the analytic band implies — L_hat =
      1.96^2 * V_1d / d^2 evaluated at the cell's MEDIAN block — within one grid rung.

Outputs (all under research/backtests/, all committed):
  .txt            full console log
  .books.csv      one row per book: fixed-window + OOS metrics and every block Sharpe
  .sweep.csv      one row per (book, tiling, L, cost): n_blocks, inside_share, leg_share, margins
  .nulls.csv      one row per (book, L, null): inside_share under each of the three nulls
  .lstar.csv      the deliverable — per-book L* under every null x tiling, plus the closed form
  .keeppaths.csv  both KEEP paths re-read with the sub-window leg at every block length
  .g3.csv         gate G3's reproduction of idea 832's committed noise table
  .wf.csv         rule-8 IS/OOS table on the tuned (L, null) axes
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_what-is-the-SHORTEST-SUB-WINDOW-at-which-a-BOOK-vs-SPY-SHARPE-COMPARISON-can-be-CALLED_B.py
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state, compare)                                        # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

DATE = "2026-09-12"
SLUG = "what-is-the-SHORTEST-SUB-WINDOW-at-which-a-BOOK-vs-SPY-SHARPE-COMPARISON-can-be-CALLED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# P1 — the swept axis.  126d = 6 months (the queue's floor) .. the full scored sample.
LGRID = [126, 189, 252, 315, 378, 504, 630, 756, 1008, 1260, 1512, 2016, 2520, 3024, 3780]
LFULL = -1                      # sentinel: the whole scored sample as ONE block
NULLS = ["ANALYTIC", "BOOTSTRAP", "PERM"]
TILINGS = ["OVERLAP21", "OVERLAP63", "DISJOINT"]
COSTS = [0, 10, 25]
COST = 10                       # PROTOCOL's rung and the headline
HEAD_TILE = "OVERLAP21"         # idea 832's own reading, so the gate and the sweep line up
BAR_INSIDE = 0.50               # the queue's bar for "callable"
ZCRIT = 1.96
BOOT_BLOCK, BOOT_REPS, NULL_SAMPLE = 21, 400, 24
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
MAX_VOL, WARMUP = 0.60, 260
SEED = 8380
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 112 + f"\n{s}\n" + "=" * 112)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from idea 832's committed script (which copied them from
# ideas 831/641/574/804), so the corpus is not silently redefined here.
# =====================================================================================
def comp_rank(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    return s.where(elig), elig


def topn_weights(px, n=20, gross=0.75, m=0, fixed=False):
    sc, elig = comp_rank(px)
    rank = sc.rank(axis=1, ascending=False)
    if m == 0:
        sel = (rank <= n).fillna(False)
    else:
        R, E = rank.values, elig.values
        held = np.zeros(px.shape[1], bool)
        out = np.zeros(px.shape, bool)
        for i in range(len(px)):
            r_i, e_i = R[i], E[i]
            ok = ~np.isnan(r_i)
            keep = held & e_i & ok & (r_i <= n + m)
            need = n - int(keep.sum())
            if need > 0:
                cand = np.where(e_i & ok & ~keep)[0]
                if len(cand):
                    cand = cand[np.argsort(r_i[cand])][:need]
                    keep[cand] = True
            held = keep
            out[i] = keep
        sel = pd.DataFrame(out, index=px.index, columns=px.columns)
    if fixed:
        return sel.astype(float).mul(gross / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(k, axis=0).mul(gross).fillna(0.0)


def band_ew_respread(px, band, gross):
    e = band_state(px, band).astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, gross=1.00):
    _, elig = comp_rank(px)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def shy_residual_weights(px, gross=0.375, sleeve="SHY"):
    W = ewall_weights(px.drop(columns=[sleeve]), gross).reindex(columns=px.columns).fillna(0.0)
    W[sleeve] = (1.0 - W.sum(axis=1)).clip(lower=0.0)
    return W


def breadth_gate_weights(px, gross=1.00, q=0.17, wroll=1008, depth=1.0, freq="W"):
    from engine import rebalance_mask
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    breadth = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = breadth.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (breadth < thr) & breadth.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    m = m.where(mask).ffill().fillna(1.0)
    return ewall_weights(px, gross).mul(m, axis=0)


def ma_respread(px, gross=0.75):
    """R2 — hold every name above its own 200d MA, gross RE-SPREAD over exactly those names."""
    pm = px.notna()
    ma = (px > px.rolling(200).mean()) & pm
    k = ma.sum(axis=1).replace(0, np.nan)
    return gross * ma.astype(float).div(k, axis=0).fillna(0.0)


def ma_dist_tophalf(px, gross=0.75, q=0.50):
    """R3 — rank priced names by px/MA200-1, hold the top ceil(q*N) at gross/K each, rest CASH."""
    pm = px.notna()
    dist = (px / px.rolling(200).mean() - 1.0).where(pm)
    rk = dist.rank(axis=1, ascending=False)
    n_priced = dist.notna().sum(axis=1)
    k = np.ceil(q * n_priced).replace(0, np.nan)
    sel = rk.le(k, axis=0).fillna(False) & dist.notna()
    kk = sel.sum(axis=1).replace(0, np.nan)
    return gross * sel.astype(float).div(kk, axis=0).fillna(0.0)


def r6_topn(px, n=20, gross=0.65):
    """R4 — idea 804's committed constructor: rank priced names by 6m return, top n at g/n."""
    pm = px.notna()
    r6 = (px / px.shift(126) - 1.0).where(pm)
    rk = r6.rank(axis=1, ascending=False)
    return (rk <= n).astype(float) * (gross / n)


# (key, label, panel, weights_fn, cadence, published (CAGR, Sharpe, MaxDD), memo file)
CORPUS = [
    ("K1", "u56 top20 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 0), "W", (0.1279, 1.064, -0.1831),
     "2026-09-07_u56-top20-g075-4b_C_MEMO.md"),
    ("K2", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W", (None, None, None),
     "2026-09-07_u56-top20-band-m20_4b_B_MEMO.md"),
    ("K3", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D", (0.1171, 1.1454, -0.1237),
     "2026-09-06_daily-plus-buffer30_PARK_MEMO.md"),
    ("K4", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.0, 1.00), "M", (0.1196, 1.2126, -0.1549),
     "2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md"),
    ("K5", "u56 RULES v2 band 0.03, W, g1.00  [the standing candidate]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W", (0.1159, 1.2055, -0.1591),
     "2026-09-08_u56-band3-fullgross_KEEP_MEMO.md"),
    ("K6", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W", (0.1402, 1.2264, -0.1942),
     "2026-09-06_band12-ewall-rw_PARK_MEMO.md"),
    ("K7", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W", (0.0627, 1.1777, -0.1110),
     "2026-09-07_b136-ewall-shy-residual"),
    ("K8", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W", (0.1413, 1.2204, -0.1479),
     "2026-09-10_does-the-BREADTH-gate-4b-pass-live-only-at-gross-1.00_cloud.memo.md"),
    ("R1", "u56 band 0.08, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W", (0.1137, 1.1439, -0.1905),
     "2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md"),
    ("R2", "u56 MA-RESPREAD, W, g0.75", "U56",
     lambda px: ma_respread(px, 0.75), "W", (0.1155, 1.0914, -0.1862),
     "2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md"),
    ("R3", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M", (0.1547, 1.2359, -0.1980),
     "2026-09-11_4b-candidate-U56-MA-DISTANCE-TOP-HALF-monthly_memo.md"),
    ("R4", "b136 R6-top20 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 20, 0.65), "W", (0.1499, 1.1264, -0.1943),
     "2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md"),
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W", (0.0863, 1.202, -0.1205), "RULES.md v2"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56",
     rules_v1_weights, "W", (None, None, None), "RULES.md v1"),
]
KEYS = [c[0] for c in CORPUS]
MEMO8 = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
MEMO12 = MEMO8 + ["R1", "R2", "R3", "R4"]
CLAIM_SETS = {"MEMO8": MEMO8, "MEMO12": MEMO12}
COMPARANDS = ["LIVE", "V1"]
WFUN = {c[0]: c[3] for c in CORPUS}
FREQ = {c[0]: c[4] for c in CORPUS}


# =====================================================================================
# metrics (G4 checks them against engine.metrics exactly)
# =====================================================================================
def w_metrics(r: np.ndarray):
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    sd = r.std(ddof=1)
    sharpe = (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan
    mdd = float(np.min(eq / np.maximum.accumulate(eq) - 1.0))
    return cagr, sharpe, mdd


def sharpe_of(r: np.ndarray):
    sd = r.std(ddof=1)
    return (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan


def bounds(T, k):
    return [(j * T) // k for j in range(k + 1)]


def memmel(a: np.ndarray, b: np.ndarray):
    """(d, z, V_1d) for two correlated DAILY return series (C7).  Annualisation cancels in z."""
    T = len(a)
    sa, sb = a.std(ddof=1), b.std(ddof=1)
    if T < 8 or sa <= 0 or sb <= 0:
        return np.nan, np.nan, np.nan
    SRa, SRb = a.mean() / sa, b.mean() / sb
    rho = np.corrcoef(a, b)[0, 1]
    V1 = 2.0 - 2.0 * rho + 0.5 * (SRa ** 2 + SRb ** 2) - SRa * SRb * rho ** 2
    d = SRa - SRb
    if not np.isfinite(V1) or V1 <= 0:
        return d, np.nan, np.nan
    return d, d / np.sqrt(V1 / T), V1


def block_starts(i0, n, L, tiling):
    """C10.  Every returned start s satisfies s + L <= n."""
    if L > n - i0:
        return []
    if tiling == "DISJOINT":
        step = L
    else:
        step = 21 if tiling == "OVERLAP21" else 63
    return list(range(i0, n - L + 1, step))


# =====================================================================================
def build(panels, cost, verbose=False):
    books, meta = {}, {}
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        t0 = time.time()
        books[key] = backtest(px, wf(px), cost_bps=cost, freq=freq)["returns"]
        meta[key] = dict(label=label, panel=pan, freq=freq, pub=pub, memo=memo)
        if verbose:
            P(f"  built {key:5s} {label:62s} panel {pan:5s} freq {freq}  ({time.time()-t0:.1f}s)")
    return books, meta


def gates_g1g2(books, starts):
    hdr("GATES G1 / G2 — printed BEFORE any new number")
    rows = []
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        if pub[0] is None:
            rows.append(dict(gate=f"G1/{key}", pub_CAGR=np.nan, got_CAGR=np.nan,
                             pub_Sharpe=np.nan, got_Sharpe=np.nan, pub_MaxDD=np.nan,
                             got_MaxDD=np.nan, verdict="NO PUBLISHED TRIPLE"))
            continue
        gc, gs, gd = w_metrics(books[key].loc[starts[pan]:].values)
        ok = abs(gc - pub[0]) <= 0.010 and abs(gs - pub[1]) <= 0.060 and abs(gd - pub[2]) <= 0.020
        rows.append(dict(gate=f"G2/{key}" if key in COMPARANDS else f"G1/{key}",
                         pub_CAGR=pub[0], got_CAGR=gc, pub_Sharpe=pub[1], got_Sharpe=gs,
                         pub_MaxDD=pub[2], got_MaxDD=gd, verdict="PASS" if ok else "FAIL"))
    g = pd.DataFrame(rows)
    P(g.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    sc = g[g.verdict.isin(["PASS", "FAIL"])]
    P("Tolerance declared: |dCAGR|<=1.00pp, |dSharpe|<=0.060, |dMaxDD|<=2.00pp.")
    P(f"G1+G2: {(sc.verdict=='PASS').sum()} of {len(sc)} PASS "
      f"({len(g)-len(sc)} books publish no triple and are marked so).")
    return g, int((sc.verdict == 'PASS').sum()) == len(sc)


def gate_g3(books, meta, panels, starts):
    """Reproduce idea 832's committed inside-share table on ITS OWN block set."""
    hdr("GATE G3 — reproduce idea 832's COMMITTED noise table on its own block set")
    want = {(756, 2): 0.9858, (756, 3): 0.9908, (756, 4): 0.9821,
            (1260, 2): 0.9649, (1260, 3): 0.9845, (1260, 4): 0.9888}
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    rows = []
    for (H, k), w in want.items():
        ins = tot = 0
        for key in MEMO12:
            pan = meta[key]["panel"]
            idx = panels[pan].index
            i0 = idx.get_loc(starts[pan])
            r_all, s_all = books[key].values, spy[pan]
            bb = bounds(H, k)
            for i in range(i0, len(idx) - H + 1, 21):
                for j in range(k):
                    a = r_all[i + bb[j]: i + bb[j + 1]]
                    b = s_all[i + bb[j]: i + bb[j + 1]]
                    _, z, _ = memmel(a, b)
                    tot += 1
                    if np.isfinite(z):
                        ins += int(abs(z) < ZCRIT)
        got = ins / tot
        rows.append(dict(H=H, k=k, block_days=H // k, n_blocks=tot, committed=w, got=got,
                         diff=got - w, verdict="PASS" if abs(got - w) <= 0.02 else "FAIL"))
    G = pd.DataFrame(rows)
    P(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok = (G.verdict == "PASS").all()
    P(f"G3: {int((G.verdict=='PASS').sum())} of {len(G)} committed cells reproduced within "
      f"0.0200 -> {'PASS' if ok else 'FAIL'}")
    G.to_csv(f"{OUT}.g3.csv", index=False)
    return G, bool(ok)


def gate_g4(books):
    rng = np.random.default_rng(SEED)
    worst = 0.0
    for _ in range(200):
        key = KEYS[rng.integers(len(KEYS))]
        r = books[key]
        T = int(rng.integers(252, 1261))
        i = int(rng.integers(0, len(r) - T))
        sl = r.iloc[i:i + T]
        a = w_metrics(sl.values)
        m = metrics(sl)
        worst = max(worst, max(abs(x - y) for x, y in zip(a, (m["CAGR"], m["Sharpe"], m["MaxDD"]))))
    ok = worst <= 1e-10
    P(f"GATE G4 — vectorised window metrics vs engine.metrics on 200 fixed-seed random windows: "
      f"max |diff| = {worst:.3e} vs bar 1e-10 -> {'PASS' if ok else 'FAIL'}")
    return worst, ok


# ----------------------------------------------------------------- the two resampling nulls
def resample_nulls(a: np.ndarray, b: np.ndarray, rng):
    """(boot_sd, perm_q975) for one paired block (C8, C9).  Both use 21d blocks, BOOT_REPS draws."""
    T = len(a)
    L = min(BOOT_BLOCK, max(2, T // 4))
    nb = int(np.ceil(T / L))
    # C8 — paired stationary block bootstrap: the SAME index draw for both series.
    st = rng.integers(0, max(1, T - L), size=(BOOT_REPS, nb))
    idxm = (st[:, :, None] + np.arange(L)[None, None, :]).reshape(BOOT_REPS, -1)[:, :T]
    A, B = a[idxm], b[idxm]
    sa, sb = A.std(axis=1, ddof=1), B.std(axis=1, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        boot_d = A.mean(axis=1) / sa - B.mean(axis=1) / sb
    boot_sd = float(np.nanstd(boot_d, ddof=1))
    # C9 — paired 21d-block label swap: exchangeable under the equal-distribution null.
    nblk = int(np.ceil(T / L))
    flip = rng.random((BOOT_REPS, nblk)) < 0.5
    flip = np.repeat(flip, L, axis=1)[:, :T]
    A2 = np.where(flip, b[None, :], a[None, :])
    B2 = np.where(flip, a[None, :], b[None, :])
    sa2, sb2 = A2.std(axis=1, ddof=1), B2.std(axis=1, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        perm_d = A2.mean(axis=1) / sa2 - B2.mean(axis=1) / sb2
    perm_q = float(np.nanquantile(np.abs(perm_d), 0.975))
    return boot_sd, perm_q


def gate_g5(books, meta, panels, starts):
    hdr("GATE G5 — the ANALYTIC band against the paired stationary block bootstrap (832's G6)")
    rng = np.random.default_rng(SEED)
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    rows = []
    H, k = 756, 2
    for _ in range(60):
        key = MEMO12[rng.integers(len(MEMO12))]
        pan = meta[key]["panel"]
        r_all, s_all = books[key].values, spy[pan]
        i0 = panels[pan].index.get_loc(starts[pan])
        i = int(rng.integers(i0, len(r_all) - H))
        bb = bounds(H, k)
        j = int(rng.integers(k))
        a, b = r_all[i + bb[j]: i + bb[j + 1]], s_all[i + bb[j]: i + bb[j + 1]]
        d, z, _ = memmel(a, b)
        bsd, _ = resample_nulls(a, b, rng)
        ana = abs(d / z) if np.isfinite(z) and z != 0 else np.nan
        rows.append(dict(book=key, i=i, block=j, T=len(a), d=d, z=z, analytic_sd=ana,
                         boot_sd=bsd, ratio=ana / bsd if bsd else np.nan))
    B = pd.DataFrame(rows)
    med = B.ratio.median()
    ok = 0.75 <= med <= 1.25
    P(f"60 sampled (book, window, block) triples; stationary block bootstrap L={BOOT_BLOCK}, "
      f"{BOOT_REPS} reps, seed {SEED}.")
    P(f"  median analytic_sd / bootstrap_sd = {med:.4f}  (IQR {B.ratio.quantile(0.25):.4f} .. "
      f"{B.ratio.quantile(0.75):.4f})  vs bar [0.75, 1.25] -> {'PASS' if ok else 'FAIL'}")
    P(f"  median |z| over the 60 = {B.z.abs().median():.3f}; share |z| < {ZCRIT} = "
      f"{(B.z.abs() < ZCRIT).mean():.4f}")
    return B, bool(ok)


# ----------------------------------------------------------------- P1 x tiling x cost sweep
def sweep(books, meta, panels, starts, cost_tag=COST):
    """ANALYTIC inside_share at every (book, tiling, L) cell."""
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    rows = []
    for key in KEYS:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key].values, spy[pan]
        n = len(idx)
        for tiling in TILINGS:
            for L in LGRID + [LFULL]:
                LL = (n - i0) if L == LFULL else L
                ss = block_starts(i0, n, LL, tiling)
                if not ss:
                    continue
                zs, ds, wins, ends = [], [], [], []
                for s0 in ss:
                    a, b = r_all[s0:s0 + LL], s_all[s0:s0 + LL]
                    d, z, _ = memmel(a, b)
                    if not np.isfinite(z):
                        continue
                    zs.append(z)
                    ds.append(d)
                    wins.append(sharpe_of(a) > sharpe_of(b))
                    ends.append(idx[s0 + LL - 1])
                if not zs:
                    continue
                z = np.asarray(zs)
                rows.append(dict(book=key, panel=pan, tiling=tiling, L=LL,
                                 L_months=round(LL / 21.0, 1), is_full=(L == LFULL),
                                 cost=cost_tag, n_blocks=len(z),
                                 inside_share=float(np.mean(np.abs(z) < ZCRIT)),
                                 callable_share=float(np.mean(np.abs(z) >= ZCRIT)),
                                 med_absz=float(np.median(np.abs(z))),
                                 med_d=float(np.median(ds)),
                                 leg_share=float(np.mean(wins)),
                                 first_end=min(ends), last_end=max(ends)))
    return pd.DataFrame(rows)


def lstar_of(sub: pd.DataFrame, col="inside_share"):
    """Smallest swept L whose inside_share < BAR_INSIDE; NaN if no rung crosses."""
    s = sub.sort_values("L")
    hit = s[s[col] < BAR_INSIDE]
    return float(hit.L.iloc[0]) if len(hit) else np.nan


# ----------------------------------------------------------------- P2 — the three nulls
def null_sweep(books, meta, panels, starts):
    """BOOTSTRAP and PERM inside_share on a fixed-seed subsample of DISJOINT + OVERLAP21 blocks."""
    rng = np.random.default_rng(SEED + 1)
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    rows = []
    for key in MEMO12 + COMPARANDS:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key].values, spy[pan]
        n = len(idx)
        for tiling in ["DISJOINT", HEAD_TILE]:
            for L in LGRID + [LFULL]:
                LL = (n - i0) if L == LFULL else L
                ss = block_starts(i0, n, LL, tiling)
                if not ss:
                    continue
                if len(ss) > NULL_SAMPLE:
                    ss = list(np.asarray(ss)[np.sort(
                        rng.choice(len(ss), NULL_SAMPLE, replace=False))])
                ia = ib = ip = 0
                m = 0
                for s0 in ss:
                    a, b = r_all[s0:s0 + LL], s_all[s0:s0 + LL]
                    d, z, _ = memmel(a, b)
                    if not np.isfinite(z):
                        continue
                    bsd, pq = resample_nulls(a, b, rng)
                    m += 1
                    ia += int(abs(z) < ZCRIT)
                    ib += int(abs(d) < ZCRIT * bsd) if bsd > 0 else 1
                    ip += int(abs(d) <= pq) if np.isfinite(pq) else 1
                if not m:
                    continue
                for nm, c in (("ANALYTIC", ia), ("BOOTSTRAP", ib), ("PERM", ip)):
                    rows.append(dict(book=key, tiling=tiling, L=LL, L_months=round(LL / 21.0, 1),
                                     is_full=(L == LFULL), null=nm, n_blocks=m,
                                     inside_share=c / m))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------- fixed window + KEEP paths
def fixed_window(books, meta, panels, starts):
    hdr("RULE 8 (b) MANDATED BOOK LEG — fixed window and OOS, vs the LIVE baseline and SPY")
    rows = []
    for key in KEYS + ["SPY_U56", "SPY_B136"]:
        if key.startswith("SPY_"):
            pan = key.split("_")[1]
            r_all, pan_k = panels[pan]["SPY"].pct_change().fillna(0.0), pan
        else:
            r_all, pan_k = books[key], meta[key]["panel"]
        f, o = r_all.loc[starts[pan_k]:], r_all.loc[OOS_START:]
        fc, fs, fd = w_metrics(f.values)
        oc, os_, od = w_metrics(o.values)
        d = dict(book=key, panel=pan_k, full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                 OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                 full_h1=sharpe_of(f.values[:len(f) // 2]),
                 full_h2=sharpe_of(f.values[len(f) // 2:]),
                 OOS_h1=sharpe_of(o.values[:len(o) // 2]),
                 OOS_h2=sharpe_of(o.values[len(o) // 2:]))
        rows.append(d)
    t = pd.DataFrame(rows).set_index("book")
    P(t[["panel", "full_CAGR", "full_Sharpe", "full_MaxDD", "full_h1", "full_h2",
         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n(OOS = 2017-01-01.. , the rule-8 evaluation window.  Baseline = LIVE (RULES v2 g0.75); "
      "benchmark = each book's own panel SPY.)")
    return t


def keep_paths(books, meta, panels, starts, bt):
    """Both KEEP paths with the SUB-WINDOW leg read at every swept block length L (P1)."""
    hdr("BOTH KEEP PATHS — the sub-window leg re-read at every swept block length L")
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    lv = bt.loc["LIVE"]
    live_r = books["LIVE"].loc[starts["U56"]:].values
    live_o = books["LIVE"].loc[OOS_START:].values
    out = []
    for key in MEMO12:
        pan = meta[key]["panel"]
        r = bt.loc[key]
        sp = bt.loc[f"SPY_{pan}"]
        f = books[key].loc[starts[pan]:].values
        o = books[key].loc[OOS_START:].values
        sf = pd.Series(spy[pan], index=panels[pan].index).loc[starts[pan]:].values
        so = pd.Series(spy[pan], index=panels[pan].index).loc[OOS_START:].values
        for L in LGRID + [LFULL]:
            LLf = len(f) if L == LFULL else L
            LLo = len(o) if L == LFULL else L
            if LLf > len(f) or LLo > len(o):
                continue
            sub_f = all(sharpe_of(f[i:i + LLf]) > sharpe_of(sf[i:i + LLf])
                        for i in range(0, len(f) - LLf + 1, LLf))
            sub_o = all(sharpe_of(o[i:i + LLo]) > sharpe_of(so[i:i + LLo])
                        for i in range(0, len(o) - LLo + 1, LLo))
            nf = min(len(live_r), len(f))
            no = min(len(live_o), len(o))
            sub_l = all(sharpe_of(f[-nf:][i:i + LLf]) > sharpe_of(live_r[-nf:][i:i + LLf])
                        for i in range(0, nf - LLf + 1, LLf)) if LLf <= nf else False
            legs4b = {"sub_full": sub_f, "OOSsh>SPY": r.OOS_Sharpe > sp.OOS_Sharpe,
                      "sub_OOS": sub_o,
                      "DD<=60%SPY": r.full_MaxDD >= 0.6 * sp.full_MaxDD,
                      "CAGR>=70%SPY": r.full_CAGR >= 0.7 * sp.full_CAGR,
                      "OOS_DD": r.OOS_MaxDD >= 0.6 * sp.OOS_MaxDD,
                      "OOS_CAGR": r.OOS_CAGR >= 0.7 * sp.OOS_CAGR}
            legs4a = {"sub>LIVE": sub_l, "DD<=LIVE": r.full_MaxDD >= lv.full_MaxDD}
            out.append(dict(book=key, L=LLf, L_months=round(LLf / 21.0, 1), is_full=(L == LFULL),
                            n_blocks_full=len(range(0, len(f) - LLf + 1, LLf)),
                            keep4b="PASS" if all(legs4b.values()) else "FAIL",
                            fail4b="+".join(n for n, v in legs4b.items() if not v),
                            keep4a="PASS" if all(legs4a.values()) else "FAIL",
                            fail4a="+".join(n for n, v in legs4a.items() if not v)))
    K = pd.DataFrame(out)
    piv = K.pivot_table(index="book", columns="L_months", values="keep4b",
                        aggfunc="first").reindex(MEMO12)
    P("4b verdict by sub-window block length (columns = block length in months, "
      "the last column is the whole window as one block):")
    P(piv.to_string())
    pv2 = K.pivot_table(index="book", columns="L_months", values="keep4a",
                        aggfunc="first").reindex(MEMO12)
    P("\n4a verdict (vs the LIVE book) by the same block length:")
    P(pv2.to_string())
    for Lm in sorted(K.L_months.unique()):
        s = K[K.L_months == Lm]
        P(f"  block {Lm:6.1f} months: 4b {int((s.keep4b=='PASS').sum())} of {len(s)} PASS, "
          f"4a {int((s.keep4a=='PASS').sum())} of {len(s)} PASS")
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    return K


# ----------------------------------------------------------------- rule 8 on the tuned axes
def rule8(books, meta, panels, starts):
    hdr("RULE 8 (a) — ON THIS RUN'S OWN TUNED AXES (L, null): L chosen on IS blocks only")
    spy = {p: px["SPY"].pct_change().fillna(0.0).values for p, px in panels.items()}
    rows = []
    for key in MEMO12:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key].values, spy[pan]
        n = len(idx)
        for L in LGRID:
            for s0 in block_starts(i0, n, L, HEAD_TILE):
                st, en = idx[s0], idx[s0 + L - 1]
                seg = "IS" if en <= IS_END else ("OOS" if st >= OOS_START else "STRADDLE")
                _, z, _ = memmel(r_all[s0:s0 + L], s_all[s0:s0 + L])
                if np.isfinite(z):
                    rows.append(dict(book=key, L=L, seg=seg, inside=int(abs(z) < ZCRIT)))
    R = pd.DataFrame(rows)
    t = (R.pivot_table(index="L", columns="seg", values="inside", aggfunc=["mean", "count"])
         .sort_index())
    t.columns = ["_".join(map(str, c)) for c in t.columns]
    P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    isr = R[R.seg == "IS"].groupby("L").inside.mean()
    oos = R[R.seg == "OOS"].groupby("L").inside.mean()
    pick = next((int(L) for L in sorted(isr.index) if isr[L] < BAR_INSIDE), None)
    oos_cross = next((int(L) for L in sorted(oos.index) if oos[L] < BAR_INSIDE), None)
    if pick is None:
        P(f"\nNo IS rung crosses {BAR_INSIDE}: the minimum callable length is NOT SELECTABLE "
          f"in sample (IS inside_share min {isr.min():.4f} at L={int(isr.idxmin())}d).")
        gap = np.nan
    else:
        gap = abs(oos.get(pick, np.nan) - isr[pick])
        P(f"\nIS-chosen L* = {pick}d ({pick/21:.1f} months) at IS inside_share {isr[pick]:.4f} "
          f"-> OOS inside_share {oos.get(pick, np.nan):.4f}, read ONCE.  |OOS-IS| = {gap:.4f} "
          f"vs bar 0.10.")
    P(f"OOS crossing rung = {oos_cross}d "
      f"(OOS inside_share min {oos.min():.4f} at L={int(oos.idxmin())}d); the IS pick "
      f"{'IS' if pick == oos_cross else 'is NOT'} the OOS crossing rung.")
    wf = pd.DataFrame(dict(L=sorted(set(isr.index) | set(oos.index)))).set_index("L")
    wf["IS_inside"] = isr
    wf["OOS_inside"] = oos
    wf["n_IS"] = R[R.seg == "IS"].groupby("L").inside.count()
    wf["n_OOS"] = R[R.seg == "OOS"].groupby("L").inside.count()
    wf.to_csv(f"{OUT}.wf.csv")
    return wf, pick, oos_cross, gap


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P(f"# {DATE} lane B — IDEA 838: what is the SHORTEST SUB-WINDOW at which a BOOK-vs-SPY")
    P("#                 SHARPE COMPARISON can be CALLED?")
    P("=" * 112)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C4), {len(v.loc[starts[k]:])} scored days")
    P(f"next-day execution, no shorting, no leverage, {COST} bps.  P1 block length L "
      f"{LGRID} + FULL | P2 null {NULLS}.  Tilings {TILINGS}, claim sets {list(CLAIM_SETS)} and "
      f"costs {COSTS} bps REPORTED, not selected.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-block resolution statement.")

    P("\nbuilding books at the PROTOCOL rung (one full-sample simulation each, C1):")
    books, meta = build(panels, COST, verbose=True)
    _, ok1 = gates_g1g2(books, starts)
    _, ok4 = gate_g4(books)
    G3, ok3 = gate_g3(books, meta, panels, starts)
    _, ok5 = gate_g5(books, meta, panels, starts)

    bt = fixed_window(books, meta, panels, starts)
    bt.to_csv(f"{OUT}.books.csv")

    # ---------------------------------------------------------------- P1 sweep
    hdr("P1 — THE SWEEP: inside_share (the share of UNCALLABLE comparisons) by block length")
    sw = [sweep(books, meta, panels, starts, COST)]
    for c in COSTS:
        if c == COST:
            continue
        P(f"  re-building every book at {c} bps for the reported cost rung ...")
        bk, _ = build(panels, c)
        sw.append(sweep(bk, meta, panels, starts, c))
    S = pd.concat(sw, ignore_index=True)
    S.to_csv(f"{OUT}.sweep.csv", index=False)
    head = S[(S.cost == COST)]
    P(f"{len(S):,} (book, tiling, L, cost) cells; {len(head):,} at the PROTOCOL rung.")

    for tiling in TILINGS:
        P(f"\n--- inside_share, tiling {tiling}, {COST} bps (rows = book, cols = block months) ---")
        sub = head[head.tiling == tiling]
        piv = sub.pivot_table(index="book", columns="L_months", values="inside_share",
                              aggfunc="first").reindex(KEYS)
        P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
        nb = sub.pivot_table(index="book", columns="L_months", values="n_blocks",
                             aggfunc="first").reindex(KEYS)
        P(f"  (block counts: min {int(np.nanmin(nb.values))}, "
          f"max {int(np.nanmax(nb.values))} per cell)")

    P(f"\n--- POOLED over MEMO12 (block-weighted), every tiling and cost rung ---")
    pool = []
    for cost in COSTS:
        for tiling in TILINGS:
            sub = S[(S.cost == cost) & (S.tiling == tiling) & (S.book.isin(MEMO12))]
            for L, g in sub.groupby("L_months"):
                pool.append(dict(cost=cost, tiling=tiling, L_months=L,
                                 L=int(g.L.iloc[0]), n_blocks=int(g.n_blocks.sum()),
                                 inside_share=float((g.inside_share * g.n_blocks).sum()
                                                    / g.n_blocks.sum()),
                                 leg_share=float((g.leg_share * g.n_blocks).sum()
                                                 / g.n_blocks.sum()),
                                 med_absz=float(g.med_absz.median())))
    PL = pd.DataFrame(pool)
    P(PL[PL.cost == COST].pivot_table(index="L_months", columns="tiling", values="inside_share")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n(the same pooled column at 0 and 25 bps, tiling " + HEAD_TILE + ":)")
    P(PL[(PL.cost != COST) & (PL.tiling == HEAD_TILE)]
      .pivot_table(index="L_months", columns="cost", values="inside_share")
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- P2 nulls
    hdr("P2 — THE THREE NULLS side by side (fixed-seed subsample, "
        f"<= {NULL_SAMPLE} blocks per cell, {BOOT_REPS} draws)")
    N = null_sweep(books, meta, panels, starts)
    N.to_csv(f"{OUT}.nulls.csv", index=False)
    for tiling in ["DISJOINT", HEAD_TILE]:
        P(f"\n--- pooled over MEMO12, tiling {tiling} ---")
        sub = N[(N.tiling == tiling) & (N.book.isin(MEMO12))]
        piv = sub.pivot_table(index="L_months", columns="null", values="inside_share",
                              aggfunc=lambda x: np.average(x))
        cnt = sub.pivot_table(index="L_months", columns="null", values="n_blocks", aggfunc="sum")
        P(pd.concat([piv, cnt[["ANALYTIC"]].rename(columns={"ANALYTIC": "n_blocks"})], axis=1)
          .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- the deliverable
    hdr("THE DELIVERABLE — per-book MINIMUM CALLABLE LENGTH L* (smallest swept L with "
        f"inside_share < {BAR_INSIDE})")
    rows = []
    for key in KEYS:
        d = dict(book=key, panel=meta[key]["panel"], full_Sharpe=bt.loc[key, "full_Sharpe"],
                 spy_Sharpe=bt.loc[f"SPY_{meta[key]['panel']}", "full_Sharpe"])
        d["dSharpe_full"] = d["full_Sharpe"] - d["spy_Sharpe"]
        for tiling in TILINGS:
            d[f"Lstar_{tiling}"] = lstar_of(head[(head.book == key) & (head.tiling == tiling)])
        for nm in NULLS:
            sub = N[(N.book == key) & (N.tiling == "DISJOINT") & (N.null == nm)]
            d[f"Lstar_{nm}"] = lstar_of(sub) if len(sub) else np.nan
        # G6 closed form: |z| = 1.96 at T = 1.96^2 * V_1d / d^2, at the cell's MEDIAN block.
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        spy_r = panels[pan]["SPY"].pct_change().fillna(0.0).values
        ds, vs = [], []
        for s0 in block_starts(i0, len(idx), 756, HEAD_TILE):
            dd, _, V = memmel(books[key].values[s0:s0 + 756], spy_r[s0:s0 + 756])
            if np.isfinite(V) and np.isfinite(dd) and dd != 0:
                ds.append(abs(dd))
                vs.append(V)
        if ds:
            d["Lhat_closedform"] = ZCRIT ** 2 * float(np.median(vs)) / float(np.median(ds)) ** 2
        else:
            d["Lhat_closedform"] = np.nan
        rows.append(d)
    D = pd.DataFrame(rows).set_index("book")
    P(D.to_string(float_format=lambda x: f"{x:.1f}" if abs(x) > 3 else f"{x:+.4f}"))
    D.to_csv(f"{OUT}.lstar.csv")

    m12 = D.loc[MEMO12]
    ls = m12[f"Lstar_{HEAD_TILE}"]
    n_cross = int(ls.notna().sum())
    P(f"\nOver the 12 committed 4b passes, tiling {HEAD_TILE}, ANALYTIC null, {COST} bps:")
    P(f"  {n_cross} of 12 books have ANY swept rung with inside_share < {BAR_INSIDE}.")
    if n_cross:
        P(f"  L* min {ls.min():.0f}d ({ls.min()/21:.1f}mo) at {ls.idxmin()}, "
          f"median {ls.median():.0f}d ({ls.median()/21:.1f}mo), "
          f"max {ls.max():.0f}d ({ls.max()/21:.1f}mo) at {ls.idxmax()}; "
          f"max/min ratio {ls.max()/ls.min():.2f}")
    lh = m12.Lhat_closedform
    P(f"  closed-form L_hat (median 756d block): min {lh.min():.0f}d, median {lh.median():.0f}d, "
      f"max {lh.max():.0f}d ({lh.max()/252:.1f} years)")
    P(f"  Spearman(|dSharpe_full|, L*) = "
      f"{m12.dSharpe_full.abs().rank().corr(ls.rank()):+.4f} (n={n_cross}) — L* is a property of "
      f"the SIZE OF THE GAP being tested, not of the calendar.")

    # G6 — swept vs closed form, one rung
    rungs = LGRID
    ok6_rows = []
    for key in MEMO12:
        sv, ch = ls.get(key, np.nan), lh.get(key, np.nan)
        if not np.isfinite(sv) or not np.isfinite(ch):
            ok6_rows.append(dict(book=key, Lstar=sv, Lhat=ch, rung_gap=np.nan, ok=False))
            continue
        nearest = min(rungs + [LGRID[-1]], key=lambda x: abs(x - ch))
        gap = abs(rungs.index(int(sv)) - rungs.index(int(nearest))) if int(sv) in rungs else 99
        ok6_rows.append(dict(book=key, Lstar=sv, Lhat=ch, nearest_rung=nearest, rung_gap=gap,
                             ok=bool(gap <= 1)))
    O6 = pd.DataFrame(ok6_rows)
    defined = O6[np.isfinite(O6.Lstar)]
    ok6 = bool(len(defined)) and bool(defined.ok.all())
    P(f"\nGATE G6 — swept L* vs the closed form it implies, on the {len(defined)} books where L* "
      f"is defined: {int(defined.ok.sum())} of {len(defined)} agree within one rung -> "
      f"{'PASS' if ok6 else 'FAIL'}")
    P(O6.to_string(index=False, float_format=lambda x: f"{x:.1f}"))

    K = keep_paths(books, meta, panels, starts, bt)
    wf, pick, oos_cross, wf_gap = rule8(books, meta, panels, starts)

    # ---------------------------------------------------------------- hypotheses
    hdr("PRE-REGISTERED HYPOTHESES")
    verd = {}
    ph = PL[(PL.cost == COST) & (PL.tiling == HEAD_TILE)].sort_values("L")
    cross_pool = ph[ph.inside_share < BAR_INSIDE]
    verd["H_CROSS"] = (len(cross_pool) > 0,
                       (f"pooled MEMO12 inside_share crosses {BAR_INSIDE} at "
                        f"L={int(cross_pool.L.iloc[0])}d ({cross_pool.L_months.iloc[0]:.1f}mo)"
                        if len(cross_pool) else
                        f"pooled MEMO12 inside_share NEVER drops below {BAR_INSIDE}: min "
                        f"{ph.inside_share.min():.4f} at L={int(ph.L.iloc[ph.inside_share.argmin()])}d "
                        f"({ph.L_months.iloc[ph.inside_share.argmin()]:.1f}mo, the full sample)"))
    ratio = (ls.max() / ls.min()) if n_cross == len(m12) else np.inf
    verd["H_CONST"] = (np.isfinite(ratio) and ratio <= 2.0,
                       f"L* defined at {n_cross} of 12 books; max/min ratio "
                       f"{'inf (undefined at >=1 book)' if not np.isfinite(ratio) else f'{ratio:.2f}'} "
                       f"vs bar 2.0")
    monob = 0
    for key in MEMO12:
        s = head[(head.book == key) & (head.tiling == HEAD_TILE)].sort_values("L").inside_share
        monob += int(bool((np.diff(s.values) <= 1e-12).all()))
    verd["H_MONO"] = (monob == len(MEMO12),
                      f"inside_share monotone non-increasing in L at {monob} of {len(MEMO12)} books")
    agree = 0
    for key in MEMO12:
        vals = [lstar_of(N[(N.book == key) & (N.tiling == "DISJOINT") & (N.null == nm)])
                for nm in NULLS]
        idxs = []
        for v in vals:
            idxs.append(LGRID.index(int(v)) if np.isfinite(v) and int(v) in LGRID
                        else (len(LGRID) if not np.isfinite(v) else len(LGRID)))
        agree += int(max(idxs) - min(idxs) <= 1)
    verd["H_NULL"] = (agree == len(MEMO12),
                      f"the three nulls give L* within one rung at {agree} of {len(MEMO12)} books")
    tile_ok = 0
    for key in MEMO12:
        a = lstar_of(head[(head.book == key) & (head.tiling == HEAD_TILE)])
        b = lstar_of(head[(head.book == key) & (head.tiling == "DISJOINT")])
        ia = LGRID.index(int(a)) if np.isfinite(a) and int(a) in LGRID else len(LGRID)
        ib = LGRID.index(int(b)) if np.isfinite(b) and int(b) in LGRID else len(LGRID)
        tile_ok += int(abs(ia - ib) <= 1)
    verd["H_TILE"] = (tile_ok == len(MEMO12),
                      f"OVERLAP21 and DISJOINT give L* within one rung at {tile_ok} of "
                      f"{len(MEMO12)} books")
    verd["H_WF"] = (pick is not None and pick == oos_cross and np.isfinite(wf_gap)
                    and wf_gap <= 0.10,
                    f"IS-chosen L* = {pick}, OOS crossing rung = {oos_cross}, |OOS-IS| = "
                    f"{wf_gap if np.isfinite(wf_gap) else float('nan'):.4f} vs bar 0.10")
    for k, (ok, why) in verd.items():
        P(f"  {k:9s} {'PASS' if ok else 'FAIL'}  — {why}")
    P(f"\n{sum(1 for v in verd.values() if v[0])} of {len(verd)} pre-registered hypotheses PASS.")
    P(f"GATES: G1/G2 {'PASS' if ok1 else 'FAIL'}, G3 {'PASS' if ok3 else 'FAIL'}, "
      f"G4 {'PASS' if ok4 else 'FAIL'}, G5 {'PASS' if ok5 else 'FAIL'}, "
      f"G6 {'PASS' if ok6 else 'FAIL'}")

    hdr("PROTOCOL rule 3 — baseline.compare on the two books this run would have to defend")
    for key in ["K4", "K5"]:
        P(f"\n--- {key}: {meta[key]['label']} ---")
        res = compare(f"838 B {key} {meta[key]['label']}", WFUN[key], panels[meta[key]["panel"]],
                      freq=FREQ[key], cost_bps=COST)
        LOG.append(str(res["table"]))

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return S, N, D, K, wf, verd


if __name__ == "__main__":
    main()
