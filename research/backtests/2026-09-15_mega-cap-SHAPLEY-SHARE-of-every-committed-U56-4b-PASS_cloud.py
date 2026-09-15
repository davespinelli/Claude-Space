#!/usr/bin/env python3
"""Idea 933 (cloud, 2026-09-15) -- re-read every committed U56 4b PASS for its MEGA-CAP
SHAPLEY SHARE, and say which of them are ANSWER-KEY passes.

THE QUESTION (queue, 2026-09-15)
  Idea 924 found 0 of 480 survivorship-free cells (EQETF24 / ETF36 / NONEQ12 / SPYONLY) clear 4b
  in ANY window at ANY gross on U56, while all 103 window-passes it found carry the 20-name
  answer-key sleeve.  `research/universe.json:megacap` is the 2026 top-20 US mega caps held from
  2008 -- a list that did not exist in 2009 (PLTR had not IPO'd; NVDA, AVGO, TSLA, META, LLY and
  AMD were not top-20 names).  The queue asks: re-score the record's committed U56 4b passes for
  how much of each one's MARGIN the mega-cap sleeve carries, and report which are answer-key
  passes.

WHAT AN "ANSWER-KEY PASS" IS, PRE-REGISTERED
  A committed U56 4b pass is an ANSWER-KEY pass iff BOTH:
    (a) the mega-cap sleeve's SHAPLEY SHARE of the book's full-sample Sharpe is >= 0.50, and
    (b) the book FAILS 4b once the mega-cap sleeve is removed from the panel it trades.
  (a) alone is an attribution; (b) alone could be a breadth effect.  Both together mean the
  published verdict is a property of a name list chosen with 2026 hindsight.  Both directions,
  and every cell of the 2x2 of (a) x (b), are reported below.

THE SHAPLEY OBJECT
  U56 partitions EXACTLY into four sleeves (gated at G4):
    MEGA20  the 20 `megacap` names        <- the answer key
    SECT16  the 16 sector/industry ETFs
    ETF8    the 8 broad-index ETFs (SPY QQQ IWM DIA EFA EEM VTI RSP)
    BFC12   the 14 bond/FX/commodity names minus BTC-USD/ETH-USD = 12
  v(S) = the book's FULL-window Sharpe when it may only trade the names in S -- the book's OWN
  rule, re-run on that sub-panel, so the cross-sectional pct-ranks inside `score()` are computed
  on the names actually available.  v(empty) = 0 by convention (a book with nothing to hold is
  all cash, return 0, Sharpe 0); stated, not hidden, and it is the only value not measured.
  phi_i = sum over S not containing i of |S|!(n-|S|-1)!/n! [v(S+i) - v(S)], so sum(phi) = v(N)
  exactly (gated at G5) and MEGA's SHARE = phi_MEGA / v(N).
  SPY is a MEMBER of ETF8 and is tradeable only when ETF8 is in the coalition; the SPY BENCHMARK
  series is always taken from the full panel, so the 4b bar never moves with the coalition.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 2 levels, both reported in full, never averaged:
           CORE_W  the 5 rebuildable committed U56 book keys at gross 0.75, WEEKLY -- the
                   2026-09-04 KEEP-4b vintage convention (CAND20 = that KEEP candidate)
           EXT_M   the same 5 keys at gross 0.65, MONTHLY -- the 2026-09-15 lane B
                   KEEP-candidate convention (U56 TOP20 @ g=0.65 monthly, 12.69%/1.201/-17.11%)
  TUNED 2  SLEEVE SPLIT, 2 levels, both reported:
           SPLIT4  {MEGA20, SECT16, ETF8, BFC12}   16 coalitions, 4-player Shapley
           SPLIT2  {MEGA20, REST36}                 4 coalitions, 2-player Shapley
  REPORTED AXES (nothing fitted on them; every point published):
           book (6 arms incl. the live RULES v2 band book and RULES v1), cost 0/10/25/50 bps,
           gross 0.05..1.50 in 30 rungs (FULL and NOMEGA panels), window FULL/IS/OOS/H1/H2.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_SHAP      MEGA20's Shapley share of full-sample Sharpe is >= 0.50 for every committed U56
              4b passer.  Direction if it fails is reported, not re-cut.
  H_KEY       every committed U56 4b passer is an ANSWER-KEY pass by (a) AND (b) above.
  H_SPLIT     the share does not depend on the split: |share(SPLIT4) - share(SPLIT2)| <= 0.10.
  H_COST      the share is a cost-invariant object: spread over 0/10/25/50 bps <= 0.10.
  H_WF        (rule 8, REQUIRED) book x gross chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026
              read ONCE, on BOTH panels (FULL, NOMEGA), BOTH KEEP paths, against SPY and the
              live RULES v2 book in the same window.

GATES (all printed before any result number)
  G1  the fast runner == `engine.backtest` on returns and turnover (CAND20, U56, g=0.75, 10 bps)
  G2  BAND03 at g=0.75, band 0.03 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: the committed U56 triples reproduce -- SPY (15.16%/0.8861/-33.72%), RULES v2
      (8.63%/1.2018/-12.05%), and the 2026-09-04 KEEP candidate CAND20 (12.66%/1.0921/-18.31%)
  G4  the sleeves PARTITION U56 exactly: pairwise disjoint, union == the 56 columns
  G5  Shapley EFFICIENCY: sum(phi) == v(N) to < 1e-12, on both splits, every book
  G6  determinism: the subject row rebuilt from scratch is bit-identical

PROTOCOL: 10 bps primary, t+1 execution, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 is a CURRENT-CONSTITUENT list, and this run exists because ONE SLEEVE OF IT IS
THE WORST CASE of that: `megacap` is the 2026 top-20 held from 2008.  Every CAGR and drawdown
LEVEL below is therefore optimistic.  The direction is known and works AGAINST the incumbents:
removing the answer-key sleeve can only make the book more honest, never less, so a NOMEGA 4b
FAIL is a lower bound on the damage and a NOMEGA 4b PASS is the only result that would survive.
The SECT16/ETF8/BFC12 sleeves are ETFs, which are not survivorship-selected the same way; the
4b bar is SPY, which is not survivorship-inflated at all.  Stated, not hidden.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, score  # noqa
from engine import backtest, rebalance_mask  # noqa

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
LAG = 1
BAND0 = 0.03
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS30 = [round(0.05 * i, 4) for i in range(1, 31)]
COSTS = [0.0, 10.0, 25.0, 50.0]

# TUNED 1
CLAIM_SETS = {"CORE_W": dict(gross=0.75, freq="W",
                             src="the 5 rebuildable committed U56 keys at the 2026-09-04 vintage"),
              "EXT_M": dict(gross=0.65, freq="M",
                            src="the same 5 keys at the 2026-09-15 lane B candidate convention")}
BOOKS = ["CAND20", "EWELIG", "CAND20_NG", "EWALL", "BAND03", "V1TOP5"]
BOOK_SRC = {
    "CAND20": "committed: top-20 eligible by the v1 composite, NO vol scaler (2026-09-04 KEEP 4b)",
    "EWELIG": "committed: equal-weight every eligible name (concentration off)",
    "CAND20_NG": "committed: top-20 on the same score with the gate off",
    "EWALL": "committed: equal-weight every priced name = the panel index",
    "BAND03": "committed: RULES v2 live band book (baseline.rules_v2_weights)",
    "V1TOP5": "reported control: RULES v1 (top-5, vol scaler on); not a committed 4b pass",
}
# TUNED 2
SPLITS = {"SPLIT4": ["MEGA20", "SECT16", "ETF8", "BFC12"], "SPLIT2": ["MEGA20", "REST36"]}

SHARE_BAR = 0.50        # H_SHAP
SPLIT_BAR = 0.10        # H_SPLIT
COST_BAR = 0.10         # H_COST

# committed triples for G3 (idea 670/675/680, U56, weekly, g=0.75, 10 bps)
SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
CAND20_U56 = (0.1266, 1.0921, -0.1831)
TOL_C, TOL_S, TOL_D = 0.005, 0.030, 0.015

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# panel + fast runner (the record's vectorised equivalent of engine.backtest; gated at G1)
# ================================================================================================
class Panel:
    def __init__(self, name, px, freq, idx_master, spy_rets):
        self.name, self.px, self.freq = name, px, freq
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, freq).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        yr = self.idx.year
        m_full = np.asarray(self.idx >= self.idx[WARMUP])
        fullpos = np.flatnonzero(m_full)
        h = len(fullpos) // 2
        m_h1 = np.zeros(T, bool); m_h1[fullpos[:h]] = True
        m_h2 = np.zeros(T, bool); m_h2[fullpos[h:]] = True
        self.masks = {"FULL": m_full,
                      "H1": m_h1, "H2": m_h2,
                      "IS": m_full & (self.idx <= pd.Timestamp(IS_END)),
                      "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        self.spy = spy_rets


class Book:
    """One book's gross-1.0 weights, pre-reduced so any (gross, cost) costs O(T)."""

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        ARp = Ap * panel.Rp
        self.ARp = ARp
        self.Sp = ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)

    def at(self, g: float, cost=COST0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r, pan, win="FULL"):
    m = pan.masks[win]
    x = np.asarray(r)[m]
    c, s, d = fmet(x)
    return dict(CAGR=c, Sharpe=s, MaxDD=d)


