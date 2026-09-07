#!/usr/bin/env python3
"""QUEUE idea 110 — selection-vs-no-selection-as-the-real-question  (lane B, 2026-09-07).

Question (as worded in QUEUE.md)
--------------------------------
"idea 109 found rule 8's selector beats the no-overlay control by 0.055 of mean OOS Sharpe
across 44 cells (1.048 vs 0.993) while the CAGR-floor constraint on top of it subtracts 0.010.
Test whether that 0.055 survives the grids being pre-registered rather than chosen after the
fact: re-run the same selector comparison on 100 random parameter grids of the same shape
(random overlay parameter values within each instrument's range) and report the null
distribution of the selection premium.  Max 2 params."

WHAT IS ACTUALLY BEING TESTED
-----------------------------
Idea 109's +0.055 is the gap  mean OOS Sharpe(S_sharpe) - mean OOS Sharpe(S_null)  over 44
cells, where the six overlay grids and their parameter VALUES were copied off the leaderboard,
i.e. chosen after those values had already been looked at.  Two things could produce +0.055:

  (i)  SELECTION SKILL — argmax-IS-Sharpe genuinely picks better-than-average points, or
  (ii) INSTRUMENT VALUE — the committed grids happen to contain good points, so ANY point
       beats the no-overlay null and the argmax is along for the ride.

The queue's randomisation separates the grid from the effect, but not (i) from (ii).  So this
run adds one pre-registered control that does:

  S_rand  = the EXPECTED OOS Sharpe of a uniformly random pick from the same grid
            (computed exactly as the mean over the grid's points, no sampling noise).

  premium_total = S_sharpe - S_null   <- idea 109's +0.055, decomposed into:
  premium_skill = S_sharpe - S_rand   <- (i), what rule 8's ARGMAX is worth
  premium_instr = S_rand  - S_null    <- (ii), what HAVING an overlay is worth

PRE-REGISTERED (declared before any number below was computed)
-------------------------------------------------------------
  Selectors: S_sharpe (PROTOCOL rule 8 as written), S_null (the no-overlay point), S_rand
             (uniform-random pick, exact expectation), S_best (oracle OOS argmax, for regret).
             Tie-break in S_sharpe: SMALLEST overlay parameter by the same pkey() as idea 109.
  IS = ..2016-12-31.  OOS = 2017-01-01.. , never touched by any selector.
  H_SURVIVES : over 100 random grids, mean premium_total > 0 AND positive in >= 75/100 grids.
               (If yes, idea 109's +0.055 is not an artefact of its hand-picked values.)
  H_NOT_CHERRY: idea 109's committed grid is NOT an upper-tail outlier of the null
               distribution of premium_total (percentile <= 95).
  H_SKILL    : premium_skill > 0 in >= 75/100 random grids.  This is the sharp test: if
               premium_skill ~ 0 while premium_instr carries the whole +0.055, then rule 8's
               SELECTOR earns nothing and idea 109's headline is a statement about overlays,
               not about selection.
  H_RANKIC   : pooled within-cell spearman(IS Sharpe, OOS Sharpe) over the pool > 0.
               Mechanism check for H_SKILL; reported whatever H_SKILL does.

TUNED (2, per PROTOCOL rule 4): the SELECTOR (4 levels) x the OVERLAY PARAMETER.  Nothing else
is selected on: universe, base book, cost rung, and which overlay instrument are reported
controls, and every pool point is written to .pool.csv and printed.  The randomisation is a
null-distribution device, not a third dial — no result is chosen by it.

THE POOL (the "instrument's range", spanning idea 109's committed values exactly)
--------------------------------------------------------------------------------
  sleeve  f       0.000 .. 1.000 step 0.025   (41)   null 0.00   committed {0,.25,.5,.75,1}
  band    w       0.000 .. 0.080 step 0.0025  (33)   null 0.00   committed {0,.02,.03,.05,.08}
  breadth p       0.000 .. 1.000 step 0.025   (41)   null 0.00   committed {0,.25,.5,.75,1}
  stop    s       None + 0.100..0.250 s 0.005 (32)   null None   committed {None,.25,.2,.15,.1}
  crypto  p       0.000 .. 0.100 step 0.0025  (41)   null 0.00   committed {0,.02,.05,.10}
  gross   g       0.500 .. 1.250 step 0.025   (31)   null 0.75   committed {.75,.5,1.0,1.25}
Every committed value is a member of its pool, so idea 109's grid is reproduced exactly as one
particular subset — that is gate G1.
A random grid keeps the SAME SHAPE as the committed one: the null point (S_null needs it) plus
(K-1) values drawn without replacement from the rest of the pool, K = the committed grid size.
Seed 20260907, fixed; 100 grids.

CELLS: 6 instruments on u56 + 5 on broad (crypto absent) x 2 books (top20, ewall) x 2 cost
rungs (10, 25 bps) = 44, identical to idea 109.

KEEP PATHS: both evaluated for every pick — 4a vs RULES v2 (the live book) and, for continuity
with idea 109, vs RULES v1; 4b vs SPY, full sample and OOS-only.

CRYPTO CAVEAT (inherited from idea 109): BTC-USD starts 2014-09-17, so the crypto grid's IS
window holds barely two years of crypto.  Reported both included and excluded.
SURVIVORSHIP: both equity panels are current constituents; the bias is identical across
selectors, which is what this run compares.
COST NOTE: the holdings path is independent of bps, so each weight matrix is run ONCE at 0 bps
and both rungs derived exactly.  Asserted at start-up (G2), as is the metric identity (G3).

Deterministic, standalone:
    python research/backtests/2026-09-07_selection-vs-no-selection-as-the-real-question_B.py
"""
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

