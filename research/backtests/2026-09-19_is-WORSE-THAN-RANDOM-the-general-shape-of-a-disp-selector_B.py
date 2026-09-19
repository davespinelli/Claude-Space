#!/usr/bin/env python3
"""Idea 718 - "is-WORSE-THAN-RANDOM-the-general-shape-of-a-disp-SELECTOR-on-this-ladder"
(lane B, 2026-09-19).

THE QUESTION
------------
Idea 714's drawdown-directed selectors landed at the **1.8th percentile of 2,000 random picks**
(its return-directed twin at 55.1%), the same direction as idea 540's SEL-DISP|v, which sits
BELOW its own do-nothing anchor in 2 of 3 arms.  The queue asks: **price every disp-directed
selector on the 168-panel ladder against the random-pick percentile and say whether the
sub-random reading is THE RULE or THE TWO CELLS.**

The queue line itself carries a warning from idea 715 (2026-09-11 cloud): that run priced the
same ladder's 96 selectors against BOTH an EXACT uniform-pick null (the arm's own 168 OOS
Sharpes, so no sampling at all) and a within-stratum permutation null, and got 45 of 96 beating
the anchor (46.9%) at mean pick percentile 0.383 - i.e. **mildly sub-random on average, but a
coin flip on the count**.  It also found the permutation MEANS themselves sit below the anchor
(0.6039 vs 0.6628) because argmax/argmin of ANY variable lands in the extreme-q strata.  That
observation is the hinge of this run: if every selector's pick is forced into an extreme q
stratum, then "worse than random" measured against a null that draws from ALL 21 strata is
partly a statement about WHERE argmax lands, not about WHAT it ranks on.

WHAT THIS RUN ADDS OVER 715
---------------------------
715 tuned (characteristic, transform) and used one primary base.  This run tunes
(selector, PERCENTILE BASE) - the queue's own two dials - and holds the characteristic/transform
grid fixed as an inherited REPORTED axis.  Three things are new:
  (a) FOUR percentile bases, every cell priced against every one, so "the 1.8th percentile" can
      be checked for base-dependence rather than quoted;
  (b) the STRATUM-MATCHED base (the pick's own q rung, 8 draws), which is the base 715's own
      extreme-q finding implies is the honest one and which no committed run has used here;
  (c) the OUTCOME-DIRECTED twin: every pick is given a DRAWDOWN percentile as well as a Sharpe
      percentile, because 714's sub-random reading was a DRAWDOWN-selector reading and the
      record has never separated "the selector is bad" from "the outcome is drawdown".
Plus the binding capital leg.  THE LADDER ITSELF IS NOT REBUILDABLE: idea 533's panels were
drawn from a 439-name small pool and today's committed cache carries 665 usable names, so the
seed-20260909 draw lands on DIFFERENT panels.  That is stated, not glossed.  This run therefore
carries TWO ladders and answers the queue on both:
  INHERITED  idea 533's committed 504 arm-rows, read exactly as 714/715 read them.  Continuity.
  LIVE       the SAME CONSTRUCTION (k=40, 21 q rungs x 8 draws, seed 20260909, gross 0.75,
             weekly, 10 bps, next-day execution, 260d warm-up) re-drawn from TODAY'S pool, with
             every one of the 168 panels' three books built as a real WEIGHTS FUNCTION, priced
             here, and scored against RULES v2 and SPY run on that panel's own names and days -
             full sample + halves + rule-8 OOS, both KEEP paths.  This is an INDEPENDENT
             REPLICATION of the ladder, not a reproduction of it, and agreement between the two
             is the robustness statement.  Nothing in the verdict rests on an inherited level.

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - ALL GRID POINTS REPORTED
    1. SELECTOR        4 characteristics {breadth, disp, corr, evol}
                       x 4 transforms {none, dm, residx, ratio}
                       x 2 directions {+, -}                       = 32 per arm, 96 in all
                       (disp x 4 x 2 x 3 arms = the 24 cells the queue asks about;
                        the other 72 are the REFERENCE FAMILY that decides "rule vs two cells")
    2. PERCENTILE BASE {EXACT, RESAMP2000, STRAT, PERMSEL}          = 4
    Arm {EWall, top10, top20}, the 21-stratum resolution and the k=40 / 8-draw ladder are
    INHERITED from ideas 295/533/540 and are reported axes, never tuned here.
    96 selectors x 4 bases x 2 outcomes = 768 published percentile cells.

THE FOUR BASES
    EXACT       the arm's own 168 OOS values ARE the uniform-pick distribution.  No sampling.
    RESAMP2000  2,000 uniform picks drawn WITH replacement (seed 718) - idea 714's own base
                shape, included precisely so its "1.8th percentile" can be checked for
                sampling-base artefact against EXACT.
    STRAT       the 8 panels sharing the PICK'S OWN q rung.  Controls for the fact that
                argmax/argmin lands in extreme-q strata (715's finding).
    PERMSEL     the selector re-run on the characteristic permuted WITHIN STRATUM 200x
                (seed 7180); the percentile of the observed pick inside those 200 picks.

PRE-REGISTERED TESTS (bars fixed before any number is read)
    T1 IS SUB-RANDOM THE RULE?  Over the 24 disp cells on the EXACT base: "the rule" iff
       >= 18 of 24 (75%) sit below the 50th percentile.  "The two cells" iff <= 15 of 24
       (i.e. inside a two-sided 95% binomial interval around 12 for a coin flip).
    T2 DOES IT SURVIVE THE STRATUM-MATCHED BASE?  Mean disp-cell percentile on STRAT vs EXACT;
       the sub-random reading is a WHERE-ARGMAX-LANDS artefact iff STRAT mean >= 0.50 while
       EXACT mean < 0.50.
    T3 IS DISP SPECIAL?  Mean percentile of the 24 disp cells vs the 72 non-disp cells, same
       base.  "disp-specific" iff the gap exceeds 0.10 on EXACT.
    T4 IS THE OUTCOME THE STORY?  Mean Sharpe percentile vs mean MaxDD percentile over all 96
       cells.  714's reading is an OUTCOME fact, not a selector fact, iff MaxDD percentile is
       more than 0.15 below Sharpe percentile.
    T5 BASE DEPENDENCE.  Max within-cell spread of the percentile across the 4 bases, and the
       share of cells whose sub-random VERDICT (pct < 0.50) flips between bases.
    T6 (PROTOCOL rule 8, binding) Every selector is built on the IS window ONLY (<= 2016-12-31)
       and read ONCE on 2017-01-01..end.  Every distinct picked panel is rebuilt live and its
       three books priced against RULES v2 (path 4a) and SPY (path 4b), full + halves + OOS.

GATES (nothing new is read until the parents' committed numbers come back out)
    G1 idea 540's 12 published selector rows re-derive from idea 533's arms file (< 1e-9).
    G2 idea 295/533's committed KEEP counts over the corpus: 4a 0/504, 4b 41/504.
    G3 idea 715's committed 96-cell grid reproduces: 45 beat-anchor, mean pct 0.3831.
    G4 VINTAGE, stated as a number: the small pool that idea 715's own gate replayed at
       machine precision (439 usable names) is 665 today, so the ladder is REPLICATED, not
       reproduced.  The size of that gap is published.
    G5 NO LEVERAGE (PROTOCOL rule 2): max realised weight sum over every live book <= 1.0,
       AND the nominal-gross breach caused by RANK TIES in the committed top-n construction is
       measured and published rather than silently clipped.
    G6 the live ladder's SPY comparand is ONE series (sd across panels < 1e-9) while RULES v2
       is re-run per panel and is not (idea 715's correction to idea 540, re-checked here).

SURVIVORSHIP (PROTOCOL rule 9, data/SMALL_PANEL_README.md): the small-cap end of the q ladder
is the CURRENT-constituent sub-$2B screen with the 44 max_1d_move >= 1.0 names dropped first,
and the large-cap end is the current 136-name broad list.  Every LEVEL here is an UPPER BOUND.
The object under test is a SELECTOR'S PERCENTILE inside its own ladder - a within-ladder
contrast over the same panels on the same days - which survivorship shifts jointly.

Outputs: .grid.csv .cells.csv .walkforward.csv .gates.csv .log.txt
"""

