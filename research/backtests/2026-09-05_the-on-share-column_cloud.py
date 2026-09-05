#!/usr/bin/env python3
"""IDEA 191  the-on-share-column   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 186 defined the matched null for an OVERLAY -- a pair (s, A) of an ON indicator and an
action, nulled by a CIRCULAR ROTATION of s, which preserves on-share and episode structure
exactly and destroys only *when* the overlay fires.  It then noticed, and flagged rather than
tested, that a rotation cannot move the sample's crises, so the clause should be a WEAKER
test the higher the overlay's ON-SHARE.  Its own evidence was:

    DDCTL   on-share  4.6% - 40.5%   clears 15/36
    BUDGET  on-share 53.0% - 93.0%   clears  2/36
    SLEEVE  on-share ~30% - ~45%     clears  0/36

which is CONFOUNDED: on-share and family move together, so nothing in idea 186 separates
"high on-share weakens the clause" from "BUDGET is a weak instrument".  This run separates
them and prices the proposed schema column.

  Q1  Does on-share predict clearing WITHIN a family, once the threshold is swept wide
      enough that each family spans a broad on-share range on its own?
  Q2  MECHANISM / SIZE.  Holding the ACTION fixed and making the ON indicator pure noise at
      a TARGETED on-share, does the clause's null band widen and its false-positive rate
      fall as on-share rises?  This is the claim idea 186 made without testing it.
  Q3  CONFOUND.  Conditional on realised effect size |dSharpe|, does on-share still predict
      clearing?  If not, on-share is a proxy for effect size and the column is cosmetic.
  Q4  CENSUS / BACK-FILL.  How many committed LEADERBOARD rows rest on a state-dependent
      instrument, how many report an on-share (prior: zero), and does the column change any
      published verdict?
  Q5  RULE 8.  Does an on-share-GATED selector (prefer low on-share) beat the IS-Sharpe
      argmax and the do-nothing control out of sample?

DESIGN
------
  panels   : U56, BROAD136, SMALL439 (the 483-name sub-$2B panel less the 44 tickers with
             max_1d_move >= 1.0 in data/small_meta.csv)
  base book: idea 2's candidate -- composite (no vol scaler), 200d & vol20<0.60 eligibility,
             top-20 equal weight, gross 0.75, WEEKLY, t+1
  families : DDCTL  de-gross by k while the book's trailing-252d drawdown is <= -D
             BUDGET skip / half-step a rebalance whose target turnover exceeds tau
             SLEEVE move f of gross into TLT/GLD/UUP while SPY is below its ma-day mean
  THRESHOLD (tuned parameter 1) is WIDENED from idea 186's 3 points to 5, chosen to span the
  widest on-share range each family can reach, NOT to maximise anything:
             DDCTL  D   in {0.03, 0.06, 0.10, 0.15, 0.25}
             BUDGET tau in {0.05, 0.10, 0.20, 0.30, 0.50}
             SLEEVE ma  in {50, 100, 200, 300, 400}
  DEPTH     (tuned parameter 2) is idea 186's, unchanged: 2 values per family.
  costs    : 10 and 25 bps, both derived EXACTLY from one 0 bps run via the engine's own
             turnover series -- a reported axis, not a tuned one.
  null     : 20 circular rotations per configuration, seeded, idea 186's construction.

  real grid : 3 panels x 3 families x 5 thr x 2 depth x 2 cost = 180 real overlay rows
  null grid : the same 90 configurations x 20 rotations x 2 cost = 3600 null rows
  NOISE arm : 3 panels x 7 target on-shares x 2 depth x 2 cost = 84 real + 1680 null rows,
              an ON indicator with NO information at all (episodic Bernoulli matched to the
              real overlays' median episode length) carrying the DDCTL action.  Its clear
              rate at each on-share IS the clause's realised SIZE, which is what Q2 asks for.
  total     : 1638 backtests -> 5544 rows.

RULE 8 (PROTOCOL clause 8, required): overlay point chosen on data <= 2016-12-31 ONLY,
2017-01-01 -> read ONCE.  18 cells = 3 panels x 3 families x 2 cost rungs.

BOTH KEEP PATHS evaluated on every real row (4a vs the panel's own RULES v1, 4b vs SPY).

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Within family, Spearman(on-share, clears) is NEGATIVE for all three families.
  P2  Q2's null band width RISES monotonically with the noise arm's target on-share.
  P3  The noise arm's clear rate is at or below the clause's nominal one-sided size (~4.8%)
      at every on-share, i.e. the clause is not oversized -- it is UNDERSIZED at high
      on-share, which is the same statement as P2.
  P4  Conditional on |dSharpe| tercile, on-share still predicts clearing (the column is NOT
      merely a proxy for effect size).
  P5  Rule 8: the on-share-gated selector does NOT beat do-nothing (the tenth consecutive
      project instance of an IS-fitted selector failing to earn its complexity).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; SMALL439 contains no
    delistings.  Real and rotated draws inherit the bias identically so the CLAUSE reading is
    unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is not a
    tradable estimate.
  * Only J-1 distinct rotations exist and neighbouring offsets are correlated, so the
    clause's nominal one-sided size (1/21 = 4.8%) is approximate.  Q2 measures the realised
    size directly rather than assuming it.
  * BUDGET-skip changes realised turnover between real and null (idea 186 measured 25.4%
    mean, 213.8% max), because suppressing a rebalance genuinely changes trading.  That gap
    is re-measured here and published, not hidden.
  * Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136.  Idea 126: t+1 only.
  * The census in Q4 counts LEADERBOARD rows by TEXT MATCH on instrument names.  It bounds
    how many rows are exposed; it does not re-price them, and says so.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .clause.csv, .noise.csv,
.walkforward.csv, .keep.csv.
"""
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_the-on-share-column_cloud"
OUT = ROOT / "research" / "backtests"

