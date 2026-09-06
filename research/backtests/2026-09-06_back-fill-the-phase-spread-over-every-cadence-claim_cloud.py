#!/usr/bin/env python3
"""QUEUE idea 220 - back-fill-the-phase-spread-over-every-cadence-claim   (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 220)
    "idea 187 measured the block-phase spread at ONE fixed cadence at 2.1-2.4x the published
     6W-minus-W cadence effect (16.1x on SMALL), and every ladder point in the record is
     phase 0.  Re-read every committed cadence comparison (ideas 3, 65, 101, 107, 171, 173,
     175, 182, 188) whose grid CSV survives, price each claimed cadence gap against its own
     phase spread, and count how many published cadence verdicts survive.  The output is the
     size of the correction.  Max 2 params."

WHAT IS AT STAKE
    Every cadence number this project has published is a PHASE-0 number: the ladder point "M"
    means "the last bar of each calendar month counting from the panel's first bar", not "a
    monthly cadence".  Idea 187 showed that at a FIXED cadence, merely moving the block grid
    (6 block phases at 6W) moves mean OOS Sharpe by 0.15-0.40 - 2.1-2.4x the published 6W-minus-W
    cadence effect and 16.1x on the small panel.  If that holds at the cadences the record
    actually argues about, then a published "M beats W" is a statement about WHICH DAYS the book
    traded, not about HOW OFTEN, and the verdict is an alignment draw.  This run prices every
    recoverable cadence verdict against its own phase spread and counts the survivors.

THE PHASE DEFINITION - the one new piece of machinery, and it is a strict generalisation
    Idea 187's phase shifts the block grid by whole sub-periods.  That is defined only for
    k>1 block points (2D,2W,6W,2M,2Q) and is DEGENERATE at D,W,M,Q - which is exactly the
    ladder ideas 3/101/171/173 argue over.  So phase here is a PAIR:
        phase = (shift, off)
          shift  the whole-sub-period block-grid shift of idea 187 (0..k-1; k=1 -> {0})
          off    the WITHIN-BLOCK trading day: rebalance on the (last - off)-th bar of each
                 block, clamped to the block's first bar.  off in {0..4} for calendar blocks
                 (a trading week), {0} for the bar-count points D/2D where it is meaningless.
    phase (0,0) IS the published convention, bar for bar, at every point - which is what makes
    control [c] below a reproduction of the record rather than a re-run of it.
    Phase counts: D 1 | 2D 2 | W 5 | 2W 10 | M 5 | 6W 30 | Q 5.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4
    1. CADENCE POINT   - swept over each parent's own ladder, ALL points reported.
    2. PHASE           - swept exhaustively over the grid above, ALL phases reported.
    Corpus, cell and metric are AUDIT AXES (they are read from the committed parents, not
    chosen here).  Nothing is picked for reporting; every grid point is written to CSV.

THE FOUR AUDITABLE CORPORA (the idea names nine; five of the nine left no machine-readable grid)
    A  ideas 175 + 188   115 books x 7-point ladder D,2D,W,2W,M,6W,Q
                         parent 2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud.ladder.csv
    B  idea 171          53 books x CADENCE dial D,W,M,Q (other four dials at incumbents)
                         parent ..._do-gross-choice-rules-lose-to-constants-in-general_C.ladder.csv
    C  idea 173          18 cells (3 panels x 3 signals x 2 cost rungs) x CADENCE ladder D,W,M,Q
                         parent ..._is-the-ladder-endpoint-a-general-selector-artefact_cloud.grid.csv
    D  idea 101          8 cells (2 universes x 2 sleeve arms x 2 f) x D,W,M, plus its idea-65
                         cadence-insensitivity BAR (|dSharpe| across D/W/M <= 0.05)
                         parent 2026-09-05_fixed-gross-S4-blend_cloud.cadence.csv
    NOT AUDITED, with the reason stated in the output rather than buried:
      idea 3    (2026-09-04_rebalance-freq_cloud) wrote NO grid CSV - console + result.md only.
      ideas 65, 107, 182 are still OPEN in QUEUE.md: they were never run, so there is no
                         published verdict to audit.
      idea 187  is the parent of this idea, not an audit target; it is used as control [d].

WHAT A "PUBLISHED CADENCE VERDICT" IS, mechanically
    For each corpus and each cell the parent reported at, every ORDERED PAIR (A,B) of ladder
    points with A faster than B is one published verdict: the SIGN of the cell's mean metric
    gap A-B at phase 0.  That is the claim "A beats B at this cadence" in the record.
    For each such verdict this run computes, over the FULL phase grid of both points:
      gap0        the phase-0 gap                   (reproduces the parent; control [c])
      gap_pa      the phase-AVERAGED gap            (mean over A's phases - mean over B's)
      sign_share  fraction of the |phase_A| x |phase_B| combinations whose gap has gap0's sign
      gap_range   max-min of the gap over those combinations = the verdict's own phase spread
      ratio       |gap0| / gap_range
    PRE-REGISTERED SURVIVAL RULE (fixed before any number was read):
      SURVIVES        sign(gap_pa) == sign(gap0)  AND  sign_share >= 0.95
      SURVIVES-WEAK   sign(gap_pa) == sign(gap0)             (the sign is at least not reversed)
    The headline output is the survivor COUNT, which is what the idea asks for.

REPRODUCTION CONTROLS, asserted before any conclusion
    [a] cad_mask at phase (0,0) equals engine.rebalance_mask at D, W, M, Q.
    [b] fast_backtest at 0 bps, netted by turnover*bps/1e4, equals engine.backtest at 10 bps to
        <1e-12 (cost linearity, on which every derived cost rung rests).
    [c] per corpus: the phase-(0,0) rows equal the parent's committed CSV to <1e-9 on the audited
        metric.  A corpus that fails [c] is reported NOT AUDITED and its claims are excluded -
        it is never silently included.
    [d] at cad=6W, this run's (shift, off=0) rows equal idea 187's committed .phase.csv OOS
        Sharpe to <1e-9, i.e. the new phase machinery contains 187's as a special case.

PROTOCOL rule 8 walk-forward (required, and it is the decision this audit implies)
    Per book of corpus A, parameters chosen on <= 2016-12-31 only, OOS window 2017-01-01.. read
    once, four arms:
      CONST-W0    W at phase 0                       the incumbent, RULES v1's cadence
      REC         cadence chosen by IS Sharpe AT PHASE 0        <- what the record does
      SEL-CP      cadence AND phase chosen by IS Sharpe         <- fitting the phase too
      PHASE-AVG   cadence chosen by IS Sharpe on the PHASE-AVERAGED book, traded as the
                  equal-weight blend of all phases of that cadence (implementable: it is k
                  sub-books at 1/k each)                        <- the honest estimator
    Reported as mean OOS CAGR/Sharpe/MaxDD over books, against RULES v1 and SPY on each parent
    panel over the same OOS window.

BOTH KEEP PATHS evaluated on every corpus-A row (4a and 4b exactly as PROTOCOL rule 4 states).

CAVEATS carried, not buried
    * SURVIVORSHIP.  SMALL439/SMALL484/small, U56/u56, B136/broad and ETF36 are all
      CURRENT-CONSTITUENT lists (data/SMALL_PANEL_README.md, idea 54).  No level here is an
      attainable return.  Phase and cadence inherit the bias identically, so the PAIRED
      comparisons that carry this run's conclusion are unaffected.
    * Corpus B reproduces idea 171 exactly, and idea 171's SMALL484 did NOT drop the
      max_1d_move >= 1.0 tickers.  Reproducing a committed parent requires its corpus; the
      standing drop rule is applied to every panel this run builds itself (A and C).
    * Idea 38: data/prices*.csv are calendar-day indexed after 2014-09-17, so an "off" of 1 bar
      on the large-cap panels can be a weekend bar (a no-op in weights).  This makes the
      large-cap phase spreads a LOWER bound, not an upper one.
    * A phase is not a tradable choice: it is fixed by an arbitrary sample-start date.  A point
      that wins on phase wins on nothing.  That asymmetry is the whole argument.
    * 10 bps, t+1 execution, except where a parent published another rung (corpus C: 10 and 25).

Deterministic, standalone.  Writes .console.txt, .rows.csv, .claims.csv, .summary.csv,
.walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_back-fill-the-phase-spread-over-every-cadence-claim_cloud"
OUT = ROOT / "research" / "backtests"

P175 = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"
P171 = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P173 = "2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud"
P101 = "2026-09-05_fixed-gross-S4-blend_cloud"
P187 = "2026-09-06_is-6W-a-grid-edge-or-a-real-optimum_B"

COST_BPS = 10.0
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
SIGN_BAR = 0.95            # pre-registered survival bar

_WEEK_K = {"W": 1, "2W": 2, "6W": 6, "7W": 7, "8W": 8, "10W": 10, "16W": 16}
_PER_K = {"M": ("M", 1), "2M": ("M", 2), "Q": ("Q", 1), "2Q": ("Q", 2)}
DAY_OFFS = [0, 1, 2, 3, 4]          # one trading week of within-block phase

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def phases_for(cad):
    """The full phase grid of a cadence point: (block shift, within-block day offset)."""
    if cad == "D":
        return [(0, 0)]
    if cad == "2D":
        return [(s, 0) for s in range(2)]
    k = _WEEK_K[cad] if cad in _WEEK_K else _PER_K[cad][1]
    return [(s, o) for s in range(k) for o in DAY_OFFS]


# ---------------------------------------------------------------- cadence mask
def cad_mask(idx, cad, shift=0, off=0):
    """True on the trading bar of each cadence block.  (shift, off) = (0, 0) is the published
    convention and equals engine.rebalance_mask at D/W/M/Q (control [a])."""
    n = len(idx)
    if cad == "D":
        key = np.arange(n)
    elif cad == "2D":
        key = (np.arange(n) + shift) // 2
    elif cad in _WEEK_K:
        ordi = np.asarray(idx.to_period("W").astype("int64"))
        ordi = ordi - ordi[0]
        key = (ordi + shift) // _WEEK_K[cad]
    elif cad in _PER_K:
        f, k = _PER_K[cad]
        ordi = np.asarray(idx.to_period(f).astype("int64"))
        key = ordi if (k == 1 and shift == 0) else (ordi - ordi[0] + shift) // k
    else:
        raise ValueError(cad)
    m = np.empty(n, bool)
    m[:-1] = key[:-1] != key[1:]
    m[-1] = True
    if off:
        last = np.flatnonzero(m)
        starts = np.concatenate(([0], last[:-1] + 1))
        pos = np.maximum(starts, last - off)
        m = np.zeros(n, bool)
        m[pos] = True
    return pd.Series(m, index=idx)


def fast_backtest(prices, weights, cad="W", shift=0, off=0):
    """Vectorised engine.backtest at ZERO cost, returning gross returns and turnover so any
    cost rung is derived exactly (control [b] asserts the linearity)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad, shift, off).shift(1, fill_value=False).values.copy()
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
    gross = (held * rets).sum(axis=1)
    return pd.Series(gross, index=idx), pd.Series(turn, index=idx)