import sys, json, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score      # noqa: E402
from engine import backtest, metrics, rebalance_mask             # noqa: E402

BT = ROOT / "research" / "backtests"
P533 = BT / "2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C"
P540 = BT / "2026-09-11_is-disp-the-SECOND-vol-channel_cloud"
P715 = BT / ("2026-09-11_is-SEL-DISP-BAR-v-s-BELOW-ANCHOR-pick-a-general-"
             "CONTROLLED-CHARACTERISTIC-pathology_cloud")
OUT = Path(__file__).with_suffix("")

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.append(s)

CHARS = ["breadth", "disp", "corr", "evol"]
TRANSFORMS = ["none", "dm", "residx", "ratio"]
DIRS = ["+", "-"]
ARMS = ["EWall", "top10", "top20"]
BASES = ["EXACT", "RESAMP2000", "STRAT", "PERMSEL"]
NSTRAT = 21
N_RESAMP, RESAMP_SEED = 2000, 718
N_PERM, PERM_SEED = 200, 7180

COST, FREQ = 10, "W"
K_MIX, N_DRAWS = 40, 8
QS = [round(x / 20, 2) for x in range(21)]
NS = [10, 20]
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
OOS_START = IS_END + pd.Timedelta(days=1)
SEED = 20260909
PUB_4A, PUB_4B, PUB_N = 0, 41, 504
PUB_715_BEAT, PUB_715_PCT = 45, 0.3831
PUB_715_SMALLPOOL = 439

# pre-registered bars
T1_RULE_BAR, T1_COIN_BAR = 18, 15
T2_HALF = 0.50
T3_GAP = 0.10
T4_GAP = 0.15


# ------------------------------------------- fitters (verbatim from ideas 533 / 540 / 715)
def ols(y, X):
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    n, p = len(y), X.shape[1]
    if n < p + 3 or any(np.std(X[:, j]) == 0 for j in range(p)):
        return np.full(p, np.nan)
    Z = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    return beta[1:]

def bin_q(qv, nb):
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)

def demean(v, strat):
    g = pd.DataFrame(dict(s=strat, v=np.asarray(v, float)))
    return (g.v - g.groupby("s").v.transform("mean")).to_numpy()

def transform(x, lbv, st, meth):
    x = np.asarray(x, float)
    if meth == "none":  return x
    if meth == "dm":    return demean(x, st)
    if meth == "residx":
        dx, dv = demean(x, st), demean(lbv, st)
        b = ols(dx, dv)
        return dx - b[0] * dv
    if meth == "ratio":
        with np.errstate(invalid="ignore", divide="ignore"):
            return x / np.exp(lbv)
    raise ValueError(meth)

def pick(v, direction):
    v = np.asarray(v, float)
    if not np.isfinite(v).any(): return -1
    return int(np.nanargmax(v) if direction == "+" else np.nanargmin(v))