FREQ = "W"
COSTS = (10, 25)
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
N_RANDOM = 100
SEED = 20260907
OUT = Path(__file__).with_suffix("")
_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ----------------------------------------------------------------- the pools
def _rng_vals(lo, hi, step):
    n = int(round((hi - lo) / step))
    return [round(lo + i * step, 6) for i in range(n + 1)]


POOLS = {
    "sleeve":  _rng_vals(0.0, 1.0, 0.025),
    "band":    _rng_vals(0.0, 0.08, 0.0025),
    "breadth": _rng_vals(0.0, 1.0, 0.025),
    "stop":    [None] + _rng_vals(0.10, 0.25, 0.005),
    "crypto":  _rng_vals(0.0, 0.10, 0.0025),
    "gross":   _rng_vals(0.50, 1.25, 0.025),
}
COMMITTED = {                                   # idea 109's grids, verbatim
    "sleeve":  [0.00, 0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.02, 0.03, 0.05, 0.08],
    "breadth": [0.00, 0.25, 0.50, 0.75, 1.00],
    "stop":    [None, 0.25, 0.20, 0.15, 0.10],
    "crypto":  [0.00, 0.02, 0.05, 0.10],
    "gross":   [0.75, 0.50, 1.00, 1.25],
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}
INSTR = list(COMMITTED)


def pk(p):
    """Canonical string key for a parameter value (None-safe, float-safe)."""
    return "none" if p is None else f"{float(p):.6f}"


def pkey(grid, p):
    """idea 109's ordering key for the smallest-parameter tie-break."""
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p
    if grid == "gross":
        return abs(float(p) - 0.75)
    return float(p)


# ----------------------------------------------------------------- cached panel pieces
class Panel:
    def __init__(self, tag, px):
        self.tag, self.px = tag, px
        self.start = px.index[260]
        self.rets = px.pct_change().fillna(0.0).values
        self.mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
        self.cols = list(px.columns)
        self.ma = px.rolling(200).mean()
        self.vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.dd126 = px / px.rolling(126).max() - 1.0
        self.s, _, _ = score(px, vol_scale=False)
        self._band = {}
        above0 = self.band_above(0.0).drop(columns=["SPY"], errors="ignore")
        self.breadth = above0.mean(axis=1)
        self.sleeve = sleeve_weights(px, [t for t in S4 if t in px.columns])

    def band_above(self, w):
        k = round(float(w), 6)
        if k not in self._band:
            up = self.px > self.ma * (1 + k)
            dn = self.px < self.ma * (1 - k)
            st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                              index=self.px.index, columns=self.px.columns)
            self._band[k] = st.ffill().fillna(0.0) > 0.5
        return self._band[k]

    def elig(self, band=0.0, stop=None):
        m = self.band_above(band) & (self.vol20 < 0.60)
        if stop is not None:
            m = m & (self.dd126 > -stop)
        return m

    def book(self, kind, band=0.0, stop=None, gross=BOOK_GROSS, n=20):
        m = self.elig(band, stop)
        if kind == "top20":
            w = (self.s.where(m).rank(axis=1, ascending=False) <= n).astype(float)
        else:
            w = (m & self.s.notna()).astype(float)
        k = w.sum(axis=1)
        return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (vote * rp).fillna(0.0)
    return out


