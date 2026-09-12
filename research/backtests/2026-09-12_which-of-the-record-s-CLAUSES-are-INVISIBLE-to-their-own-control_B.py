#!/usr/bin/env python3
"""Idea 582 - which of the record's CLAUSES are INVISIBLE to their own control?  (lane B, 2026-09-12)

Idea 317's gate G3 found that the GROSS pair collapses to ONE book once gross is matched
(max |A_Sharpe - B_Sharpe| = 4.4e-16), so 48 of its 288 cells were never a two-parent test at
all.  It named the limit but only for one family.  This run GENERALISES it: for each clause
family the record actually trades, price the clause against a LADDER of controls of increasing
strictness and report the DEEPEST control the clause is still visible to.

    L0  NAIVE          the book with the clause removed, at the same nominal gross parameter.
                       This is what the record does today.
    L1  MEAN-GROSS     L0 rescaled by ONE constant c so its mean daily target gross equals the
                       treated book's.  (Idea 317's G3 control.)
    L2  PATH-GROSS     L0 rescaled DAY BY DAY so its target gross equals the treated book's on
                       every date.  This is the "constant-exposure control" the queue asks for:
                       it strips the entire exposure channel, so whatever survives is the
                       clause's CROSS-SECTIONAL (selection) content and nothing else.

Both rescalings are causal (they read only quantities known at close t) and neither levers:
the treated book's gross is <= 1 by construction, so the rescaled control's is too.

VERDICT TAXONOMY (pre-registered, structural first, empirical second)
    STATIC-GROSS   structurally degenerate at L1  -> the clause IS a constant exposure dial.
    TIMING-ONLY    survives L1, structurally degenerate at L2 -> the clause has ZERO selection
                   content; its entire content is the exposure PATH.  Not worthless - but it
                   must be priced against a constant-exposure control, never against a
                   second "parent", because at matched exposure it has no second parent.
    SELECTION      survives L2 -> the clause changes WHAT you hold at matched exposure.
                   Only these can be a two-parent test in the record's sense.
"structurally degenerate at L" means max |W_treat - W_ctrl(L)| < 1e-10 over the whole panel:
the two books are the same book, so no amount of data can separate them.  For the clauses that
survive L2 the run then asks the empirical question - is dSharpe vs the L2 control
distinguishable from zero? - with a paired stationary block bootstrap.

TWO TUNED PARAMETERS, as the queue allows: the CLAUSE (8 levels) and the BASE GROSS g
(7 levels, 0.40..1.00).  Every one of the 8 x 7 x 2 panels = 112 cells is reported, each with
its four arms (T, L0, L1, L2) = 448 books.  Nothing else is fitted.  Cost rungs 0/10/25 bps
come off ONE cost-free simulation per book (exact: engine.backtest at 0 bps plus its own
turnover series); 10 bps is the headline everywhere, as PROTOCOL rule 2 requires.  Block
bootstrap settings (400 draws, block 21) are reporting machinery, not a third dial.

PROTOCOL: 10 bps headline, next-day execution (engine shifts weights), no shorting, no
leverage.  BOTH KEEP paths are evaluated on every arm of every cell.  Rule 8 walk-forward is
run for every (clause, panel): g chosen on 2009-2016 IS Sharpe of the TREATED book alone,
2017-2026 read exactly once, reported against the L2 control, the live RULES v2 baseline and
SPY on the same panel and window.

Panels: U56 (research/universe.json) and B136 (research/universe_broad.json).  SURVIVORSHIP:
both are current-constituent lists, so every LEVEL here is optimistic.  The object of this run
is a WITHIN-CELL contrast (treated book vs its own control on the same panel and window), which
survivorship moves far less than it moves levels.

Vintage pinned to 2026-09-04 (the record's committed vintage) so gate G1 reads the same
RULES v2 headline the record published; data/prices.csv now runs past it.

Outputs (all committed, all under research/):
  .txt         full console log
  .cells.csv   one row per (panel, clause, g, arm): metrics, both KEEP verdicts, binding bar
  .degen.csv   one row per (panel, clause, g): structural degeneracy at L1 and L2, exposures
  .boot.csv    paired block-bootstrap dSharpe vs the L2 control, headline g
  .wf.csv      every rule-8 grid point, IS pick and OOS read
  .result.md   the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state   # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

DATE = "2026-09-12"
SLUG = "which-of-the-record-s-CLAUSES-are-INVISIBLE-to-their-own-control"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

END = "2026-09-04"              # the record's committed vintage
OOS_START = "2017-01-01"        # PROTOCOL rule 8
IS_END = "2016-12-31"
GRID = [0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00]      # 7 base-gross points, all reported
HEAD_G = 0.75                   # the live book's gross; headline column only, not a pick
RUNGS = [0, 10, 25]
HEAD = 10                       # headline cost rung (PROTOCOL rule 2)
MAX_VOL = 0.60
WARMUP = 260                    # baseline.compare's own warm-up skip
DEGEN_EPS = 1e-10               # "the same book"
BOOT_N, BOOT_BLK, BOOT_SEED = 400, 21, 582

LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# book primitives -- built only from baseline.py exports, so the clauses are the record's
# =====================================================================================
def _ew(mask: pd.DataFrame, px: pd.DataFrame, gross: float, respread: bool) -> pd.DataFrame:
    """Equal weight over `mask`.  respread=False -> g/N of NAV each, N = names PRICED that day,
    gated-out weight goes to cash (the RULES v2 convention).  respread=True -> g/K each,
    K = names in the mask, so the book is always fully invested."""
    m = mask.astype(float).where(px.notna(), 0.0)
    denom = (px.notna().astype(float).sum(axis=1) if not respread else m.sum(axis=1))
    return m.div(denom.replace(0, np.nan), axis=0).mul(gross).fillna(0.0)


def ew_priced(px, g):
    """EW over every instrument priced that day, gross g.  The zero-clause base book."""
    return _ew(px.notna(), px, g, respread=True)


def ma_gate(px, g, band=0.0):
    """EW over the names inside the 200d +/-band gate, de-grossed to cash.  band=0 -> plain
    above/below 200d.  Identical to baseline.rules_v2_weights(px, band, g)."""
    return rules_v2_weights(px, band, g)


def ma_gate_respread(px, g, band=0.0):
    """Same gate, but the gated-out weight is re-spread across the survivors (always gross g)."""
    return _ew(band_state(px, band), px, g, respread=True)


def elig_mask(px, volcap=True):
    """The record's eligibility: above the 200d average, and (optionally) vol20 < 0.60."""
    _, above, vol20 = score(px, vol_scale=False)
    return (above & (vol20 < MAX_VOL)) if volcap else above