# ---------------------------------------------------------------- books
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def top_n_weights(px, tradable, n=20, gross=0.75, sig=None, p=0.0, max_vol=MAX_VOL):
    s = comp_score(px) if sig is None else sig
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    if p:
        s = s / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        elig[drop] = np.nan
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def raw_signal(px, sig):
    if sig == "COMP":
        return comp_score(px)
    if sig == "MOM":
        return px.shift(21) / px.shift(252) - 1
    if sig == "R6":
        return px / px.shift(126) - 1
    raise ValueError(sig)


def sleeve_weights(px, assets):
    """idea 18 variant B, verbatim from idea 101: trend vote x inverse-60d-vol risk parity."""
    sub = px[assets]
    vol = sub.pct_change().rolling(60).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    rp = inv.div(inv.sum(axis=1), axis=0)
    sigs = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    vote = sum((s > 0).astype(float).where(s.notna()) for s in sigs) / len(sigs)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (vote * rp).fillna(0.0)
    return out


# ---------------------------------------------------------------- metric helpers
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def row_metrics(r):
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                OOS_MaxDD=mo["MaxDD"])


def keep_4a(rm, base_h1, base_h2, base_dd):
    f = []
    if not rm["H1"] > base_h1: f.append("H1")
    if not rm["H2"] > base_h2: f.append("H2")
    if not rm["MaxDD"] >= base_dd: f.append("DD")
    return ",".join(f) if f else "-"