# ---- inherited verbatim from idea 186 ----------------------------------------------------------
COST_RUNGS = [10, 25]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
FREQ = "W"
BASE_N, BASE_GROSS = 20, 0.75
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]
N_NULL = 20
SEED = 186_400                      # idea 186's own rotation seed, so bands are comparable

# ---- the ONE thing this run changes: the threshold grid is widened to span on-share ------------
FAMILIES = {
    "DDCTL":  ("D",   [0.03, 0.06, 0.10, 0.15, 0.25], "k",    [0.50, 1.00]),
    "BUDGET": ("tau", [0.05, 0.10, 0.20, 0.30, 0.50], "mode", ["skip", "half"]),
    "SLEEVE": ("ma",  [50, 100, 200, 300, 400],       "f",    [0.50, 1.00]),
}
FAM_ORDER = ["DDCTL", "BUDGET", "SLEEVE"]
NOISE_SHARES = [0.05, 0.15, 0.30, 0.50, 0.70, 0.85, 0.95]
NOISE_SEED = 191_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- engine equivalent (idea 186)
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
    m = np.concatenate([[False], m[:-1]]).copy()
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


def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, name, px, tradable):
        self.name, self.px = name, px
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
        self.ma_spy = {m: px["SPY"] < px["SPY"].rolling(m).mean()
                       for m in FAMILIES["SLEEVE"][1]}
        self._r0 = fast_backtest(px, self.W, 0.0, FREQ)      # cached: DDCTL state + control


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} "
      "tradable (SURVIVORSHIP: current constituents only, no delistings)")
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)

    def add_sleeve(px):
        a = ref[SLEEVE_ASSETS].reindex(px.index, method="ffill")
        return pd.concat([px.drop(columns=SLEEVE_ASSETS, errors="ignore"), a], axis=1).ffill()

    pxs = add_sleeve(pxs[s_stk + ["SPY"]])
    px136 = add_sleeve(px136)
    u_stk = [c for c in px56.columns if c != "SPY"]
    b_stk = [c for c in px136.columns if c != "SPY" and c not in SLEEVE_ASSETS]
    return [Panel("U56", px56, set(u_stk)),
            Panel("BROAD136", px136, set(b_stk)),
            Panel("SMALL439", pxs, set(s_stk))]


# ---------------------------------------------------------------- overlays (idea 186 verbatim)
def on_indicator(pan, fam, thr):
    idx = pan.px.index
    if fam == "DDCTL":
        eq = (1 + pan._r0["returns"]).cumprod()
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
        s = pan.ma_spy[thr].values
    else:
        raise ValueError(fam)
    return s[pan.reb]