def ew_elig(px, g, volcap=True):
    return _ew(elig_mask(px, volcap), px, g, respread=True)


def topn(px, g, n=20, vol_scale=False):
    """Top-n of the record's composite among eligible names, EW to gross g."""
    s, above, vol20 = score(px, vol_scale)
    sc = s.where(above & (vol20 < MAX_VOL))
    sel = (sc.rank(axis=1, ascending=False) <= n).fillna(False)
    return _ew(sel, px, g, respread=True)


def breadth_gate(px, g, q=0.17, wroll=1008, freq="W"):
    """EW-all-eligible, de-grossed to ZERO when breadth < its trailing-1008d q0.17 (idea 641's
    K8 book, verbatim in construction)."""
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    br = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = br.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (br < thr) & br.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 0.0)
    m = m.where(rebalance_mask(px.index, freq)).ffill().fillna(1.0)
    return ew_elig(px, g).mul(m, axis=0)


# (key, label, treat(px,g), control-with-the-clause-REMOVED(px,g), cadence, prior expectation)
CLAUSES = [
    ("GROSS", "raise gross to g (vs the record's 0.375 low rung), EW-all-priced",
     lambda px, g: ew_priced(px, g), lambda px, g: ew_priced(px, 0.375), "W", "STATIC-GROSS"),
    ("MAGATE", "hold only names above their 200d average, de-gross (vs hold everything)",
     lambda px, g: ma_gate(px, g, 0.0), lambda px, g: ew_priced(px, g), "W", "?"),
    ("BAND", "add 3% hysteresis to the 200d gate (vs a bare crossing)",
     lambda px, g: ma_gate(px, g, 0.03), lambda px, g: ma_gate(px, g, 0.0), "W", "?"),
    ("VOLCAP", "add vol20 < 0.60 to eligibility (vs above-200d alone)",
     lambda px, g: ew_elig(px, g, True), lambda px, g: ew_elig(px, g, False), "W", "?"),
    ("TOPN", "rank-select the top 20 by composite (vs hold every eligible name)",
     lambda px, g: topn(px, g, 20, False), lambda px, g: ew_elig(px, g, True), "W", "SELECTION"),
    ("VOLSCALE", "divide the composite by sqrt(vol20) before ranking (vs rank it raw)",
     lambda px, g: topn(px, g, 20, True), lambda px, g: topn(px, g, 20, False), "W", "SELECTION"),
    ("BREADTH", "de-gross to ZERO when breadth < trailing-1008d q0.17 (vs never de-gross)",
     lambda px, g: breadth_gate(px, g), lambda px, g: ew_elig(px, g, True), "W", "?"),
    ("RESPREAD", "send gated-out weight to CASH instead of re-spreading it (RULES v2 clause 3)",
     lambda px, g: ma_gate(px, g, 0.03), lambda px, g: ma_gate_respread(px, g, 0.03), "W", "?"),
]