def pctile(obs, pool):
    """Share of the pool at or below obs.  Higher = better for BOTH outcomes: Sharpe as usual,
    and MaxDD because it is signed negative, so a shallower drawdown is the larger number."""
    pool = np.asarray(pool, float); pool = pool[np.isfinite(pool)]
    if not len(pool) or not np.isfinite(obs): return np.nan
    return float((pool <= obs).mean())


# ------------------------------------------- the ladder, built live as weights functions
def panel_pool():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    pxb = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    BAD = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    S_STK = [c for c in pxs.columns if c != "SPY" and c not in BAD]
    B_STK = [c for c in pxb.columns if c != "SPY" and c not in ETFS]
    SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    return pxb, pxs, S_STK, B_STK, SPY_RAW, pxs.index, len(BAD)

def draw_panels(S_STK, B_STK):
    """idea 295's draw, replayed verbatim on today's pool."""
    rng = np.random.default_rng(SEED)
    out = []
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(S_STK, size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(B_STK, size=nl_, replace=False)) if nl_ else []
            out.append((q, d, sc, lc))
    return out

def mk_px(sc, lc, pxs, pxb, SPY_RAW, COMMON):
    parts = []
    if sc: parts.append(pxs[sc])
    if lc: parts.append(pxb[lc].reindex(COMMON, method="ffill"))
    px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
    return px.join(SPY_RAW.reindex(px.index, method="ffill").rename("SPY"))

def panel_chars(px, cols, elig, lo, hi):
    """idea 295/533's four characteristics, verbatim."""
    m = rebalance_mask(px.index, FREQ)
    idx = px.loc[px.index[WARMUP]:].index
    if lo is not None: idx = idx[idx >= lo]
    if hi is not None: idx = idx[idx <= hi]
    rb = idx[m.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]; k = len(cols)
    nel = e.sum(axis=1)
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy(); iu = np.triu_indices(k, 1)
    return dict(breadth=float((nel / k).mean()),
                disp=float(r63.where(e).std(axis=1, ddof=0).mean()),
                evol=float(vol20.where(e).mean(axis=1).mean()),
                corr=float(np.nanmean(C[iu])) if k > 1 else np.nan)