def apply_overlay(pan, fam, depth, s_reb):
    idx = pan.px.index
    on = pd.Series(False, index=idx)
    on.iloc[pan.reb] = s_reb
    on = on.where(pd.Series(pan.mask, index=idx)).ffill().fillna(False).astype(bool)
    mask = pan.mask.copy()
    W = pan.W
    if fam in ("DDCTL", "NOISE"):
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0)
    elif fam == "BUDGET":
        if depth == "skip":
            mask = mask & ~np.isin(np.arange(len(idx)), pan.reb[s_reb])
        else:
            w = pan.W.values.copy()
            wr = w[pan.reb]
            for j in np.flatnonzero(s_reb):
                prev = wr[j - 1] if j > 0 else np.zeros(wr.shape[1])
                wr[j] = 0.5 * wr[j] + 0.5 * prev
            w[pan.reb] = wr
            W = pd.DataFrame(w, index=idx, columns=pan.W.columns)
    elif fam == "SLEEVE":
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0).copy()
        add = np.where(on.values, depth * BASE_GROSS / len(pan.sleeve_cols), 0.0)
        for c in pan.sleeve_cols:
            W[c] = W[c].values + add
    return W, mask


def circ_switches(s):
    return int((np.asarray(s) != np.roll(np.asarray(s), 1)).sum())


def rotations(J, n, seed):
    rng = np.random.default_rng(seed)
    return sorted(rng.permutation(np.arange(1, J))[:n].tolist())