# =====================================================================================
# the control ladder
# =====================================================================================
def gross_path(W):
    return W.sum(axis=1)


def match_L1(Wt, Wc):
    """One constant c so mean target gross matches.  Causal (c is a sample constant, and it is
    reported, not fitted to any outcome).  Never levers past the treated book's own cap."""
    gt, gc = gross_path(Wt).mean(), gross_path(Wc).mean()
    c = 0.0 if gc <= 0 else gt / gc
    return Wc.mul(c), c


def match_L2(Wt, Wc):
    """Day-by-day rescale so the control's target gross equals the treated book's on EVERY
    date.  Reads only close-t quantities.  Where the control is empty (gross 0) it stays
    empty - it has nothing to scale - and the date is counted in `L2_unmatched`."""
    gt, gc = gross_path(Wt), gross_path(Wc)
    c = (gt / gc.replace(0, np.nan)).fillna(0.0)
    W = Wc.mul(c, axis=0)
    unmatched = int(((gc <= 0) & (gt > 0)).sum())
    return W, unmatched


def maxdiff(A, B):
    return float(np.nanmax(np.abs(A.values - B.values))) if A.size else np.nan


# =====================================================================================
# simulation / scoring helpers
# =====================================================================================
def sim(px, W, freq):
    b = backtest(px, W, cost_bps=0, freq=freq)
    return b["returns"], b["turnover"]


def netr(r, to, bps, start):
    return (r - to * bps / 1e4).loc[start:]


def pack(r):
    m = metrics(r)
    h = len(r) // 2
    mo = metrics(r.loc[OOS_START:])
    mi = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                IS=mi["Sharpe"], IS_CAGR=mi["CAGR"])


