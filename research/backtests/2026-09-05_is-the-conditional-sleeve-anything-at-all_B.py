#!/usr/bin/env python3
"""QUEUE idea 190 - is-the-conditional-sleeve-anything-at-all  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 190)
    "idea 186 found the conditional TLT/GLD/UUP sleeve clears its rotation null in 0 of 36 points
     on Sharpe AND 0 of 36 on drawdown, i.e. an equally-frequent randomly-timed sleeve delivers
     the same MaxDD improvement (u56 ma=200/f=0.5: -14.07% vs the base's -18.21%, OOS Sharpe
     1.2333 vs 1.1775, all inside the null band).  527 LEADERBOARD rows mention a sleeve.
     Re-run the STATIC (always-on) sleeve of ideas 101/134 against the correct null for an
     always-on overlay - a random SUBSTITUTION of the sleeve assets, since rotation is degenerate
     at on-share 1.0 - and report whether the static sleeve's separation survives.  This is the
     other half of idea 186."

WHY ROTATION IS DEGENERATE HERE, AND WHAT REPLACES IT.
    Idea 186's matched null for an OVERLAY is a circular rotation of its ON indicator s_t: it
    preserves the on-share and the episode structure exactly and destroys only WHEN the overlay
    fires.  A STATIC sleeve has s_t == 1 for every rebalance date, so every rotation of s returns
    the identical book and the null is not merely weak, it is the point mass at the real value.
    The free parameter a static sleeve actually has is not TIMING, it is WHICH ASSETS.  So its
    matched null is a random SUBSTITUTION: the same construction (idea 100/104's momentum-vote x
    risk-parity sleeve), the same share f, the same cadence, the same gross rescale, the same
    number of sleeve names k - drawn from a stated pool instead of being named TLT/GLD/UUP.
    That null preserves, exactly and by construction:
        * the always-on schedule (on-share 1.0 for real and null alike)
        * the sleeve's pre-rescale share f and its name count k
        * the base leg (1-f) x R20 and the rescale to gross 0.75
    and destroys only the one thing under test: the IDENTITY of the three (or four) assets.

TWO POOLS, both reported, because they answer two different questions.
    DIV   the 12 non-crypto members of universe.json's `bonds_fx_commod` group
          (TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBC UUP) minus the real sleeve's own members.
          The sharp question: among liquid non-equity diversifiers, is TLT/GLD/UUP special?
          THE POPULATION IS ENUMERABLE - C(9,3) = 84 for S3, C(8,4) = 70 for S4 - so this run
          ENUMERATES IT WHOLE and reports an EXACT percentile, with no seed and no draw band.
          That is idea 208's proposal 11b applied at the first opportunity after it was written.
    ALL   every price column on the panel except SPY and the real members.  The loose question:
          is the sleeve distinguishable from an arbitrary 3-name carve-out (mostly equities)?
          C(55,3) is not enumerable, so 200 draws from an INT-LITERAL seed (idea 208's proposal 5:
          no hash() of a str anywhere; the seed is printed).

THE THIRD ARM THE NULL CANNOT SUPPLY - a cash carve-out.
    The substitution null holds the CONSTRUCTION fixed, so it cannot tell us whether the sleeve
    assets do anything beyond reducing equity exposure.  CASH-f does: weights (1-f) x R20 with NO
    rescale, i.e. mean gross 0.75 x (1-f).  If CASH-f captures the sleeve's drawdown improvement,
    the sleeve is a de-grossing lever (ideas 66/184: gross carries no Sharpe content) wearing
    three tickers.  Reported beside every real row.

CORPUS.  Static-sleeve books exactly as ideas 101/133/134 built them, IMPORTED not re-typed from
    research/backtests/2026-09-05_sleeve-f-that-clears-the-floor_cloud.py:
        R20      top-20 equal weight on the scan.py composite, gross 0.75, weekly, t+1
        S3-f     (1-f) x R20 + f x sleeve(TLT, GLD, UUP),      rescaled to gross 0.75
        S4-f     (1-f) x R20 + f x sleeve(TLT, GLD, DBC, UUP), rescaled to gross 0.75
        sleeve   = momentum-vote x risk-parity over the sleeve's own members (ideas 100/104)
    Panels U56 and BROAD136.  SMALL439 is OUT OF SCOPE and the reason is stated rather than
    buried: the static-sleeve corpus was published on u56/broad only, and joining diversifier
    ETFs to the small panel would put them in the composite's ranking pool and change the base
    book itself.  Ideas 136/186 found the small panel contributes 0 of 36 on both KEEP paths.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.  ALL grid points reported.
    1. sleeve share f    in {0.10, 0.20, 0.50}   (all three are published points of idea 134's FS)
    2. sleeve asset set  in {S3, S4}             (ideas 101 and 102)
    => 6 points per (panel, base-n, cost rung).  PANEL, BASE BOOK SIZE n in {10, 20, 40} and COST
    RUNG in {10, 25} are CARRIED AXES, not tuned: nothing is ever selected on them, every level is
    reported, and the rule-8 selector below chooses only over the 6 (f, set) points inside a cell.

COSTS.  Every book is run ONCE at 0 bps; the 10 and 25 bps rungs are derived from the engine's own
    turnover series (r_net = r_gross - turnover * bps / 1e4).  Asserted exact in check [b].

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12.
    [b] the cost identity: 10 bps derived from the 0 bps run == a genuine 10 bps engine run.
    [c] this run's blended weights == the committed idea-134 `book_weights` for all 6 real points
        on both panels, max|delta| == 0.0.
    [d] this run's 12 real n=20 books reproduce the committed
        `2026-09-05_sleeve-f-that-clears-the-floor_cloud.grid.csv` control-arm rows (24 rows x 9
        metrics) to < 1e-12.
    [e] the null is matched BY CONSTRUCTION and it is checked: every draw's name count equals k,
        no draw contains a real member, and its realised gross equals the real book's on every
        rebalance date.  Two quantities the null does NOT match exactly are MEASURED and reported
        rather than assumed - the sleeve's realised ON-SHARE (the momentum vote can zero the
        sleeve leg on a date) and realised TURNOVER - which is the same honesty idea 186 applied
        to its rotation null's turnover.

WALK-FORWARD (PROTOCOL rule 8).  12 cells = 2 panels x 3 base-n x 2 cost rungs.  Everything is
    fitted on <= 2016-12-31; 2017-01-01..2026 is read ONCE.
        S0  do nothing            - R20, the untreated base book (the control)
        S1  IS-argmax sleeve      - the (f, set) point with the best IS Sharpe
        S2  clause-gated argmax   - the same argmax restricted to points whose IS |dSharpe| beats
                                    at least 95% of the ENUMERATED DIV null; abstain -> hold R20
                                    (idea 194's clause 8b: an abstaining arm IS do-nothing)
        S3  random sleeve         - the mean over the enumerated DIV null at S1's own (f, set)
        S4  cash carve-out        - CASH at S1's own f
        S5  IS-argmax SUBSTITUTE  - the triple in the enumerated DIV population with the best IS
                                    Sharpe at S1's own (f, k).  This is the arm that decides
                                    whether the named sleeve's standing in its own null is a
                                    property AVAILABLE OUT OF SAMPLE or a hindsight property of
                                    three assets that are famous because of this very sample.
                                    (S5 and the signed-percentile reading in [1] were added AFTER
                                    the first pass of this script, in response to what P2/P5 did;
                                    they are declared POST-HOC.  P7 below was written before any
                                    S5 number existed, but not before P1-P6 were scored.)
    OOS CAGR / Sharpe / MaxDD reported for every arm against RULES v1 and SPY on the same window,
    and both KEEP paths are re-evaluated on the OOS window for every arm - a Sharpe gain bought
    with CAGR is not a capital-worthy gain (PROTOCOL 4b), and this run says which it is.

BOTH KEEP PATHS (4a vs live RULES v1, 4b vs SPY) are evaluated on every real row, every null draw
    and every control, full sample and OOS window.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a]-[e] all hold.
    P2  The static sleeve does NOT clear the substitution null on Sharpe in most points: I expect
        the DIV-pool clear rate (real |dSharpe| above the 95th percentile of the enumerated
        population) below 40%, in line with idea 181's 32.8% for tilts and idea 186's 0/36 for
        the conditional sleeve.
    P3  The sleeve separates BETTER against the ALL pool than against the DIV pool, on both
        Sharpe and drawdown, because against mostly-equity substitutes the sleeve is being
        credited for being a bond/gold/dollar basket rather than for being THIS basket.  If so,
        the published sleeve rows are an ASSET-CLASS result and not an asset-selection one.
    P4  CASH-f captures at least half of the sleeve's MaxDD improvement over R20 at matched f,
        i.e. de-grossing is most of the mechanism (ideas 66/184).
    P5  Rule 8: neither S1 nor S2 beats S0 on mean paired OOS Sharpe - the thirteenth consecutive
        do-nothing result (ideas 110/132/151/166/171/174/175/181/186/194/201/208).
    P6  4b passes exist among the sleeve rows (idea 134 found a plateau) but a majority of them
        sit inside their own enumerated DIV null, i.e. the pass is a property of the carve-out
        and not of the assets.
    P7  (POST-HOC, written after P1-P6 were scored and before any S5 number existed) the IS-chosen
        SUBSTITUTE triple does not reproduce the named sleeve's OOS advantage - S5's mean OOS
        Sharpe comes in below S1's - because the named sleeve's standing at the top of its own
        full-sample population is a hindsight property, not one a chooser could have had in 2016.

CAVEATS carried, not buried
    * SURVIVORSHIP.  U56 and BROAD136 are current-constituent lists (idea 54).  Real and null
      draws inherit the bias identically, so the COMPARISON is unaffected; every LEVEL is not.
    * The DIV pool is itself a survivor list of instruments that existed and stayed liquid over
      2008-2026, and its members are the ones this project has always used.  An enumeration over
      a hand-picked pool is exact for that pool and says nothing about assets outside it.
    * The two pools overlap the ranked book: on u56 and broad the diversifier ETFs are also
      eligible for the top-20 composite, so a null draw can hold a name the base leg also holds.
      That is true of the REAL sleeve too and is therefore matched, not a defect.
    * Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.
    * Idea 144: an overlaid book is the same book with an instrument on it, not a new book.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .null.csv, .clause.csv,
.walkforward.csv, .keep.csv next to itself.
"""
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_is-the-conditional-sleeve-anything-at-all_B"
OUT = ROOT / "research" / "backtests"
I134 = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.py"
I134_GRID = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.grid.csv"