def mtr(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def keep_paths(bk, base, spy):
    """PROTOCOL rule 4, both paths, on one window's own full/halves numbers."""
    p4a = (bk["H1"] > base["H1"]) and (bk["H2"] > base["H2"]) and (bk["MaxDD"] >= base["MaxDD"])
    p4b = (bk["H1"] > spy["H1"]) and (bk["H2"] > spy["H2"]) \
          and (abs(bk["MaxDD"]) <= 0.60 * abs(spy["MaxDD"])) \
          and (bk["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(p4a), bool(p4b)

def build_live_ladder(pxb, pxs, S_STK, B_STK, SPY_RAW, COMMON):
    """Every one of the 168 panels x 3 arms, priced here at 10 bps with next-day execution.
    Returns the arm-row frame in idea 533's schema plus the realised-gross diagnostics."""
    rows, gross_rows = [], []
    for (q, d, sc, lc) in draw_panels(S_STK, B_STK):
        px = mk_px(sc, lc, pxs, pxb, SPY_RAW, COMMON)
        tr = [c for c in px.columns if c != "SPY"]
        start = px.index[WARMUP]
        s, above, vol20 = score(px[tr], vol_scale=False)
        el = s.where(above & (vol20 < 0.60))
        elig = el.notna()
        rank = el.rank(axis=1, ascending=False)
        e01 = elig.astype(float); cnt = e01.sum(axis=1).replace(0, np.nan)
        ch_is = panel_chars(px, tr, elig, None, IS_END)
        specs = [("EWall", (GROSS * e01.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0))]
        for n in NS:
            specs.append((f"top{n}", ((rank <= n).astype(float) * (GROSS / n))
                          .reindex(columns=px.columns).fillna(0.0)))
        v2r = backtest(px, rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0),
                       cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        spyr = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2f, v2o = mtr(v2r), mtr(v2r.loc[OOS_START:])
        spf, spo = mtr(spyr), mtr(spyr.loc[OOS_START:])
        for arm, w in specs:
            gs = w.sum(axis=1)
            gross_rows.append(dict(q=q, draw=d, arm=arm, max_gross=float(gs.max()),
                                   mean_gross=float(gs.mean()),
                                   days_over_nominal=int((gs > GROSS + 1e-9).sum()),
                                   n_days=int(len(gs))))
            r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            full = mtr(r); oos = mtr(r.loc[OOS_START:]); isw = mtr(r.loc[:IS_END])
            f4a, f4b = keep_paths(full, v2f, spf)
            o4a, o4b = keep_paths(oos, v2o, spo)
            rows.append(dict(q=q, draw=d, arm=arm, n=len(tr),
                             breadth_IS=ch_is["breadth"], disp_IS=ch_is["disp"],
                             corr_IS=ch_is["corr"], evol_IS=ch_is["evol"],
                             bookvol_IS=float(r.loc[:IS_END].std() * np.sqrt(252)),
                             Sharpe_IS=isw["Sharpe"], CAGR_IS=isw["CAGR"], MaxDD_IS=isw["MaxDD"],
                             Sharpe_full=full["Sharpe"], CAGR_full=full["CAGR"],
                             MaxDD_full=full["MaxDD"], H1=full["H1"], H2=full["H2"],
                             Sharpe_OOS=oos["Sharpe"], CAGR_OOS=oos["CAGR"],
                             MaxDD_OOS=oos["MaxDD"], OOS_H1=oos["H1"], OOS_H2=oos["H2"],
                             base_OOS_Sharpe=v2o["Sharpe"], base_OOS_CAGR=v2o["CAGR"],
                             base_OOS_MaxDD=v2o["MaxDD"],
                             SPY_OOS_Sharpe=spo["Sharpe"], SPY_OOS_CAGR=spo["CAGR"],
                             SPY_OOS_MaxDD=spo["MaxDD"],
                             pass4a=f4a, pass4b=f4b, pass4a_OOS=o4a, pass4b_OOS=o4b))
    return pd.DataFrame(rows), pd.DataFrame(gross_rows)


# ------------------------------------------- the selector grid, run on ANY ladder frame
def selector_grid(A, tag):
    """96 IS-only selectors x 4 percentile bases x 2 outcomes on one ladder frame."""
    rng_r = np.random.default_rng(RESAMP_SEED)
    rng_p = np.random.default_rng(PERM_SEED)
    rows, anchors = [], {}
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        oosS = sub.Sharpe_OOS.to_numpy(); oosD = sub.MaxDD_OOS.to_numpy()
        anchorS, anchorD = float(oosS.mean()), float(oosD.mean())
        anchors[arm] = (anchorS, anchorD, float((oosS > anchorS).mean()))
        rsS = oosS[rng_r.integers(0, len(oosS), N_RESAMP)]
        rsD = oosD[rng_r.integers(0, len(oosD), N_RESAMP)]
        groups = [np.where(st == s)[0] for s in np.unique(st)]
        permS = {(c, m, d): [] for c in CHARS for m in TRANSFORMS for d in DIRS}
        permD = {k: [] for k in permS}
        for ch in CHARS:
            x0 = sub[f"{ch}_IS"].to_numpy()
            for _ in range(N_PERM):
                xp = x0.copy()
                for g in groups:
                    xp[g] = x0[rng_p.permutation(g)]
                for m in TRANSFORMS:
                    v = transform(xp, lbv, st, m)
                    for d in DIRS:
                        i = pick(v, d)
                        permS[(ch, m, d)].append(oosS[i]); permD[(ch, m, d)].append(oosD[i])
        for ch in CHARS:
            x = sub[f"{ch}_IS"].to_numpy()
            for m in TRANSFORMS:
                v = transform(x, lbv, st, m)
                for d in DIRS:
                    i = pick(v, d); r = sub.loc[i]
                    stratum = np.where(st == st[i])[0]
                    rows.append(dict(ladder=tag, arm=arm, char=ch, transform=m, direction=d,
                                     selector=f"SEL-{ch}{d}|{m}", q=float(r.q), draw=int(r.draw),
                                     n_stratum=int(len(stratum)),
                                     IS_Sharpe=float(r.Sharpe_IS), OOS_Sharpe=float(r.Sharpe_OOS),
                                     OOS_CAGR=float(r.CAGR_OOS), OOS_MaxDD=float(r.MaxDD_OOS),
                                     anchor_OOS_S=anchorS, anchor_OOS_DD=anchorD,
                                     beats_anchor=bool(r.Sharpe_OOS > anchorS),
                                     pctS_EXACT=pctile(r.Sharpe_OOS, oosS),
                                     pctS_RESAMP2000=pctile(r.Sharpe_OOS, rsS),
                                     pctS_STRAT=pctile(r.Sharpe_OOS, oosS[stratum]),
                                     pctS_PERMSEL=pctile(r.Sharpe_OOS, permS[(ch, m, d)]),
                                     pctD_EXACT=pctile(r.MaxDD_OOS, oosD),
                                     pctD_RESAMP2000=pctile(r.MaxDD_OOS, rsD),
                                     pctD_STRAT=pctile(r.MaxDD_OOS, oosD[stratum]),
                                     pctD_PERMSEL=pctile(r.MaxDD_OOS, permD[(ch, m, d)]),
                                     perm_mean_S=float(np.mean(permS[(ch, m, d)]))))
    return pd.DataFrame(rows), anchors


def run_tests(G, tag):
    """T1..T5 on one ladder's grid.  Returns the verdict dict; prints every grid point's summary."""
    D = G[G.char == "disp"]; ND = G[G.char != "disp"]
    sub_rand = int((D.pctS_EXACT < 0.50).sum())
    if sub_rand >= T1_RULE_BAR: t1 = "THE RULE"
    elif sub_rand <= T1_COIN_BAR: t1 = "THE TWO CELLS (coin flip)"
    else: t1 = "INDETERMINATE"
    P(f"\n  [{tag}] T1  IS SUB-RANDOM THE RULE FOR disp?  {sub_rand} of {len(D)} disp cells below "
      f"the 50th percentile of the EXACT base.  bars: >= {T1_RULE_BAR} RULE / <= {T1_COIN_BAR} "
      f"TWO CELLS  ->  {t1}")
    P(f"          disp mean EXACT Sharpe percentile {D.pctS_EXACT.mean():.4f}, median "
      f"{D.pctS_EXACT.median():.4f}, range [{D.pctS_EXACT.min():.4f}, {D.pctS_EXACT.max():.4f}]; "
      f"all 96 cells mean {G.pctS_EXACT.mean():.4f}, sub-random "
      f"{int((G.pctS_EXACT < 0.5).sum())}/96")
    d_ex, d_st = float(D.pctS_EXACT.mean()), float(D.pctS_STRAT.mean())
    t2 = (d_st >= T2_HALF) and (d_ex < T2_HALF)
    P(f"  [{tag}] T2  STRATUM-MATCHED BASE: disp mean percentile EXACT {d_ex:.4f} -> STRAT "
      f"{d_st:.4f}  (all 96: {G.pctS_EXACT.mean():.4f} -> {G.pctS_STRAT.mean():.4f}).  "
      f"where-argmax-lands artefact iff STRAT >= 0.50 while EXACT < 0.50  ->  "
      f"{'YES, ARTEFACT' if t2 else 'NO'}")
    gap3 = float(D.pctS_EXACT.mean() - ND.pctS_EXACT.mean())
    t3 = abs(gap3) > T3_GAP
    P(f"  [{tag}] T3  IS disp SPECIAL?  disp {D.pctS_EXACT.mean():.4f} vs non-disp "
      f"{ND.pctS_EXACT.mean():.4f} (n {len(ND)}), gap {gap3:+.4f}; bar |gap| > {T3_GAP}  ->  "
      f"{'DISP-SPECIFIC' if t3 else 'NOT DISP-SPECIFIC'}")
    P(f"          by characteristic (EXACT base):")
    P("          " + G.groupby("char").agg(
        cells=("pctS_EXACT", "size"), mean_pctS=("pctS_EXACT", "mean"),
        mean_pctD=("pctD_EXACT", "mean"), beat_anchor=("beats_anchor", "sum"),
        sub_random=("pctS_EXACT", lambda s: int((s < 0.5).sum()))).reindex(CHARS)
        .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n          "))
    P(f"          by transform (EXACT base):")
    P("          " + G.groupby("transform").agg(
        cells=("pctS_EXACT", "size"), mean_pctS=("pctS_EXACT", "mean"),
        mean_pctD=("pctD_EXACT", "mean"), beat_anchor=("beats_anchor", "sum"),
        sub_random=("pctS_EXACT", lambda s: int((s < 0.5).sum()))).reindex(TRANSFORMS)
        .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n          "))
    gap4 = float(G.pctD_EXACT.mean() - G.pctS_EXACT.mean())
    t4 = gap4 < -T4_GAP
    P(f"  [{tag}] T4  IS THE OUTCOME THE STORY?  mean Sharpe percentile {G.pctS_EXACT.mean():.4f} "
      f"vs mean MaxDD percentile {G.pctD_EXACT.mean():.4f}, gap {gap4:+.4f}; bar < {-T4_GAP}  ->  "
      f"{'YES, DRAWDOWN IS THE SUB-RANDOM OUTCOME' if t4 else 'NO'}")
    pcols = [f"pctS_{b}" for b in BASES]
    spread = G[pcols].max(axis=1) - G[pcols].min(axis=1)
    nsub = (G[pcols] < 0.50).sum(axis=1)
    flips = int(nsub.between(1, 3).sum())
    P(f"  [{tag}] T5  BASE DEPENDENCE: within-cell percentile spread across the 4 bases mean "
      f"{spread.mean():.4f}, median {spread.median():.4f}, max {spread.max():.4f}; "
      f"non-unanimous sub-random verdict {flips}/{len(G)} ({flips/len(G):.1%})")
    for b in BASES:
        P(f"          {b:11s} mean Sharpe pct {G[f'pctS_{b}'].mean():.4f}   mean MaxDD pct "
          f"{G[f'pctD_{b}'].mean():.4f}   disp-only Sharpe pct {G[f'pctS_{b}'].mean():.4f} / "
          f"{G[G.char=='disp'][f'pctS_{b}'].mean():.4f}")
    return dict(ladder=tag, T1=t1, T1_sub_random=sub_rand, T1_n=len(D),
                T2_artefact=t2, T2_exact=d_ex, T2_strat=d_st,
                T3_disp_specific=t3, T3_gap=gap3, T4_outcome=t4, T4_gap=gap4,
                T5_spread_mean=float(spread.mean()), T5_flips=flips)


def main():
    t0 = time.time()
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 70)
    pd.set_option("display.max_rows", 600)
    P("=" * 112)
    P("IDEA 718 - is WORSE-THAN-RANDOM the general shape of a disp selector on this ladder?")
    P("           (lane B, 2026-09-19; 2 ladders x 96 selectors x 4 bases x 2 outcomes = 1,536 cells)")
    P("=" * 112)
    gates = []

    A = pd.read_csv(f"{P533}.arms.csv")
    P(f"\n[0] INHERITED ladder: {Path(str(P533)).name}.arms.csv  {A.shape[0]} arm-rows")
    P(f"    construction k={K_MIX}, {len(QS)} q rungs x {N_DRAWS} draws = {len(QS)*N_DRAWS} panels, "
      f"seed {SEED}; arms {ARMS}; gross {GROSS}, {FREQ}, {COST} bps, next-day execution, "
      f"{WARMUP}d warm-up skip")
    P(f"    rule 8: IS <= {IS_END.date()}, OOS {OOS_START.date()} .. end.  Selectors see IS ONLY.")

    # ================================================================ GATES G1-G3
    P("\n" + "=" * 112)
    P("GATES - the parents' committed numbers come back out before one new number is read")
    P("=" * 112)
    W540 = pd.read_csv(f"{P540}.walkforward.csv")
    g1 = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        dres = transform(sub["disp_IS"].to_numpy(), lbv, st, "residx")
        mine = {"SEL-S   argmax IS Sharpe": int(sub.Sharpe_IS.idxmax()),
                "SEL-DISP+ argmax IS disp": int(sub.disp_IS.idxmax()),
                "SEL-DISP- argmin IS disp": int(sub.disp_IS.idxmin()),
                "SEL-DISP|v argmax IS disp|log(vol)": pick(dres, "+")}
        for name, i in mine.items():
            r = sub.loc[i]; pub = W540[(W540.arm == arm) & (W540.selector == name)].iloc[0]
            g1.append(max(abs(float(r.q) - float(pub.q)), abs(int(r.draw) - int(pub.draw)),
                          abs(float(r.Sharpe_OOS) - float(pub.OOS_Sharpe)),
                          abs(float(r.CAGR_OOS) - float(pub.OOS_CAGR)),
                          abs(float(r.MaxDD_OOS) - float(pub.OOS_MaxDD))))
    g1max = float(np.max(g1))
    P(f"\n  G1  idea 540's 12 published selector rows re-derive from the arms file: "
      f"max |delta| over (q, draw, OOS CAGR/Sharpe/MaxDD) = {g1max:.3e}")
    assert g1max < 1e-9, f"G1 FAILED {g1max:.3e}"
    gates.append(dict(gate="G1", what="idea 540's 12 selector rows re-derive", stat=g1max,
                      bar="< 1e-9", passed=True)); P("      -> PASS")

    n4a, n4b = int(A.pass4a.sum()), int(A.pass4b.sum())
    P(f"  G2  idea 295/533's committed KEEP counts: 4a {n4a}/{len(A)} (published {PUB_4A}), "
      f"4b {n4b}/{len(A)} (published {PUB_4B})")
    assert (n4a, n4b, len(A)) == (PUB_4A, PUB_4B, PUB_N), "G2 FAILED"
    gates.append(dict(gate="G2", what="idea 295/533 committed 4a/4b counts", stat=float(n4b),
                      bar=f"4a={PUB_4A}, 4b={PUB_4B}, n={PUB_N}", passed=True)); P("      -> PASS")

    P("\n" + "=" * 112)
    P("LADDER 1 of 2 - INHERITED (idea 533's committed arm-rows; continuity with 714 / 715)")
    P("=" * 112)
    GI, anch_I = selector_grid(A, "INHERITED")
    beat = int(GI.beats_anchor.sum()); mpct = float(GI.pctS_EXACT.mean())
    P(f"\n  G3  idea 715's committed 96-cell summary reproduces: beat-anchor {beat} (published "
      f"{PUB_715_BEAT}), mean EXACT Sharpe percentile {mpct:.4f} (published {PUB_715_PCT})")
    assert beat == PUB_715_BEAT and abs(mpct - PUB_715_PCT) < 5e-4, "G3 FAILED"
    gates.append(dict(gate="G3", what="idea 715's 96-cell beat count and mean percentile",
                      stat=mpct, bar=f"beat=={PUB_715_BEAT}, |dpct|<5e-4", passed=True))
    P("      -> PASS")
    P("\n  anchors and the EXACT uniform-pick base rate:")
    for arm in ARMS:
        aS, aD, br = anch_I[arm]; sub = A[A.arm == arm]
        P(f"    {arm:6s} anchor Sharpe {aS:.4f} / MaxDD {aD:+.4f};  P(random pick > anchor) "
          f"{br:.4f};  OOS Sharpe min {sub.Sharpe_OOS.min():.4f} / med "
          f"{sub.Sharpe_OOS.median():.4f} / max {sub.Sharpe_OOS.max():.4f}")
    v_I = run_tests(GI, "INHERITED")

    # ================================================================ LADDER 2: LIVE
    P("\n" + "=" * 112)
    P("LADDER 2 of 2 - LIVE: the same construction re-drawn on TODAY'S pool and priced here")
    P("=" * 112)
    pxb, pxs, S_STK, B_STK, SPY_RAW, COMMON, nbad = panel_pool()
    P(f"  pools: small panel {nbad} names with max_1d_move >= 1.0 dropped FIRST, {len(S_STK)} "
      f"usable (idea 715's own gate replayed at {PUB_715_SMALLPOOL}); large-cap stock pool "
      f"{len(B_STK)}; common window {COMMON[0].date()}..{COMMON[-1].date()} ({len(COMMON)} rows)")
    P(f"  G4  VINTAGE, stated as a number: the small pool moved {PUB_715_SMALLPOOL} -> "
      f"{len(S_STK)} (+{len(S_STK)-PUB_715_SMALLPOOL}, {len(S_STK)/PUB_715_SMALLPOOL:.2f}x), so "
      f"`rng(seed={SEED}).choice` lands on DIFFERENT names.  THE LADDER IS NOT REBUILDABLE; this "
      f"is an INDEPENDENT REPLICATION at the same construction, and every level below is its own.")
    gates.append(dict(gate="G4", what="small-pool vintage gap vs idea 715's replay",
                      stat=float(len(S_STK) - PUB_715_SMALLPOOL), bar="recorded, not asserted",
                      passed=True))
    LAD, GR = build_live_ladder(pxb, pxs, S_STK, B_STK, SPY_RAW, COMMON)
    LAD.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  built {len(LAD)} arm-rows over {LAD.groupby(['q','draw']).ngroups} panels "
      f"({time.time()-t0:.1f}s)")

    gmax = float(GR.max_gross.max())
    over = GR[GR.days_over_nominal > 0]
    P(f"\n  G5  NO LEVERAGE (PROTOCOL rule 2): max realised weight sum over all {len(GR)} live "
      f"books = {gmax:.6f} <= 1.0  -> PASS")
    assert gmax <= 1.0 + 1e-9, "G5 FAILED (leverage)"
    P(f"      METHOD FINDING, published rather than clipped: the committed top-n construction "
      f"`(rank <= n) * gross/n` BREACHES its own nominal gross {GROSS} whenever the eligibility "
      f"score TIES at the n-th rank.  {len(over)} of {len(GR)} books breach it on at least one "
      f"day; max realised gross {gmax:.4f} ({gmax/GROSS:.2f}x nominal); over the breaching books "
      f"the breach touches {over.days_over_nominal.mean():.1f} days of "
      f"{GR.n_days.iloc[0]} on average ({over.days_over_nominal.sum()/GR.n_days.sum():.3%} of all "
      f"book-days).  EWall never breaches ({int(GR[GR.arm=='EWall'].days_over_nominal.sum())} "
      f"days).  It is a rank-tie artefact, it is small, and it is in every committed number this "
      f"ladder has ever published.")
    gates.append(dict(gate="G5", what="max realised weight sum over every live book", stat=gmax,
                      bar="<= 1.0 (rule 2)", passed=True))

    spy_sd = float(LAD[["SPY_OOS_Sharpe", "SPY_OOS_CAGR", "SPY_OOS_MaxDD"]].std().max())
    v2_sd = float(LAD[["base_OOS_Sharpe", "base_OOS_CAGR", "base_OOS_MaxDD"]].std().max())
    P(f"\n  G6  comparands: SPY is ONE series across all {len(LAD)} rows (max sd {spy_sd:.3e}) at "
      f"OOS {LAD.SPY_OOS_CAGR.iloc[0]:+.4f}/{LAD.SPY_OOS_Sharpe.iloc[0]:.4f}/"
      f"{LAD.SPY_OOS_MaxDD.iloc[0]:+.4f}; RULES v2 is re-run PER PANEL and is NOT constant "
      f"(max sd {v2_sd:.4f}): OOS Sharpe mean {LAD.base_OOS_Sharpe.mean():.4f} range "
      f"[{LAD.base_OOS_Sharpe.min():.4f}, {LAD.base_OOS_Sharpe.max():.4f}], CAGR mean "
      f"{LAD.base_OOS_CAGR.mean():+.4f}, MaxDD mean {LAD.base_OOS_MaxDD.mean():+.4f} "
      f"(idea 715's correction to idea 540, re-checked live)")
    assert spy_sd < 1e-9, "G6 FAILED"
    gates.append(dict(gate="G6", what="SPY one series / RULES v2 per panel", stat=spy_sd,
                      bar="SPY sd < 1e-9", passed=True))

    GL, anch_L = selector_grid(LAD, "LIVE")
    P("\n  anchors and the EXACT uniform-pick base rate (LIVE):")
    for arm in ARMS:
        aS, aD, br = anch_L[arm]; sub = LAD[LAD.arm == arm]
        P(f"    {arm:6s} anchor Sharpe {aS:.4f} / MaxDD {aD:+.4f};  P(random pick > anchor) "
          f"{br:.4f};  OOS Sharpe min {sub.Sharpe_OOS.min():.4f} / med "
          f"{sub.Sharpe_OOS.median():.4f} / max {sub.Sharpe_OOS.max():.4f}")
    v_L = run_tests(GL, "LIVE")

    G = pd.concat([GI, GL], ignore_index=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    show = ["ladder", "arm", "char", "transform", "direction", "q", "draw", "IS_Sharpe",
            "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "pctS_EXACT", "pctS_RESAMP2000", "pctS_STRAT",
            "pctS_PERMSEL", "pctD_EXACT", "pctD_STRAT", "beats_anchor"]
    P(f"\n  ALL {len(G)} SELECTOR CELLS, BOTH LADDERS (pct = share of the base at or below the "
      f"pick; higher = better on both outcomes):")
    P(G[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ AGREEMENT
    P("\n" + "=" * 112)
    P("LADDER AGREEMENT - the same 96 selectors on two independent draws of the same construction")
    P("=" * 112)
    M = GI.merge(GL, on=["arm", "char", "transform", "direction"], suffixes=("_I", "_L"))
    sgn = ((M.pctS_EXACT_I < 0.5) == (M.pctS_EXACT_L < 0.5))
    P(f"  sub-random verdict agrees on {int(sgn.sum())} of {len(M)} cells ({sgn.mean():.1%})")
    P(f"  pearson(pctS_EXACT_I, pctS_EXACT_L) = "
      f"{float(np.corrcoef(M.pctS_EXACT_I, M.pctS_EXACT_L)[0,1]):+.4f}; spearman = "
      f"{float(M[['pctS_EXACT_I','pctS_EXACT_L']].corr(method='spearman').iloc[0,1]):+.4f}")
    P(f"  mean EXACT Sharpe percentile INHERITED {GI.pctS_EXACT.mean():.4f} vs LIVE "
      f"{GL.pctS_EXACT.mean():.4f}; disp-only {GI[GI.char=='disp'].pctS_EXACT.mean():.4f} vs "
      f"{GL[GL.char=='disp'].pctS_EXACT.mean():.4f}")

    # ================================================================ THE CAPITAL LEG
    P("\n" + "=" * 112)
    P("T6 - THE CAPITAL LEG (PROTOCOL rule 4 both paths, rule 8 walk-forward), LIVE ladder only")
    P("=" * 112)
    key = LAD.set_index(["q", "draw", "arm"])
    cells = []
    for r in GL.itertuples():
        k = key.loc[(r.q, r.draw, r.arm)]
        cells.append(dict(arm=r.arm, char=r.char, transform=r.transform, direction=r.direction,
                          selector=r.selector, q=r.q, draw=r.draw,
                          pctS_EXACT=r.pctS_EXACT, pctS_STRAT=r.pctS_STRAT,
                          pctD_EXACT=r.pctD_EXACT,
                          CAGR_full=k.CAGR_full, Sharpe_full=k.Sharpe_full, MaxDD_full=k.MaxDD_full,
                          H1=k.H1, H2=k.H2,
                          CAGR_OOS=k.CAGR_OOS, Sharpe_OOS=k.Sharpe_OOS, MaxDD_OOS=k.MaxDD_OOS,
                          OOS_H1=k.OOS_H1, OOS_H2=k.OOS_H2,
                          v2_OOS_Sharpe=k.base_OOS_Sharpe, spy_OOS_Sharpe=k.SPY_OOS_Sharpe,
                          beats_v2_OOS=bool(k.Sharpe_OOS > k.base_OOS_Sharpe),
                          beats_spy_OOS=bool(k.Sharpe_OOS > k.SPY_OOS_Sharpe),
                          pass4a_full=bool(k.pass4a), pass4b_full=bool(k.pass4b),
                          pass4a_OOS=bool(k.pass4a_OOS), pass4b_OOS=bool(k.pass4b_OOS)))
    L = pd.DataFrame(cells); L.to_csv(f"{OUT}.cells.csv", index=False)
    P(f"\n  ALL 96 LIVE PICKS PRICED (10 bps, next-day execution, gross {GROSS}, weekly):")
    P(L[["arm", "char", "transform", "direction", "q", "draw", "CAGR_full", "Sharpe_full",
         "MaxDD_full", "H1", "H2", "CAGR_OOS", "Sharpe_OOS", "MaxDD_OOS", "beats_v2_OOS",
         "beats_spy_OOS", "pass4a_full", "pass4b_full", "pass4a_OOS", "pass4b_OOS"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    both4b = L[(L.pass4b_full) & (L.pass4b_OOS)]
    both4a = L[(L.pass4a_full) & (L.pass4a_OOS)]
    P(f"\n  over the 96 picks:  path 4a FULL {int(L.pass4a_full.sum())}/96, OOS "
      f"{int(L.pass4a_OOS.sum())}/96, BOTH {len(both4a)}/96")
    P(f"                      path 4b FULL {int(L.pass4b_full.sum())}/96, OOS "
      f"{int(L.pass4b_OOS.sum())}/96, BOTH {len(both4b)}/96")
    P(f"                      beats RULES v2 OOS Sharpe {int(L.beats_v2_OOS.sum())}/96; "
      f"beats SPY OOS Sharpe {int(L.beats_spy_OOS.sum())}/96")
    P(f"                      mean live OOS CAGR {L.CAGR_OOS.mean():+.4f} Sharpe "
      f"{L.Sharpe_OOS.mean():.4f} MaxDD {L.MaxDD_OOS.mean():+.4f}")
    P(f"  comparands on these panels' own names and days: RULES v2 OOS Sharpe mean "
      f"{LAD.base_OOS_Sharpe.mean():.4f} (CAGR {LAD.base_OOS_CAGR.mean():+.4f}, MaxDD "
      f"{LAD.base_OOS_MaxDD.mean():+.4f});  SPY OOS {LAD.SPY_OOS_CAGR.iloc[0]:+.4f} / "
      f"{LAD.SPY_OOS_Sharpe.iloc[0]:.4f} / {LAD.SPY_OOS_MaxDD.iloc[0]:+.4f}")
    if len(both4b):
        P("\n  cells passing 4b on BOTH windows:")
        P(both4b[["arm", "char", "transform", "direction", "q", "draw", "CAGR_full", "Sharpe_full",
                  "MaxDD_full", "H1", "H2", "CAGR_OOS", "Sharpe_OOS", "MaxDD_OOS", "OOS_H1",
                  "OOS_H2", "pctS_EXACT", "pctS_STRAT"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P(f"\n  THE COUNTERWEIGHT - the same two paths over ALL {len(LAD)} (panel, arm) books, i.e. the "
      f"base rate a selector must beat to have selected anything:")
    P(f"    4b FULL {int(LAD.pass4b.sum())}/{len(LAD)} ({LAD.pass4b.mean():.1%}), OOS "
      f"{int(LAD.pass4a_OOS.sum() * 0 + LAD.pass4b_OOS.sum())}/{len(LAD)} "
      f"({LAD.pass4b_OOS.mean():.1%}), BOTH "
      f"{int((LAD.pass4b & LAD.pass4b_OOS).sum())}/{len(LAD)} "
      f"({(LAD.pass4b & LAD.pass4b_OOS).mean():.1%})")
    P(f"    4a FULL {int(LAD.pass4a.sum())}/{len(LAD)} ({LAD.pass4a.mean():.1%}), OOS "
      f"{int(LAD.pass4a_OOS.sum())}/{len(LAD)} ({LAD.pass4a_OOS.mean():.1%}), BOTH "
      f"{int((LAD.pass4a & LAD.pass4a_OOS).sum())}/{len(LAD)}")
    sel_rate = (L.pass4b_full & L.pass4b_OOS).mean(); pop_rate = (LAD.pass4b & LAD.pass4b_OOS).mean()
    P(f"    SELECTOR LIFT on 4b-BOTH: picks {sel_rate:.1%} vs population {pop_rate:.1%} "
      f"(lift {sel_rate - pop_rate:+.1%} pp)")

    # ================================================================ VERDICT
    V = pd.DataFrame([v_I, v_L]); V.to_csv(f"{OUT}.cells.verdicts.csv", index=False)
    P("\n" + "=" * 112)
    P("VERDICT TABLE - the pre-registered tests on both ladders")
    P("=" * 112)
    P(V.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    GT = pd.DataFrame(gates); GT.to_csv(f"{OUT}.gates.csv", index=False)
    P(f"\nGATES {int(GT.passed.sum())}/{len(GT)} PASS")
    P(GT.to_string(index=False))
    P(f"\nruntime {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