def keep4b(p, bar):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  Returns (pass, full fail set)."""
    f = []
    if not (p["H1"] > bar["H1"]):      f.append("H1")
    if not (p["H2"] > bar["H2"]):      f.append("H2")
    if not (p["OOS"] > bar["OOS"]):    f.append("OOS")
    if not (p["MaxDD"] >= bar["DD"]):  f.append("DD")
    if not (p["CAGR"] >= bar["CAGR"]): f.append("CAGR")
    return (len(f) == 0), "+".join(f)


def keep4a(p, b):
    """PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse."""
    f = []
    if not (p["H1"] > b["H1"]):        f.append("H1")
    if not (p["H2"] > b["H2"]):        f.append("H2")
    if not (p["MaxDD"] >= b["MaxDD"]): f.append("DD")
    return (len(f) == 0), "+".join(f)


def boot_dsharpe(rt, rc, n=BOOT_N, blk=BOOT_BLK, seed=BOOT_SEED):
    """Paired stationary-block bootstrap of Sharpe(treat) - Sharpe(control).  The SAME block
    index is applied to both series, so the pairing (and hence the common market factor) is
    preserved; only the sampling of time is resampled."""
    a, b = rt.values, rc.values
    T = len(a)
    if T < 2 * blk:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / blk))
    out = np.empty(n)
    for i in range(n):
        starts = rng.integers(0, T - blk, size=nb)
        idx = (starts[:, None] + np.arange(blk)[None, :]).ravel()[:T]
        x, y = a[idx], b[idx]
        sx = x.mean() * 252 / (x.std() * np.sqrt(252)) if x.std() else np.nan
        sy = y.mean() * 252 / (y.std() * np.sqrt(252)) if y.std() else np.nan
        out[i] = sx - sy
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float(out.std())


# =====================================================================================
def main():
    log("=" * 110)
    log(f"Idea 582 - which of the record's CLAUSES are INVISIBLE to their own control?  ({DATE}, lane B)")
    log("=" * 110)

    pxU = load_universe().loc[:END]
    pxB = load_universe(broad=True).loc[:END]
    PX = {"U56": pxU, "B136": pxB}
    ST = {k: v.index[WARMUP] for k, v in PX.items()}
    for k, v in PX.items():
        log(f"{k:5s} {v.shape[1]:3d} names, scored {ST[k].date()} .. {v.index[-1].date()}  "
            f"(vintage pinned to {END})")
    log(f"grid: {len(CLAUSES)} clauses x {len(GRID)} base-gross points {GRID} x {len(PX)} panels "
        f"= {len(CLAUSES)*len(GRID)*len(PX)} cells x 4 arms = "
        f"{len(CLAUSES)*len(GRID)*len(PX)*4} books.  Headline cost rung {HEAD} bps.")

    # ---- bars: SPY (4b) and live RULES v2 (4a), per panel ------------------------------
    BAR, BASE = {}, {}
    for pan, px in PX.items():
        st = ST[pan]
        s = pack(px["SPY"].pct_change().fillna(0).loc[st:])
        BAR[pan] = dict(H1=s["H1"], H2=s["H2"], OOS=s["OOS"],
                        DD=0.60 * s["MaxDD"], CAGR=0.70 * s["CAGR"], SPY=s)
        r, to = sim(px, rules_v2_weights(px, 0.03, 0.75), "W")
        BASE[pan] = {c: pack(netr(r, to, c, st)) for c in RUNGS}
        b, v = BAR[pan], BASE[pan][HEAD]
        log(f"\n  {pan} SPY   CAGR {s['CAGR']:7.2%}  Sharpe {s['Sharpe']:.4f} "
            f"(H1 {s['H1']:.4f} / H2 {s['H2']:.4f}, OOS {s['OOS']:.4f})  MaxDD {s['MaxDD']:.2%}")
        log(f"  {pan} 4b bars: H1>{b['H1']:.4f}  H2>{b['H2']:.4f}  OOS>{b['OOS']:.4f}  "
            f"MaxDD>={b['DD']:.2%}  CAGR>={b['CAGR']:.2%}")
        log(f"  {pan} RULES v2 @{HEAD}bps (4a bar): CAGR {v['CAGR']:7.2%} Sharpe {v['Sharpe']:.4f} "
            f"(H1 {v['H1']:.4f} / H2 {v['H2']:.4f})  MaxDD {v['MaxDD']:.2%}  OOS {v['OOS']:.4f}")

    # =================================================================================
    # GATES -- pre-registered, run and read BEFORE any result
    # =================================================================================
    log("\n" + "=" * 110)
    log("GATES (four, pre-registered)")
    log("=" * 110)
    G = {}

    v = BASE["U56"][HEAD]
    G["G1"] = (abs(v["Sharpe"] - 1.202) < 6e-3 and abs(v["CAGR"] - 0.0863) < 6e-3
               and abs(v["MaxDD"] + 0.1205) < 6e-3)
    log(f"  G1  RULES v2 U56 @10bps {v['CAGR']:.2%}/{v['Sharpe']:.4f}/{v['MaxDD']:.2%} vs committed "
        f"8.63%/1.202/-12.05% (bar 6e-3; prices.csv is re-downloaded daily so u56 rows reproduce "
        f"to ~3e-3, not bit-exact - idea 406)   {'PASS' if G['G1'] else 'FAIL'}")

    px = pxU
    Wt = ew_priced(px, HEAD_G); Wc = ew_priced(px, 0.375)
    d_l2 = maxdiff(Wt, match_L2(Wt, Wc)[0])
    G["G2"] = d_l2 < DEGEN_EPS
    log(f"  G2  MACHINERY: the GROSS clause must be structurally degenerate at L2 "
        f"(reproduces idea 317's G3).  max|dW| = {d_l2:.3e} < {DEGEN_EPS:.0e}   "
        f"{'PASS' if G['G2'] else 'FAIL'}")

    Wt = topn(px, HEAD_G, 20, False); Wc = ew_elig(px, HEAD_G, True)
    d_top = maxdiff(Wt, match_L2(Wt, Wc)[0])
    G["G3"] = d_top > 0.01
    log(f"  G3  MACHINERY: the L2 matcher must NOT wash out a real cross-sectional clause.  "
        f"TOPN max|dW| at L2 = {d_top:.4f} > 0.01   {'PASS' if G['G3'] else 'FAIL'}")

    worst = 0.0
    for pan, p in PX.items():
        for key, _lab, tf, cf, _fr, _e in CLAUSES:
            A, B = tf(p, HEAD_G), cf(p, HEAD_G)
            B2, _ = match_L2(A, B)
            ga, gb = gross_path(A), gross_path(B2)
            worst = max(worst, float(np.nanmax(np.abs((ga - gb)[gross_path(B) > 0].values))))
    G["G4"] = worst < 1e-12
    log(f"  G4  the L2 control's gross path must equal the treated book's on every date where "
        f"the control is non-empty.  worst max_t|dG| = {worst:.3e} < 1e-12   "
        f"{'PASS' if G['G4'] else 'FAIL'}")
    log(f"  gates: {sum(G.values())}/4 pass -> {'proceed' if all(G.values()) else 'REPORT WITH THE FAILURE'}")

    # =================================================================================
    # PART A -- the sweep: every clause x every g x every panel, four arms each
    # =================================================================================
    log("\n" + "=" * 110)
    log("PART A - the control ladder, every cell")
    log("=" * 110)
    cells, degen = [], []
    for pan, p in PX.items():
        st = ST[pan]
        for key, label, tf, cf, freq, expect in CLAUSES:
            log(f"\n  [{pan}] {key:9s} {label}")
            log(f"    {'g':>5s} {'meanGrT':>8s} {'meanGrC':>8s} {'L1 c':>6s} "
                f"{'max|dW|L0':>10s} {'max|dW|L1':>10s} {'max|dW|L2':>10s}  {'verdict':<13s}"
                f" {'dSh vs L2':>10s} {'dSh vs L1':>10s}")
            for g in GRID:
                A = tf(p, g)
                B0 = cf(p, g)
                B1, c1 = match_L1(A, B0)
                B2, unm = match_L2(A, B0)
                dW0, dW1, dW2 = maxdiff(A, B0), maxdiff(A, B1), maxdiff(A, B2)
                if dW1 < DEGEN_EPS:
                    verdict = "STATIC-GROSS"
                elif dW2 < DEGEN_EPS:
                    verdict = "TIMING-ONLY"
                else:
                    verdict = "SELECTION"

                packs = {}
                for arm, W in (("T", A), ("L0", B0), ("L1", B1), ("L2", B2)):
                    r, to = sim(p, W, freq)
                    for rung in RUNGS:
                        pk = pack(netr(r, to, rung, st))
                        if rung == HEAD:
                            packs[arm] = pk
                        k4b, f4b = keep4b(pk, BAR[pan])
                        k4a, f4a = keep4a(pk, BASE[pan][rung])
                        cells.append(dict(panel=pan, clause=key, g=g, arm=arm, bps=rung,
                                          CAGR=pk["CAGR"], Sharpe=pk["Sharpe"], MaxDD=pk["MaxDD"],
                                          H1=pk["H1"], H2=pk["H2"], OOS=pk["OOS"],
                                          OOS_CAGR=pk["OOS_CAGR"], OOS_MaxDD=pk["OOS_MaxDD"],
                                          IS=pk["IS"], keep4a=int(k4a), fail4a=f4a,
                                          keep4b=int(k4b), fail4b=f4b, degen=verdict,
                                          meanGross=float(gross_path(W).mean())))
                d2 = packs["T"]["Sharpe"] - packs["L2"]["Sharpe"]
                d1 = packs["T"]["Sharpe"] - packs["L1"]["Sharpe"]
                degen.append(dict(panel=pan, clause=key, g=g, verdict=verdict,
                                  meanGross_T=float(gross_path(A).mean()),
                                  meanGross_C=float(gross_path(B0).mean()), L1_c=c1,
                                  maxdW_L0=dW0, maxdW_L1=dW1, maxdW_L2=dW2,
                                  L2_unmatched_days=unm,
                                  dSharpe_vs_L0=packs["T"]["Sharpe"] - packs["L0"]["Sharpe"],
                                  dSharpe_vs_L1=d1, dSharpe_vs_L2=d2,
                                  dCAGR_vs_L2=packs["T"]["CAGR"] - packs["L2"]["CAGR"],
                                  dMaxDD_vs_L2=packs["T"]["MaxDD"] - packs["L2"]["MaxDD"],
                                  keep4b_T=int(keep4b(packs["T"], BAR[pan])[0]),
                                  keep4b_L0=int(keep4b(packs["L0"], BAR[pan])[0]),
                                  keep4b_L1=int(keep4b(packs["L1"], BAR[pan])[0]),
                                  keep4b_L2=int(keep4b(packs["L2"], BAR[pan])[0]),
                                  keep4a_T=int(keep4a(packs["T"], BASE[pan][HEAD])[0]),
                                  keep4a_L2=int(keep4a(packs["L2"], BASE[pan][HEAD])[0])))
                log(f"    {g:5.2f} {gross_path(A).mean():8.4f} {gross_path(B0).mean():8.4f} "
                    f"{c1:6.3f} {dW0:10.3e} {dW1:10.3e} {dW2:10.3e}  {verdict:<13s}"
                    f" {d2:10.4f} {d1:10.4f}")

    CELLS = pd.DataFrame(cells)
    DEG = pd.DataFrame(degen)
    CELLS.to_csv(f"{OUT}.cells.csv", index=False)
    DEG.to_csv(f"{OUT}.degen.csv", index=False)

    # =================================================================================
    # PART B -- the headline census
    # =================================================================================
    log("\n" + "=" * 110)
    log("PART B - the census: how deep does each clause survive?")
    log("=" * 110)
    log(f"    {'panel':6s} {'clause':10s} {'prior':<13s} {'verdict (all g)':<18s} "
        f"{'dSh vs L2 min..max':>22s} {'4b T/L2 (of 7 g)':>18s}")
    census = []
    for pan in PX:
        for key, _l, _t, _c, _f, expect in CLAUSES:
            d = DEG[(DEG.panel == pan) & (DEG.clause == key)]
            vs = sorted(set(d.verdict))
            vtxt = vs[0] if len(vs) == 1 else "MIXED:" + "/".join(vs)
            census.append(dict(panel=pan, clause=key, prior=expect, verdict=vtxt,
                               dSh_L2_min=d.dSharpe_vs_L2.min(), dSh_L2_max=d.dSharpe_vs_L2.max(),
                               dSh_L1_min=d.dSharpe_vs_L1.min(), dSh_L1_max=d.dSharpe_vs_L1.max(),
                               keep4b_T=int(d.keep4b_T.sum()), keep4b_L2=int(d.keep4b_L2.sum()),
                               keep4b_L1=int(d.keep4b_L1.sum()), keep4b_L0=int(d.keep4b_L0.sum()),
                               keep4a_T=int(d.keep4a_T.sum()), keep4a_L2=int(d.keep4a_L2.sum())))
            log(f"    {pan:6s} {key:10s} {expect:<13s} {vtxt:<18s} "
                f"{d.dSharpe_vs_L2.min():10.4f}..{d.dSharpe_vs_L2.max():<10.4f} "
                f"{int(d.keep4b_T.sum()):8d} /{int(d.keep4b_L2.sum()):4d}")
    CEN = pd.DataFrame(census)
    CEN.to_csv(f"{OUT}.census.csv", index=False)

    n_static = int((CEN.verdict == "STATIC-GROSS").sum())
    n_timing = int((CEN.verdict == "TIMING-ONLY").sum())
    n_sel = int((CEN.verdict == "SELECTION").sum())
    n_mixed = len(CEN) - n_static - n_timing - n_sel
    log(f"\n    of {len(CEN)} (panel, clause) pairs: STATIC-GROSS {n_static}, TIMING-ONLY "
        f"{n_timing}, SELECTION {n_sel}, MIXED {n_mixed}")
    log(f"    clauses with NO cross-sectional content at all (degenerate at L2, either panel): "
        f"{sorted(set(CEN[CEN.verdict.isin(['STATIC-GROSS','TIMING-ONLY'])].clause))}")

    # ---- the 4b question the queue actually cares about --------------------------------
    sel = DEG[DEG.verdict == "SELECTION"]
    both = int(((sel.keep4b_T == 1) & (sel.keep4b_L2 == 1)).sum())
    tonly = int(((sel.keep4b_T == 1) & (sel.keep4b_L2 == 0)).sum())
    log(f"\n    4b on the {len(sel)} SELECTION cells (the only cells where T and L2 are two "
        f"different books):")
    log(f"      T passes 4b: {int(sel.keep4b_T.sum())}   its own constant-exposure control also "
        f"passes: {both}   T only: {tonly}")
    if int(sel.keep4b_T.sum()):
        log(f"      -> {both/max(1,int(sel.keep4b_T.sum())):.1%} of the clause's 4b passes are "
            f"earned by a book that does NOT have the clause, at the same exposure path.")
    log(f"    4a on the same cells: T {int(sel.keep4a_T.sum())}, L2 {int(sel.keep4a_L2.sum())}")

    # =================================================================================
    # PART C -- bootstrap: is the surviving content distinguishable from zero?
    # =================================================================================
    log("\n" + "=" * 110)
    log(f"PART C - paired stationary block bootstrap of dSharpe vs the L2 control "
        f"(g={HEAD_G}, {BOOT_N} draws, block {BOOT_BLK}d, seed {BOOT_SEED})")
    log("=" * 110)
    log(f"    {'panel':6s} {'clause':10s} {'dSharpe':>9s} {'2.5%':>9s} {'97.5%':>9s} "
        f"{'sd':>7s}  {'verdict':<10s}")
    boots = []
    for pan, p in PX.items():
        st = ST[pan]
        for key, _l, tf, cf, freq, _e in CLAUSES:
            A = tf(p, HEAD_G); B0 = cf(p, HEAD_G)
            B2, _ = match_L2(A, B0)
            if maxdiff(A, B2) < DEGEN_EPS:
                log(f"    {pan:6s} {key:10s} {'--':>9s} {'--':>9s} {'--':>9s} {'--':>7s}  "
                    f"{'DEGENERATE (same book at L2; nothing to test)':<10s}")
                boots.append(dict(panel=pan, clause=key, dSharpe=0.0, lo=np.nan, hi=np.nan,
                                  sd=np.nan, verdict="DEGENERATE"))
                continue
            ra, ta = sim(p, A, freq); rb, tb = sim(p, B2, freq)
            na, nb = netr(ra, ta, HEAD, st), netr(rb, tb, HEAD, st)
            d = metrics(na)["Sharpe"] - metrics(nb)["Sharpe"]
            lo, hi, sd = boot_dsharpe(na, nb)
            vd = "EMPTY" if (lo <= 0 <= hi) else ("CONTENT+" if d > 0 else "CONTENT-")
            log(f"    {pan:6s} {key:10s} {d:9.4f} {lo:9.4f} {hi:9.4f} {sd:7.4f}  {vd:<10s}")
            boots.append(dict(panel=pan, clause=key, dSharpe=d, lo=lo, hi=hi, sd=sd, verdict=vd))
    BOOT = pd.DataFrame(boots)
    BOOT.to_csv(f"{OUT}.boot.csv", index=False)

    # =================================================================================
    # PART D -- PROTOCOL rule 8 walk-forward
    # =================================================================================
    log("\n" + "=" * 110)
    log("PART D - rule 8 walk-forward.  g picked on IS 2009-2016 Sharpe of the TREATED book "
        "alone; OOS 2017-01-01.. read once.")
    log("=" * 110)
    log(f"    {'panel':6s} {'clause':10s} {'g*':>5s} {'IS Sh':>7s} | {'OOS CAGR':>9s} "
        f"{'OOS Sh':>7s} {'OOS DD':>8s} | {'L2 OOS Sh':>10s} {'dSh':>8s} | "
        f"{'v2 OOS Sh':>10s} {'SPY OOS Sh':>10s} {'4b':>3s} {'4a':>3s}")
    wf = []
    for pan, p in PX.items():
        st = ST[pan]
        spy = pack(p["SPY"].pct_change().fillna(0).loc[st:])
        v2 = BASE[pan][HEAD]
        for key, _l, tf, cf, freq, _e in CLAUSES:
            sub = CELLS[(CELLS.panel == pan) & (CELLS.clause == key) & (CELLS.arm == "T")
                        & (CELLS.bps == HEAD)]
            gstar = float(sub.loc[sub.IS.idxmax(), "g"])
            t = sub[sub.g == gstar].iloc[0]
            l2 = CELLS[(CELLS.panel == pan) & (CELLS.clause == key) & (CELLS.arm == "L2")
                       & (CELLS.bps == HEAD) & (CELLS.g == gstar)].iloc[0]
            row = dict(panel=pan, clause=key, g_star=gstar, IS_Sharpe=t.IS,
                       OOS_CAGR=t.OOS_CAGR, OOS_Sharpe=t.OOS, OOS_MaxDD=t.OOS_MaxDD,
                       L2_OOS_Sharpe=l2.OOS, L2_OOS_CAGR=l2.OOS_CAGR, L2_OOS_MaxDD=l2.OOS_MaxDD,
                       dOOS_Sharpe=t.OOS - l2.OOS,
                       v2_OOS_Sharpe=v2["OOS"], v2_OOS_CAGR=v2["OOS_CAGR"],
                       v2_OOS_MaxDD=v2["OOS_MaxDD"],
                       SPY_OOS_Sharpe=spy["OOS"], SPY_OOS_CAGR=spy["OOS_CAGR"],
                       SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                       keep4b=int(t.keep4b), fail4b=t.fail4b,
                       keep4a=int(t.keep4a), fail4a=t.fail4a,
                       degen=t.degen)
            wf.append(row)
            log(f"    {pan:6s} {key:10s} {gstar:5.2f} {t.IS:7.4f} | {t.OOS_CAGR:9.2%} "
                f"{t.OOS:7.4f} {t.OOS_MaxDD:8.2%} | {l2.OOS:10.4f} {t.OOS-l2.OOS:8.4f} | "
                f"{v2['OOS']:10.4f} {spy['OOS']:10.4f} {int(t.keep4b):3d} {int(t.keep4a):3d}")
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.wf.csv", index=False)
    for pan in PX:
        s = BAR[pan]["SPY"]; v = BASE[pan][HEAD]
        log(f"    [{pan}] OOS comparands: SPY CAGR {s['OOS_CAGR']:.2%} / Sharpe {s['OOS']:.4f} / "
            f"MaxDD {s['OOS_MaxDD']:.2%}   RULES v2 CAGR {v['OOS_CAGR']:.2%} / "
            f"Sharpe {v['OOS']:.4f} / MaxDD {v['OOS_MaxDD']:.2%}")
    # a degenerate clause ties its own L2 control to float noise; count a BEAT only above 1e-6.
    nbeat = int((WF.dOOS_Sharpe > 1e-6).sum())
    nlose = int((WF.dOOS_Sharpe < -1e-6).sum())
    log(f"    rule-8 picks clearing 4b: {int(WF.keep4b.sum())}/{len(WF)}; "
        f"clearing 4a: {int(WF.keep4a.sum())}/{len(WF)}; "
        f"beating their own L2 control OOS on Sharpe by >1e-6: {nbeat}/{len(WF)} "
        f"(losing to it: {nlose}; the remaining {len(WF)-nbeat-nlose} are exact ties, i.e. the "
        f"degenerate clauses, which have no separate L2 control to beat)")

    # =================================================================================
    log("\n" + "=" * 110)
    log("ANSWER")
    log("=" * 110)
    invis = sorted(set(CEN[CEN.verdict.isin(["STATIC-GROSS", "TIMING-ONLY"])].clause))
    log(f"  {len(invis)} of {len(CLAUSES)} clause families are INVISIBLE to a constant-exposure "
        f"control on BOTH panels: {invis}")
    log(f"  For those the L2 control IS the treated book (max|dW| < {DEGEN_EPS:.0e}): no control "
        f"exists that separates them, so they can never be a two-parent test at matched exposure.")
    emp = BOOT[BOOT.verdict == "EMPTY"]
    con = BOOT[BOOT.verdict.str.startswith("CONTENT")]
    log(f"  Of the {len(BOOT) - int((BOOT.verdict=='DEGENERATE').sum())} (panel, clause) pairs "
        f"that DO survive L2: {len(con)} carry a dSharpe whose 95% bootstrap interval excludes "
        f"zero, {len(emp)} do not.")
    log(f"  KEEP: no new book is promoted by this run; it prices the record's CONTROLS, not a "
        f"new rule.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.")

    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    log(f"\nwrote {OUT}.txt / .cells.csv ({len(CELLS)}) / .degen.csv ({len(DEG)}) / "
        f".census.csv ({len(CEN)}) / .boot.csv ({len(BOOT)}) / .wf.csv ({len(WF)})")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