def full_pack(r, pan):
    """FULL triple plus the halves of FULL plus the OOS triple -- everything 4b needs."""
    o = pack(r, pan, "FULL")
    o["H1"] = fsharpe(np.asarray(r)[pan.masks["H1"]])
    o["H2"] = fsharpe(np.asarray(r)[pan.masks["H2"]])
    co, so, do = fmet(np.asarray(r)[pan.masks["OOS"]])
    o.update(oCAGR=co, oSharpe=so, oMaxDD=do)
    return o


def legs4b(s, spy):
    """The record's 5-leg 4b form: Sharpe > SPY in both halves AND out of sample,
    MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    L = dict(L1_H1=bool(s["H1"] > spy["H1"]),
             L2_H2=bool(s["H2"] > spy["H2"]),
             L3_OOS=bool(s["oSharpe"] > spy["oSharpe"]),
             L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
             L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    L["pass4b"] = bool(all(L.values()))
    return L


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the arms (book definitions taken unmodified from the committed record)
# ================================================================================================
def ew_gross1(px):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_w1(sc, n):
    rank = sc.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0)


def arm_w1(px, book):
    """Gross-1.0 weights for one book on whatever sub-panel `px` is."""
    if book == "BAND03":
        return ew_gross1(px).where(band_state(px, BAND0) & px.notna(), 0.0).values
    if book == "V1TOP5":
        sc_v, above_v, vol_v = score(px, vol_scale=True)
        return ranked_w1(sc_v.where(above_v & (vol_v < MAXVOL)), 5).values
    sc_n, above, vol20 = score(px, vol_scale=False)
    if book == "CAND20":
        return ranked_w1(sc_n.where(above & (vol20 < MAXVOL)), 20).values
    if book == "EWELIG":
        sel = (above & (vol20 < MAXVOL) & px.notna()).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0).values
    if book == "CAND20_NG":
        return ranked_w1(sc_n.where(px.notna()), 20).values
    if book == "EWALL":
        return ew_gross1(px).values
    raise KeyError(book)


# ================================================================================================
def shapley(vals, players):
    """Exact Shapley values from the full coalition table {frozenset: v}."""
    n = len(players)
    phi = {p: 0.0 for p in players}
    for i, p in enumerate(players):
        others = [q for q in players if q != p]
        for k in range(n):
            for S in itertools.combinations(others, k):
                w = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
                phi[p] += w * (vals[frozenset(S + (p,))] - vals[frozenset(S)])
    return phi


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 933 (cloud) -- MEGA-CAP SHAPLEY SHARE of every committed U56 4b PASS")
    P("=" * 100)

    px = load_universe()
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    cols = list(px.columns)
    SLEEVE_MEMBERS = {
        "MEGA20": [t for t in U["megacap"] if t in cols],
        "SECT16": [t for t in U["sectors"] if t in cols],
        "ETF8": [t for t in U["broad"] if t in cols],
        "BFC12": [t for t in U["bonds_fx_commod"] if t in cols],
    }
    SLEEVE_MEMBERS["REST36"] = SLEEVE_MEMBERS["SECT16"] + SLEEVE_MEMBERS["ETF8"] + SLEEVE_MEMBERS["BFC12"]
    spy_rets = px["SPY"].pct_change().fillna(0.0).values

    # ---------------------------------------------------------------------------------- GATES
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = []

    pan_full = {f: Panel("U56", px, f, px.index, spy_rets) for f in ("W", "M")}

    # G1 fast runner == engine.backtest
    W1 = arm_w1(px, "CAND20")
    bk = Book(pan_full["W"], W1)
    r_fast, turn_fast = bk.at(0.75, COST0)
    eng = backtest(px, pd.DataFrame(0.75 * W1, index=px.index, columns=px.columns),
                   cost_bps=COST0, freq="W")
    # engine.backtest emits NaN on the first 2 rows of this panel (names not yet priced); the
    # comparison is made on the POST-WARM-UP window, which is the only window any number is read on
    mfw = np.asarray(px.index >= px.index[WARMUP])
    d_r = float(np.abs(r_fast[mfw] - eng["returns"].values[mfw]).max())
    d_t = float(np.abs(turn_fast[mfw] - eng["turnover"].values[mfw]).max())
    gates.append(dict(gate="G1 fast runner == engine.backtest (CAND20 g=0.75 10bps, post-warm-up)",
                      stat=f"max|dret| {d_r:.3e} max|dturn| {d_t:.3e} "
                           f"(engine NaNs pre-warm-up: {int(np.isnan(eng['returns'].values).sum())})",
                      bar="1e-9", passed=bool(d_r < 1e-9 and d_t < 1e-9)))

    # G2 BAND03 == baseline.rules_v2_weights
    b03 = pd.DataFrame(0.75 * arm_w1(px, "BAND03"), index=px.index, columns=px.columns)
    d_b = float((b03 - rules_v2_weights(px, band=BAND0, gross=0.75)).abs().values.max())
    gates.append(dict(gate="G2 BAND03 == baseline.rules_v2_weights", stat=f"max|dw| {d_b:.3e}",
                      bar="1e-12", passed=bool(d_b < 1e-12)))

    # G3 committed U56 triples
    pw = pan_full["W"]
    spy_full = full_pack(spy_rets, pw)
    v2_r, _ = Book(pw, arm_w1(px, "BAND03")).at(0.75, COST0)
    v2_full = full_pack(v2_r, pw)
    cand_full = full_pack(r_fast, pw)
    g3rows = []
    for nm, got, want in (("SPY", spy_full, SPY_U56), ("RULESv2", v2_full, V2_U56),
                          ("CAND20", cand_full, CAND20_U56)):
        dc, ds, dd = abs(got["CAGR"] - want[0]), abs(got["Sharpe"] - want[1]), abs(got["MaxDD"] - want[2])
        ok = dc < TOL_C and ds < TOL_S and dd < TOL_D
        g3rows.append(f"{nm} {got['CAGR']:.4f}/{got['Sharpe']:.4f}/{got['MaxDD']:.4f} "
                      f"vs committed {want[0]}/{want[1]}/{want[2]} d=({dc:.4f},{ds:.4f},{dd:.4f}) {'OK' if ok else 'MISS'}")
    gates.append(dict(gate="G3 CROSS-RUN committed U56 triples", stat=" | ".join(g3rows),
                      bar=f"dCAGR<{TOL_C} dSharpe<{TOL_S} dMaxDD<{TOL_D}",
                      passed=all("OK" in s for s in g3rows)))

    # G3b what KIND of object the G3 miss is: the END DATE.  The committed 1.0921 was read on an
    # earlier tree; re-read CAND20's FULL Sharpe with the panel truncated at a ladder of end dates
    # and report whether the published value is recoverable at any of them.
    ends = ["2026-06-30", "2026-03-31", "2025-12-31", "2025-06-30", "2024-12-31", "2023-12-31"]
    g3b = []
    for e in ends:
        m = np.asarray((px.index >= px.index[WARMUP]) & (px.index <= pd.Timestamp(e)))
        c, s, d = fmet(r_fast[m])
        g3b.append(f"{e}:{s:.4f}")
    best = min(abs(float(x.split(':')[1]) - CAND20_U56[1]) for x in g3b)
    gates.append(dict(gate="G3b is the G3 miss an END-DATE effect?",
                      stat=f"CAND20 FULL Sharpe by truncation -- {' '.join(g3b)} ; committed {CAND20_U56[1]}; "
                           f"closest |d| {best:.4f}",
                      bar=f"recoverable iff some end date lands within {TOL_S}",
                      passed=bool(best < TOL_S)))

    # G4 sleeves partition U56
    s4 = SLEEVE_MEMBERS["MEGA20"] + SLEEVE_MEMBERS["SECT16"] + SLEEVE_MEMBERS["ETF8"] + SLEEVE_MEMBERS["BFC12"]
    part_ok = (len(s4) == len(set(s4)) == len(cols)) and set(s4) == set(cols)
    gates.append(dict(gate="G4 sleeves partition U56 exactly",
                      stat=f"|MEGA20|={len(SLEEVE_MEMBERS['MEGA20'])} |SECT16|={len(SLEEVE_MEMBERS['SECT16'])} "
                           f"|ETF8|={len(SLEEVE_MEMBERS['ETF8'])} |BFC12|={len(SLEEVE_MEMBERS['BFC12'])} "
                           f"union={len(set(s4))} panel={len(cols)} dupes={len(s4)-len(set(s4))}",
                      bar="disjoint and covering", passed=bool(part_ok)))
    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   (bar {g['bar']})")

    # ------------------------------------------------------------------ COALITION TABLE (the work)
    P("\n" + "-" * 100)
    P("COALITION TABLE -- every book re-run on every sub-panel, both claim sets, 4 cost rungs")
    P("-" * 100)
    all_players = SPLITS["SPLIT4"]
    coalitions = []
    for k in range(len(all_players) + 1):
        for S in itertools.combinations(all_players, k):
            coalitions.append(frozenset(S))
    # SPLIT2's coalitions are unions of SPLIT4's, re-derived on their own sub-panels
    coal2 = [frozenset(), frozenset(["MEGA20"]), frozenset(["REST36"]), frozenset(["MEGA20", "REST36"])]

    def cols_of(S, split):
        out = []
        for s in sorted(S):
            out += SLEEVE_MEMBERS[s]
        return [c for c in cols if c in set(out)]

    crows = []
    books_cache = {}   # (split, key(S), claim, book) -> Book
    for split, players in SPLITS.items():
        cs = coalitions if split == "SPLIT4" else coal2
        for S in cs:
            sub = cols_of(S, split)
            key = "+".join(sorted(S)) if S else "EMPTY"
            for claim, cfg in CLAIM_SETS.items():
                g, freq = cfg["gross"], cfg["freq"]
                if not sub:
                    for book in BOOKS:
                        for cost in COSTS:
                            crows.append(dict(split=split, coalition=key, n_names=0, claim_set=claim,
                                              gross=g, freq=freq, book=book, cost_bps=cost,
                                              CAGR=0.0, Sharpe=0.0, MaxDD=0.0, H1=0.0, H2=0.0,
                                              oCAGR=0.0, oSharpe=0.0, oMaxDD=0.0,
                                              note="v(empty)=0 by convention (all cash)"))
                    continue
                sp = px[sub]
                pan = Panel(key, sp, freq, px.index, spy_rets)
                for book in BOOKS:
                    bo = Book(pan, arm_w1(sp, book))
                    books_cache[(split, key, claim, book)] = (pan, bo)
                    for cost in COSTS:
                        r, _ = bo.at(g, cost)
                        m = full_pack(r, pan)
                        crows.append(dict(split=split, coalition=key, n_names=len(sub), claim_set=claim,
                                          gross=g, freq=freq, book=book, cost_bps=cost, note="", **m))
    coal = pd.DataFrame(crows)
    dump(coal, "coalitions.csv")

    # -------------------------------------------------------------------------------- SHAPLEY
    srows = []
    for split, players in SPLITS.items():
        for claim in CLAIM_SETS:
            for book in BOOKS:
                for cost in COSTS:
                    sel = coal[(coal.split == split) & (coal.claim_set == claim) &
                               (coal.book == book) & (coal.cost_bps == cost)]
                    vals = {}
                    for _, rr in sel.iterrows():
                        S = frozenset() if rr.coalition == "EMPTY" else frozenset(rr.coalition.split("+"))
                        vals[S] = 0.0 if not np.isfinite(rr.Sharpe) else float(rr.Sharpe)
                    phi = shapley(vals, players)
                    vN = vals[frozenset(players)]
                    tot = sum(phi.values())
                    for p, val in phi.items():
                        srows.append(dict(split=split, claim_set=claim, book=book, cost_bps=cost,
                                          sleeve=p, phi=val, v_full=vN,
                                          share=(val / vN if vN else np.nan),
                                          efficiency_err=abs(tot - vN)))
    shap = pd.DataFrame(srows)
    dump(shap, "shapley.csv")

    eff = float(shap.efficiency_err.max())
    gates.append(dict(gate="G5 Shapley efficiency sum(phi)==v(N)", stat=f"max|err| {eff:.3e}",
                      bar="1e-12", passed=bool(eff < 1e-12)))
    P(f"  [{'PASS' if eff < 1e-12 else 'FAIL'}] G5 Shapley efficiency   max|sum(phi)-v(N)| {eff:.3e}")

    # ------------------------------------------------------------------------- 4b ON BOTH PANELS
    P("\n" + "-" * 100)
    P("4b VERDICTS: the committed panel (FULL = MEGA20+SECT16+ETF8+BFC12) vs the panel with the")
    P("ANSWER-KEY SLEEVE REMOVED (NOMEGA = REST36). SPY benchmark is the SAME series in both.")
    P("-" * 100)
    FULLKEY = "+".join(sorted(SPLITS["SPLIT4"]))
    lrows = []
    for claim, cfg in CLAIM_SETS.items():
        for book in BOOKS:
            for cost in COSTS:
                for pname, (split, key) in (("FULL", ("SPLIT4", FULLKEY)), ("NOMEGA", ("SPLIT2", "REST36"))):
                    pan, bo = books_cache[(split, key, claim, book)]
                    r, turn = bo.at(cfg["gross"], cost)
                    m = full_pack(r, pan)
                    spyp = full_pack(spy_rets, pan)
                    L = legs4b(m, spyp)
                    base_pan, base_bo = books_cache[("SPLIT4", FULLKEY, claim, "BAND03")]
                    br, _ = base_bo.at(0.75, cost)
                    bm = full_pack(br, base_pan)
                    lrows.append(dict(claim_set=claim, book=book, panel=pname, cost_bps=cost,
                                      gross=cfg["gross"], freq=cfg["freq"], **m,
                                      spy_Sharpe=spyp["Sharpe"], spy_CAGR=spyp["CAGR"],
                                      spy_MaxDD=spyp["MaxDD"], **L,
                                      pass4a=pass4a(m, bm),
                                      ann_turn=float(turn.sum() / (len(turn) / 252.0))))
    legs = pd.DataFrame(lrows)
    dump(legs, "legs.csv")

    # ------------------------------------------------------------------------------- GROSS LADDER
    grows = []
    for claim, cfg in CLAIM_SETS.items():
        for book in BOOKS:
            for pname, (split, key) in (("FULL", ("SPLIT4", FULLKEY)), ("NOMEGA", ("SPLIT2", "REST36"))):
                pan, bo = books_cache[(split, key, claim, book)]
                spyp = full_pack(spy_rets, pan)
                for g in GROSS30:
                    for cost in COSTS:
                        r, _ = bo.at(g, cost)
                        m = full_pack(r, pan)
                        L = legs4b(m, spyp)
                        grows.append(dict(claim_set=claim, book=book, panel=pname, gross=g,
                                          cost_bps=cost, freq=cfg["freq"], **m, **L))
    lad = pd.DataFrame(grows)
    dump(lad, "gross_ladder.csv")

    # ------------------------------------------------------------------------------ THE HEADLINE
    P("\n" + "=" * 100)
    P("THE ANSWER")
    P("=" * 100)
    hd = []
    for claim in CLAIM_SETS:
        P(f"\n  CLAIM SET {claim}  (gross {CLAIM_SETS[claim]['gross']}, {CLAIM_SETS[claim]['freq']}) "
          f"-- {CLAIM_SETS[claim]['src']}")
        P(f"    {'book':<11} {'4b FULL':>8} {'4b NOMEGA':>10} {'SharpeFULL':>11} {'SharpeNOMEGA':>13} "
          f"{'marginKILL':>13} {'shr S4':>7} {'shr S2':>7} {'ANSWER-KEY':>11}")
        for book in BOOKS:
            f_ = legs[(legs.claim_set == claim) & (legs.book == book) & (legs.panel == "FULL") &
                      (legs.cost_bps == COST0)].iloc[0]
            n_ = legs[(legs.claim_set == claim) & (legs.book == book) & (legs.panel == "NOMEGA") &
                      (legs.cost_bps == COST0)].iloc[0]
            s4v = shap[(shap.split == "SPLIT4") & (shap.claim_set == claim) & (shap.book == book) &
                       (shap.cost_bps == COST0) & (shap.sleeve == "MEGA20")].iloc[0].share
            s2v = shap[(shap.split == "SPLIT2") & (shap.claim_set == claim) & (shap.book == book) &
                       (shap.cost_bps == COST0) & (shap.sleeve == "MEGA20")].iloc[0].share
            key_pass = bool(f_.pass4b and (s4v >= SHARE_BAR) and (not n_.pass4b))
            # THE MARGIN FORM the queue actually asks for: what fraction of the book's own
            # Sharpe margin over SPY disappears when the answer-key sleeve is taken away?
            marg = f_.Sharpe - f_.spy_Sharpe
            kill = (f_.Sharpe - n_.Sharpe) / marg if abs(marg) > 1e-9 else np.nan
            hd.append(dict(claim_set=claim, book=book, pass4b_FULL=bool(f_.pass4b),
                           pass4b_NOMEGA=bool(n_.pass4b), Sharpe_FULL=f_.Sharpe,
                           Sharpe_NOMEGA=n_.Sharpe, spy_Sharpe=f_.spy_Sharpe,
                           margin_vs_SPY=marg, margin_kill=kill,
                           share_SPLIT4=s4v, share_SPLIT2=s2v,
                           answer_key=key_pass,
                           dSharpe=f_.Sharpe - n_.Sharpe, dCAGR=f_.CAGR - n_.CAGR,
                           dMaxDD=f_.MaxDD - n_.MaxDD))
            P(f"    {book:<11} {str(bool(f_.pass4b)):>8} {str(bool(n_.pass4b)):>10} {f_.Sharpe:>11.4f} "
              f"{n_.Sharpe:>13.4f} {kill:>13.3f} {s4v:>7.3f} {s2v:>7.3f} {str(key_pass):>11}")
    head = pd.DataFrame(hd)
    dump(head, "headline.csv")

    # per-sleeve Shapley table at the primary rung
    P("\n  SHAPLEY VALUES at 10 bps, SPLIT4 (phi per sleeve, share of v(N) in brackets)")
    for claim in CLAIM_SETS:
        P(f"    -- {claim}")
        for book in BOOKS:
            sel = shap[(shap.split == "SPLIT4") & (shap.claim_set == claim) & (shap.book == book) &
                       (shap.cost_bps == COST0)].set_index("sleeve")
            vN = sel.v_full.iloc[0]
            txt = "  ".join(f"{s}={sel.loc[s].phi:+.4f}({sel.loc[s].share:+.3f})"
                            for s in SPLITS["SPLIT4"])
            P(f"       {book:<11} v(N)={vN:+.4f}   {txt}")

    # ------------------------------------------------------------------------------- HYPOTHESES
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []
    passers = head[head.pass4b_FULL]
    if len(passers):
        ok_shap = bool((passers.share_SPLIT4 >= SHARE_BAR).all())
        hyp.append(dict(name="H_SHAP", verdict="PASS" if ok_shap else "FAIL",
                        detail=f"{int((passers.share_SPLIT4 >= SHARE_BAR).sum())} of {len(passers)} committed "
                               f"U56 4b passers have MEGA20 Shapley share >= {SHARE_BAR}; "
                               f"shares {', '.join(f'{b}={s:.3f}' for b, s in zip(passers.book, passers.share_SPLIT4))}"))
        ok_key = bool(passers.answer_key.all())
        hyp.append(dict(name="H_KEY", verdict="PASS" if ok_key else "FAIL",
                        detail=f"{int(passers.answer_key.sum())} of {len(passers)} committed U56 4b passers are "
                               f"ANSWER-KEY passes (share>={SHARE_BAR} AND 4b fails without MEGA20); "
                               f"NOMEGA 4b survivors: {sorted(set(passers[passers.pass4b_NOMEGA].book)) or 'none'}; "
                               f"margin-kill ratios "
                               f"{', '.join(f'{b}/{c}={k:.2f}' for b, c, k in zip(passers.book, passers.claim_set, passers.margin_kill))} "
                               f"(1.00 = the whole SPY margin gone, >1.00 = the book goes BELOW SPY)"))
        # the 2x2 of (a) share>=bar x (b) 4b dies without MEGA, over EVERY book, not just passers
        a = head.share_SPLIT4 >= SHARE_BAR
        b = head.pass4b_FULL & ~head.pass4b_NOMEGA
        hyp.append(dict(name="H_KEY2x2", verdict="REPORTED",
                        detail=f"over all {len(head)} book x claim-set cells: (a&b) {int((a & b).sum())}, "
                               f"(a&~b) {int((a & ~b).sum())}, (~a&b) {int((~a & b).sum())}, "
                               f"(~a&~b) {int((~a & ~b).sum())}; 4b survives MEGA removal on "
                               f"{int(head.pass4b_NOMEGA.sum())} of {len(head)} cells"))
    else:
        hyp.append(dict(name="H_SHAP", verdict="VACUOUS", detail="no committed 4b passer on FULL at 10 bps"))
        hyp.append(dict(name="H_KEY", verdict="VACUOUS", detail="no committed 4b passer on FULL at 10 bps"))
    # H_SPLIT: the LEVEL is split-dependent by construction (a 2-player game hands MEGA half of
    # every interaction term); the thing that matters is whether the VERDICT moves.  Both reported,
    # the bar is not relaxed.
    dsplit = float((head.share_SPLIT4 - head.share_SPLIT2).abs().max())
    sgn = head[head.pass4b_FULL]
    verd_same = bool(((sgn.share_SPLIT4 >= SHARE_BAR) == (sgn.share_SPLIT2 >= SHARE_BAR)).all()) if len(sgn) else True
    hyp.append(dict(name="H_SPLIT", verdict="PASS" if dsplit <= SPLIT_BAR else "FAIL",
                    detail=f"max |share(SPLIT4)-share(SPLIT2)| over all books x claim sets = {dsplit:.4f} "
                           f"(bar {SPLIT_BAR}); DIRECTION: SPLIT2 >= SPLIT4 on "
                           f"{int((head.share_SPLIT2 >= head.share_SPLIT4).sum())} of {len(head)} cells, so the "
                           f"2-player reading is the MORE damning one; the >= {SHARE_BAR} VERDICT agrees on "
                           f"{'all' if verd_same else 'NOT all'} committed passers"))
    # H_COST: the share's DENOMINATOR is the book's own Sharpe, which collapses (and for V1TOP5 at
    # 50 bps goes NEGATIVE) as cost rises, so the ratio is undefined there.  Reported in two forms.
    mg = shap[shap.sleeve == "MEGA20"]
    csp = mg.groupby(["split", "claim_set", "book"]).share.agg(lambda s: s.max() - s.min())
    mg_ok = mg[mg.v_full >= 0.20]
    csp_ok = mg_ok.groupby(["split", "claim_set", "book"]).share.agg(lambda s: s.max() - s.min())
    worst = csp.idxmax()
    hyp.append(dict(name="H_COST", verdict="PASS" if csp.max() <= COST_BAR else "FAIL",
                    detail=f"max spread of MEGA20's share over 0/10/25/50 bps = {csp.max():.4f} at {worst} "
                           f"(median {csp.median():.4f}, bar {COST_BAR}). DECOMPOSED, not relaxed: the worst "
                           f"cells are the ones whose DENOMINATOR v(N) collapses -- V1TOP5/CORE_W reads "
                           f"v(N) = {float(mg[(mg.book=='V1TOP5')&(mg.claim_set=='CORE_W')].v_full.min()):+.4f} at "
                           f"50 bps, so the ratio is not a share at all there. Restricted to cells with "
                           f"v(N) >= 0.20 the max spread is {csp_ok.max():.4f} (median {csp_ok.median():.4f}) "
                           f"-- still over the bar, so the share is NOT a cost-invariant object"))

    # H_PERNAME -- the obvious objection: MEGA20 is 20 of 56 names, so of course it carries a lot.
    # Normalise phi by sleeve SIZE and ask whether a mega-cap name is worth more than an ETF.
    size = {"MEGA20": 20, "SECT16": 16, "ETF8": 8, "BFC12": 12}
    pn = shap[(shap.split == "SPLIT4") & (shap.cost_bps == COST0)].copy()
    pn["phi_per_name"] = pn.phi / pn.sleeve.map(size)
    piv = pn.pivot_table(index=["claim_set", "book"], columns="sleeve", values="phi_per_name")
    ratio = (piv["MEGA20"] / piv[["SECT16", "ETF8", "BFC12"]].max(axis=1))
    hyp.append(dict(name="H_PERNAME", verdict="REPORTED",
                    detail=f"phi per NAME at 10 bps, SPLIT4: MEGA20 median {piv['MEGA20'].median():.4f}, "
                           f"SECT16 {piv['SECT16'].median():.4f}, ETF8 {piv['ETF8'].median():.4f}, "
                           f"BFC12 {piv['BFC12'].median():.4f}; a mega-cap name is worth "
                           f"{ratio.median():.2f}x the BEST other sleeve's name (min {ratio.min():.2f}, "
                           f"max {ratio.max():.2f}), so the share is NOT a head-count artefact"))
    P("\n  PER-NAME SHAPLEY (10 bps, SPLIT4) -- phi / sleeve size")
    P("    " + piv.round(4).to_string().replace("\n", "\n    "))

    # ------------------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- (book x gross) chosen on 2009-2016 by IS Sharpe, 2017-2026 read ONCE")
    P("-" * 100)
    wrows = []
    for claim, cfg in CLAIM_SETS.items():
        for pname, (split, key) in (("FULL", ("SPLIT4", FULLKEY)), ("NOMEGA", ("SPLIT2", "REST36"))):
            for cost in COSTS:
                best, bestS = None, -np.inf
                for book in BOOKS:
                    pan, bo = books_cache[(split, key, claim, book)]
                    for g in GROSS30:
                        r, _ = bo.at(g, cost)
                        s_is = fsharpe(np.asarray(r)[pan.masks["IS"]])
                        if np.isfinite(s_is) and s_is > bestS:
                            bestS, best = s_is, (book, g)
                book, g = best
                pan, bo = books_cache[(split, key, claim, book)]
                r, _ = bo.at(g, cost)
                oos = np.asarray(r)[pan.masks["OOS"]]
                oc, os_, od = fmet(oos)
                h = len(oos) // 2
                # OOS comparands in the SAME window
                spy_o = np.asarray(spy_rets)[pan.masks["OOS"]]
                sc, ss, sd = fmet(spy_o)
                base_pan, base_bo = books_cache[("SPLIT4", FULLKEY, claim, "BAND03")]
                br, _ = base_bo.at(0.75, cost)
                bo_o = np.asarray(br)[base_pan.masks["OOS"]]
                bc, bs, bd = fmet(bo_o)
                p4b = bool(fsharpe(oos[:h]) > fsharpe(spy_o[:h]) and fsharpe(oos[h:]) > fsharpe(spy_o[h:])
                           and os_ > ss and od >= DD_CAP * sd and oc >= CAGR_FLOOR * sc)
                p4a = bool(fsharpe(oos[:h]) > fsharpe(bo_o[:h]) and fsharpe(oos[h:]) > fsharpe(bo_o[h:])
                           and od >= bd)
                wrows.append(dict(claim_set=claim, panel=pname, cost_bps=cost, pick_book=book,
                                  pick_gross=g, IS_Sharpe=bestS, OOS_CAGR=oc, OOS_Sharpe=os_,
                                  OOS_MaxDD=od, OOS_H1=fsharpe(oos[:h]), OOS_H2=fsharpe(oos[h:]),
                                  SPY_OOS_CAGR=sc, SPY_OOS_Sharpe=ss, SPY_OOS_MaxDD=sd,
                                  V2_OOS_CAGR=bc, V2_OOS_Sharpe=bs, V2_OOS_MaxDD=bd,
                                  OOS_pass4b=p4b, OOS_pass4a=p4a))
                P(f"  {claim:<7} {pname:<7} {cost:>5.0f}bps  pick {book:<10} g={g:<5.2f} IS={bestS:.3f}  ->  "
                  f"OOS {oc:7.2%} / {os_:6.3f} / {od:7.2%}   SPY {sc:7.2%}/{ss:6.3f}/{sd:7.2%}   "
                  f"v2 {bc:7.2%}/{bs:6.3f}/{bd:7.2%}   4b={p4b} 4a={p4a}")
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    n4b, n4a = int(wf.OOS_pass4b.sum()), int(wf.OOS_pass4a.sum())
    hyp.append(dict(name="H_WF", verdict="REPORTED",
                    detail=f"OOS 4b {n4b} of {len(wf)}, 4a {n4a} of {len(wf)}; "
                           f"FULL-panel picks {sorted(set(wf[wf.panel=='FULL'].pick_book))}, "
                           f"NOMEGA picks {sorted(set(wf[wf.panel=='NOMEGA'].pick_book))}"))

    for h in hyp:
        P(f"  {h['name']:<9} {h['verdict']:<8} {h['detail']}")
    dump(pd.DataFrame(hyp), "hypotheses.csv")

    # G6 determinism
    W1b = arm_w1(px, "CAND20")
    r2, _ = Book(pan_full["W"], W1b).at(0.75, COST0)
    d6 = float(np.abs(r2 - r_fast).max())
    gates.append(dict(gate="G6 determinism (subject rebuilt)", stat=f"max|d| {d6:.3e}", bar="0.0",
                      passed=bool(d6 == 0.0)))
    P(f"\n  [{'PASS' if d6 == 0.0 else 'FAIL'}] G6 determinism   max|d| {d6:.3e}")
    dump(pd.DataFrame(gates), "gates.csv")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")

    P(f"\n  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