FREQ, GROSS = "W", 0.75
COST_RUNGS = [10.0, 25.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60
FS = [0.10, 0.20, 0.50]                 # tuned parameter 1
SETS = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}   # tuned parameter 2
NS = [10, 20, 40]                       # carried axis (base book size)
PANELS = ["u56", "broad"]               # carried axis
DIV_POOL = ["TLT", "IEF", "SHY", "HYG", "LQD", "TIP", "GLD", "SLV", "USO", "UNG", "DBC", "UUP"]
N_ALL_DRAWS = 200
SEED = 190_2026                         # int literal (idea 208 proposal 5); printed below
CLAUSE_Q = 0.95                         # the clause bar: real above this percentile of the null

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_tee = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SF = _load(I134, "i134")            # idea 134's committed static-sleeve construction
H = SF.H                            # idea 94's helper (composite, halves, pass4a)


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Vectorised equivalent of engine.backtest (idea 186's, imported by value not by reference
    so this script is standalone).  Asserted against the engine in check [a]."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]])          # decided at t, applied at t+1
    m = m.copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
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


def net(res, bps):
    return res["returns"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- books
def blend(ranked_w, sleeve_w, f):
    """(1-f) x ranked + f x sleeve, rescaled to GROSS.  Identical to idea 134's book_weights;
    asserted at 0.0 in check [c].  ranked_w is cached per (panel, n) so the composite is not
    recomputed for every one of the several thousand null draws."""
    base = (1 - f) * ranked_w + f * sleeve_w
    return base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def sleeve_of(px, assets):
    return SF.sleeve_weights(px, assets)


class Panel:
    def __init__(self, key):
        self.key = key
        self.px = load_universe(broad=(key == "broad"))
        missing = [t for t in DIV_POOL if t not in self.px.columns]
        if missing:
            raise RuntimeError(f"{key} lacks {missing}")
        self.start = self.px.index[260]
        self.spy = self.px["SPY"].pct_change().fillna(0.0).loc[self.start:]
        self.ranked = {n: SF.ranked(self.px, n) for n in NS}
        self.v1 = {c: backtest(self.px, rules_v1_weights(self.px), cost_bps=c,
                               freq=FREQ)["returns"].loc[self.start:] for c in COST_RUNGS}
        self.pool_all = [c for c in self.px.columns if c != "SPY"]
        self._sleeve_cache = {}

    def sleeve(self, assets):
        k = tuple(assets)
        if k not in self._sleeve_cache:
            self._sleeve_cache[k] = sleeve_of(self.px, assets)
        return self._sleeve_cache[k]


# ---------------------------------------------------------------- metrics
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def row_metrics(r):
    m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def fail4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b(r, spy):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# ---------------------------------------------------------------- reproduction
def checks(pans):
    ok = True
    P("\n[REPRODUCTION] asserted before any new number is read")
    for pan in pans:
        W = pan.ranked[20]
        a = backtest(pan.px, W, cost_bps=10.0, freq=FREQ)
        b = fast_backtest(pan.px, W, 10.0, FREQ)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        P(f"  [a] {pan.key:6s} fast_backtest vs engine.backtest: max|dret| {dr:.3e} "
          f"max|dturn| {dt:.3e} -> {'PASS' if dr < 1e-12 else 'FAIL'}")
        ok &= dr < 1e-12 and dt < 1e-10
        z = fast_backtest(pan.px, W, 0.0, FREQ)
        d = float((net(z, 10.0) - a["returns"]).abs().max())
        P(f"  [b] {pan.key:6s} cost identity 0->10 bps vs a genuine 10 bps run: max|d| {d:.3e} "
          f"-> {'PASS' if d < 1e-15 else 'FAIL'}")
        ok &= d < 1e-15
        worst = 0.0
        for sk, f in itertools.product(SETS, FS):
            mine = blend(pan.ranked[20], pan.sleeve(SETS[sk]), f)
            theirs = SF.book_weights(pan.px, f"{sk}-{int(f*100)}")
            worst = max(worst, float((mine - theirs.reindex(columns=mine.columns)).abs().max().max()))
        P(f"  [c] {pan.key:6s} blend() vs idea 134 book_weights over 6 points: max|d| {worst:.3e} "
          f"-> {'PASS' if worst == 0.0 else 'FAIL'}")
        ok &= worst == 0.0
    return ok


def check_d(pans, real_rows):
    """This run's n=20 real rows vs idea 134's committed grid.csv control-arm rows."""
    g = pd.read_csv(I134_GRID)
    g = g[(g.arm == "control") & (g.book != "R20")]
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    mine = real_rows[real_rows.n == 20].copy()
    mine["book"] = mine.set_ + "-" + (mine.f * 100).round().astype(int).astype(str)
    m = mine.merge(g, left_on=["panel", "book", "bps"], right_on=["panel", "book", "cost"],
                   suffixes=("", "_pub"))
    worst, worstcol = 0.0, ""
    for c in cols:
        d = float((m[c] - m[c + "_pub"]).abs().max())
        if d > worst:
            worst, worstcol = d, c
    P(f"  [d] {len(m)} of 24 committed control-arm rows matched; max|d| {worst:.3e} on "
      f"{worstcol or '-'} -> {'PASS' if (len(m) == 24 and worst < 1e-12) else 'FAIL'}")
    return len(m) == 24 and worst < 1e-12


# ---------------------------------------------------------------- null draws
def div_draws(assets):
    """The WHOLE enumerated substitution population from the DIV pool (idea 208 proposal 11b)."""
    pool = [t for t in DIV_POOL if t not in assets]
    return [list(c) for c in itertools.combinations(pool, len(assets))]


def all_draws(pan, assets, n_draws, seed):
    pool = [t for t in pan.pool_all if t not in assets]
    rng = np.random.default_rng(seed)
    seen, out = set(), []
    while len(out) < n_draws:
        d = tuple(sorted(rng.choice(len(pool), size=len(assets), replace=False).tolist()))
        if d in seen:
            continue
        seen.add(d)
        out.append([pool[i] for i in d])
    return out


def _sleeve_stats(pan, assets, f, reb):
    """(realised on-share, realised sleeve share of gross, realised turnover) for one asset set.
    on-share < 1 is possible because the momentum vote can zero the sleeve leg on a date."""
    sw = pan.sleeve(assets)
    W = blend(pan.ranked[20], sw, f)
    leg = (f * sw).sum(axis=1)
    pre = ((1 - f) * pan.ranked[20] + f * sw).sum(axis=1)
    on = (leg.iloc[reb] > 1e-12).mean()
    share = (leg.iloc[reb] / pre.iloc[reb].replace(0, np.nan)).dropna().mean()
    to = fast_backtest(pan.px, W, 0.0, FREQ)["turnover"].loc[pan.start:].sum()
    return float(on), float(share), float(to), W


def check_e(pan, assets, f, draws, n_probe=10):
    """The null is matched by construction where it claims to be, and MEASURED where it is not."""
    reb = np.flatnonzero(rebalance_mask(pan.px.index, FREQ).values)
    on_r, sh_r, to_r, Wr = _sleeve_stats(pan, assets, f, reb)
    gr = Wr.iloc[reb].sum(axis=1)
    hard = []          # invariants that must hold EXACTLY
    ons, shs, tos = [], [], []
    for d in draws[:n_probe]:
        hard.append(len(d) == len(assets))
        hard.append(not (set(d) & set(assets)))
        on_n, sh_n, to_n, Wn = _sleeve_stats(pan, d, f, reb)
        hard.append(float((Wn.iloc[reb].sum(axis=1) - gr).abs().max()) < 1e-12)
        ons.append(on_n); shs.append(sh_n); tos.append(to_n)
    ok = all(hard)
    P(f"  [e] {pan.key:6s} null match over {n_probe} draws x 3 exact invariants (name count, "
      f"disjoint from the real set, realised gross identical on every rebalance date): "
      f"{'PASS' if ok else 'FAIL'}")
    P(f"      gross on rebalance dates in [{gr.min():.4f}, {gr.max():.4f}] "
      f"(0.0 only on warm-up dates where no name is eligible, real and null alike)")
    P(f"      MEASURED, not assumed - sleeve on-share real {on_r:.4f} vs null "
      f"[{min(ons):.4f}, {max(ons):.4f}]; sleeve share of gross real {sh_r:.4f} vs null "
      f"[{min(shs):.4f}, {max(shs):.4f}]; turnover ratio null/real "
      f"[{min(tos)/to_r:.3f}, {max(tos)/to_r:.3f}]")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"=== idea 190  is-the-conditional-sleeve-anything-at-all  (lane B) ===")
    P(f"seed (int literal, no hash()): {SEED};  DIV pool {len(DIV_POOL)} names; "
      f"ALL-pool draws {N_ALL_DRAWS}; clause bar = {CLAUSE_Q:.0%} of the null population")
    P(f"tuned params: f in {FS} x set in {list(SETS)};  carried axes: panel {PANELS}, "
      f"base n {NS}, cost {COST_RUNGS}")

    pans = [Panel(k) for k in PANELS]
    for pan in pans:
        ms = metrics(pan.spy)
        s1, s2 = halves(pan.spy)
        P(f"\n[panel] {pan.key}: {pan.px.shape[1]} cols, {pan.px.index[0].date()}.."
          f"{pan.px.index[-1].date()}, eval from {pan.start.date()}")
        P(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
          f"halves {s1:.3f}/{s2:.3f} OOS {metrics(pan.spy.loc[OOS_START:])['Sharpe']:.3f} | "
          f"4b bars: MaxDD <= {DELTA*abs(ms['MaxDD']):.2%}, CAGR >= {PHI*ms['CAGR']:.2%}")
        for c in COST_RUNGS:
            v = pan.v1[c]
            P(f"    RULES v1 @{int(c)}bps: CAGR {metrics(v)['CAGR']:.2%} Sharpe "
              f"{metrics(v)['Sharpe']:.3f} MaxDD {metrics(v)['MaxDD']:.2%}")

    if not checks(pans):
        raise SystemExit("reproduction checks [a]-[c] failed - nothing below is trustworthy")

    # ---------------- real books, controls, and the two null populations ----------------
    rows, nulls, rets = [], [], {}
    nbt = 0
    for pan in pans:
        for n in NS:
            r20 = fast_backtest(pan.px, pan.ranked[n], 0.0, FREQ)
            nbt += 1
            for c in COST_RUNGS:
                r = net(r20, c).loc[pan.start:]
                rets[(pan.key, n, c, "R20", 0.0)] = r
                rows.append(dict(panel=pan.key, n=n, bps=c, kind="control", set_="R20", f=0.0,
                                 draw=-1, assets="-", turnover=r20["turnover"].loc[pan.start:].sum()
                                 / metrics(r)["Years"], **row_metrics(r),
                                 fail4a=fail4a(r, pan.v1[c]), fail4b=fail4b(r, pan.spy)))
            for f in FS:                                    # CASH-f control (de-grossing only)
                rc = fast_backtest(pan.px, (1 - f) * pan.ranked[n], 0.0, FREQ)
                nbt += 1
                for c in COST_RUNGS:
                    r = net(rc, c).loc[pan.start:]
                    rets[(pan.key, n, c, "CASH", f)] = r
                    rows.append(dict(panel=pan.key, n=n, bps=c, kind="cash", set_="CASH", f=f,
                                     draw=-1, assets="cash",
                                     turnover=rc["turnover"].loc[pan.start:].sum() / metrics(r)["Years"],
                                     **row_metrics(r), fail4a=fail4a(r, pan.v1[c]),
                                     fail4b=fail4b(r, pan.spy)))
            for sk, f in itertools.product(SETS, FS):
                assets = SETS[sk]
                W = blend(pan.ranked[n], pan.sleeve(assets), f)
                rr = fast_backtest(pan.px, W, 0.0, FREQ)
                nbt += 1
                for c in COST_RUNGS:
                    r = net(rr, c).loc[pan.start:]
                    rets[(pan.key, n, c, sk, f)] = r
                    rows.append(dict(panel=pan.key, n=n, bps=c, kind="real", set_=sk, f=f, draw=-1,
                                     assets="+".join(assets),
                                     turnover=rr["turnover"].loc[pan.start:].sum() / metrics(r)["Years"],
                                     **row_metrics(r), fail4a=fail4a(r, pan.v1[c]),
                                     fail4b=fail4b(r, pan.spy)))
                # ---- null populations ----
                specs = [("DIV", div_draws(assets))]
                if n == 20:
                    specs.append(("ALL", all_draws(pan, assets, N_ALL_DRAWS,
                                                   SEED + 1000 * PANELS.index(pan.key)
                                                   + 100 * list(SETS).index(sk) + FS.index(f))))
                for pool, draws in specs:
                    for j, d in enumerate(draws):
                        Wn = blend(pan.ranked[n], pan.sleeve(d), f)
                        rn = fast_backtest(pan.px, Wn, 0.0, FREQ)
                        nbt += 1
                        for c in COST_RUNGS:
                            r = net(rn, c).loc[pan.start:]
                            mm = metrics(r)
                            nulls.append(dict(panel=pan.key, n=n, bps=c, set_=sk, f=f, pool=pool,
                                              draw=j, assets="+".join(d), Sharpe=mm["Sharpe"],
                                              MaxDD=mm["MaxDD"], CAGR=mm["CAGR"],
                                              IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                              OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                              OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                              OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                              turnover=rn["turnover"].loc[pan.start:].sum() / mm["Years"],
                                              fail4b=fail4b(r, pan.spy),
                                              fail4a=fail4a(r, pan.v1[c])))
            P(f"    ... {pan.key} n={n} done, {nbt} genuine backtests, {time.time()-t0:.0f}s")

    G = pd.DataFrame(rows)
    NU = pd.DataFrame(nulls)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    NU.to_csv(OUT / f"{STEM}.null.csv", index=False)
    P(f"\n[corpus] {nbt} genuine backtests -> {len(G)} real/control rows, {len(NU)} null rows "
      f"({time.time()-t0:.0f}s)")

    ok_d = check_d(pans, G[G.kind == "real"])
    if not ok_d:
        P("  [d] FAILED - this run's books are not idea 134's books; everything below is void")
        raise SystemExit("reproduction check [d] failed")
    ok_e = all(check_e(pan, SETS["S3"], 0.20, div_draws(SETS["S3"])) for pan in pans)

    # ---------------- the clause: where does the real sleeve sit in its null? -------------
    P("\n[1] THE SUBSTITUTION NULL.  For every real point, the real effect vs R20 is placed in the")
    P("    null population of the SAME construction with substituted assets.  DIV is ENUMERATED")
    P("    (exact percentile, no seed); ALL is 200 seeded draws (n=20 only).")
    cl = []
    for _, rr in G[G.kind == "real"].iterrows():
        base = rets[(rr.panel, rr.n, rr.bps, "R20", 0.0)]
        mb = metrics(base)
        dS, dD = rr.Sharpe - mb["Sharpe"], abs(mb["MaxDD"]) - abs(rr.MaxDD)   # dD>0 = less DD
        mbi = metrics(base.loc[:IS_END])["Sharpe"]
        mbo = metrics(base.loc[OOS_START:])["Sharpe"]
        sub = NU[(NU.panel == rr.panel) & (NU.n == rr.n) & (NU.bps == rr.bps)
                 & (NU.set_ == rr.set_) & (NU.f == rr.f)]
        for pool in sorted(sub.pool.unique()):
            q = sub[sub.pool == pool]
            nS = q.Sharpe.values - mb["Sharpe"]
            nD = abs(mb["MaxDD"]) - q.MaxDD.abs().values
            pctS = float((np.abs(nS) < abs(dS)).mean())
            pctD = float((nD < dD).mean())
            pctS_signed = float((nS < dS).mean())
            pct_IS = float((q.IS_Sharpe.values - mbi < rr.IS_Sharpe - mbi).mean())
            pct_OOS = float((q.OOS_Sharpe.values - mbo < rr.OOS_Sharpe - mbo).mean())
            cl.append(dict(panel=rr.panel, n=rr.n, bps=rr.bps, set_=rr.set_, f=rr.f, pool=pool,
                           npop=len(q), dSharpe=dS, dMaxDD=dD,
                           pct_signed_IS=pct_IS, pct_signed_OOS=pct_OOS,
                           argmax_full=bool(dS > nS.max()), argmax_IS=bool(pct_IS == 1.0),
                           argmax_OOS=bool(pct_OOS == 1.0),
                           null_dS_mean=float(nS.mean()), null_dS_sd=float(nS.std(ddof=1)),
                           null_dS_absmax=float(np.abs(nS).max()),
                           null_dD_mean=float(nD.mean()), null_dD_max=float(nD.max()),
                           pct_absSharpe=pctS, pct_signedSharpe=pctS_signed, pct_MaxDD=pctD,
                           clears_S=bool(pctS >= CLAUSE_Q), clears_D=bool(pctD >= CLAUSE_Q),
                           clears_S_strict=bool(abs(dS) > np.abs(nS).max()),
                           clears_D_strict=bool(dD > nD.max())))
    CL = pd.DataFrame(cl)
    CL.to_csv(OUT / f"{STEM}.clause.csv", index=False)
    for pool in ["DIV", "ALL"]:
        q = CL[CL.pool == pool]
        if not len(q):
            continue
        P(f"\n    pool {pool}: {len(q)} real points against populations of "
          f"{sorted(q.npop.unique())} draws")
        P(f"      clears on |dSharpe| (>= {CLAUSE_Q:.0%} of the null): "
          f"{int(q.clears_S.sum())}/{len(q)} = {q.clears_S.mean():.1%}   "
          f"[strict 'above every draw': {int(q.clears_S_strict.sum())}/{len(q)}]")
        P(f"      clears on  dMaxDD  (>= {CLAUSE_Q:.0%} of the null): "
          f"{int(q.clears_D.sum())}/{len(q)} = {q.clears_D.mean():.1%}   "
          f"[strict: {int(q.clears_D_strict.sum())}/{len(q)}]")
        P(f"      mean percentile of the real point: |dSharpe| {q.pct_absSharpe.mean():.3f}, "
          f"signed dSharpe {q.pct_signedSharpe.mean():.3f}, dMaxDD {q.pct_MaxDD.mean():.3f}")
        P(f"      mean real dSharpe {q.dSharpe.mean():+.4f} vs null mean {q.null_dS_mean.mean():+.4f}"
          f" (null |dS| max {q.null_dS_absmax.mean():.4f});  mean real dMaxDD "
          f"{q.dMaxDD.mean():+.4f} vs null mean {q.null_dD_mean.mean():+.4f}")
        P(f"      SIGNED reading (post-hoc, see [1b]): the real sleeve is the STRICT ARGMAX of its "
          f"own population in {int(q.argmax_full.sum())}/{len(q)} points full-sample, "
          f"{int(q.argmax_IS.sum())}/{len(q)} on the IS window and {int(q.argmax_OOS.sum())}/{len(q)}"
          f" on the OOS window; mean signed percentile IS {q.pct_signed_IS.mean():.3f}, "
          f"OOS {q.pct_signed_OOS.mean():.3f}")
    P("\n    per-point table (n=20 rows, both pools):")
    show = CL[CL.n == 20].sort_values(["panel", "bps", "set_", "f", "pool"])
    P(show[["panel", "bps", "set_", "f", "pool", "npop", "dSharpe", "dMaxDD", "null_dS_mean",
            "null_dS_absmax", "pct_absSharpe", "pct_MaxDD", "clears_S", "clears_D"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[1b] WHY THE TWO-SIDED CLAUSE AND THE SIGNED READING DISAGREE (post-hoc, declared).")
    P("     Ideas 181/186 clear a clause when |dSharpe(real)| exceeds every null draw.  For an")
    P("     instrument whose null draws are mostly HARMFUL that statistic is perverse: a")
    P("     substitute that destroys 0.27 of Sharpe has a larger |dSharpe| than the real sleeve's")
    P("     +0.10 and blocks it.  The numbers this run can put on that:")
    for pool in ["DIV", "ALL"]:
        q = CL[CL.pool == pool]
        if not len(q):
            continue
        harm = float((q.null_dS_mean < 0).mean())
        P(f"       pool {pool}: null mean dSharpe is negative in {harm:.1%} of points; two-sided "
          f"clear {q.clears_S.mean():.1%} vs signed argmax {q.argmax_full.mean():.1%} "
          f"(mean signed percentile {q.pct_signedSharpe.mean():.3f})")
    P("     The signed reading is NOT evidence the sleeve was chosen well - it is exactly what")
    P("     picking three assets with 2008-2026 in view produces.  The arm that tells them apart")
    P("     is S5 in [4], which picks the triple on the IS window alone.")

    # ---------------- the cash arm: is it de-grossing? ----------------
    P("\n[2] THE CASH CONTROL.  Sleeve vs a cash carve-out at the same f (no rescale), both vs R20.")
    cash = []
    for (pan_k, n, c, sk, f), r in rets.items():
        if sk in ("R20", "CASH"):
            continue
        base = rets[(pan_k, n, c, "R20", 0.0)]
        ca = rets[(pan_k, n, c, "CASH", f)]
        mb, mc, mr = metrics(base), metrics(ca), metrics(r)
        cash.append(dict(panel=pan_k, n=n, bps=c, set_=sk, f=f,
                         dS_sleeve=mr["Sharpe"] - mb["Sharpe"], dS_cash=mc["Sharpe"] - mb["Sharpe"],
                         dD_sleeve=abs(mb["MaxDD"]) - abs(mr["MaxDD"]),
                         dD_cash=abs(mb["MaxDD"]) - abs(mc["MaxDD"]),
                         dC_sleeve=mr["CAGR"] - mb["CAGR"], dC_cash=mc["CAGR"] - mb["CAGR"]))
    CA = pd.DataFrame(cash)
    CA["dd_share"] = CA.dD_cash / CA.dD_sleeve.replace(0, np.nan)
    P(f"    mean dSharpe vs R20:  sleeve {CA.dS_sleeve.mean():+.4f}  cash {CA.dS_cash.mean():+.4f}"
      f"   (sleeve better in {int((CA.dS_sleeve > CA.dS_cash).sum())}/{len(CA)})")
    P(f"    mean dMaxDD  vs R20:  sleeve {CA.dD_sleeve.mean():+.4f}  cash {CA.dD_cash.mean():+.4f}"
      f"   -> cash captures {CA.dd_share.median():.1%} of the sleeve's drawdown gain (median)")
    P(f"    mean dCAGR   vs R20:  sleeve {CA.dC_sleeve.mean():+.4%}  cash {CA.dC_cash.mean():+.4%}")
    P("    by f:")
    P(CA.groupby("f")[["dS_sleeve", "dS_cash", "dD_sleeve", "dD_cash", "dd_share"]].mean()
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------- KEEP paths ----------------
    P("\n[3] BOTH KEEP PATHS on every real row, control and null draw.")
    real = G[G.kind == "real"]
    ctl = G[G.kind == "control"]
    csh = G[G.kind == "cash"]
    P(f"    real sleeve rows:  4a {int((real.fail4a=='-').sum())}/{len(real)}   "
      f"4b {int((real.fail4b=='-').sum())}/{len(real)}")
    P(f"    R20 controls:      4a {int((ctl.fail4a=='-').sum())}/{len(ctl)}   "
      f"4b {int((ctl.fail4b=='-').sum())}/{len(ctl)}")
    P(f"    CASH controls:     4a {int((csh.fail4a=='-').sum())}/{len(csh)}   "
      f"4b {int((csh.fail4b=='-').sum())}/{len(csh)}")
    P(f"    null draws:        4a {int((NU.fail4a=='-').sum())}/{len(NU)} = "
      f"{(NU.fail4a=='-').mean():.1%}   4b {int((NU.fail4b=='-').sum())}/{len(NU)} = "
      f"{(NU.fail4b=='-').mean():.1%}")
    P("    real 4b failing-bar census (idea 177's column):")
    P("      " + ", ".join(f"{k}:{v}" for k, v in real.fail4b.value_counts().items()))
    kp = real[real.fail4b == "-"]
    if len(kp):
        P(f"\n    the {len(kp)} real rows that PASS 4b, with their own DIV percentile:")
        mm = kp.merge(CL[CL.pool == "DIV"], on=["panel", "n", "bps", "set_", "f"])
        P(mm[["panel", "n", "bps", "set_", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe", "pct_absSharpe", "pct_MaxDD", "clears_S", "clears_D"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"    of those {len(mm)} 4b passes, {int(mm.clears_S.sum())} clear the enumerated DIV null "
          f"on Sharpe and {int(mm.clears_D.sum())} on drawdown")
        nb = NU[NU.fail4b == "-"]
        P(f"    null draws that pass 4b: {len(nb)}/{len(NU)} = {len(nb)/max(len(NU),1):.1%} "
          f"(real rate {(real.fail4b=='-').mean():.1%}) - a substituted sleeve reaches 4b "
          f"{'MORE' if len(nb)/max(len(NU),1) > (real.fail4b=='-').mean() else 'LESS'} often")
    G[["panel", "n", "bps", "kind", "set_", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover", "fail4a", "fail4b"]].to_csv(
        OUT / f"{STEM}.keep.csv", index=False)

    # ---------------- rule 8 ----------------
    P("\n[4] RULE 8 WALK-FORWARD.  Everything fitted on <= 2016-12-31; 2017-2026 read ONCE.")
    P("    12 cells = 2 panels x 3 base-n x 2 cost rungs.  S0 do-nothing, S1 IS-argmax sleeve,")
    P("    S2 clause-gated argmax (abstain -> hold R20), S3 random-sleeve mean, S4 cash at S1's f.")
    wf = []
    for pan in pans:
        for n in NS:
            for c in COST_RUNGS:
                base = rets[(pan.key, n, c, "R20", 0.0)]
                cand = [(sk, f) for sk in SETS for f in FS]
                isS = {(sk, f): metrics(rets[(pan.key, n, c, sk, f)].loc[:IS_END])["Sharpe"]
                       for sk, f in cand}
                pick = max(cand, key=lambda k: isS[k])
                # S2: the clause read on the IS WINDOW only
                mbi = metrics(base.loc[:IS_END])["Sharpe"]
                gated = []
                for sk, f in cand:
                    q = NU[(NU.panel == pan.key) & (NU.n == n) & (NU.bps == c) & (NU.set_ == sk)
                           & (NU.f == f) & (NU.pool == "DIV")]
                    d = isS[(sk, f)] - mbi
                    nd = q.IS_Sharpe.values - mbi
                    if float((np.abs(nd) < abs(d)).mean()) >= CLAUSE_Q:
                        gated.append((sk, f))
                pick2 = max(gated, key=lambda k: isS[k]) if gated else None
                oos = lambda r: metrics(r.loc[OOS_START:])                      # noqa: E731
                o0 = oos(base)
                o1 = oos(rets[(pan.key, n, c, pick[0], pick[1])])
                r2 = base if pick2 is None else rets[(pan.key, n, c, pick2[0], pick2[1])]
                o2 = oos(r2)
                q = NU[(NU.panel == pan.key) & (NU.n == n) & (NU.bps == c) & (NU.set_ == pick[0])
                       & (NU.f == pick[1]) & (NU.pool == "DIV")]
                o4 = oos(rets[(pan.key, n, c, "CASH", pick[1])])
                # S5: the SUBSTITUTE triple with the best IS Sharpe, at S1's own (f, k).
                s5 = q.loc[q.IS_Sharpe.idxmax()]
                v1o, spyo = oos(pan.v1[c]), oos(pan.spy)
                ob = dict(o0=o0, o1=o1, o2=o2, o4=o4)
                wf.append(dict(panel=pan.key, n=n, bps=c, pick=f"{pick[0]}-{pick[1]}",
                               pick2=("abstain" if pick2 is None else f"{pick2[0]}-{pick2[1]}"),
                               n_gated=len(gated), pick5=s5.assets,
                               S0=o0["Sharpe"], S1=o1["Sharpe"], S2=o2["Sharpe"],
                               S3=float(q.OOS_Sharpe.mean()), S4=o4["Sharpe"],
                               S5=float(s5.OOS_Sharpe),
                               S0_CAGR=o0["CAGR"], S1_CAGR=o1["CAGR"], S2_CAGR=o2["CAGR"],
                               S3_CAGR=float(q.OOS_CAGR.mean()), S4_CAGR=o4["CAGR"],
                               S5_CAGR=float(s5.OOS_CAGR),
                               S0_DD=o0["MaxDD"], S1_DD=o1["MaxDD"], S2_DD=o2["MaxDD"],
                               S3_DD=float(q.OOS_MaxDD.mean()), S4_DD=o4["MaxDD"],
                               S5_DD=float(s5.OOS_MaxDD),
                               **{f"{a}_4b": fail4b(rr_.loc[OOS_START:], pan.spy.loc[OOS_START:])
                                  for a, rr_ in [("S0", base),
                                                 ("S1", rets[(pan.key, n, c, pick[0], pick[1])]),
                                                 ("S2", r2),
                                                 ("S4", rets[(pan.key, n, c, "CASH", pick[1])])]},
                               **{f"{a}_4a": fail4a(rr_.loc[OOS_START:], pan.v1[c].loc[OOS_START:])
                                  for a, rr_ in [("S0", base),
                                                 ("S1", rets[(pan.key, n, c, pick[0], pick[1])]),
                                                 ("S2", r2),
                                                 ("S4", rets[(pan.key, n, c, "CASH", pick[1])])]},
                               S3_4b_rate=float((q.fail4b == "-").mean()),
                               v1_Sharpe=v1o["Sharpe"], v1_CAGR=v1o["CAGR"], v1_DD=v1o["MaxDD"],
                               spy_Sharpe=spyo["Sharpe"], spy_CAGR=spyo["CAGR"], spy_DD=spyo["MaxDD"]))
                _ = ob
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(WF[["panel", "n", "bps", "pick", "pick2", "n_gated", "pick5", "S0", "S1", "S2", "S3", "S4",
          "S5", "v1_Sharpe", "spy_Sharpe"]].to_string(index=False,
                                                     float_format=lambda x: f"{x:.4f}"))
    P("")
    for arm in ["S1", "S2", "S3", "S4", "S5"]:
        d = (WF[arm] - WF.S0).values
        P(f"    {arm} - S0 mean paired OOS Sharpe {d.mean():+.4f} (t {tstat(d):+.2f}), "
          f"wins {int((d > 0).sum())}/{len(d)};  mean OOS CAGR {WF[arm+'_CAGR'].mean():.2%} vs "
          f"S0 {WF.S0_CAGR.mean():.2%};  mean OOS MaxDD {WF[arm+'_DD'].mean():.2%} vs "
          f"S0 {WF.S0_DD.mean():.2%}")
    d51 = (WF.S5 - WF.S1).values
    P(f"    S5 - S1 (the whole asset-identity question) {d51.mean():+.4f} (t {tstat(d51):+.2f}), "
      f"S5 wins {int((d51 > 0).sum())}/{len(d51)};  S1 - S3 (named vs the average substitute) "
      f"{(WF.S1-WF.S3).mean():+.4f}")
    P("\n    BOTH KEEP PATHS on the OOS window itself (the bars that decide capital):")
    for arm in ["S0", "S1", "S2", "S4"]:
        P(f"      {arm}: 4a {int((WF[arm+'_4a']=='-').sum())}/12"
          f"   4b {int((WF[arm+'_4b']=='-').sum())}/12   "
          f"(4b failing bars: {', '.join(f'{k}:{v}' for k, v in WF[arm+'_4b'].value_counts().items())})")
    P(f"      S3: mean 4b pass rate over the enumerated substitutes at each cell's pick "
      f"{WF.S3_4b_rate.mean():.1%}")
    P(f"    S0 mean OOS Sharpe {WF.S0.mean():.4f} / CAGR {WF.S0_CAGR.mean():.2%} / "
      f"MaxDD {WF.S0_DD.mean():.2%}")
    P(f"    RULES v1 OOS  Sharpe {WF.v1_Sharpe.mean():.4f} / CAGR {WF.v1_CAGR.mean():.2%} / "
      f"MaxDD {WF.v1_DD.mean():.2%}   (per panel: " +
      ", ".join(f"{k} {v:.3f}" for k, v in WF.groupby('panel').v1_Sharpe.mean().items()) + ")")
    P(f"    SPY      OOS  Sharpe {WF.spy_Sharpe.mean():.4f} / CAGR {WF.spy_CAGR.mean():.2%} / "
      f"MaxDD {WF.spy_DD.mean():.2%}")

    # ---------------- predictions ----------------
    P("\n[5] PRE-REGISTERED PREDICTIONS, scored as they fell")
    divq, allq = CL[CL.pool == "DIV"], CL[CL.pool == "ALL"]
    p1 = bool(ok_d and ok_e)          # [a]-[c] already hard-stopped the run if they failed
    P(f"    P1 reproduction [a]-[e] hold -> {'HIT' if p1 else 'MISS'}")
    p2 = divq.clears_S.mean() < 0.40
    P(f"    P2 DIV Sharpe clear rate < 40%: {divq.clears_S.mean():.1%} -> {'HIT' if p2 else 'MISS'}")
    p3 = (allq.pct_absSharpe.mean() > divq[divq.n == 20].pct_absSharpe.mean()
          and allq.pct_MaxDD.mean() > divq[divq.n == 20].pct_MaxDD.mean())
    P(f"    P3 ALL pool separates better than DIV (n=20): |dSharpe| pct "
      f"{allq.pct_absSharpe.mean():.3f} vs {divq[divq.n==20].pct_absSharpe.mean():.3f}, dMaxDD pct "
      f"{allq.pct_MaxDD.mean():.3f} vs {divq[divq.n==20].pct_MaxDD.mean():.3f} -> "
      f"{'HIT' if p3 else 'MISS'}")
    p4 = CA.dd_share.median() >= 0.50
    P(f"    P4 cash captures >= 50% of the sleeve's dMaxDD: {CA.dd_share.median():.1%} -> "
      f"{'HIT' if p4 else 'MISS'}")
    d1, d2 = (WF.S1 - WF.S0).mean(), (WF.S2 - WF.S0).mean()
    p5 = d1 <= 0 and d2 <= 0
    P(f"    P5 neither S1 nor S2 beats S0: {d1:+.4f} / {d2:+.4f} -> {'HIT' if p5 else 'MISS'}")
    kp2 = real[real.fail4b == "-"]
    if len(kp2):
        mm2 = kp2.merge(CL[CL.pool == "DIV"], on=["panel", "n", "bps", "set_", "f"])
        p6 = len(mm2) > 0 and mm2.clears_S.mean() < 0.50
        P(f"    P6 4b passes exist and a majority sit inside their DIV null: {len(kp2)} passes, "
          f"{int(mm2.clears_S.sum())}/{len(mm2)} clear -> {'HIT' if p6 else 'MISS'}")
    else:
        p6 = False
        P(f"    P6 4b passes exist: 0 real rows pass 4b -> MISS")
    p7 = bool((WF.S5 - WF.S1).mean() < 0)
    P(f"    P7 (post-hoc) the IS-chosen substitute does not reproduce the named sleeve's OOS "
      f"advantage: S5 {WF.S5.mean():.4f} vs S1 {WF.S1.mean():.4f} "
      f"({(WF.S5-WF.S1).mean():+.4f}) -> {'HIT' if p7 else 'MISS'}")
    P(f"    -> {sum([p1,p2,p3,p4,p5,p6])} of 6 pre-registered predictions hit; P7 (post-hoc) "
      f"{'HIT' if p7 else 'MISS'}")

    P(f"\n[done] {nbt} genuine backtests in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
