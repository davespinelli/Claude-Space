#!/usr/bin/env python3
"""QUEUE idea 186 - the-null-column-for-instruments-that-are-not-keyed-tilts  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 186)
    "idea 181's census found 76 of 3315 leaderboard rows rest on a tilt's realised magnitude, but
     they are dominated by sleeve-separation, entry-budget and drawdown-control rows whose
     construction is NOT a keyed tilt and which idea 181 therefore did not re-run.  Define the
     matched null for an OVERLAY (a randomly-timed overlay with the same on-share and turnover)
     and re-price those rows against it.  Until this exists the proposed clause 11 covers only
     keyed tilts, and the memo says so."

WHAT IS AT STAKE.
    Idea 181 proposed PROTOCOL clause 11: an instrument's claimed effect must be reported against
    a MATCHED NULL of the same construction that carries no information, and the clause is
    "cleared" only when |dSharpe(real)| exceeds every one of N matched null draws.  It defined
    that null for exactly one construction - a KEYED TILT, where the null is a random key with
    the same tilt magnitude.  Most of this project's instruments are not keyed tilts.  They are
    OVERLAYS: a rule that watches some state, turns ON some of the time, and does something to
    the book while it is on (cut gross, skip the rebalance, shift into a defensive sleeve).
    For an overlay the obvious null is not a random key, it is RANDOM TIMING: intervene exactly
    as often, in exactly the same episode pattern, at the wrong times.

    That null is worth building because an overlay has a large free parameter the tilt does not:
    HOW OFTEN IT ACTS.  An overlay that is on 3% of the time in 2008 and 2020 looks like genius
    on a sample containing 2008 and 2020, and an overlay that is on 40% of the time is mostly a
    de-grossing lever (idea 66/184: gross is a scale lever with no Sharpe content).  Neither
    reading is available from the published dSharpe alone.

    SCOPE, stated up front so the result is not over-claimed.  This run prices the overlay
    CONSTRUCTIONS, not each of the individual published rows.  A keyword census of the committed
    LEADERBOARD (3330 data rows) finds 527 rows mentioning a sleeve, 54 a drawdown control or
    trailing stop, and 11 an entry/turnover budget.  Re-running 592 heterogeneous published rows
    is not what a run can do; re-pricing the three CONSTRUCTIONS they are built from, on the
    project's three panels and two cost rungs, is.  The memo says exactly this.

THE MATCHED NULL FOR AN OVERLAY (this run's definition, the deliverable idea 186 asks for)
    An overlay is a pair (s, A):  s_t in {0,1} evaluated at each rebalance date - the ON
    indicator, a function of state - and A, the action applied to the book while on.
    The MATCHED NULL is the same action A applied on a CIRCULAR ROTATION of s over the rebalance
    dates:  s~_j = s_{(j + d) mod J} for a random offset d.
    Rotation is the right null here because it preserves, EXACTLY and by construction:
        * the on-share       (identical count of on-dates)
        * the episode-length distribution and the number of on/off switches
        * therefore the overlay's own switching turnover budget
    and destroys only the one thing under test: WHEN the overlay fires relative to the market.
    A random permutation would not do this - it shatters episodes and inflates switching - and a
    random re-draw of the state variable would change the construction, not the timing.
    20 draws per cell, offsets from a fixed seed, offsets distinct and never 0 or J.
    Realised TURNOVER is not exactly preserved (the action's cost depends on the market state at
    the dates it fires), so it is MEASURED and reported rather than assumed - see .null.csv.

THE THREE OVERLAY FAMILIES - the three constructions idea 186 names.
    DDCTL   drawdown control (ideas 22/40/93):  ON when the base book's drawdown from its
            TRAILING 252-day high is <= -D;  action: scale gross by (1-k).
            Trailing-window high, not a running high-water mark: idea 93 established that a HWM
            re-entry condition is absorbing and must not be used.
    BUDGET  entry / turnover budget (idea 68's turnover-budget row):  ON at a rebalance date when
            the target-to-target turnover |w_t - w_prev| exceeds tau;  action: SKIP the rebalance
            entirely (mode 'skip') or move only half way to the target (mode 'half').
    SLEEVE  defensive sleeve, made conditional (ideas 101/102/134 + idea 75's conditional arming):
            ON when SPY is below its own MA(ma);  action: shift share f of the book into an equal
            split of TLT/GLD/UUP.
    Each family carries a 3 x 2 ladder = 6 points; all 18 points are reported for every panel.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.
    1. the overlay's THRESHOLD   (D / tau / ma), 3 values, all reported
    2. the overlay's DEPTH       (k / mode / f),  2 values, all reported
    FAMILY, PANEL and COST RUNG are corpus axes, not tuned parameters.  Nothing is picked for
    reporting; the rule-8 selector below is the only place a point is ever chosen, and it chooses
    on the IS window alone.

BASE BOOK, held fixed everywhere: idea 2's 4b candidate - top-20 equal weight on the scan.py
    composite with NO vol scaler, gross 0.75, weekly, t+1.  Panels U56, BROAD136, SMALL439
    (the 483-name sub-$2B panel with the 44 tickers whose data/small_meta.csv max_1d_move >= 1.0
    dropped first).  TLT/GLD/UUP are joined to BROAD136 and SMALL439 as untradable price columns
    so the SLEEVE family exists identically on all three panels.

COSTS.  Every book is run ONCE at 0 bps and the 10 and 25 bps rungs are derived exactly from the
    engine's own turnover series (port_net = port_gross - turnover * bps / 1e4, which is the
    engine's definition).  The identity is asserted to 0.0 in check_b(), so the two rungs are not
    an approximation.

WALK-FORWARD (PROTOCOL rule 8), the same three-arm design idea 181 used for keyed tilts:
    S0  do nothing            - the untreated base book (the control)
    S1  IS-argmax overlay     - the ladder point with the best IS Sharpe, chosen on <= 2016-12-31
    S2  clause-gated argmax   - the same argmax restricted to points that CLEAR the null clause
                                on the IS window
    18 cells (3 panels x 3 families x 2 cost rungs).  The 2017-2026 window is read once.

BOTH KEEP PATHS (4a and 4b) are evaluated exactly on every real and every null row.

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover.
    [b] the cost identity: deriving 10 bps from the 0 bps run reproduces a genuine 10 bps engine
        run to 0.0.
    [c] the base book's CAND-20 weights equal idea 78/171's weights_cand exactly.
    [d] the null is null BY CONSTRUCTION and it is checked: every null draw's on-share equals the
        real overlay's on-share exactly, and its switch count equals the real one exactly.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a]-[d] hold.
    P2  Most real overlays do NOT clear the clause.  I expect the clear rate to be below 40%,
        in line with idea 181's 32.8% for keyed tilts.
    P3  SLEEVE clears LEAST often of the three.  A static-ish defensive shift is close to a
        de-grossing lever, and idea 184 showed gross carries no Sharpe content, so its dSharpe
        should sit inside the null band.
    P4  DDCTL clears MOST often, because its ON indicator is a function of the book's own
        drawdown and therefore mechanically aligned with the drawdown it is measured on.
        (If DDCTL clears on Sharpe but its null draws match it on MaxDD, the clause is telling us
        the instrument is real for the wrong metric - reported either way.)
    P5  The clause moves few VERDICTS: I expect real-vs-null 4b verdict agreement above 80%,
        as idea 181 found (84.3% / 88.8% / 87.7%).
    P6  S2 does not beat S0.  Six consecutive project results (ideas 110/132/151/166/171/174,
        plus idea 175 today) say an IS-fitted selector does not earn its complexity, and idea
        181 specifically killed the clause-as-a-gate for tilts.
    P7  Null draws pass 4b at a rate within a factor of two of the real overlays', i.e. clearing
        a KEEP path is a property of the base book and the bars, not of the overlay's timing.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists (idea 54); SMALL439 contains
      no delistings at all.  Real and null draws inherit the bias identically, so the null
      COMPARISON is unaffected; the LEVEL of every number is not.
    * Rotation gives only J distinct nulls and neighbouring offsets are correlated; with 20 draws
      out of ~900 rebalance dates that is not binding, but the clause's nominal 1/21 = 4.8%
      one-sided size is approximate, not exact.
    * A rotation moves an overlay's episodes but cannot move the sample's crises.  An overlay that
      is on 40% of the time will have null draws that also cover 2020 - so the clause is a WEAKER
      test for high-on-share overlays than for rare ones.  On-share is reported alongside every
      clause result for exactly this reason.
    * Idea 38 (calendar-day index on U56/BROAD after 2014-09-17) and idea 126 (t+1 only) carry.
    * Idea 144: an overlaid book is the same book with an instrument on it, not a new book.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .null.csv, .clause.csv,
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

STEM = "2026-09-05_the-null-column-for-instruments-that-are-not-keyed-tilts_cloud"
OUT = ROOT / "research" / "backtests"

COST_RUNGS = [10, 25]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
FREQ = "W"
BASE_N, BASE_GROSS = 20, 0.75
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]
N_NULL = 20
SEED = 186_400

FAMILIES = {
    "DDCTL":  ("D",   [0.06, 0.10, 0.15], "k",    [0.50, 1.00]),
    "BUDGET": ("tau", [0.10, 0.20, 0.30], "mode", ["skip", "half"]),
    "SLEEVE": ("ma",  [100, 200, 300],    "f",    [0.50, 1.00]),
}
FAM_ORDER = ["DDCTL", "BUDGET", "SLEEVE"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    """Vectorised equivalent of engine.backtest.  `mask` (bool array over prices.index, True on
    rebalance days) overrides `freq`; that is how the BUDGET family skips a rebalance."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
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
    """The engine's own cost definition, applied to a 0 bps run.  Asserted exact in check_b()."""
    return res["returns"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- panels and base book
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, name, px, tradable):
        self.name = name
        self.px = px
        self.tradable = [c for c in px.columns if c in tradable]
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop:
            elig[drop] = False
        rank = comp_score(px).where(elig).rank(axis=1, ascending=False)
        self.W = (rank <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        self.sleeve_cols = [c for c in SLEEVE_ASSETS if c in px.columns]
        self.start = px.index[260]
        self.mask = rebalance_mask(px.index, FREQ).values
        self.reb = np.flatnonzero(self.mask)
        self.spy = px["SPY"].pct_change().fillna(0.0)
        # breadth of the panel's own tradables, kept for the DDCTL/SLEEVE state series
        self.ma200_spy = {m: px["SPY"] < px["SPY"].rolling(m).mean() for m in FAMILIES["SLEEVE"][1]}


def build_panels():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL: {len([c for c in pxs.columns if c!='SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable")

    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)

    def add_sleeve(px):
        a = ref[SLEEVE_ASSETS].reindex(px.index, method="ffill")
        return pd.concat([px.drop(columns=SLEEVE_ASSETS, errors="ignore"), a], axis=1).ffill()

    pxs = add_sleeve(pxs[s_stk + ["SPY"]])
    px136 = add_sleeve(px136)
    u_stk = [c for c in px56.columns if c != "SPY"]
    b_stk = [c for c in px136.columns if c != "SPY" and c not in SLEEVE_ASSETS]
    _ = crypto, U
    return [Panel("U56", px56, set(u_stk)),
            Panel("BROAD136", px136, set(b_stk)),
            Panel("SMALL439", pxs, set(s_stk))]


# ---------------------------------------------------------------- overlays
def on_indicator(pan, fam, thr):
    """The overlay's ON indicator, evaluated at the panel's rebalance dates.  Causal: every
    input is known at the date it is read, and the engine applies the weights at t+1."""
    idx = pan.px.index
    if fam == "DDCTL":
        r0 = fast_backtest(pan.px, pan.W, 0.0, FREQ)["returns"]
        eq = (1 + r0).cumprod()
        dd = eq / eq.rolling(252, min_periods=20).max() - 1
        s = (dd <= -thr).values
    elif fam == "BUDGET":
        w = pan.W.values[pan.reb]
        prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        tt = np.abs(w - prev).sum(axis=1)
        s = np.zeros(len(idx), bool)
        s[pan.reb] = tt > thr
        return s[pan.reb]
    elif fam == "SLEEVE":
        s = pan.ma200_spy[thr].values
    else:
        raise ValueError(fam)
    return s[pan.reb]


def apply_overlay(pan, fam, depth, s_reb):
    """Return (weights, mask) with the overlay's action applied on the ON rebalance dates."""
    idx = pan.px.index
    on = pd.Series(False, index=idx)
    on.iloc[pan.reb] = s_reb
    on = on.where(pd.Series(pan.mask, index=idx)).ffill().fillna(False).astype(bool)
    mask = pan.mask.copy()
    W = pan.W
    if fam == "DDCTL":
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0)
    elif fam == "BUDGET":
        if depth == "skip":
            mask = mask & ~np.isin(np.arange(len(idx)), pan.reb[s_reb])
        else:                                   # 'half': move half way to the target
            w = pan.W.values.copy()
            wr = w[pan.reb]
            for j in np.flatnonzero(s_reb):
                prev = wr[j - 1] if j > 0 else np.zeros(wr.shape[1])
                wr[j] = 0.5 * wr[j] + 0.5 * prev
            w[pan.reb] = wr
            W = pd.DataFrame(w, index=idx, columns=pan.W.columns)
    elif fam == "SLEEVE":
        if not pan.sleeve_cols:
            raise RuntimeError("no sleeve assets on panel")
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0).copy()
        add = np.where(on.values, depth * BASE_GROSS / len(pan.sleeve_cols), 0.0)
        for c in pan.sleeve_cols:
            W[c] = W[c].values + add
    return W, mask


def circ_switches(s):
    """Number of on/off transitions counted CIRCULARLY.  This is the quantity a circular
    rotation preserves exactly; the LINEAR count can differ by one at the wrap seam, which is
    reported separately as the one respect in which the matched null is not exact."""
    return int((np.asarray(s) != np.roll(np.asarray(s), 1)).sum())


def rotations(J, n, seed):
    rng = np.random.default_rng(seed)
    cand = rng.permutation(np.arange(1, J))
    return sorted(cand[:n].tolist())


# ---------------------------------------------------------------- metrics
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def keep_4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def keep_4b(r, spy):
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
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# ---------------------------------------------------------------- reproduction
def checks(pan):
    ok = True
    P("  [a] fast_backtest vs engine.backtest (products/backtester/engine.py):")
    a = backtest(pan.px, pan.W, cost_bps=10, freq=FREQ)
    b = fast_backtest(pan.px, pan.W, 10, FREQ)
    dr = float((a["returns"] - b["returns"]).abs().max())
    dt = float((a["turnover"] - b["turnover"]).abs().max())
    P(f"      {pan.name:9s} max|dret|={dr:.3e}  max|dturn|={dt:.3e}  -> {'PASS' if dr<1e-12 else 'FAIL'}")
    ok &= dr < 1e-12 and dt < 1e-10
    P("  [b] cost identity: 10 bps derived from the 0 bps run vs a genuine 10 bps engine run:")
    z = fast_backtest(pan.px, pan.W, 0.0, FREQ)
    d = float((net(z, 10) - a["returns"]).abs().max())
    P(f"      max|d|={d:.3e}  -> {'PASS' if d < 1e-15 else 'FAIL'}")
    ok &= d < 1e-15
    P("  [c] base CAND-20 weights vs idea 78/171 weights_cand:")
    _, above, vol20 = score(pan.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in pan.px.columns if c not in set(pan.tradable)]
    if drop:
        m[drop] = False
    s78 = score(pan.px, vol_scale=False)[0]
    w78 = (s78.where(m).rank(axis=1, ascending=False) <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
    dw = float((w78 - pan.W).abs().max().max())
    P(f"      {pan.name:9s} max|dw|={dw:.3e}  -> {'PASS' if dw < 1e-12 else 'FAIL'}")
    ok &= dw < 1e-12
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 186 - the-null-column-for-instruments-that-are-not-keyed-tilts   (cloud, {pd.Timestamp.today().date()})")
    P("=" * 122)
    P("Idea 181 defined PROTOCOL clause 11's matched null for a KEYED TILT only.  This run defines it")
    P("for an OVERLAY - same action, same on-share, same episode structure, RANDOM TIMING (a circular")
    P("rotation of the ON indicator over the rebalance dates) - and prices the three overlay families")
    P("the queue names: drawdown control, entry/turnover budget, defensive sleeve.")
    P(f"Base book: top-20 EW composite, no vol scaler, gross {BASE_GROSS}, weekly, t+1.  "
      f"Cost rungs {COST_RUNGS} bps derived exactly from one 0 bps run.")
    P(f"Two tuned params: overlay THRESHOLD (3) x overlay DEPTH (2) = 18 points per panel, all reported.")
    P(f"Nulls: {N_NULL} rotations per point, seed {SEED}.")
    P("")
    P("SCOPE (stated, not buried): this prices the three CONSTRUCTIONS, not each published row.")
    P("Keyword census of the committed LEADERBOARD (3330 data rows): 527 mention a sleeve, 54 a")
    P("drawdown control or trailing stop, 11 an entry/turnover budget.")
    P("")

    panels = build_panels()
    for p_ in panels:
        P(f"   {p_.name:9s} {p_.px.shape[0]}d x {p_.px.shape[1]}c  tradable={len(p_.tradable):3d}  "
          f"{p_.px.index[0].date()}..{p_.px.index[-1].date()}  rebalances={len(p_.reb)}  sleeve={p_.sleeve_cols}")
    P("")
    P("REPRODUCTION CONTROLS (asserted before any new number is read)")
    if not all(checks(p_) for p_ in panels):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ---- benchmarks
    REF = {}
    for pan in panels:
        st = pan.start
        spy = pan.spy.loc[st:]
        base0 = fast_backtest(pan.px, pan.W, 0.0, FREQ)
        v1 = fast_backtest(pan.px, rules_v1_weights(pan.px), 0.0, FREQ)
        REF[pan.name] = dict(spy=spy, base0=base0, v1=v1, st=st)
        m, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        P(f"  {pan.name:9s} SPY  {m['CAGR']:6.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:7.2%}  OOS {mo['CAGR']:6.2%}/{mo['Sharpe']:.3f}")
        for bps in COST_RUNGS:
            b = net(base0, bps).loc[st:]
            r1 = net(v1, bps).loc[st:]
            mb, m1 = metrics(b), metrics(r1)
            P(f"  {'':9s} @{bps:2d}bps  BASE (untreated) {mb['CAGR']:6.2%}/{mb['Sharpe']:.4f}/{mb['MaxDD']:7.2%}  "
              f"4b={keep_4b(b, spy)}  |  RULES v1 {m1['CAGR']:6.2%}/{m1['Sharpe']:.4f}/{m1['MaxDD']:7.2%}")
    P("")

    # ---- run the grid
    P("RUNNING THE GRID (real + 20 matched nulls per point) ...")
    rows = []
    for pan in panels:
        st, spy = pan.start, REF[pan.name]["spy"]
        base_by_bps = {bps: net(REF[pan.name]["base0"], bps).loc[st:] for bps in COST_RUNGS}
        v1_by_bps = {bps: net(REF[pan.name]["v1"], bps).loc[st:] for bps in COST_RUNGS}
        J = len(pan.reb)
        offs = rotations(J, N_NULL, SEED)
        for fam in FAM_ORDER:
            tname, thrs, dname, deps = FAMILIES[fam]
            for thr in thrs:
                s_real = on_indicator(pan, fam, thr)
                onshare = float(s_real.mean())
                sw = circ_switches(s_real)
                for dep in deps:
                    for draw in range(-1, N_NULL):
                        s = s_real if draw < 0 else np.roll(s_real, offs[draw])
                        W, mk = apply_overlay(pan, fam, dep, s)
                        res = fast_backtest(pan.px, W, 0.0, FREQ, mask=mk)
                        for bps in COST_RUNGS:
                            r = net(res, bps).loc[st:]
                            b = base_by_bps[bps]
                            mf = metrics(r)
                            h1, h2 = halves(r)
                            rows.append(dict(
                                panel=pan.name, family=fam, thr=thr, depth=str(dep), bps=bps,
                                kind=("real" if draw < 0 else "null"), draw=draw,
                                on_share=float(s.mean()),
                                switches=circ_switches(s),
                                lin_switches=int((s[1:] != s[:-1]).sum()),
                                real_on_share=onshare, real_switches=sw,
                                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                                turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                dSharpe=mf["Sharpe"] - metrics(b)["Sharpe"],
                                dMaxDD=abs(metrics(b)["MaxDD"]) - abs(mf["MaxDD"]),
                                IS_dSharpe=metrics(r.loc[:IS_END])["Sharpe"] - metrics(b.loc[:IS_END])["Sharpe"],
                                fail4a=keep_4a(r, v1_by_bps[bps]), fail4b=keep_4b(r, spy)))
        P(f"   {pan.name} done ({time.time()-t0:.0f}s)")
    g = pd.DataFrame(rows)
    g.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"   {len(g)} rows ({g[g.kind=='real'].shape[0]} real, {g[g.kind=='null'].shape[0]} null) "
      f"-> {STEM}.grid.csv   ({time.time()-t0:.0f}s)")
    P("")

    # ---- [d] the null is null by construction: verify it
    P("  [d] MATCHED-NULL VALIDATION - a rotation must preserve on-share and switch count EXACTLY")
    nn = g[g.kind == "null"]
    bad_share = int((nn.on_share != nn.real_on_share).sum())
    bad_sw = int((nn.switches != nn.real_switches).sum())
    lin = int((nn.lin_switches != nn.groupby(["panel", "family", "thr", "depth", "bps"])
               .lin_switches.transform("first")).sum())
    P(f"      on-share mismatches {bad_share}/{len(nn)}   CIRCULAR switch-count mismatches {bad_sw}/{len(nn)}"
      f"   -> {'PASS' if bad_share == 0 and bad_sw == 0 else 'FAIL'}")
    P(f"      (the LINEAR episode count can differ by one at the wrap seam; that is the single respect")
    P(f"       in which rotation is not exact, and it is reported rather than hidden)")
    tr = g.groupby(["panel", "family", "thr", "depth", "bps", "kind"])["turnover"].mean().unstack()
    rel = ((tr["null"] - tr["real"]) / tr["real"]).abs()
    P(f"      realised turnover: mean |null-real|/real = {rel.mean():.2%}, max {rel.max():.2%} "
      f"(rotation matches the overlay's SWITCHING exactly, its ACTION cost only approximately)")
    for fam in FAM_ORDER:
        rf = rel.reset_index()
        rf = rf[rf.family == fam].iloc[:, -1]
        P(f"      turnover gap, {fam:7s}: mean {rf.mean():6.2%}  max {rf.max():7.2%}")
    _ = lin
    P("")

    # ---- on-share of each overlay
    P("OVERLAY ON-SHARE (fraction of rebalance dates the overlay fires) - the free parameter the")
    P("published dSharpe does not show.  A high on-share overlay is close to a de-grossing lever.")
    P(f"  {'panel':10s} {'family':7s} " + " ".join(f"{FAMILIES[f][0]}={t}".rjust(11)
                                                   for f in FAM_ORDER for t in FAMILIES[f][1]))
    for pan in panels:
        cells = []
        for fam in FAM_ORDER:
            for thr in FAMILIES[fam][1]:
                v = g[(g.panel == pan.name) & (g.family == fam) & (g.thr == thr) & (g.kind == "real")]["real_on_share"].iloc[0]
                cells.append(f"{v:11.1%}")
        P(f"  {pan.name:10s} {'':7s} " + " ".join(cells))
    P("")

    # ---- THE CLAUSE
    P("=" * 122)
    P("THE CLAUSE, applied: |dSharpe(real)| > max over the 20 matched null draws  (one-sided 1/21 = 4.8%)")
    P("")
    clause = []
    for (pan_, fam, thr, dep, bps), sub in g.groupby(["panel", "family", "thr", "depth", "bps"], sort=False):
        real = sub[sub.kind == "real"].iloc[0]
        nul = sub[sub.kind == "null"]
        nmax = float(nul.dSharpe.abs().max())
        pct = float((nul.dSharpe.abs() < abs(real.dSharpe)).mean())
        nmaxdd = float(nul.dMaxDD.abs().max())
        clause.append(dict(panel=pan_, family=fam, thr=thr, depth=dep, bps=bps,
                           on_share=real.real_on_share, dSharpe=real.dSharpe,
                           null_max_abs=nmax, null_pctile=pct, clears=abs(real.dSharpe) > nmax,
                           dMaxDD=real.dMaxDD, null_max_abs_dMaxDD=nmaxdd,
                           clears_DD=abs(real.dMaxDD) > nmaxdd,
                           null_mean_dSharpe=float(nul.dSharpe.mean()),
                           Sharpe=real.Sharpe, MaxDD=real.MaxDD,
                           fail4b=real.fail4b, fail4a=real.fail4a))
    cl = pd.DataFrame(clause)
    cl.to_csv(OUT / f"{STEM}.clause.csv", index=False)
    g.groupby(["panel", "family", "thr", "depth", "bps", "kind"]).agg(
        dSharpe=("dSharpe", "mean"), turnover=("turnover", "mean"),
        pass4b=("fail4b", lambda s: (s == "-").mean())).to_csv(OUT / f"{STEM}.null.csv")

    P(f"  overall: {int(cl.clears.sum())} of {len(cl)} real overlays clear on SHARPE ({cl.clears.mean():.1%});"
      f"  {int(cl.clears_DD.sum())} of {len(cl)} clear on DRAWDOWN ({cl.clears_DD.mean():.1%})")
    P("")
    P(f"  {'family':7s} {'clears (Sharpe)':>16s} {'clears (MaxDD)':>15s} {'mean |dSharpe|':>15s} "
      f"{'mean null max':>14s} {'mean null pctile':>17s} {'mean on-share':>14s}")
    for fam in FAM_ORDER:
        s = cl[cl.family == fam]
        P(f"  {fam:7s} {f'{int(s.clears.sum())}/{len(s)} ({s.clears.mean():.0%})':>16s} "
          f"{f'{int(s.clears_DD.sum())}/{len(s)} ({s.clears_DD.mean():.0%})':>15s} "
          f"{s.dSharpe.abs().mean():15.4f} {s.null_max_abs.mean():14.4f} {s.null_pctile.mean():17.3f} "
          f"{s.on_share.mean():14.1%}")
    P("")
    P(f"  {'panel':10s} {'bps':>4s} " + " ".join(f"{f:>14s}" for f in FAM_ORDER) + "     (clears on Sharpe)")
    for pan in panels:
        for bps in COST_RUNGS:
            cells = []
            for fam in FAM_ORDER:
                s = cl[(cl.panel == pan.name) & (cl.bps == bps) & (cl.family == fam)]
                cells.append(f"{int(s.clears.sum())}/{len(s)}".rjust(14))
            P(f"  {pan.name:10s} {bps:4d} " + " ".join(cells))
    P("")
    P("  Every point, sorted by |dSharpe| (the full table is in .clause.csv):")
    P(f"  {'panel':10s} {'family':7s} {'thr':>5s} {'depth':>5s} {'bps':>4s} {'on-share':>9s} "
      f"{'dSharpe':>9s} {'null max':>9s} {'pctile':>7s} {'clears':>7s} {'dMaxDD':>8s} {'4b':>12s}")
    for _, r in cl.sort_values("dSharpe", key=lambda s: -s.abs()).iterrows():
        P(f"  {r.panel:10s} {r.family:7s} {str(r.thr):>5s} {str(r.depth):>5s} {r.bps:4d} {r.on_share:9.1%} "
          f"{r.dSharpe:+9.4f} {r.null_max_abs:9.4f} {r.null_pctile:7.3f} {str(r.clears):>7s} "
          f"{r.dMaxDD:+8.2%} {r.fail4b:>12s}")
    P("")

    # ---- does the clause move a VERDICT?
    P("=" * 122)
    P("DOES THE OVERLAY NULL MOVE A PUBLISHED VERDICT?  (idea 181's Q2, asked of overlays)")
    P("Every real overlay is compared with each of its 20 matched nulls in the SAME cell; a")
    P("disagreement is a cell where the KEEP/KILL verdict depends on the overlay's timing.")
    P("")
    agree = {"4a": [], "4b": []}
    for (pan_, fam, thr, dep, bps), sub in g.groupby(["panel", "family", "thr", "depth", "bps"], sort=False):
        real = sub[sub.kind == "real"].iloc[0]
        nul = sub[sub.kind == "null"]
        agree["4a"] += list((nul.fail4a == "-") == (real.fail4a == "-"))
        agree["4b"] += list((nul.fail4b == "-") == (real.fail4b == "-"))
    for k in ["4a", "4b"]:
        a = np.asarray(agree[k])
        P(f"  {k} verdict identical in {a.sum()} of {len(a)} real-vs-null swaps = {a.mean():.1%}")
    rp = g[g.kind == "real"]
    npp = g[g.kind == "null"]
    P(f"  4a pass rate  real {(rp.fail4a=='-').mean():.1%} ({int((rp.fail4a=='-').sum())}/{len(rp)})   "
      f"null {(npp.fail4a=='-').mean():.1%} ({int((npp.fail4a=='-').sum())}/{len(npp)})")
    P(f"  4b pass rate  real {(rp.fail4b=='-').mean():.1%} ({int((rp.fail4b=='-').sum())}/{len(rp)})   "
      f"null {(npp.fail4b=='-').mean():.1%} ({int((npp.fail4b=='-').sum())}/{len(npp)})")
    P("  4b pass rate by family (real vs null):")
    for fam in FAM_ORDER:
        a = rp[rp.family == fam]; b = npp[npp.family == fam]
        P(f"    {fam:7s} real {(a.fail4b=='-').mean():6.1%}  null {(b.fail4b=='-').mean():6.1%}")
    P("  most-violated 4b bar over failing REAL rows:")
    bars = {}
    for f in rp.loc[rp.fail4b != "-", "fail4b"]:
        for b in f.split(","):
            bars[b] = bars.get(b, 0) + 1
    P("    " + "  ".join(f"{k}:{v}" for k, v in sorted(bars.items(), key=lambda kv: -kv[1])))
    P("")

    # ---- rule 8
    P("=" * 122)
    P("PROTOCOL RULE 8 WALK-FORWARD - overlay point chosen on <= 2016-12-31, 2017-2026 read once")
    P("S0 = do nothing (untreated base)   S1 = IS-Sharpe argmax over the 6 points")
    P("S2 = the same argmax restricted to points that CLEAR the null clause ON THE IS WINDOW")
    P("")
    wf = []
    P(f"  {'panel':10s} {'family':7s} {'bps':>4s} | {'S0 do-nothing':>22s} | {'S1 IS-argmax':>28s} | "
      f"{'S2 clause-gated':>28s}")
    for pan in panels:
        st = pan.start
        for fam in FAM_ORDER:
            for bps in COST_RUNGS:
                sub = g[(g.panel == pan.name) & (g.family == fam) & (g.bps == bps)]
                real = sub[sub.kind == "real"].copy()
                # IS-window clause: |IS dSharpe(real)| > max over the same cell's null IS dSharpes
                ok_is = []
                for _, r in real.iterrows():
                    nl = sub[(sub.kind == "null") & (sub.thr == r.thr) & (sub.depth == r.depth)]
                    ok_is.append(abs(r.IS_dSharpe) > float(nl.IS_dSharpe.abs().max()))
                real["clears_IS"] = ok_is
                b = net(REF[pan.name]["base0"], bps).loc[st:]
                s0 = metrics(b.loc[OOS_START:])
                i1 = real.IS_Sharpe.idxmax()
                r1 = real.loc[i1]
                sub2 = real[real.clears_IS]
                r2 = real.loc[sub2.IS_Sharpe.idxmax()] if len(sub2) else None
                def fmt(x):
                    return f"{x.OOS_CAGR:6.2%}/{x.OOS_Sharpe:.4f}/{x.OOS_MaxDD:7.2%}"
                s0_txt = "{:6.2%}/{:.4f}/{:7.2%}".format(s0["CAGR"], s0["Sharpe"], s0["MaxDD"])
                s1_txt = "{}/{} {}".format(r1.thr, r1.depth, fmt(r1))
                s2_txt = "none (abstain)" if r2 is None else "{}/{} {}".format(r2.thr, r2.depth, fmt(r2))
                P(f"  {pan.name:10s} {fam:7s} {bps:4d} | {s0_txt:>22s} | {s1_txt:>28s} | {s2_txt:>28s}")
                wf.append(dict(panel=pan.name, family=fam, bps=bps,
                               S0_CAGR=s0["CAGR"], S0_Sharpe=s0["Sharpe"], S0_MaxDD=s0["MaxDD"],
                               S1_pt=f"{r1.thr}/{r1.depth}", S1_Sharpe=r1.OOS_Sharpe,
                               S1_CAGR=r1.OOS_CAGR, S1_MaxDD=r1.OOS_MaxDD,
                               S2_pt=(f"{r2.thr}/{r2.depth}" if r2 is not None else "abstain"),
                               S2_Sharpe=(r2.OOS_Sharpe if r2 is not None else s0["Sharpe"]),
                               S2_CAGR=(r2.OOS_CAGR if r2 is not None else s0["CAGR"]),
                               S2_MaxDD=(r2.OOS_MaxDD if r2 is not None else s0["MaxDD"]),
                               S2_abstained=(r2 is None), n_clear_IS=int(real.clears_IS.sum())))
    w = pd.DataFrame(wf)
    w.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("")
    d1 = (w.S1_Sharpe - w.S0_Sharpe).values
    d2 = (w.S2_Sharpe - w.S0_Sharpe).values
    P(f"  paired over {len(w)} cells (S2 falls back to S0 when it abstains, which it does in "
      f"{int(w.S2_abstained.sum())}):")
    P(f"    S1 - S0  mean {d1.mean():+.4f}  t {tstat(d1):+.2f}  wins {int((d1>0).sum())}/{len(d1)}")
    P(f"    S2 - S0  mean {d2.mean():+.4f}  t {tstat(d2):+.2f}  wins {int((d2>0).sum())}/{len(d2)}")
    P(f"    S1 and S2 pick the same point in {int((w.S1_pt == w.S2_pt).sum())}/{len(w)} cells")
    P(f"  mean OOS Sharpe: S0 {w.S0_Sharpe.mean():.4f}  S1 {w.S1_Sharpe.mean():.4f}  S2 {w.S2_Sharpe.mean():.4f}")
    P("")

    # ---- both KEEP paths
    P("=" * 122)
    P("BOTH KEEP PATHS on every row (PROTOCOL rule 4a and 4b, exactly)")
    g["pass4a"] = g.fail4a == "-"
    g["pass4b"] = g.fail4b == "-"
    g.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'panel':10s} {'bps':>4s} {'real 4a':>9s} {'real 4b':>9s} {'null 4a':>9s} {'null 4b':>9s}")
    for pan in panels:
        for bps in COST_RUNGS:
            a = g[(g.panel == pan.name) & (g.bps == bps) & (g.kind == "real")]
            b = g[(g.panel == pan.name) & (g.bps == bps) & (g.kind == "null")]
            P(f"  {pan.name:10s} {bps:4d} {f'{int(a.pass4a.sum())}/{len(a)}':>9s} {f'{int(a.pass4b.sum())}/{len(a)}':>9s} "
              f"{f'{int(b.pass4a.sum())}/{len(b)}':>9s} {f'{int(b.pass4b.sum())}/{len(b)}':>9s}")
    P("")
    rb = g[(g.kind == "real") & g.pass4b]
    if len(rb):
        P("  REAL overlay rows clearing 4b (idea 144: these are the base book with an instrument on it,")
        P("  not new books):")
        for _, r in rb.iterrows():
            P(f"   {r.panel:10s} {r.family:7s} {str(r.thr):>5s}/{r.depth:<5s} @{r.bps:2d}bps  "
              f"{r.CAGR:6.2%}/{r.Sharpe:.4f}/{r.MaxDD:7.2%}  halves {r.H1:.3f}/{r.H2:.3f}  "
              f"OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}  turnover {r.turnover:.1f}x/yr  "
              f"clause={'CLEARS' if bool(cl[(cl.panel==r.panel)&(cl.family==r.family)&(cl.thr==r.thr)&(cl.depth==r.depth)&(cl.bps==r.bps)].clears.iloc[0]) else 'inside the null band'}")
    else:
        P("  REAL overlay rows clearing 4b: NONE.")
    P("")

    # ---- predictions
    P("=" * 122)
    P("PRE-REGISTERED PREDICTIONS - scored")
    fam_clear = {f: cl[cl.family == f].clears.mean() for f in FAM_ORDER}
    a4b = np.asarray(agree["4b"])
    P(f"  P1 reproduction [a][b][c][d]                                  -> "
      f"{'HIT' if bad_share == 0 and bad_sw == 0 else 'MISS'}")
    P(f"  P2 clear rate < 40%   actual {cl.clears.mean():.1%}            -> {'HIT' if cl.clears.mean()<0.40 else 'MISS'}")
    P(f"  P3 SLEEVE clears least  " + " ".join(f"{f}:{v:.0%}" for f, v in fam_clear.items())
      + f"  -> {'HIT' if fam_clear['SLEEVE'] == min(fam_clear.values()) else 'MISS'}")
    P(f"  P4 DDCTL clears most                                          -> "
      f"{'HIT' if fam_clear['DDCTL'] == max(fam_clear.values()) else 'MISS'}")
    P(f"  P5 4b real-vs-null verdict agreement > 80%   actual {a4b.mean():.1%}  -> {'HIT' if a4b.mean()>0.80 else 'MISS'}")
    P(f"  P6 S2 does not beat S0   S2-S0 {d2.mean():+.4f}                 -> {'HIT' if d2.mean()<=0 else 'MISS'}")
    rr, nr = (rp.fail4b == "-").mean(), (npp.fail4b == "-").mean()
    ratio = (rr / nr) if nr > 0 else np.inf
    P(f"  P7 null 4b pass rate within 2x of real   real {rr:.1%} null {nr:.1%} ratio {ratio:.2f} -> "
      f"{'HIT' if 0.5 <= ratio <= 2.0 else 'MISS'}")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