def noise_state(n, share, ep_len, rng):
    """Episodic Bernoulli ON series with NO information: a two-state Markov chain whose
    stationary on-share is `share` and whose mean ON episode length is `ep_len` rebalances.
    That matches the real overlays' episode structure while carrying zero signal."""
    p_off = 1.0 / max(ep_len, 1.0)                      # P(leave ON)
    p_on = p_off * share / max(1.0 - share, 1e-9)       # P(enter ON)
    p_on = min(p_on, 1.0)
    s = np.zeros(n, bool)
    cur = rng.random() < share
    for i in range(n):
        s[i] = cur
        cur = (rng.random() > p_off) if cur else (rng.random() < p_on)
    return s


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
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return np.nan
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def checks(pan):
    ok = True
    a = backtest(pan.px, pan.W, cost_bps=10, freq=FREQ)
    b = fast_backtest(pan.px, pan.W, 10, FREQ)
    dr = float((a["returns"] - b["returns"]).abs().max())
    dt = float((a["turnover"] - b["turnover"]).abs().max())
    P(f"  [a] {pan.name:9s} fast_backtest vs engine.backtest: max|dret|={dr:.3e} "
      f"max|dturn|={dt:.3e} -> {'PASS' if dr < 1e-12 else 'FAIL'}")
    ok &= dr < 1e-12 and dt < 1e-10
    d = float((net(pan._r0, 10) - a["returns"]).abs().max())
    P(f"  [b] {pan.name:9s} cost identity 10bps from the 0bps run: max|d|={d:.3e} "
      f"-> {'PASS' if d < 1e-15 else 'FAIL'}")
    ok &= d < 1e-15
    _, above, vol20 = score(pan.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in pan.px.columns if c not in set(pan.tradable)]
    if drop:
        m[drop] = False
    s78 = score(pan.px, vol_scale=False)[0]
    w78 = ((s78.where(m).rank(axis=1, ascending=False) <= BASE_N).astype(float)
           * (BASE_GROSS / BASE_N))
    dw = float((w78 - pan.W).abs().max().max())
    P(f"  [c] {pan.name:9s} base CAND-20 weights vs idea 78/171 weights_cand: max|dw|={dw:.3e} "
      f"-> {'PASS' if dw < 1e-12 else 'FAIL'}")
    ok &= dw < 1e-12
    return ok


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 191  the-on-share-column   (cloud, 2026-09-05)")
    P("=" * 118)

    P("\nbuilding panels ...")
    panels = build_panels()
    P(f"  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))

    P("\nREPRODUCTION, asserted before any new number is read:")
    ok = all(checks(p) for p in panels)
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
      f"  (published 6.45305% / 0.66418 / -13.82780%) -> "
      f"{'PASS' if abs(mu['Sharpe'] - 0.66418) < 5e-5 else 'FAIL'}")
    ok &= abs(mu["Sharpe"] - 0.66418) < 5e-5
    P(f"\nreproduction {'PASSES' if ok else 'FAILS'} -- "
      f"{'proceeding' if ok else 'STOP'}")
    if not ok:
        return

    # ------------------------------------------------------------------------------- the grid
    P("\n" + "=" * 118)
    P("GRID  3 panels x 3 families x 5 thresholds x 2 depths x (1 real + 20 rotations) x 2 cost")
    P("      threshold grid WIDENED from idea 186's 3 points to span on-share within family")
    P("=" * 118)
    rows, ep_lens = [], []
    for pan in panels:
        start = pan.start
        spy = pan.spy.loc[start:]
        basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
        c0 = pan._r0
        for fam in FAM_ORDER:
            tname, thrs, dname, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = on_indicator(pan, fam, thr)
                J = len(s_real)
                onshare = float(s_real.mean())
                sw = circ_switches(s_real)
                if sw > 0:
                    ep_lens.append(2.0 * s_real.sum() / sw)
                offs = rotations(J, N_NULL, SEED + hash((pan.name, fam, thr)) % 10_000)
                for depth in depths:
                    variants = [("real", 0, s_real)] + [
                        ("null", o, np.roll(s_real, o)) for o in offs]
                    for kind, off, s in variants:
                        W, mask = apply_overlay(pan, fam, depth, s)
                        res = fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                        for bps in COST_RUNGS:
                            r = net(res, bps).loc[start:]
                            cr = net(c0, bps).loc[start:]
                            br = b0 - bt * bps / 1e4
                            m = metrics(r)
                            h1, h2 = halves(r)
                            rows.append(dict(
                                panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                                kind=kind, offset=off, on_share=float(s.mean()),
                                switches=circ_switches(s), real_on_share=onshare,
                                turnover_yr=float(res["turnover"].loc[start:].sum()
                                                  / (len(r) / 252)),
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                H1=h1, H2=h2,
                                Sharpe_IS=_sh(r.loc[:IS_END]), Sharpe_OOS=_sh(r.loc[OOS_START:]),
                                CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                                ctrl_Sharpe=metrics(cr)["Sharpe"],
                                ctrl_Sharpe_IS=_sh(cr.loc[:IS_END]),
                                ctrl_Sharpe_OOS=_sh(cr.loc[OOS_START:]),
                                ctrl_MaxDD=metrics(cr)["MaxDD"],
                                ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                                ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                                fail4a=keep_4a(r, br), fail4b=keep_4b(r, spy)))
        P(f"  {pan.name} done ({time.time() - t0:.0f}s)")

    G = pd.DataFrame(rows)
    G["dSharpe"] = G["Sharpe"] - G["ctrl_Sharpe"]
    G["dSharpe_IS"] = G["Sharpe_IS"] - G["ctrl_Sharpe_IS"]
    G["dMaxDD"] = G["MaxDD"] - G["ctrl_MaxDD"]
    G["pass4a"] = G["fail4a"] == "-"
    G["pass4b"] = G["fail4b"] == "-"
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\ngrid: {len(G)} rows ({int((G.kind == 'real').sum())} real) "
      f"({time.time() - t0:.0f}s) -> {STEM}.grid.csv")

    # null validity, idea 186's own check
    nn = G[G.kind == "null"]
    bad_share = int((nn.on_share.round(10) != nn.real_on_share.round(10)).sum())
    P(f"  null validity: on-share preserved in {len(nn) - bad_share}/{len(nn)} rotated rows")
    real_sw = G[G.kind == "real"].set_index(["panel", "family", "thr", "depth", "bps"])["switches"]
    bad_sw = int(sum(1 for _, r in nn.iterrows()
                     if r["switches"] != real_sw.loc[(r.panel, r.family, r.thr,
                                                      r.depth, r.bps)]))
    P(f"  null validity: circular switch count preserved in {len(nn) - bad_sw}/{len(nn)} rows")

    # turnover fidelity of the null (idea 186's published caveat, re-measured)
    P("\n  turnover fidelity of the rotation null (mean |null - real| / real), by family:")
    tf = []
    for (pn, fm, th, dp, bp), sub in G.groupby(["panel", "family", "thr", "depth", "bps"]):
        rt = float(sub[sub.kind == "real"]["turnover_yr"].iloc[0])
        nt = sub[sub.kind == "null"]["turnover_yr"].values
        tf.append(dict(panel=pn, family=fm, depth=dp,
                       rel=float(np.mean(np.abs(nt - rt)) / rt) if rt else np.nan))
    TF = pd.DataFrame(tf)
    P(TF.pivot_table(index="family", columns="depth", values="rel")
      .to_string(float_format=lambda x: f"{x:.1%}"))

    # ------------------------------------------------------------- the clause, per real overlay
    cl = []
    for (pn, fm, th, dp, bp), sub in G.groupby(["panel", "family", "thr", "depth", "bps"]):
        r = sub[sub.kind == "real"].iloc[0]
        nb = sub[sub.kind == "null"]
        bandS = float(nb["dSharpe"].abs().max())
        bandD = float(nb["dMaxDD"].abs().max())
        bandS_IS = float(nb["dSharpe_IS"].abs().max())
        cl.append(dict(panel=pn, family=fm, thr=th, depth=dp, bps=bp,
                       on_share=float(r["on_share"]), switches=int(r["switches"]),
                       dSharpe=float(r["dSharpe"]), band=bandS,
                       clears=bool(abs(r["dSharpe"]) > bandS),
                       dMaxDD=float(r["dMaxDD"]), bandDD=bandD,
                       clearsDD=bool(abs(r["dMaxDD"]) > bandD),
                       dSharpe_IS=float(r["dSharpe_IS"]), band_IS=bandS_IS,
                       clears_IS=bool(abs(r["dSharpe_IS"]) > bandS_IS),
                       Sharpe=float(r["Sharpe"]), Sharpe_OOS=float(r["Sharpe_OOS"]),
                       CAGR=float(r["CAGR"]), MaxDD=float(r["MaxDD"]),
                       CAGR_OOS=float(r["CAGR_OOS"]), MaxDD_OOS=float(r["MaxDD_OOS"]),
                       ctrl_Sharpe_OOS=float(r["ctrl_Sharpe_OOS"]),
                       ctrl_CAGR_OOS=float(r["ctrl_CAGR_OOS"]),
                       ctrl_MaxDD_OOS=float(r["ctrl_MaxDD_OOS"]),
                       pass4a=bool(r["pass4a"]), pass4b=bool(r["pass4b"]),
                       fail4b=r["fail4b"]))
    C = pd.DataFrame(cl)
    C.to_csv(OUT / f"{STEM}.clause.csv", index=False)

    P("\n" + "=" * 118)
    P("Q1  does ON-SHARE predict clearing WITHIN a family, on a widened threshold grid?")
    P("=" * 118)
    P("\n  on-share range reached by each family (this run vs idea 186's 3-point grid):")
    P(C.groupby("family")["on_share"]
      .agg(["min", "max", "mean"]).to_string(float_format=lambda x: f"{x:.1%}"))
    P("\n  clear rate and mean band by family:")
    P(C.groupby("family").agg(n=("clears", "size"), clears=("clears", "sum"),
                              clearsDD=("clearsDD", "sum"), band=("band", "mean"),
                              absd=("dSharpe", lambda s: s.abs().mean()))
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  the confound made visible -- clear rate by (family x on-share tercile):")
    C["os_terc"] = pd.qcut(C["on_share"], 3, labels=["low", "mid", "high"])
    P(pd.crosstab(C["family"], C["os_terc"], values=C["clears"], aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.2f}"))
    P("\n  Spearman(on_share, .) WITHIN each family, and pooled on family-demeaned values:")
    q1 = []
    for fm, sub in C.groupby("family"):
        q1.append(dict(family=fm, n=len(sub),
                       rho_clears=spearman(sub.on_share, sub.clears.astype(float)),
                       rho_band=spearman(sub.on_share, sub.band),
                       rho_absd=spearman(sub.on_share, sub.dSharpe.abs()),
                       rho_margin=spearman(sub.on_share, sub.dSharpe.abs() - sub.band)))
    dem = C.copy()
    for col in ("on_share", "band"):
        dem[col + "_d"] = dem[col] - dem.groupby("family")[col].transform("mean")
    dem["absd_d"] = (dem.dSharpe.abs()
                     - dem.groupby("family")["dSharpe"].transform(lambda s: s.abs().mean()))
    dem["clears_d"] = (dem.clears.astype(float)
                       - dem.groupby("family")["clears"].transform("mean"))
    q1.append(dict(family="POOLED (family-demeaned)", n=len(dem),
                   rho_clears=spearman(dem.on_share_d, dem.clears_d),
                   rho_band=spearman(dem.on_share_d, dem.band_d),
                   rho_absd=spearman(dem.on_share_d, dem.absd_d),
                   rho_margin=spearman(dem.on_share_d, dem.absd_d - dem.band_d)))
    Q1 = pd.DataFrame(q1)
    P(Q1.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------------------------------------------------ Q2: the mechanism
    P("\n" + "=" * 118)
    P("Q2  MECHANISM / SIZE.  Action held FIXED (de-gross by k); ON indicator is pure noise at a")
    P("    TARGETED on-share.  A zero-effect overlay's clear rate IS the clause's realised size.")
    P("=" * 118)
    ep_med = float(np.median(ep_lens))
    P(f"    noise episode length matched to the real overlays' median: {ep_med:.2f} rebalances")
    nrows = []
    for pan in panels:
        start = pan.start
        spy = pan.spy.loc[start:]
        c0 = pan._r0
        J = len(pan.reb)
        for tgt in NOISE_SHARES:
            rng = np.random.default_rng(NOISE_SEED + int(tgt * 1000)
                                        + 7 * abs(hash(pan.name)) % 1000)
            s_real = noise_state(J, tgt, ep_med, rng)
            offs = rotations(J, N_NULL, SEED + int(tgt * 1000))
            for depth in FAMILIES["DDCTL"][3]:
                for kind, off, s in ([("real", 0, s_real)]
                                     + [("null", o, np.roll(s_real, o)) for o in offs]):
                    W, mask = apply_overlay(pan, "NOISE", depth, s)
                    res = fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = net(res, bps).loc[start:]
                        cr = net(c0, bps).loc[start:]
                        m = metrics(r)
                        nrows.append(dict(panel=pan.name, target=tgt, depth=depth, bps=bps,
                                          kind=kind, offset=off, on_share=float(s.mean()),
                                          switches=circ_switches(s),
                                          Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                          dSharpe=m["Sharpe"] - metrics(cr)["Sharpe"],
                                          dMaxDD=m["MaxDD"] - metrics(cr)["MaxDD"]))
        P(f"    noise arm on {pan.name} done ({time.time() - t0:.0f}s)")
    NZ = pd.DataFrame(nrows)
    NZ.to_csv(OUT / f"{STEM}.noise.csv", index=False)
    nz = []
    for (pn, tg, dp, bp), sub in NZ.groupby(["panel", "target", "depth", "bps"]):
        r = sub[sub.kind == "real"].iloc[0]
        nb = sub[sub.kind == "null"]
        band = float(nb["dSharpe"].abs().max())
        bandD = float(nb["dMaxDD"].abs().max())
        nz.append(dict(panel=pn, target=tg, depth=dp, bps=bp, on_share=float(r["on_share"]),
                       dSharpe=float(r["dSharpe"]), band=band,
                       clears=bool(abs(r["dSharpe"]) > band),
                       band_sd=float(nb["dSharpe"].std(ddof=1)),
                       bandDD=bandD, clearsDD=bool(abs(r["dMaxDD"]) > bandD)))
    NC = pd.DataFrame(nz)
    P("\n  band width and realised SIZE of the clause, by target on-share "
      f"(n = {len(NC) // len(NOISE_SHARES)} cells each; nominal one-sided size 1/21 = 4.8%):")
    P(NC.groupby("target").agg(realised_on_share=("on_share", "mean"),
                               band=("band", "mean"), band_sd=("band_sd", "mean"),
                               size_Sharpe=("clears", "mean"),
                               size_MaxDD=("clearsDD", "mean"), n=("clears", "size"))
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  Spearman(target on-share, band width) = "
      f"{spearman(NC.target, NC.band):+.4f}   over {len(NC)} noise cells")
    P(f"  Spearman(target on-share, realised size) = {spearman(NC.target, NC.clears.astype(float)):+.4f}")
    P(f"  overall realised size of the clause on a ZERO-EFFECT overlay: "
      f"{NC.clears.mean():.1%} on Sharpe, {NC.clearsDD.mean():.1%} on drawdown "
      f"(nominal 4.8%)")

    # ------------------------------------------------------- Q3: is on-share just effect size?
    P("\n" + "=" * 118)
    P("Q3  CONFOUND.  Conditional on realised |dSharpe| tercile, does on-share still predict")
    P("    clearing?  If not, the column is a proxy for effect size and is cosmetic.")
    P("=" * 118)
    C["absd"] = C["dSharpe"].abs()
    C["absd_terc"] = pd.qcut(C["absd"], 3, labels=["small", "mid", "large"])
    P("\n  clear rate by |dSharpe| tercile x on-share tercile (n in parentheses):")
    ct = pd.crosstab(C["absd_terc"], C["os_terc"], values=C["clears"], aggfunc="mean")
    cn = pd.crosstab(C["absd_terc"], C["os_terc"])
    P(ct.to_string(float_format=lambda x: f"{x:.2f}"))
    P("  counts:")
    P(cn.to_string())
    P("\n  within each |dSharpe| tercile, Spearman(on_share, clears):")
    for tg, sub in C.groupby("absd_terc", observed=True):
        P(f"    {str(tg):6s} n={len(sub):3d}  rho={spearman(sub.on_share, sub.clears.astype(float)):+.4f}"
          f"   mean band {sub.band.mean():.4f}   mean |d| {sub.absd.mean():.4f}")
    P("\n  and the same for the BAND (the quantity the mechanism claim is actually about):")
    for tg, sub in C.groupby("absd_terc", observed=True):
        P(f"    {str(tg):6s} n={len(sub):3d}  rho(on_share, band)={spearman(sub.on_share, sub.band):+.4f}")

    # ---------------------------------------------------------------------- Q4: census/backfill
    P("\n" + "=" * 118)
    P("Q4  CENSUS.  How many committed LEADERBOARD rows rest on a state-dependent instrument,")
    P("    and how many publish an on-share?  (TEXT MATCH: bounds exposure, does not re-price.)")
    P("=" * 118)
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().splitlines()
    data = [ln for ln in lb if ln.startswith("| 20")]
    pats = {"sleeve": r"\bsleeve\b", "drawdown control / stop": r"drawdown control|trailing stop|DDCTL|\bstop\b",
            "entry/turnover budget": r"entry budget|turnover budget|BUDGET", "gate": r"\bgate\b",
            "breadth": r"\bbreadth\b"}
    tot = len(data)
    P(f"\n  {tot} committed data rows in LEADERBOARD.md")
    hits = {}
    for nm, pat in pats.items():
        h = [ln for ln in data if re.search(pat, ln, re.I)]
        hits[nm] = h
        P(f"    {nm:26s} {len(h):5d} rows ({len(h) / tot:.1%})")
    anyh = [ln for ln in data
            if any(re.search(p, ln, re.I) for p in pats.values())]
    P(f"    {'ANY state-dependent':26s} {len(anyh):5d} rows ({len(anyh) / tot:.1%})")
    withos = [ln for ln in anyh if re.search(r"on-share|on_share|fires on", ln, re.I)]
    P(f"    of those, publishing an on-share: {len(withos)} ({len(withos) / max(len(anyh), 1):.2%})")
    P(f"  -> the column is missing from {len(anyh) - len(withos)} of {len(anyh)} exposed rows.")
    P("\n  BACK-FILL for every configuration this run prices (the column, as proposed):")
    bf = C.groupby(["family", "thr"]).agg(on_share=("on_share", "mean"),
                                          switches=("switches", "mean"),
                                          clears=("clears", "mean"), band=("band", "mean"),
                                          absd=("absd", "mean"))
    P(bf.to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------------ Q5: rule 8
    P("\n" + "=" * 118)
    P("Q5  RULE 8 WALK-FORWARD.  Overlay point chosen on data <= 2016-12-31 ONLY; 2017-2026 read")
    P("    ONCE.  18 cells = 3 panels x 3 families x 2 cost rungs.  Pool = 10 (5 thr x 2 depth).")
    P("=" * 118)
    med_os = float(C["on_share"].median())
    wf = []
    for (pn, fm, bp), sub in C.groupby(["panel", "family", "bps"]):
        base_oos = float(sub["ctrl_Sharpe_OOS"].iloc[0])
        base = dict(OOS_Sharpe=base_oos, OOS_CAGR=float(sub["ctrl_CAGR_OOS"].iloc[0]),
                    OOS_MaxDD=float(sub["ctrl_MaxDD_OOS"].iloc[0]))

        def take(df, tag):
            if not len(df):
                return dict(selector=tag, pick="ABSTAIN", **base)
            r = df.loc[df["dSharpe_IS"].idxmax()]
            return dict(selector=tag, pick=f"{r['thr']}/{r['depth']} os={r['on_share']:.0%}",
                        OOS_Sharpe=float(r["Sharpe_OOS"]), OOS_CAGR=float(r["CAGR_OOS"]),
                        OOS_MaxDD=float(r["MaxDD_OOS"]))

        rows_ = [dict(selector="S0 do-nothing", pick="-", **base),
                 take(sub, "S1 IS-Sharpe argmax"),
                 take(sub[sub.on_share <= med_os], "S4 IS-argmax | on-share <= median"),
                 take(sub[sub.clears_IS], "S2 IS-clause-gated (idea 186)"),
                 take(sub[sub.clears_IS & (sub.on_share <= med_os)],
                      "S5 IS-clause + low on-share")]
        o = sub.loc[sub["Sharpe_OOS"].idxmax()]
        rows_.append(dict(selector="ORACLE-OOS", pick=f"{o['thr']}/{o['depth']}",
                          OOS_Sharpe=float(o["Sharpe_OOS"]), OOS_CAGR=float(o["CAGR_OOS"]),
                          OOS_MaxDD=float(o["MaxDD_OOS"])))
        for r in rows_:
            r.update(panel=pn, family=fm, bps=bp, dOOS=r["OOS_Sharpe"] - base_oos)
            wf.append(r)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  on-share median used as the gate: {med_os:.1%}")
    piv = W.pivot_table(index=["panel", "family", "bps"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()), dOOS=float(d.mean()),
                        t=tstat(d), wins=int((d > 0).sum()), losses=int((d < 0).sum()),
                        n=int(len(d)),
                        abstains=int((W[W.selector == s]["pick"] == "ABSTAIN").sum())))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P(SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\n  every walk-forward cell:")
    P(W[["panel", "family", "bps", "selector", "pick", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "dOOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->):")
    for pan in panels:
        st = pan.start
        bb = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10.0,
                      freq="W")["returns"].loc[st:]
        sp = pan.spy.loc[st:]
        mb, ms_ = metrics(bb.loc[OOS_START:]), metrics(sp.loc[OOS_START:])
        P(f"    {pan.name:9s} RULES v1 OOS {mb['CAGR']:7.2%}/{mb['Sharpe']:.4f}/{mb['MaxDD']:8.2%}"
          f"   SPY OOS {ms_['CAGR']:7.2%}/{ms_['Sharpe']:.4f}/{ms_['MaxDD']:8.2%}")

    # ------------------------------------------------------------------------ both KEEP paths
    P("\n" + "=" * 118)
    P("BOTH KEEP PATHS")
    P("=" * 118)
    realG = G[G.kind == "real"]
    nullG = G[G.kind == "null"]
    P(f"\n  real overlays : 4a {int(realG.pass4a.sum())}/{len(realG)}, "
      f"4b {int(realG.pass4b.sum())}/{len(realG)}")
    P(f"  rotated nulls : 4a {int(nullG.pass4a.sum())}/{len(nullG)} "
      f"({nullG.pass4a.mean():.1%}), 4b {int(nullG.pass4b.sum())}/{len(nullG)} "
      f"({nullG.pass4b.mean():.1%})   [idea 186 found the null passes MORE often]")
    P("\n  4b passes by panel x family (real):")
    P(realG.pivot_table(index="panel", columns="family", values="pass4b",
                        aggfunc="sum").to_string())
    p4b = C[C.pass4b]
    P(f"\n  all {len(p4b)} real 4b passes, with the proposed ON-SHARE column beside them:")
    if len(p4b):
        P(p4b[["panel", "family", "thr", "depth", "bps", "on_share", "CAGR", "Sharpe", "MaxDD",
               "Sharpe_OOS", "dSharpe", "band", "clears", "pass4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"\n  of those {len(p4b)}, inside their own null band (clears == False): "
          f"{int((~p4b.clears).sum())}  -- idea 186 found 18 of 18")
        P(f"  their on-share range: {p4b.on_share.min():.1%} - {p4b.on_share.max():.1%} "
          f"(median {p4b.on_share.median():.1%})")
    G.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ------------------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    rho_by_fam = {r["family"]: r["rho_clears"] for _, r in Q1.iterrows()}
    all_neg = all(v < 0 for k, v in rho_by_fam.items() if k in FAM_ORDER)
    bnd = NC.groupby("target")["band"].mean()
    mono = bool((np.diff(bnd.values) > 0).all())
    size_ok = bool(NC.clears.mean() <= 0.048 + 1e-9)
    terc_rho = [spearman(sub.on_share, sub.clears.astype(float))
                for _, sub in C.groupby("absd_terc", observed=True)]
    p4 = bool(np.nanmean(terc_rho) < 0)
    s4 = float(SW.loc[SW.selector == "S4 IS-argmax | on-share <= median", "dOOS"].iloc[0])
    preds = [
        ("P1 within-family rho(on-share, clears) < 0 for all three", all_neg,
         "  ".join(f"{k} {v:+.3f}" for k, v in rho_by_fam.items() if k in FAM_ORDER)),
        ("P2 noise band width rises monotonically with on-share", mono,
         "  ".join(f"{t:.2f}:{b:.4f}" for t, b in bnd.items())),
        ("P3 realised size <= nominal 4.8% everywhere", size_ok,
         f"overall {NC.clears.mean():.1%}; by target "
         + " ".join(f"{t:.2f}:{v:.0%}" for t, v in NC.groupby('target')['clears'].mean().items())),
        ("P4 on-share predicts clearing within |dSharpe| tercile", p4,
         "  ".join(f"{r:+.3f}" for r in terc_rho)),
        ("P5 on-share-gated selector does NOT beat do-nothing", s4 <= 0,
         f"S4 dOOS {s4:+.4f}"),
    ]
    for nm, hit, ev in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:52s}  {ev}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")

    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