def _regross(w, g=1.00):
    tot = w.sum(axis=1)
    return w.mul((g / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


def overlay(pn, kind, grid, p):
    """idea 109's overlay(), re-expressed on the cached Panel.  Same weights, exactly."""
    if grid == "sleeve":
        return _regross((1 - p) * pn.book(kind) + p * pn.sleeve, 1.00)
    if grid == "band":
        return pn.book(kind, band=p)
    if grid == "breadth":
        mult = pd.Series(np.where(pn.breadth < BREADTH_B, 1.0 - p, 1.0), index=pn.px.index)
        return pn.book(kind).mul(mult, axis=0)
    if grid == "stop":
        return pn.book(kind, stop=p)
    if grid == "gross":
        return pn.book(kind, gross=p)
    if grid == "crypto":
        E = pn.book(kind, gross=BOOK_GROSS * (1 - p))
        if p == 0.0:
            return E
        c = [t for t in CRYPTO if t in pn.px.columns]
        avail = pn.px[c].notna().astype(float)
        k = avail.sum(axis=1)
        cw = avail.div(k.where(k > 0), axis=0).fillna(0.0) * (BOOK_GROSS * p)
        E = E.copy()
        E[c] = E[c].values + cw.values
        return E
    raise ValueError(grid)


# ----------------------------------------------------------------- fast backtest + metrics
def fast_bt(pn, w):
    wt = w.reindex(pn.px.index).reindex(columns=pn.cols).fillna(0.0).shift(1).fillna(0.0).values
    rets, mask = pn.rets, pn.mask
    n = len(rets)
    cur = np.zeros(len(pn.cols))
    port = np.empty(n)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        g = cur * (1.0 + rets[i])
        tot = g.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = g / tot
    return pd.Series(port, index=pn.px.index), pd.Series(turn, index=pn.px.index)


def nm3(r):
    r = np.asarray(r, dtype=float)
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return cagr, ((float(r.mean()) * 252.0) / sd if sd else np.nan), dd


def full_row(r):
    h = len(r) // 2
    c, s, d = nm3(r.values)
    _, h1, _ = nm3(r.iloc[:h].values)
    _, h2, _ = nm3(r.iloc[h:].values)
    ic, is_, idd = nm3(r.loc[:IS_END].values)
    oc, os_, od = nm3(r.loc[SPLIT:].values)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(r, base):
    return bool(r["H1"] > base["H1"] and r["H2"] > base["H2"] and r["MaxDD"] >= base["MaxDD"])


def keep_4b(r, spy):
    return bool(r["H1"] > spy["H1"] and r["H2"] > spy["H2"] and r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["MaxDD"] >= 0.60 * spy["MaxDD"] and r["CAGR"] >= 0.70 * spy["CAGR"])


def keep_4b_oos(r, spy):
    return bool(r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and r["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    sa, sb = ra.std(), rb.std()
    return float(np.mean((ra - ra.mean()) * (rb - rb.mean())) / (sa * sb)) if sa and sb else np.nan


# ----------------------------------------------------------------- selection on one grid
def cell_stats(sub, vals):
    """sub: dict pk -> row (full_row + extras) for every pool point of one cell.
    vals: the grid's parameter values.  Returns (sharpe_pick, null_pick, rand_mean, best_oos)."""
    rows = [(v, sub[pk(v)]) for v in vals]
    gname = rows[0][1]["grid"]
    rows.sort(key=lambda t: pkey(gname, t[0]))
    best_is, pick = -np.inf, None
    for v, r in rows:
        if r["IS_Sharpe"] > best_is:
            best_is, pick = r["IS_Sharpe"], (v, r)
    nullv = NULL_P[gname]
    nullr = sub[pk(nullv)]
    rand_oos = float(np.mean([r["OOS_Sharpe"] for _, r in rows]))
    rand_cagr = float(np.mean([r["OOS_CAGR"] for _, r in rows]))
    rand_dd = float(np.mean([r["OOS_MaxDD"] for _, r in rows]))
    best_oos = float(np.max([r["OOS_Sharpe"] for _, r in rows]))
    return pick, nullr, (rand_oos, rand_cagr, rand_dd), best_oos


def main():
    t0 = time.time()
    P("=" * 150)
    P("IDEA 110 — selection-vs-no-selection-as-the-real-question   (lane B, 2026-09-07)")
    P("=" * 150)
    P("  Pre-registered: H_SURVIVES (mean premium_total > 0 and >= 75/100 random grids positive) |")
    P("  H_NOT_CHERRY (committed grid <= 95th percentile of the null) | H_SKILL (S_sharpe - S_rand")
    P("  > 0 in >= 75/100) | H_RANKIC (pooled within-cell spearman(IS Sharpe, OOS Sharpe) > 0).")
    P(f"  Pool spans each instrument's range; 100 random grids of the SAME SHAPE, seed {SEED}.")

    u56 = load_universe(exclude=set())          # keeps BTC/ETH for the crypto instrument
    broad = load_universe(broad=True)
    P(f"\n[data] u56 {u56.shape[1]} cols (incl. {[t for t in CRYPTO if t in u56.columns]}), "
      f"broad {broad.shape[1]} cols; index {u56.index[0].date()} -> {u56.index[-1].date()}")

    panels = {"u56": Panel("u56", u56), "broad": Panel("broad", broad)}

    # ---------------- G2/G3: cost linearity and metric identity, before any result
    pn = panels["u56"]
    w0 = pn.book("top20")
    gr, to = fast_bt(pn, w0)
    st = pn.start
    direct = backtest(pn.px, w0, cost_bps=10, freq=FREQ)["returns"].loc[st:]
    derived = (gr - to * 10 / 1e4).loc[st:]
    e_cost = float((derived - direct).abs().max())
    m_eng = metrics(derived)
    c, s, d = nm3(derived.values)
    e_met = max(abs(c - m_eng["CAGR"]), abs(s - m_eng["Sharpe"]), abs(d - m_eng["MaxDD"]))
    P(f"[G2] cost linearity, max |derived - engine.backtest(10bps)| = {e_cost:.3e}")
    P(f"[G3] metric identity, max |nm3 - engine.metrics|           = {e_met:.3e}")
    assert e_cost < 1e-12 and e_met < 1e-12

    # ---------------- references
    refs = {}
    for tag, pn in panels.items():
        st = pn.start
        spy = full_row(pn.px["SPY"].pct_change().fillna(0).loc[st:])
        v1g, v1t = fast_bt(pn, rules_v1_weights(pn.px))
        v2g, v2t = fast_bt(pn, rules_v2_weights(pn.px))
        refs[tag] = dict(spy=spy, v1=(v1g.loc[st:], v1t.loc[st:]), v2=(v2g.loc[st:], v2t.loc[st:]))
        P("\n" + "=" * 150)
        P(f"### PANEL {tag}: {pn.px.shape[1]} tickers | eval {st.date()} -> {pn.px.index[-1].date()}")
        tbl = {"SPY": spy}
        for bps in COSTS:
            tbl[f"RULES v2 (live) @{bps}"] = full_row(v2g.loc[st:] - v2t.loc[st:] * bps / 1e4)
            tbl[f"RULES v1 @{bps}"] = full_row(v1g.loc[st:] - v1t.loc[st:] * bps / 1e4)
        P(fmt(pd.DataFrame(tbl).T[["CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                   "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]))

    # ---------------- run the whole pool once
    P("\n" + "=" * 150)
    P("### THE POOL — every parameter value of every instrument, backtested once")
    P("=" * 150)
    pool_rows = []
    store = {}                     # (tag, grid, book, bps) -> {pk: row}
    npts = 0
    for tag, pn in panels.items():
        st = pn.start
        for grid in INSTR:
            if grid == "crypto" and not all(t in pn.px.columns for t in CRYPTO):
                P(f"  [skip] {tag} | {grid}: crypto tickers absent from this panel")
                continue
            for kind in ("top20", "ewall"):
                for p in POOLS[grid]:
                    w = overlay(pn, kind, grid, p)
                    g, t = fast_bt(pn, w)
                    g, t = g.loc[st:], t.loc[st:]
                    gross = float(w.loc[st:].sum(axis=1).mean())
                    turn = float(t.sum() / (len(g) / 252))
                    npts += 1
                    for bps in COSTS:
                        row = full_row(g - t * bps / 1e4)
                        row.update(universe=tag, grid=grid, book=kind, param=pk(p),
                                   param_num=(np.nan if p is None else float(p)),
                                   cost_bps=bps, Gross=gross, Turn_yr=turn,
                                   is_null=(pk(p) == pk(NULL_P[grid])),
                                   in_committed=any(pk(p) == pk(q) for q in COMMITTED[grid]))
                        spy = refs[tag]["spy"]
                        bg, bt_ = refs[tag]["v2"]
                        og, ot = refs[tag]["v1"]
                        row["4a_v2"] = keep_4a(row, full_row(bg - bt_ * bps / 1e4))
                        row["4a_v1"] = keep_4a(row, full_row(og - ot * bps / 1e4))
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        pool_rows.append(row)
                        store.setdefault((tag, grid, kind, bps), {})[pk(p)] = row
    POOL = pd.DataFrame(pool_rows)
    POOL.to_csv(OUT.with_suffix(".pool.csv"), index=False)
    P(f"[pool] {npts} weight matrices x {len(COSTS)} cost rungs = {len(POOL)} points "
      f"-> {OUT.name}.pool.csv   ({time.time() - t0:.0f}s)")
    P(f"[pool] 4a vs RULES v2 {int(POOL['4a_v2'].sum())}/{len(POOL)} · "
      f"4a vs RULES v1 {int(POOL['4a_v1'].sum())}/{len(POOL)} · "
      f"4b full {int(POOL['4b'].sum())}/{len(POOL)} · 4b OOS-only {int(POOL['4b_oos'].sum())}/{len(POOL)}")

    cells = sorted(store)
    P(f"[cells] {len(cells)} = "
      + ", ".join(f"{t}x{len([c for c in cells if c[0] == t])}" for t in ("u56", "broad")))

    P("\n--- EVERY POOL POINT, 10 bps (25 bps in .pool.csv).  '*' = member of idea 109's grid")
    for (tag, grid, kind, bps), sub in sorted(store.items()):
        if bps != 10:
            continue
        d = pd.DataFrame([sub[k] for k in sub]).set_index("param")
        d.insert(0, "c", np.where(d["in_committed"], "*", ""))
        P(f"\n--- {tag} | {grid} | {kind} | 10 bps")
        P(fmt(d[["c", "Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD", "IS_CAGR", "IS_Sharpe",
                 "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a_v2", "4b", "4b_oos"]]))

    # ---------------- G1: reproduce idea 109 on the committed grid
    def run_grid(gridvals, label):
        """gridvals: {instrument: [values]}.  Returns per-cell picks DataFrame."""
        out = []
        for (tag, grid, kind, bps) in cells:
            sub = store[(tag, grid, kind, bps)]
            vals = gridvals[grid]
            (pv, pr), nullr, (r_oos, r_cagr, r_dd), best = cell_stats(sub, vals)
            spy = refs[tag]["spy"]
            out.append(dict(label=label, universe=tag, grid=grid, book=kind, cost_bps=bps,
                            param=pk(pv),
                            sh_IS=pr["IS_Sharpe"], sh_OOS=pr["OOS_Sharpe"],
                            sh_OOS_CAGR=pr["OOS_CAGR"], sh_OOS_MaxDD=pr["OOS_MaxDD"],
                            sh_CAGR=pr["CAGR"], sh_Sharpe=pr["Sharpe"], sh_MaxDD=pr["MaxDD"],
                            sh_H1=pr["H1"], sh_H2=pr["H2"],
                            nl_OOS=nullr["OOS_Sharpe"], nl_OOS_CAGR=nullr["OOS_CAGR"],
                            nl_OOS_MaxDD=nullr["OOS_MaxDD"],
                            rd_OOS=r_oos, rd_OOS_CAGR=r_cagr, rd_OOS_MaxDD=r_dd,
                            best_OOS=best, regret=pr["OOS_Sharpe"] - best,
                            sh_4a_v2=bool(pr["4a_v2"]), sh_4a_v1=bool(pr["4a_v1"]),
                            sh_4b=bool(pr["4b"]), sh_4b_oos=bool(pr["4b_oos"]),
                            nl_4b=bool(nullr["4b"]), nl_4b_oos=bool(nullr["4b_oos"]),
                            spy_OOS=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                            spy_OOS_MaxDD=spy["OOS_MaxDD"]))
        return pd.DataFrame(out)

    C = run_grid(COMMITTED, "committed")
    C.to_csv(OUT.with_suffix(".picks.csv"), index=False)
    prem_tot_C = float((C.sh_OOS - C.nl_OOS).mean())
    prem_skl_C = float((C.sh_OOS - C.rd_OOS).mean())
    prem_ins_C = float((C.rd_OOS - C.nl_OOS).mean())

    P("\n" + "=" * 150)
    P("### G1 — REPRODUCE IDEA 109 ON ITS COMMITTED GRID (its numbers: S_sharpe 1.048, S_null 0.993, gap +0.055)")
    P("=" * 150)
    P(f"  S_sharpe mean OOS Sharpe {C.sh_OOS.mean():.4f}   (idea 109: 1.048, |d| = {abs(C.sh_OOS.mean() - 1.048):.4f})")
    P(f"  S_null   mean OOS Sharpe {C.nl_OOS.mean():.4f}   (idea 109: 0.993, |d| = {abs(C.nl_OOS.mean() - 0.993):.4f})")
    P(f"  premium_total            {prem_tot_C:+.4f}   (idea 109: +0.055)")
    P(f"  cells {len(C)} (idea 109: 44)")
    P(f"\n  DECOMPOSITION on the committed grid:")
    P(f"    premium_total  S_sharpe - S_null  = {prem_tot_C:+.4f}")
    P(f"    premium_skill  S_sharpe - S_rand  = {prem_skl_C:+.4f}   <- what rule 8's ARGMAX is worth")
    P(f"    premium_instr  S_rand   - S_null  = {prem_ins_C:+.4f}   <- what HAVING an overlay is worth")
    P(f"    share of the total carried by the argmax: {100 * prem_skl_C / prem_tot_C:.1f}%"
      if abs(prem_tot_C) > 1e-9 else "")
    P("\n  Per-cell picks on the committed grid:")
    P(fmt(C.set_index(["universe", "grid", "book", "cost_bps"])[
        ["param", "sh_IS", "sh_OOS", "nl_OOS", "rd_OOS", "best_OOS", "regret",
         "sh_4a_v2", "sh_4b", "sh_4b_oos"]]))

    # ---------------- the null distribution
    P("\n" + "=" * 150)
    P(f"### THE NULL DISTRIBUTION — {N_RANDOM} random grids of the SAME SHAPE (seed {SEED})")
    P("=" * 150)
    rng = np.random.default_rng(SEED)
    nulls = []
    for it in range(N_RANDOM):
        gv = {}
        for g in INSTR:
            k = len(COMMITTED[g])
            rest = [v for v in POOLS[g] if pk(v) != pk(NULL_P[g])]
            idx = rng.choice(len(rest), size=k - 1, replace=False)
            gv[g] = [NULL_P[g]] + [rest[i] for i in idx]
        R = run_grid(gv, f"rand{it:03d}")
        nulls.append(dict(
            it=it,
            prem_total=float((R.sh_OOS - R.nl_OOS).mean()),
            prem_skill=float((R.sh_OOS - R.rd_OOS).mean()),
            prem_instr=float((R.rd_OOS - R.nl_OOS).mean()),
            sh_OOS=float(R.sh_OOS.mean()), nl_OOS=float(R.nl_OOS.mean()),
            rd_OOS=float(R.rd_OOS.mean()),
            sh_OOS_CAGR=float(R.sh_OOS_CAGR.mean()), sh_OOS_MaxDD=float(R.sh_OOS_MaxDD.mean()),
            regret=float(R.regret.mean()),
            sh_4b=int(R.sh_4b.sum()), sh_4b_oos=int(R.sh_4b_oos.sum()),
            sh_4a_v2=int(R.sh_4a_v2.sum()), sh_4a_v1=int(R.sh_4a_v1.sum()),
            beats_SPY_OOS=int((R.sh_OOS > R.spy_OOS).sum()),
            prem_total_xc=float((R[R.grid != "crypto"].sh_OOS - R[R.grid != "crypto"].nl_OOS).mean()),
            prem_skill_xc=float((R[R.grid != "crypto"].sh_OOS - R[R.grid != "crypto"].rd_OOS).mean()),
            cells_sh_gt_nl=int((R.sh_OOS > R.nl_OOS).sum()),
            cells_sh_gt_rd=int((R.sh_OOS > R.rd_OOS).sum()),
        ))
    NU = pd.DataFrame(nulls)
    NU.to_csv(OUT.with_suffix(".null.csv"), index=False)
    P(f"[null] {len(NU)} random grids -> {OUT.name}.null.csv   ({time.time() - t0:.0f}s)")

    def pct_of(series, x):
        return 100.0 * float((np.asarray(series) <= x).mean())

    def describe(col, committed_val, name):
        v = NU[col].values
        P(f"\n  {name}")
        P(f"    null over {len(v)} random grids: mean {v.mean():+.4f}  sd {v.std(ddof=1):.4f}  "
          f"min {v.min():+.4f}  p05 {np.percentile(v, 5):+.4f}  median {np.median(v):+.4f}  "
          f"p95 {np.percentile(v, 95):+.4f}  max {v.max():+.4f}")
        P(f"    positive in {int((v > 0).sum())}/{len(v)} random grids")
        P(f"    idea 109's COMMITTED grid = {committed_val:+.4f}  ->  percentile "
          f"{pct_of(v, committed_val):.0f} of the null")

    describe("prem_total", prem_tot_C, "premium_total = mean OOS Sharpe(S_sharpe) - mean OOS Sharpe(S_null)   [idea 109's +0.055]")
    describe("prem_skill", prem_skl_C, "premium_skill = mean OOS Sharpe(S_sharpe) - mean OOS Sharpe(S_rand)   [the ARGMAX's own contribution]")
    describe("prem_instr", prem_ins_C, "premium_instr = mean OOS Sharpe(S_rand)   - mean OOS Sharpe(S_null)   [HAVING an overlay]")
    describe("prem_total_xc", float((C[C.grid != "crypto"].sh_OOS - C[C.grid != "crypto"].nl_OOS).mean()),
             "premium_total EXCLUDING the crypto instrument (short IS window)")
    describe("prem_skill_xc", float((C[C.grid != "crypto"].sh_OOS - C[C.grid != "crypto"].rd_OOS).mean()),
             "premium_skill EXCLUDING the crypto instrument")

    P("\n  Level of each selector across the null (mean over 44 cells, then over grids):")
    lv = pd.DataFrame({
        "S_sharpe": [NU.sh_OOS.mean(), NU.sh_OOS.std(ddof=1), NU.sh_OOS.min(), NU.sh_OOS.max(), C.sh_OOS.mean()],
        "S_rand":   [NU.rd_OOS.mean(), NU.rd_OOS.std(ddof=1), NU.rd_OOS.min(), NU.rd_OOS.max(), C.rd_OOS.mean()],
        "S_null":   [NU.nl_OOS.mean(), NU.nl_OOS.std(ddof=1), NU.nl_OOS.min(), NU.nl_OOS.max(), C.nl_OOS.mean()],
    }, index=["null mean", "null sd", "null min", "null max", "COMMITTED"]).T
    P(fmt(lv))

    # ---------------- hypotheses
    P("\n" + "=" * 150)
    P("### PRE-REGISTERED HYPOTHESES")
    P("=" * 150)
    n_pos_tot = int((NU.prem_total > 0).sum())
    n_pos_skl = int((NU.prem_skill > 0).sum())
    h_surv = (NU.prem_total.mean() > 0) and (n_pos_tot >= 75)
    p_cherry = pct_of(NU.prem_total.values, prem_tot_C)
    h_cherry = p_cherry <= 95
    h_skill = n_pos_skl >= 75
    P(f"  H_SURVIVES  : mean premium_total {NU.prem_total.mean():+.4f} > 0 and positive "
      f"{n_pos_tot}/100 (bar 75)  ->  {'PASS' if h_surv else 'FAIL'}")
    P(f"  H_NOT_CHERRY: committed grid at percentile {p_cherry:.0f} (bar <= 95)  ->  "
      f"{'PASS' if h_cherry else 'FAIL'}")
    P(f"  H_SKILL     : premium_skill positive {n_pos_skl}/100 (bar 75), null mean "
      f"{NU.prem_skill.mean():+.4f}  ->  {'PASS' if h_skill else 'FAIL'}")

    # H_RANKIC — the mechanism
    ics = []
    for (tag, grid, kind, bps), sub in store.items():
        d = pd.DataFrame(list(sub.values()))
        ics.append(dict(universe=tag, grid=grid, book=kind, cost_bps=bps, n=len(d),
                        rho=spearman(d.IS_Sharpe.values, d.OOS_Sharpe.values)))
    IC = pd.DataFrame(ics)
    pooled = float(IC.rho.mean())
    h_ic = pooled > 0
    P(f"  H_RANKIC    : within-cell spearman(IS Sharpe, OOS Sharpe) over the pool, mean over "
      f"{len(IC)} cells = {pooled:+.4f}, positive in {int((IC.rho > 0).sum())}/{len(IC)}  ->  "
      f"{'PASS' if h_ic else 'FAIL'}")
    P("\n  Rank IC by instrument (mean over cells):")
    P(fmt(IC.groupby("grid").rho.agg(["mean", "min", "max", "count"])))
    P("\n  Rank IC by panel x cost rung:")
    P(fmt(IC.pivot_table(index="universe", columns="cost_bps", values="rho")))
    IC.to_csv(OUT.with_suffix(".rankic.csv"), index=False)

    # ---------------- rule-8 walk-forward table: OOS outcome vs baseline and SPY
    P("\n" + "=" * 150)
    P("### RULE 8 WALK-FORWARD — OOS 2017-01-01.. , parameters chosen on IS only, vs baseline and SPY")
    P("=" * 150)
    wf = []
    for tag, pn in panels.items():
        st = pn.start
        for bps in COSTS:
            spy = refs[tag]["spy"]
            bg, bt_ = refs[tag]["v2"]
            og, ot = refs[tag]["v1"]
            v2 = full_row(bg - bt_ * bps / 1e4)
            v1 = full_row(og - ot * bps / 1e4)
            sel = C[(C.universe == tag) & (C.cost_bps == bps)]
            wf.append(dict(panel=tag, cost_bps=bps, arm="S_sharpe (committed grid)",
                           OOS_CAGR=sel.sh_OOS_CAGR.mean(), OOS_Sharpe=sel.sh_OOS.mean(),
                           OOS_MaxDD=sel.sh_OOS_MaxDD.mean()))
            wf.append(dict(panel=tag, cost_bps=bps, arm="S_rand (uniform pick)",
                           OOS_CAGR=sel.rd_OOS_CAGR.mean(), OOS_Sharpe=sel.rd_OOS.mean(),
                           OOS_MaxDD=sel.rd_OOS_MaxDD.mean()))
            wf.append(dict(panel=tag, cost_bps=bps, arm="S_null (no overlay)",
                           OOS_CAGR=sel.nl_OOS_CAGR.mean(), OOS_Sharpe=sel.nl_OOS.mean(),
                           OOS_MaxDD=sel.nl_OOS_MaxDD.mean()))
            wf.append(dict(panel=tag, cost_bps=bps, arm="RULES v2 (live baseline)",
                           OOS_CAGR=v2["OOS_CAGR"], OOS_Sharpe=v2["OOS_Sharpe"], OOS_MaxDD=v2["OOS_MaxDD"]))
            wf.append(dict(panel=tag, cost_bps=bps, arm="RULES v1 (previous)",
                           OOS_CAGR=v1["OOS_CAGR"], OOS_Sharpe=v1["OOS_Sharpe"], OOS_MaxDD=v1["OOS_MaxDD"]))
            wf.append(dict(panel=tag, cost_bps=bps, arm="SPY",
                           OOS_CAGR=spy["OOS_CAGR"], OOS_Sharpe=spy["OOS_Sharpe"], OOS_MaxDD=spy["OOS_MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(fmt(WF.set_index(["panel", "cost_bps", "arm"])))

    P("\n  Full-sample halves for S_sharpe's picks on the committed grid (4a/4b inputs):")
    P(fmt(C.groupby(["universe", "cost_bps"])[["sh_CAGR", "sh_Sharpe", "sh_MaxDD", "sh_H1", "sh_H2"]].mean()))
    P(f"\n  KEEP paths on the committed grid's 44 picks: 4a vs RULES v2 {int(C.sh_4a_v2.sum())}/44 · "
      f"4a vs RULES v1 {int(C.sh_4a_v1.sum())}/44 · 4b full {int(C.sh_4b.sum())}/44 · "
      f"4b OOS-only {int(C.sh_4b_oos.sum())}/44")
    P(f"  ... and on S_null's 44 points: 4b full {int(C.nl_4b.sum())}/44 · "
      f"4b OOS-only {int(C.nl_4b_oos.sum())}/44")
    P(f"  Across the 100 random grids, S_sharpe's 4b passes: mean {NU.sh_4b.mean():.2f}/44 "
      f"(min {NU.sh_4b.min()}, max {NU.sh_4b.max()}); 4a vs v2 mean {NU.sh_4a_v2.mean():.2f}/44 "
      f"(max {NU.sh_4a_v2.max()}); beats SPY OOS mean {NU.beats_SPY_OOS.mean():.1f}/44")

    # ---------------- per-cell sign counts
    P("\n" + "=" * 150)
    P("### HOW OFTEN DOES THE ARGMAX BEAT THE ALTERNATIVES, CELL BY CELL?")
    P("=" * 150)
    P(f"  committed grid: S_sharpe > S_null in {int((C.sh_OOS > C.nl_OOS).sum())}/44 cells, "
      f"S_sharpe > S_rand in {int((C.sh_OOS > C.rd_OOS).sum())}/44")
    P(f"  null (mean over 100 random grids): S_sharpe > S_null {NU.cells_sh_gt_nl.mean():.1f}/44, "
      f"S_sharpe > S_rand {NU.cells_sh_gt_rd.mean():.1f}/44")
    P("\n  Committed grid, premium by instrument (mean over its 4-8 cells):")
    bg = C.assign(prem_total=C.sh_OOS - C.nl_OOS, prem_skill=C.sh_OOS - C.rd_OOS,
                  prem_instr=C.rd_OOS - C.nl_OOS)
    P(fmt(bg.groupby("grid")[["prem_total", "prem_skill", "prem_instr", "regret"]].mean()
          .join(bg.groupby("grid").size().rename("cells"))))

    P("\n" + "=" * 150)
    P(f"### VERDICT INPUTS  (runtime {time.time() - t0:.0f}s)")
    P("=" * 150)
    P(f"  H_SURVIVES {'PASS' if h_surv else 'FAIL'} | H_NOT_CHERRY {'PASS' if h_cherry else 'FAIL'} | "
      f"H_SKILL {'PASS' if h_skill else 'FAIL'} | H_RANKIC {'PASS' if h_ic else 'FAIL'}")
    P(f"  committed premium_total {prem_tot_C:+.4f} = skill {prem_skl_C:+.4f} + instr {prem_ins_C:+.4f}")
    P(f"  null mean premium_total {NU.prem_total.mean():+.4f} = skill {NU.prem_skill.mean():+.4f} "
      f"+ instr {NU.prem_instr.mean():+.4f}")

    (OUT.with_suffix(".console.txt")).write_text("\n".join(_LOG) + "\n")
    print(f"\n[written] {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