def keep_4b(rm, sp):
    f = []
    if not rm["H1"] > sp["H1"]: f.append("H1")
    if not rm["H2"] > sp["H2"]: f.append("H2")
    if not rm["OOS_Sharpe"] > sp["OOS_Sharpe"]: f.append("OOS")
    if not abs(rm["MaxDD"]) <= DELTA * abs(sp["MaxDD"]): f.append("DD")
    if not rm["CAGR"] >= PHI * sp["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# ---------------------------------------------------------------- corpora
class Unit:
    """One auditable cell member: a price panel, a weight matrix, a ladder and a cost rung."""

    def __init__(self, corpus, cell, unit, px, w, panel, cost, ladder):
        self.corpus, self.cell, self.unit = corpus, cell, unit
        self.px, self.w, self.panel, self.cost, self.ladder = px, w, panel, cost, ladder


def build_all():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs_raw = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_ok = [c for c in pxs_raw.columns if c != "SPY" and c not in bad]
    P(f"  small panel: {len([c for c in pxs_raw.columns if c!='SPY'])} names, dropped "
      f"{len([c for c in pxs_raw.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_ok)} tradable")
    pxs = pxs_raw[s_ok + ["SPY"]]

    def keep(px, cols, extra=()):
        cols = [c for c in cols if c in px.columns]
        allc = list(dict.fromkeys(cols + ["SPY"] + [c for c in extra if c in px.columns]))
        return px[allc].dropna(how="all").ffill()

    panels = {"U56": px56, "B136": px136, "SMALL": pxs, "SMALL484": pxs_raw}
    units = []

    # ---------------- corpus A: ideas 175 + 188, 115 books, 7-point ladder
    LADA = ["D", "2D", "W", "2W", "M", "6W", "Q"]
    u_stk = [c for c in px56.columns if c != "SPY"]
    e_stk = [t for t in etf36 if t in px56.columns and t != "SPY"]
    fixedA = [("SMALL439", "SMALL", pxs, s_ok, "SMALL"), ("U56", "U56", px56, u_stk, "U56"),
              ("ETF36", "ETF", px56, e_stk, "U56")]
    for nm, fam, px, tr, par in fixedA:
        pk = keep(px, tr)
        units.append(Unit("A", fam, nm, pk, top_n_weights(pk, set(tr)), par, COST_BPS, LADA))
    poolsA = {"SMALL": (pxs, s_ok, 175_500, [20, 40, 80], "SMALL"),
              "U56": (px56, u_stk, 175_600, [20, 40], "U56"),
              "ETF": (px56, e_stk, 175_700, [12, 24], "U56")}
    for fam, (pxp, pool, seed, ks, par) in poolsA.items():
        for k in ks:
            rng = np.random.default_rng(seed + k)
            for d in range(16):
                sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
                pk = keep(pxp, sub)
                units.append(Unit("A", fam, f"{fam}k{k}d{d:02d}", pk,
                                  top_n_weights(pk, set(sub)), par, COST_BPS, LADA))

    # ---------------- corpus B: idea 171's CADENCE dial, other four dials at incumbents
    LADB = ["D", "W", "M", "Q"]
    SLV = ["TLT", "GLD", "UUP"]
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    add = ref[SLV].reindex(pxs_raw.index, method="ffill")
    pxs484 = pd.concat([pxs_raw.drop(columns=SLV, errors="ignore"), add], axis=1)
    panels["SMALL484"] = pxs484
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s484 = [c for c in pxs484.columns if c not in set(["SPY"] + SLV)]
    fixedB = [("U56", px56, [c for c in px56.columns if c != "SPY"], "U56"),
              ("B136", px136, [c for c in px136.columns if c != "SPY"], "B136"),
              ("BSTK100", px136, b_stk, "B136"),
              ("ETF36", px56, [c for c in etf36 if c in px56.columns], "U56"),
              ("SMALL484", pxs484, s484, "SMALL484")]
    for nm, px, tr, par in fixedB:
        pk = keep(px, tr, SLV)
        units.append(Unit("B", par, nm, pk, top_n_weights(pk, set(tr)), par, COST_BPS, LADB))
    poolB = [c for c in px136.columns if c != "SPY"]
    for k in [20, 40, 80]:
        rng = np.random.default_rng(171_500 + k)
        for d in range(16):
            sub = sorted(rng.choice(poolB, size=k, replace=False).tolist())
            pk = keep(px136, sub, SLV)
            units.append(Unit("B", "B136", f"B136k{k}d{d:02d}", pk,
                              top_n_weights(pk, set(sub)), "B136", COST_BPS, LADB))

    # ---------------- corpus C: idea 173's CADENCE ladder, 3 panels x 3 signals x 2 cost rungs
    panC = {"u56": (px56, "U56"), "broad": (px136, "B136"), "small": (pxs, "SMALL")}
    for pn, (px, par) in panC.items():
        # idea 173's weights() ranks over EVERY column of the panel (SPY included); reproducing
        # its committed rows means reproducing that, so tradable = all columns here.
        tr = list(px.columns)
        for sg in ["COMP", "MOM", "R6"]:
            w = top_n_weights(px, set(tr), n=20, gross=0.75, sig=raw_signal(px, sg), p=0.5)
            for cst in [10.0, 25.0]:
                units.append(Unit("C", f"{pn}|{sg}|{cst:.0f}", f"{pn}|{sg}|{cst:.0f}",
                                  px, w, par, cst, LADB))

    # ---------------- corpus D: idea 101's cadence bar, 2 universes x 2 arms x 2 f
    LADD = ["D", "W", "M"]
    for tag, px, par in [("u56", px56, "U56"), ("broad", px136, "B136")]:
        # idea 101's book_top20 likewise ranks over every column of the panel.
        E = top_n_weights(px, set(px.columns), n=20, gross=0.75)
        for arm, assets in [("S4", ["TLT", "GLD", "DBC", "UUP"]), ("S3", ["TLT", "GLD", "UUP"])]:
            S = sleeve_weights(px, assets)
            for f in [0.0, 0.5]:
                w = (1 - f) * E + f * S
                g = w.sum(axis=1)
                w = w.mul((1.00 / g.where(g > 1e-12)).fillna(0.0), axis=0)
                units.append(Unit("D", f"{tag}|{arm}|{f:.2f}", f"{tag}|{arm}|{f:.2f}",
                                  px, w, par, COST_BPS, LADD))
    return units, panels


# ---------------------------------------------------------------- controls
def check_a(idx):
    ok = True
    for cd in ["D", "W", "M", "Q"]:
        same = bool((rebalance_mask(idx, cd).values == cad_mask(idx, cd).values).all())
        P(f"  [a] cad_mask(0,0) == engine.rebalance_mask at {cd:2s}: {same}")
        ok &= same
    return ok


def check_b(px, w):
    ok = True
    for cd in ["D", "W", "M", "Q"]:
        a = backtest(px, w, cost_bps=COST_BPS, freq=cd)["returns"]
        g, t = fast_backtest(px, w, cd)
        d = float((a - (g - t * COST_BPS / 1e4)).abs().max())
        P(f"  [b] fast_backtest netted at {COST_BPS:.0f} bps vs engine at {cd:2s}: max|d| = {d:.2e}")
        ok &= d < 1e-12
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 220 - back-fill-the-phase-spread-over-every-cadence-claim  (cloud, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Every cadence number in the record is a PHASE-0 number.  This run re-prices each published")
    P("cadence verdict against its own phase spread and counts the survivors.")
    P("Two tuned params: CADENCE POINT (swept, all reported) x PHASE (swept, all reported).")
    P(f"Phase = (block shift, within-block day offset in {DAY_OFFS}); (0,0) IS the published point.")
    P("")
    for c in ["D", "2D", "W", "2W", "M", "6W", "Q"]:
        P(f"   phase grid {c:3s}: {len(phases_for(c)):3d} phases")
    P("")

    units, panels = build_all()
    for cp in "ABCD":
        n = len([u for u in units if u.corpus == cp])
        P(f"  corpus {cp}: {n} units")
    P("")

    # references per panel
    START, SPYM, BASE = {}, {}, {}
    for pk, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        g, t = fast_backtest(px, rules_v1_weights(px), "W")
        base = (g - t * COST_BPS / 1e4).loc[st:]
        START[pk] = st
        SPYM[pk] = dict(ret=spy, **row_metrics(spy))
        BASE[pk] = dict(ret=base, **row_metrics(base))
    P("  panel references (SPY | RULES v1), full-sample and OOS")
    for pk in panels:
        s, b = SPYM[pk], BASE[pk]
        P(f"   {pk:9s} SPY  CAGR {s['CAGR']:6.2%} Sh {s['Sharpe']:.3f} DD {s['MaxDD']:7.2%} "
          f"H {s['H1']:.3f}/{s['H2']:.3f} OOS {s['OOS_CAGR']:6.2%}/{s['OOS_Sharpe']:.3f}/{s['OOS_MaxDD']:7.2%}")
        P(f"   {'':9s} v1   CAGR {b['CAGR']:6.2%} Sh {b['Sharpe']:.3f} DD {b['MaxDD']:7.2%} "
          f"H {b['H1']:.3f}/{b['H2']:.3f} OOS {b['OOS_CAGR']:6.2%}/{b['OOS_Sharpe']:.3f}/{b['OOS_MaxDD']:7.2%}")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b]")
    u0 = [u for u in units if u.unit == "U56" and u.corpus == "A"][0]
    okA = check_a(u0.px.index)
    okB = check_b(u0.px, u0.w)
    if not (okA and okB):
        P("*** [a]/[b] FAILED - stopping.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ------------------------------------------------ the sweep
    P("SWEEPING CADENCE x PHASE OVER ALL FOUR CORPORA ...")
    rows = []
    pa_ret = {}          # (corpus, unit, cad) -> running sum of net returns over phases, count
    for i, u in enumerate(units):
        st = START[u.panel]
        sp = SPYM[u.panel]
        bs = BASE[u.panel]
        for cad in u.ladder:
            phs = phases_for(cad)
            acc = None
            for (sh, off) in phs:
                g, t = fast_backtest(u.px, u.w, cad, sh, off)
                r = (g - t * u.cost / 1e4).loc[st:]
                rm = row_metrics(r)
                acc = r.values.copy() if acc is None else acc + r.values
                rows.append(dict(corpus=u.corpus, cell=u.cell, unit=u.unit, panel=u.panel,
                                 cost=u.cost, point=cad, shift=sh, off=off,
                                 is_phase0=(sh == 0 and off == 0),
                                 turnover=t.loc[st:].sum() / (len(r) / 252), **rm,
                                 fail4a=keep_4a(rm, bs["H1"], bs["H2"], bs["MaxDD"]),
                                 fail4b=keep_4b(rm, sp)))
            pa_ret[(u.corpus, u.unit, cad)] = pd.Series(acc / len(phs), index=r.index)
        if (i + 1) % 25 == 0:
            P(f"   ... {i+1}/{len(units)} units  ({time.time()-t0:.0f}s)")
    R = pd.DataFrame(rows)
    R.to_csv(OUT / f"{STEM}.rows.csv", index=False)
    P(f"   {len(R)} (unit, cadence, phase) rows -> {STEM}.rows.csv   ({time.time()-t0:.0f}s)")
    P("")

    # ------------------------------------------------ control [c] per corpus, [d]
    P("REPRODUCTION CONTROL [c] - phase-(0,0) rows must equal the committed parent CSVs")
    audited = {}
    p0 = R[R.is_phase0]

    def rep(corpus, got, want, label):
        m = got.merge(want, on=["k", "point"], how="inner", suffixes=("_n", "_o"))
        d = float((m["v_n"] - m["v_o"]).abs().max()) if len(m) else np.nan
        ok = len(m) == len(want) and len(m) == len(got) and np.isfinite(d) and d < 1e-9
        P(f"  [c] corpus {corpus} vs {label}: matched {len(m)}/{len(want)} parent rows, "
          f"max|d| = {d:.3e} -> {'AUDITED' if ok else 'NOT AUDITED'}")
        audited[corpus] = ok
        return ok

    a_old = pd.read_csv(OUT / f"{P175}.ladder.csv")[["book", "point", "OOS_Sharpe"]]
    a_old.columns = ["k", "point", "v"]
    a_new = p0[p0.corpus == "A"][["unit", "point", "OOS_Sharpe"]]
    a_new.columns = ["k", "point", "v"]
    rep("A", a_new, a_old, f"{P175}.ladder.csv (OOS_Sharpe)")

    b_all = pd.read_csv(OUT / f"{P171}.ladder.csv")
    b_old = b_all[b_all.dial == "CADENCE"][["book", "point", "OOS_Sharpe"]]
    b_old.columns = ["k", "point", "v"]
    b_new = p0[p0.corpus == "B"][["unit", "point", "OOS_Sharpe"]]
    b_new.columns = ["k", "point", "v"]
    rep("B", b_new, b_old, f"{P171}.ladder.csv CADENCE dial (OOS_Sharpe)")

    c_all = pd.read_csv(OUT / f"{P173}.grid.csv")
    c_old = c_all[c_all.ladder == "CADENCE"].copy()
    c_old["k"] = c_old.panel + "|" + c_old.signal + "|" + c_old.cost.round().astype(int).astype(str)
    c_old = c_old[["k", "value", "Sharpe_F"]]
    c_old.columns = ["k", "point", "v"]
    c_new = p0[p0.corpus == "C"][["unit", "point", "Sharpe"]]
    c_new.columns = ["k", "point", "v"]
    rep("C", c_new, c_old, f"{P173}.grid.csv CADENCE ladder (full-sample Sharpe)")

    d_raw = pd.read_csv(OUT / f"{P101}.cadence.csv")
    d_old = d_raw.melt(id_vars=["universe", "arm", "f"],
                       value_vars=["Sharpe_D", "Sharpe_W", "Sharpe_M"], var_name="point",
                       value_name="v")
    d_old["point"] = d_old["point"].str.replace("Sharpe_", "", regex=False)
    d_old["k"] = d_old.universe + "|" + d_old.arm + "|" + d_old.f.map(lambda x: f"{x:.2f}")
    d_old = d_old[["k", "point", "v"]]
    d_new = p0[p0.corpus == "D"][["unit", "point", "Sharpe"]]
    d_new.columns = ["k", "point", "v"]
    rep("D", d_new, d_old, f"{P101}.cadence.csv (full-sample Sharpe)")

    P("")
    P("REPRODUCTION CONTROL [d] - the new phase machinery contains idea 187's as a special case")
    ph187 = OUT / f"{P187}.phase.csv"
    if ph187.exists():
        o = pd.read_csv(ph187)
        o = o[(o.cad == "6W")][["book", "phase", "OOS_Sharpe"]]
        n = R[(R.corpus == "A") & (R.point == "6W") & (R.off == 0)][["unit", "shift", "OOS_Sharpe"]]
        n.columns = ["book", "phase", "OOS_Sharpe"]
        m = o.merge(n, on=["book", "phase"], suffixes=("_o", "_n"))
        d = float((m.OOS_Sharpe_o - m.OOS_Sharpe_n).abs().max())
        P(f"  [d] cad=6W, off=0, shift sweep vs {P187}.phase.csv: matched {len(m)}/{len(o)} rows, "
          f"max|d| = {d:.3e} -> {'PASS' if (len(m)==len(o) and d < 1e-9) else 'FAIL'}")
    else:
        P("  [d] idea 187's .phase.csv not found -> control skipped")
    P("")

    # ------------------------------------------------ the phase spread, per corpus and point
    P("=" * 118)
    P("PHASE SPREAD AT A FIXED CADENCE (mean over the cell's units; nothing picked)")
    P("  'spread' = max-min of the cell-mean metric over the point's own phase grid.")
    P("")
    METRIC = {"A": "OOS_Sharpe", "B": "OOS_Sharpe", "C": "Sharpe", "D": "Sharpe"}
    for cp in "ABCD":
        sub = R[R.corpus == cp]
        if sub.empty:
            continue
        met = METRIC[cp]
        P(f"  corpus {cp}  (metric {met}, {'AUDITED' if audited.get(cp) else 'NOT AUDITED'})")
        P(f"  {'cell':16s} " + " ".join(f"{p:>13s}" for p in sub.point.unique()))
        for cell, g in sub.groupby("cell"):
            line = f"  {cell:16s} "
            for pt in sub.point.unique():
                gg = g[g.point == pt]
                if gg.empty:
                    line += f"{'-':>13s} "
                    continue
                piv = gg.pivot_table(index="unit", columns=["shift", "off"], values=met)
                mm = piv.mean()
                line += f"{mm.max()-mm.min():13.4f} "
            P(line)
        P("")

    # ------------------------------------------------ THE AUDIT
    P("=" * 118)
    P("THE AUDIT - every published pairwise cadence verdict, priced against its own phase spread")
    P(f"  SURVIVES  = sign(phase-averaged gap) == sign(phase-0 gap) AND sign_share >= {SIGN_BAR:.2f}")
    P("  (sign_share = fraction of phase_A x phase_B combinations preserving the published sign)")
    P("")
    claims = []
    for cp in "ABCD":
        if not audited.get(cp):
            continue
        sub = R[R.corpus == cp]
        met = METRIC[cp]
        pts = list(sub.point.unique())
        cells = list(sub.cell.unique())
        # for corpus A the parent also published pooled-over-all-books rows
        groups = [(c, sub[sub.cell == c]) for c in cells]
        if cp in ("A", "B"):
            groups = [("ALL", sub)] + groups
        for cell, g in groups:
            piv = {}
            for pt in pts:
                gg = g[g.point == pt]
                if gg.empty:
                    continue
                piv[pt] = gg.pivot_table(index="unit", columns=["shift", "off"], values=met).mean()
            avail = [p for p in pts if p in piv]
            for i in range(len(avail)):
                for j in range(i + 1, len(avail)):
                    A, B = avail[i], avail[j]
                    a, b = piv[A].values, piv[B].values
                    gap0 = float(piv[A][(0, 0)] - piv[B][(0, 0)])
                    gap_pa = float(a.mean() - b.mean())
                    D = a[:, None] - b[None, :]
                    s = np.sign(gap0)
                    sign_share = float((np.sign(D) == s).mean()) if s != 0 else np.nan
                    rng_ = float(D.max() - D.min())
                    surv = bool((np.sign(gap_pa) == s) and sign_share >= SIGN_BAR)
                    claims.append(dict(corpus=cp, cell=cell, metric=met, A=A, B=B, n_units=g.unit.nunique(),
                                       nphA=len(a), nphB=len(b), gap0=gap0, gap_pa=gap_pa,
                                       sign_share=sign_share, gap_range=rng_,
                                       ratio=abs(gap0) / rng_ if rng_ else np.inf,
                                       survives=surv, survives_weak=bool(np.sign(gap_pa) == s)))
    CL = pd.DataFrame(claims)
    CL.to_csv(OUT / f"{STEM}.claims.csv", index=False)
    P(f"  {len(CL)} published pairwise cadence verdicts recovered and re-priced")
    P("")
    P(f"  {'corpus':7s} {'cells':>6s} {'claims':>7s} {'SURVIVE':>8s} {'share':>7s} {'weak':>6s} "
      f"{'wk share':>9s} {'median |gap0|':>14s} {'median range':>13s} {'median ratio':>13s}")
    summ = []
    for cp in ["A", "B", "C", "D", "ALL"]:
        s = CL if cp == "ALL" else CL[CL.corpus == cp]
        if s.empty:
            P(f"  {cp:7s} {'-':>6s} {'-':>7s}   (not audited / no claims)")
            summ.append(dict(corpus=cp, claims=0, survives=0, share=np.nan))
            continue
        P(f"  {cp:7s} {s.cell.nunique():6d} {len(s):7d} {int(s.survives.sum()):8d} "
          f"{s.survives.mean():7.1%} {int(s.survives_weak.sum()):6d} {s.survives_weak.mean():9.1%} "
          f"{s.gap0.abs().median():14.4f} {s.gap_range.median():13.4f} {s.ratio.median():13.3f}")
        summ.append(dict(corpus=cp, cells=s.cell.nunique(), claims=len(s),
                         survives=int(s.survives.sum()), share=float(s.survives.mean()),
                         survives_weak=int(s.survives_weak.sum()),
                         weak_share=float(s.survives_weak.mean()),
                         median_abs_gap0=float(s.gap0.abs().median()),
                         median_gap_range=float(s.gap_range.median()),
                         median_ratio=float(s.ratio.median())))
    pd.DataFrame(summ).to_csv(OUT / f"{STEM}.summary.csv", index=False)
    P("")
    P("  the record's headline cadence claims, individually (corpus A, pooled and by family):")
    hd = CL[(CL.corpus == "A") & (CL.A.isin(["W", "M"])) & (CL.B.isin(["M", "6W", "Q"]))]
    P(f"  {'cell':10s} {'pair':10s} {'gap0':>9s} {'gap_pa':>9s} {'sign share':>11s} "
      f"{'phase range':>12s} {'ratio':>7s}  survives")
    for _, r in hd.sort_values(["cell", "A", "B"]).iterrows():
        P(f"  {r.cell:10s} {r.A+'-'+r.B:10s} {r.gap0:+9.4f} {r.gap_pa:+9.4f} {r.sign_share:11.1%} "
          f"{r.gap_range:12.4f} {r.ratio:7.3f}  {'YES' if r.survives else 'no'}")
    P("")
    P("  worst-hit and best-held verdicts overall (by sign share):")
    for lab, s in [("weakest 8", CL.nsmallest(8, "sign_share")), ("strongest 5", CL.nlargest(5, "sign_share"))]:
        P(f"   {lab}:")
        for _, r in s.iterrows():
            P(f"     {r.corpus} {r.cell:18s} {r.A+'-'+r.B:8s} gap0 {r.gap0:+8.4f}  pa {r.gap_pa:+8.4f}  "
              f"sign {r.sign_share:6.1%}  range {r.gap_range:8.4f}")
    P("")

    # ---- idea 101's cadence BAR, audited as a verdict in its own right
    if audited.get("D"):
        P("  IDEA 101's CADENCE-INSENSITIVITY BAR (idea 65: |dSharpe| across D/W/M <= 0.05)")
        P(f"  {'cell':18s} {'phase-0 spread':>15s} {'published pass':>15s} "
          f"{'spread incl. phase':>19s} {'pass':>6s}")
        for cell, g in R[R.corpus == "D"].groupby("cell"):
            p0m = g[g.is_phase0].set_index("point")["Sharpe"]
            sp0 = float(p0m.max() - p0m.min())
            allm = g["Sharpe"]
            spA = float(allm.max() - allm.min())
            P(f"  {cell:18s} {sp0:15.4f} {str(sp0 <= 0.05):>15s} {spA:19.4f} {str(spA <= 0.05):>6s}")
        P("")

    # ---- idea 188's family-split verdict (SMALL wants M, large caps want 6W)
    if audited.get("A"):
        P("  IDEA 188's FAMILY-SPLIT VERDICT - the argmax cadence per family, phase-0 vs phase-averaged")
        P(f"  {'family':8s} {'phase-0 argmax':>15s} {'phase-avg argmax':>17s} {'same':>6s}")
        for fam, g in R[R.corpus == "A"].groupby("cell"):
            a0 = g[g.is_phase0].groupby("point")["OOS_Sharpe"].mean().idxmax()
            ap = g.groupby("point")["OOS_Sharpe"].mean().idxmax()
            P(f"  {fam:8s} {a0:>15s} {ap:>17s} {str(a0==ap):>6s}")
        P("")

    # ------------------------------------------------ rule 8 walk-forward
    P("=" * 118)
    P("PROTOCOL RULE 8 WALK-FORWARD - cadence and phase chosen on <= 2016-12-31, OOS read once")
    P("  CONST-W0 = W at phase 0 (incumbent) | REC = cadence by IS Sharpe AT PHASE 0 (what the")
    P("  record does) | SEL-CP = cadence AND phase by IS Sharpe | PHASE-AVG = cadence by IS")
    P("  Sharpe of the equal-weight blend of all its phases, traded as that blend.")
    P("")
    wf_rows = []
    A = R[R.corpus == "A"]
    for unit, g in A.groupby("unit"):
        fam = g.cell.iloc[0]
        pan = g.panel.iloc[0]
        p0g = g[g.is_phase0].set_index("point")
        pa = {}
        for cad in g.point.unique():
            r = pa_ret[("A", unit, cad)]
            pa[cad] = row_metrics(r)
        pad = pd.DataFrame(pa).T
        sel = g.loc[g["IS_Sharpe"].idxmax()]
        picks = [
            ("CONST-W0", p0g.loc["W"], "W", "(0,0)"),
            ("REC", p0g.loc[p0g["IS_Sharpe"].idxmax()], p0g["IS_Sharpe"].idxmax(), "(0,0)"),
            ("SEL-CP", sel, sel["point"], f"({sel['shift']},{sel['off']})"),
            ("PHASE-AVG", pad.loc[pad["IS_Sharpe"].idxmax()], pad["IS_Sharpe"].idxmax(), "blend"),
        ]
        for arm, row, pt, ph in picks:
            wf_rows.append(dict(unit=unit, family=fam, panel=pan, arm=arm, point=pt, phase=ph,
                                OOS_Sharpe=row["OOS_Sharpe"], OOS_CAGR=row["OOS_CAGR"],
                                OOS_MaxDD=row["OOS_MaxDD"], IS_Sharpe=row["IS_Sharpe"]))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  {'family':8s} {'arm':10s} {'n':>4s} {'mean OOS CAGR':>14s} {'mean OOS Sharpe':>16s} "
      f"{'mean OOS MaxDD':>15s} {'vs CONST-W0':>12s} {'t':>7s}")
    for fam in ["ALL"] + sorted(A.cell.unique()):
        sel = WF if fam == "ALL" else WF[WF.family == fam]
        base = sel[sel.arm == "CONST-W0"].set_index("unit")["OOS_Sharpe"]
        for arm in ["CONST-W0", "REC", "SEL-CP", "PHASE-AVG"]:
            a = sel[sel.arm == arm].set_index("unit")
            d = (a["OOS_Sharpe"] - base).dropna()
            P(f"  {fam:8s} {arm:10s} {len(a):4d} {a.OOS_CAGR.mean():14.2%} {a.OOS_Sharpe.mean():16.3f} "
              f"{a.OOS_MaxDD.mean():15.2%} {d.mean():+12.4f} {tstat(d.values):+7.2f}")
        P("")
    for pk in ["U56", "SMALL"]:
        s, b = SPYM[pk], BASE[pk]
        P(f"  reference {pk:6s} OOS  SPY {s['OOS_CAGR']:7.2%}/{s['OOS_Sharpe']:.3f}/{s['OOS_MaxDD']:7.2%}"
          f"   RULES v1 {b['OOS_CAGR']:7.2%}/{b['OOS_Sharpe']:.3f}/{b['OOS_MaxDD']:7.2%}")
    P("")

    # ------------------------------------------------ KEEP paths
    P("=" * 118)
    P("BOTH KEEP PATHS on every corpus-A row (PROTOCOL rule 4a and 4b, exactly)")
    A2 = R[R.corpus == "A"].copy()
    A2["pass4a"] = A2.fail4a == "-"
    A2["pass4b"] = A2.fail4b == "-"
    A2.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'family':8s} {'rows':>6s} {'4a':>5s} {'4b':>5s} {'4b at phase 0':>14s} {'4b off-phase':>13s}")
    for fam in ["ALL"] + sorted(A2.cell.unique()):
        s = A2 if fam == "ALL" else A2[A2.cell == fam]
        P(f"  {fam:8s} {len(s):6d} {int(s.pass4a.sum()):5d} {int(s.pass4b.sum()):5d} "
          f"{int(s[s.is_phase0].pass4b.sum()):14d} {int(s[~s.is_phase0].pass4b.sum()):13d}")
    P("")
    fx = A2[A2.pass4b & A2.unit.isin(["SMALL439", "U56", "ETF36"])]
    if len(fx):
        P("  4b passes on the three FIXED panels:")
        for _, r in fx.sort_values("OOS_Sharpe", ascending=False).head(20).iterrows():
            P(f"   {r.unit:9s} @ {r.point:3s} phase({r['shift']},{r['off']}) CAGR {r.CAGR:6.2%} "
              f"Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:7.2%} halves {r.H1:.3f}/{r.H2:.3f} "
              f"OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}")
        P(f"   ({len(fx)} such rows in total; the phase is NOT a tradable choice, so a 4b pass that")
        P("    exists only off phase 0 is not a candidate - it is the measurement of the problem.)")
    else:
        P("  4b passes on the three FIXED panels: NONE.")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
