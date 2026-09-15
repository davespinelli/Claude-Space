#!/usr/bin/env python3
"""Idea 674 (cloud, 2026-09-15) -- is the CAGR FLOOR the only bar separating a CONCENTRATED book
from its MATCHED control?

THE QUESTION (queue, 2026-09-11)
  Idea 504 found that on 1,000 nested k=40 draws of U56 at 10 bps the top-20 ranked book clears
  PROTOCOL 4b on 0.723 of draws while its EXACTLY gross-matched control (every eligible name,
  equal weight, at the ranked book's own daily gross) clears it on 0.178 -- a pass-rate gap of
  +0.545 -- even though the ranked book LOSES to that control on Sharpe (median dSharpe -0.0007).
  The queue's reading: 4b's three Sharpe legs are measured against SPY, so they cannot see
  concentration at all; only the CAGR floor can.  It asks: sweep the floor multiple against a
  FIXED matched-control family and report the concentration level at which 4b stops
  discriminating.

THE TWO BOOKS (idea 504's definitions, unchanged -- NOT 675's g/k convention)
  CAND_n   top n by the v1 composite WITHOUT the vol scaler, among names above their own 200d MA
           with 20d realised vol < 0.60, at a FIXED gross/n per name: fewer than n eligible means
           the book holds CASH (de-gross, never re-spread).
  EWmg_n   every eligible name in the same draw, equal weight, at CAND_n's OWN gross that day.
           This is the exactly gross-matched control, so CAND_n - EWmg_n is SELECTION and nothing
           else.  EWall (full gross on every eligible name) is reported beside it as the record's
           older, un-matched comparand.
  Weekly, decided at the close, executed next close, gross 0.75, 10 bps primary.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CAGR FLOOR MULTIPLE (the queue's own first dial), 8 levels, every one reported:
           0.00 / 0.40 / 0.55 / 0.70 (PROTOCOL 4b) / 0.85 / 1.00 / 1.15 / 1.30 x SPY's CAGR.
           The DD cap stays at PROTOCOL's 0.60 x SPY's MaxDD at every level.
  TUNED 2  CONCENTRATION n (the queue's own second dial), 6 levels: 3 / 5 / 10 / 20 / 30 / 40.
           n = 40 == k, i.e. the book can hold the whole draw and concentration is switched off.
  REPORTED AXES (nothing fitted on them; every point published): panel U56 / B136 / SMALL;
           cost rung 0 / 10 / 25 bps; window FULL / IS / OOS; the five 4b legs separately and
           every leave-one-leg-out reading; {CAND_n, EWmg_n, EWall} per draw.

PRE-REGISTERED BARS (fixed before any number is read; both directions reported)
  H_ONLY     the CAGR floor is the ONLY bar separating the two books iff, at PROTOCOL's own floor
             (0.70) and rung (10 bps), the FOUR-LEG discrimination -- 4b with the CAGR leg deleted
             -- is below 0.05 in absolute value at EVERY n.  Otherwise another leg also separates
             them and the queue's premise is only partly right.
  H_STOP     there is a concentration level n* at which 4b stops discriminating:
             |D(0.70, n*)| < 0.05, where D = pass4b(CAND_n) - pass4b(EWmg_n).  Reported at every n
             and every floor whether or not such an n* exists.
  H_MONO     D is monotone non-increasing in n (dilution): the less concentrated the book, the less
             4b can tell it from its own control.
  H_FLOOR    D is monotone non-decreasing in the floor multiple: a higher floor should favour the
             concentrated book, because concentration buys CAGR and not Sharpe.
  H_WF       (rule 8, required) n chosen on 2009-2016 ONLY, OOS 2017-2026 read once, both KEEP
             paths, against SPY and RULES v2 in the same window.

GATES (all printed before any result number)
  G1  the fast runner == engine.backtest on a draw's own CAND20 book (returns and turnover)
  G2  EWmg_n's daily gross == CAND_n's, every day, every n, every panel      bar 1e-12
  G3  CROSS-RUN: idea 504's committed `.draws.csv` numbers reproduce from this run's own grid at
      the same seed and draw count -- U56 / 10 bps / n=20 pass-rate gap +0.545 and median
      dSharpe -0.00067, against the committed CSV and re-derived here
  G4  the committed U56 triples (SPY, RULES v2)
  G5  floor monotonicity: a book's 4b pass rate is non-increasing in the floor multiple
  G6  determinism (rebuild one panel's draws, compare)

PROTOCOL: 10 bps primary, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown LEVEL
below is optimistic -- the concentrated book's and its control's alike.  A 4b bar is a RATIO of a
book's level to SPY's and SPY is not survivorship-inflated, so the bars are NOT protected by the
same-tape argument.  Worse for THIS question: concentration on a current-constituent list is the
exact place survivorship bites hardest -- the top-n book is picking, with hindsight-clean names,
out of a list that already excludes the dead -- so every pass rate for CAND_n here is an UPPER
bound and the discrimination D is an upper bound on what a point-in-time panel would show.  SMALL
additionally drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv.  Stated, not
hidden.
"""
from __future__ import annotations

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
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
COSTS = [0.0, 10.0, 25.0]
FREQ = "W"
LAG = 1
BAND0, GROSS0 = 0.03, 0.75
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP = 0.60                      # PROTOCOL 4b, fixed at every floor level
K = 40                             # idea 504's own sub-panel width
DRAWS = 1000                       # idea 504's own draw count (so G3 is an exact comparison)
SEED0 = 504                        # idea 504's own seed, for the same reason

# ---- TUNED DIAL 1: the CAGR floor multiple ----------------------------------------------------
FLOORS = [0.00, 0.40, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30]
FLOOR0 = 0.70                      # PROTOCOL 4b's own

# ---- TUNED DIAL 2: the concentration ----------------------------------------------------------
NS = [3, 5, 10, 20, 30, 40]
N0 = 20                            # the standing candidate's width (and 504's headline)

PANELS = ["U56", "B136", "SMALL"]
WINDOWS = ["FULL", "IS", "OOS"]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G504_GAP, G504_DS = 0.545, -0.00067        # idea 504's committed U56 / 10 bps / n=20 headline
G504_GAP_BAR, G504_DS_BAR = 0.05, 5e-3
PARENT504 = ROOT / "research" / "backtests" / \
    "2026-09-10_price-the-EW-ALL-control-for-the-top-20-book-on-the-1000-draw-grid_cloud.draws.csv"

ONLY_BAR = 0.05                    # H_ONLY / H_STOP
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# runner (the vectorised equivalent of engine.backtest; G1 pins it)
# ================================================================================================
class Panel:
    def __init__(self, px, masks=None):
        self.px = px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, FREQ).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        if masks is None:
            m_full = self.idx >= self.idx[WARMUP]
            masks = {"FULL": m_full,
                     "IS": m_full & (self.idx <= pd.Timestamp(IS_END)),
                     "OOS": self.idx >= pd.Timestamp(OOS_START)}
        self.masks = masks


class Book:
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

    def raw(self, g=GROSS0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross, turn

    def at(self, g=GROSS0, cost=COST0):
        r0, turn = self.raw(g)
        return r0 - turn * cost / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))


# ================================================================================================
# the 4b legs, with the CAGR floor as a FREE MULTIPLE (the tuned dial) -- everything else fixed
# ================================================================================================
def legs(full, oos_sharpe, spy_full, spy_oos_sharpe, floor):
    return dict(L1_H1=bool(full["H1"] > spy_full["H1"]),
                L2_H2=bool(full["H2"] > spy_full["H2"]),
                L3_OOS=bool(oos_sharpe > spy_oos_sharpe),
                L4_DDcap=bool(abs(full["MaxDD"]) <= DD_CAP * abs(spy_full["MaxDD"])),
                L5_CAGRfloor=bool(full["CAGR"] >= floor * spy_full["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the books (idea 504's definitions, unchanged), as gross-1.0 weight matrices
# ================================================================================================
def books_for_draw(sc_sub, el_sub):
    """rank ONCE per draw, then every n and both books come off it.
    CAND_n  = (rank<=n)/n            -> daily gross k_sel/n (cash below n eligible)
    EWmg_n  = elig/k_elig * k_sel/n  -> the SAME daily gross, spread over every eligible name
    EWall   = elig/k_elig            -> full gross (the record's older, un-matched comparand)"""
    rank = sc_sub.where(el_sub).rank(axis=1, ascending=False)
    kel = el_sub.sum(axis=1).replace(0, np.nan)
    ew = el_sub.astype(float).div(kel, axis=0).fillna(0.0)
    W = {"EWall": ew.values}
    for n in NS:
        sel = (rank <= n).astype(float)
        cand = sel / n
        W[f"CAND{n}"] = cand.values
        W[f"EWmg{n}"] = ew.mul(cand.sum(axis=1), axis=0).fillna(0.0).values
    return W


# ================================================================================================
def build_refs(px, masks):
    pan = Panel(px, masks)
    spy = px["SPY"].pct_change().fillna(0.0).values
    spyref = {w: pack(spy[masks[w]]) for w in WINDOWS}
    v2w = rules_v2_weights(px, band=BAND0, gross=1.0).values
    v2b = Book(pan, v2w)
    v2ref = {}
    for c in COSTS:
        r = v2b.at(GROSS0, c)[0]
        v2ref[c] = {w: pack(r[masks[w]]) for w in WINDOWS}
    return pan, spyref, v2ref


def run_draws(px, spyref, v2ref, masks, sc, el, names, draws=DRAWS, seed0=SEED0):
    kk = min(K, len(names))
    rows = []
    for s in range(draws):
        sub = list(np.random.default_rng(seed0 + s).permutation(names))[:kk]
        q = px[sub]
        pan = Panel(q, masks)
        W = books_for_draw(sc[sub], el[sub])
        for bk, w1 in W.items():
            b = Book(pan, w1)
            r0, turn = b.raw(GROSS0)
            for c in COSTS:
                r = r0 - turn * c / 1e4
                full = pack(r[masks["FULL"]])
                iss = fsharpe(r[masks["IS"]])
                oos = pack(r[masks["OOS"]])
                rows.append(dict(draw=s, book=bk, cost=c,
                                 CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                                 H1=full["H1"], H2=full["H2"], IS_Sharpe=iss,
                                 OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"],
                                 OOS_MaxDD=oos["MaxDD"], OOS_H1=oos["H1"], OOS_H2=oos["H2"],
                                 gross_mean=float(np.abs(w1).sum(axis=1).mean() * GROSS0),
                                 pass4a=pass4a(full, v2ref[c]["FULL"])))
    G = pd.DataFrame(rows)
    # the five legs at every floor level
    for f in FLOORS:
        L = [legs(dict(H1=r.H1, H2=r.H2, MaxDD=r.MaxDD, CAGR=r.CAGR), r.OOS_Sharpe,
                  spyref["FULL"], spyref["OOS"]["Sharpe"], f) for r in G.itertuples()]
        tag = f"{f:.2f}"
        for leg in LEGS:
            G[f"{leg}@{tag}"] = [x[leg] for x in L]
        G[f"pass4b@{tag}"] = [all(x.values()) for x in L]
        # leave-one-leg-out readings (the H_ONLY decomposition)
        for drop in LEGS:
            G[f"pass4b_no{drop}@{tag}"] = [all(v for k, v in x.items() if k != drop) for x in L]
    return G


# ================================================================================================
# gates
# ================================================================================================
def run_gates(px, pan, spyref, v2ref, masks, sc, el, names, G_u56):
    P("=" * 112)
    P("GATES (printed before any result number is read)")
    P("=" * 112)
    ok = {}
    sub = list(np.random.default_rng(SEED0).permutation(names))[:K]
    q = px[sub]
    p2 = Panel(q, masks)
    W = books_for_draw(sc[sub], el[sub])
    b = Book(p2, W[f"CAND{N0}"])
    r_fast, t_fast = b.at(GROSS0, COST0)
    wdf = pd.DataFrame(W[f"CAND{N0}"] * GROSS0, index=q.index, columns=q.columns)
    res = backtest(q, wdf, cost_bps=COST0, freq=FREQ)
    dr = float(np.nanmax(np.abs(r_fast - res["returns"].values)))
    dt = float(np.nanmax(np.abs(t_fast - res["turnover"].values)))
    ok["G1"] = max(dr, dt) < 1e-10
    P(f"G1  fast Book.at == engine.backtest (one draw's CAND20)   max|dr| {dr:.3e} "
      f"max|dturn| {dt:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")

    worst = 0.0
    for n in NS:
        gc = np.abs(W[f"CAND{n}"]).sum(axis=1)
        gm = np.abs(W[f"EWmg{n}"]).sum(axis=1)
        worst = max(worst, float(np.nanmax(np.abs(gc - gm))))
    ok["G2"] = worst < 1e-12
    P(f"G2  EWmg_n daily gross == CAND_n's, every n, every day    max|dg| {worst:.3e}   -> "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    z = G_u56[G_u56.cost == COST0]
    c20 = z[z.book == f"CAND{N0}"].set_index("draw")
    mg20 = z[z.book == f"EWmg{N0}"].set_index("draw")
    gap = float(c20[f"pass4b@{FLOOR0:.2f}"].mean() - mg20[f"pass4b@{FLOOR0:.2f}"].mean())
    dsh = float((c20.Sharpe - mg20.Sharpe).median())
    com = pd.read_csv(PARENT504)
    cz = com[(com.panel == "U56") & (com.cost == COST0)]
    gap_c = float(cz.CAND20_keep4b.mean() - cz.EWmg_keep4b.mean())
    dsh_c = float((cz.CAND20_Sharpe - cz.EWmg_Sharpe).median())
    ok["G3"] = (abs(gap - G504_GAP) < G504_GAP_BAR and abs(dsh - G504_DS) < G504_DS_BAR
                and abs(gap_c - G504_GAP) < 1e-9)
    P(f"G3  CROSS-RUN vs idea 504's committed .draws.csv          pass-rate gap "
      f"{gap:+.4f} (committed {gap_c:+.4f}, headline {G504_GAP:+.3f}); median dSharpe "
      f"{dsh:+.5f} (committed {dsh_c:+.5f})   -> {'PASS' if ok['G3'] else 'FAIL'}")

    s, v = spyref["FULL"], v2ref[COST0]["FULL"]
    d1 = (abs(s["CAGR"] - SPY_U56[0]), abs(s["Sharpe"] - SPY_U56[1]), abs(s["MaxDD"] - SPY_U56[2]))
    d2 = (abs(v["CAGR"] - V2_U56[0]), abs(v["Sharpe"] - V2_U56[1]), abs(v["MaxDD"] - V2_U56[2]))
    ok["G4"] = all(a < b for a, b in zip(d1, (TOL_C, TOL_S, TOL_D))) and \
        all(a < b for a, b in zip(d2, (TOL_C, TOL_S, TOL_D)))
    P(f"G4  committed U56 triples                                 SPY {s['CAGR']:.4%}/"
      f"{s['Sharpe']:.4f}/{s['MaxDD']:.4%}  v2 {v['CAGR']:.4%}/{v['Sharpe']:.4f}/{v['MaxDD']:.4%}"
      f"   -> {'PASS' if ok['G4'] else 'FAIL'}")

    bad = 0
    for bk, zz in G_u56[G_u56.cost == COST0].groupby("book"):
        rates = [zz[f"pass4b@{f:.2f}"].mean() for f in FLOORS]
        if any(rates[i + 1] > rates[i] + 1e-12 for i in range(len(rates) - 1)):
            bad += 1
    ok["G5"] = bad == 0
    P(f"G5  floor monotonicity (pass rate non-increasing in floor) {bad} violating books of "
      f"{G_u56.book.nunique()}   -> {'PASS' if ok['G5'] else 'FAIL'}")
    return ok


# ================================================================================================
def discrimination(G, floor, cost):
    """D(n) = pass4b(CAND_n) - pass4b(EWmg_n) over draws, plus every leave-one-leg-out reading."""
    tag = f"{floor:.2f}"
    z = G[G.cost == cost]
    rows = []
    for n in NS:
        a = z[z.book == f"CAND{n}"]
        b = z[z.book == f"EWmg{n}"]
        rec = dict(n=n, floor=floor, cost=cost,
                   cand=float(a[f"pass4b@{tag}"].mean()), ctrl=float(b[f"pass4b@{tag}"].mean()))
        rec["D"] = rec["cand"] - rec["ctrl"]
        for drop in LEGS:
            rec[f"D_no{drop}"] = float(a[f"pass4b_no{drop}@{tag}"].mean()
                                       - b[f"pass4b_no{drop}@{tag}"].mean())
        for leg in LEGS:
            rec[f"cand_{leg}"] = float(a[f"{leg}@{tag}"].mean())
            rec[f"ctrl_{leg}"] = float(b[f"{leg}@{tag}"].mean())
            rec[f"Dleg_{leg}"] = rec[f"cand_{leg}"] - rec[f"ctrl_{leg}"]
        # PAIRED medians: the per-draw difference, median over draws (not a difference of medians)
        ai, bi = a.set_index("draw"), b.set_index("draw")
        rec["dSharpe_med"] = float((ai.Sharpe - bi.Sharpe).median())
        rec["dCAGR_med"] = float((ai.CAGR - bi.CAGR).median())
        rec["dMaxDD_med"] = float((ai.MaxDD - bi.MaxDD).median())
        rec["dSharpe_win"] = float((ai.Sharpe > bi.Sharpe).mean())
        rec["gross_cand"] = float(a.gross_mean.mean())
        rec["gross_ctrl"] = float(b.gross_mean.mean())
        rows.append(rec)
    return pd.DataFrame(rows)


def rule8(G, spyref, v2ref, panel):
    """n chosen on 2009-2016 IS Sharpe ALONE, among the concentrated family and its controls;
    2017-2026 read once.  Both KEEP paths, per draw, at every cost rung."""
    rows = []
    fam = {"CANDfam": [f"CAND{n}" for n in NS],
           "CTRLfam": [f"EWmg{n}" for n in NS],
           "BOTH": [f"CAND{n}" for n in NS] + [f"EWmg{n}" for n in NS] + ["EWall"]}
    for cost in COSTS:
        z = G[G.cost == cost]
        piv_is = z.pivot(index="draw", columns="book", values="IS_Sharpe")
        for label, cols in fam.items():
            pick = piv_is[cols].idxmax(axis=1)
            recs = []
            for d, bk in pick.items():
                r = z[(z.draw == d) & (z.book == bk)].iloc[0]
                Lo = legs(dict(H1=r.OOS_H1, H2=r.OOS_H2, MaxDD=r.OOS_MaxDD, CAGR=r.OOS_CAGR),
                          r.OOS_Sharpe, spyref["OOS"], spyref["OOS"]["Sharpe"], FLOOR0)
                recs.append(dict(book=bk, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                 OOS_MaxDD=r.OOS_MaxDD, p4b=all(Lo.values()),
                                 p4a=pass4a(dict(H1=r.OOS_H1, H2=r.OOS_H2, MaxDD=r.OOS_MaxDD),
                                            v2ref[cost]["OOS"])))
            R = pd.DataFrame(recs)
            top = R.book.value_counts()
            rows.append(dict(panel=panel, cost=cost, family=label, n_draws=len(R),
                             modal_pick=top.index[0], modal_share=float(top.iloc[0] / len(R)),
                             OOS_CAGR=float(R.OOS_CAGR.mean()),
                             OOS_Sharpe=float(R.OOS_Sharpe.mean()),
                             OOS_MaxDD=float(R.OOS_MaxDD.mean()),
                             OOS_4b=float(R.p4b.mean()), OOS_4a=float(R.p4a.mean()),
                             SPY_OOS_CAGR=spyref["OOS"]["CAGR"],
                             SPY_OOS_Sharpe=spyref["OOS"]["Sharpe"],
                             SPY_OOS_MaxDD=spyref["OOS"]["MaxDD"],
                             V2_OOS_CAGR=v2ref[cost]["OOS"]["CAGR"],
                             V2_OOS_Sharpe=v2ref[cost]["OOS"]["Sharpe"],
                             V2_OOS_MaxDD=v2ref[cost]["OOS"]["MaxDD"]))
    return pd.DataFrame(rows)


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 674 (cloud, 2026-09-15) -- is the CAGR FLOOR the only bar separating a CONCENTRATED")
    P("                               book from its MATCHED control?")
    P("=" * 112)
    P(f"TUNED 1 CAGR floor multiple ({len(FLOORS)} levels, all reported): {FLOORS}  "
      f"(PROTOCOL 4b's own is {FLOOR0}; the DD cap stays {DD_CAP} throughout)")
    P(f"TUNED 2 concentration n ({len(NS)} levels): {NS}  (n = {K} == k, concentration OFF)")
    P(f"reported: panels {PANELS} x cost {[int(c) for c in COSTS]} bps x {DRAWS} nested k={K} "
      f"draws (seed {SEED0}, idea 504's own) x windows {WINDOWS}; five legs and every "
      f"leave-one-out")
    P(f"BOOKS: CAND_n (gross {GROSS0}/n per name, CASH below n eligible) vs EWmg_n (every eligible "
      f"name at CAND_n's OWN daily gross) -- idea 504's definitions; EWall reported beside them")
    P(f"BARS: H_ONLY four-leg |D| < {ONLY_BAR} at every n; H_STOP an n* with |D| < {ONLY_BAR}; "
      f"H_MONO D non-increasing in n; H_FLOOR D non-decreasing in the floor; H_WF rule 8")
    P("")

    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    GRIDS, REFS, WF = {}, {}, []
    gates = None
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in bad]]
        m_full = px.index >= px.index[WARMUP]
        masks = {"FULL": m_full, "IS": m_full & (px.index <= pd.Timestamp(IS_END)),
                 "OOS": px.index >= pd.Timestamp(OOS_START)}
        pan, spyref, v2ref = build_refs(px, masks)
        sc, above, vol20 = score(px, vol_scale=False)
        el = above & (vol20 < MAXVOL) & px.notna()
        names = [c for c in px.columns if c != "SPY"]
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols, {len(names)} tradable  "
          f"SPY {spyref['FULL']['CAGR']:.2%}/{spyref['FULL']['Sharpe']:.4f}/"
          f"{spyref['FULL']['MaxDD']:.2%}  (H1 {spyref['FULL']['H1']:.4f}/"
          f"H2 {spyref['FULL']['H2']:.4f}, OOS S {spyref['OOS']['Sharpe']:.4f})")
        t1 = time.time()
        G = run_draws(px, spyref, v2ref, masks, sc, el, names)
        P(f"       {DRAWS} draws x {len(NS) * 2 + 1} books x {len(COSTS)} rungs "
          f"= {len(G):,} scored books in {time.time() - t1:.1f}s")
        GRIDS[nm], REFS[nm] = G, (spyref, v2ref)
        if nm == "U56":
            P("")
            gates = run_gates(px, pan, spyref, v2ref, masks, sc, el, names, G)
            P("")
        WF.append(rule8(G, spyref, v2ref, nm))
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    P("")
    P("=" * 112)
    P("(A) THE FLOOR x CONCENTRATION SURFACE -- D = pass4b(CAND_n) - pass4b(EWmg_n), 10 bps")
    P("=" * 112)
    DS = []
    for nm in PANELS:
        for f in FLOORS:
            for c in COSTS:
                d = discrimination(GRIDS[nm], f, c)
                d.insert(0, "panel", nm)
                DS.append(d)
    D = pd.concat(DS, ignore_index=True)
    dump(D, "surface.csv")
    for nm in PANELS:
        P("")
        P(f"  {nm}  (rows = CAGR floor multiple, cols = n; each cell D = CAND - CTRL pass rate)")
        z = D[(D.panel == nm) & (D.cost == COST0)]
        P("    floor |" + "".join(f"  n={n:<6d}" for n in NS))
        for f in FLOORS:
            r = z[z.floor == f].set_index("n")
            star = " <- PROTOCOL" if f == FLOOR0 else ""
            P(f"    {f:5.2f} |" + "".join(f"  {r.loc[n, 'D']:+.4f} " for n in NS) + star)
        P("    pass rates at the PROTOCOL floor, CAND / CTRL:")
        r = z[z.floor == FLOOR0].set_index("n")
        P("          |" + "".join(f"  {r.loc[n, 'cand']:.3f}/{r.loc[n, 'ctrl']:.3f}" for n in NS))

    P("")
    P("=" * 112)
    P("(B) H_ONLY -- delete ONE leg at a time and re-read the discrimination (PROTOCOL floor, "
      "10 bps)")
    P("=" * 112)
    P("  panel   n |      D   | D with the named leg DELETED")
    P("            |          |" + "".join(f"  no-{L:12s}" for L in LEGS))
    for nm in PANELS:
        z = D[(D.panel == nm) & (D.cost == COST0) & (D.floor == FLOOR0)].set_index("n")
        for n in NS:
            r = z.loc[n]
            P(f"  {nm:6s} {n:2d} |  {r.D:+.4f} |" + "".join(f"  {r[f'D_no{L}']:+.4f}       "
                                                            for L in LEGS))
    P("")
    worst_noL5 = D[(D.cost == COST0) & (D.floor == FLOOR0)].D_noL5_CAGRfloor.abs().max()
    n_over = int((D[(D.cost == COST0) & (D.floor == FLOOR0)].D_noL5_CAGRfloor.abs()
                  >= ONLY_BAR).sum())
    P(f"  H_ONLY: with the CAGR floor deleted, max |D| over all {len(PANELS) * len(NS)} "
      f"(panel, n) cells = {worst_noL5:.4f}; {n_over} cells at or above the {ONLY_BAR} bar  -> "
      f"{'CONFIRMED (the CAGR floor is the only separating bar)' if n_over == 0 else 'REFUTED (another leg separates them too)'}")
    P("  per-leg pass-rate gaps at the PROTOCOL floor and 10 bps (CAND minus CTRL):")
    P("    panel   n |" + "".join(f"  {L:14s}" for L in LEGS))
    for nm in PANELS:
        z = D[(D.panel == nm) & (D.cost == COST0) & (D.floor == FLOOR0)].set_index("n")
        for n in NS:
            r = z.loc[n]
            P(f"    {nm:6s} {n:2d} |" + "".join(f"  {r[f'Dleg_{L}']:+.4f}        " for L in LEGS))

    P("")
    P("=" * 112)
    P("(C) H_STOP -- the concentration at which 4b stops discriminating")
    P("=" * 112)
    stops = []
    for nm in PANELS:
        for f in FLOORS:
            z = D[(D.panel == nm) & (D.cost == COST0) & (D.floor == f)].set_index("n")
            ns = [n for n in NS if abs(z.loc[n, "D"]) < ONLY_BAR]
            stops.append(dict(panel=nm, floor=f, n_star=(min(ns) if ns else np.nan),
                              D_at_20=z.loc[N0, "D"], D_at_40=z.loc[40, "D"],
                              mono=bool(all(z.loc[NS[i + 1], "D"] <= z.loc[NS[i], "D"] + 1e-12
                                            for i in range(len(NS) - 1)))))
    S = pd.DataFrame(stops)
    dump(S, "stops.csv")
    P("  panel   floor   n* (first n with |D| < bar)   D(n=20)   D(n=40)   D monotone in n?")
    for _, r in S.iterrows():
        ns = "none <= 40" if not np.isfinite(r.n_star) else f"{int(r.n_star)}"
        P(f"  {r.panel:6s} {r.floor:5.2f}   {ns:>26s}   {r.D_at_20:+.4f}   {r.D_at_40:+.4f}   "
          f"{'yes' if r.mono else 'NO'}")
    P("")
    P(f"  H_MONO: D non-increasing in n on {int(S.mono.sum())} of {len(S)} (panel, floor) rows")
    fl = []
    for nm in PANELS:
        for n in NS:
            z = D[(D.panel == nm) & (D.cost == COST0) & (D.n == n)].sort_values("floor")
            fl.append(bool(all(np.diff(z.D.values) >= -1e-12)))
    P(f"  H_FLOOR: D non-decreasing in the floor multiple on {sum(fl)} of {len(fl)} (panel, n) "
      f"cells")

    P("")
    P("=" * 112)
    P("(D) WHAT THE CONCENTRATED BOOK ACTUALLY BUYS (medians over draws, 10 bps)")
    P("=" * 112)
    P("  panel   n |  dSharpe   dCAGR    dMaxDD   win(S) | mean gross CAND / CTRL")
    P("  (paired per-draw differences, median over 1,000 draws; win(S) = share of draws where the")
    P("   concentrated book's Sharpe beats its own matched control's)")
    for nm in PANELS:
        z = D[(D.panel == nm) & (D.cost == COST0) & (D.floor == FLOOR0)].set_index("n")
        for n in NS:
            r = z.loc[n]
            P(f"  {nm:6s} {n:2d} |  {r.dSharpe_med:+.4f}  {r.dCAGR_med:+.4f}  "
              f"{r.dMaxDD_med:+.4f}  {r.dSharpe_win:.3f}  |  {r.gross_cand:.4f} / "
              f"{r.gross_ctrl:.4f}")

    P("")
    P("=" * 112)
    P("(E) RULE 8 -- n chosen on 2009-2016 IS Sharpe ALONE, 2017-2026 read once")
    P("=" * 112)
    W = pd.concat(WF, ignore_index=True)
    dump(W, "walkforward.csv")
    P("  panel  cost  family     modal pick (share)   OOS CAGR  Sharpe   MaxDD  | 4b rate  4a rate"
      "  | SPY OOS / RULES v2 OOS")
    for _, r in W.iterrows():
        P(f"  {r.panel:6s} {int(r.cost):3d}  {r.family:9s}  {r.modal_pick:8s} "
          f"({r.modal_share:.3f})   {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:7.2%}  | "
          f"{r.OOS_4b:.4f}   {r.OOS_4a:.4f}  | {r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.3f}/"
          f"{r.SPY_OOS_MaxDD:.2%}  {r.V2_OOS_CAGR:.2%}/{r.V2_OOS_Sharpe:.3f}/"
          f"{r.V2_OOS_MaxDD:.2%}")

    P("")
    P("=" * 112)
    P("(F) DETERMINISM (G6) and VERDICT")
    P("=" * 112)
    px = load_universe()
    m_full = px.index >= px.index[WARMUP]
    masks = {"FULL": m_full, "IS": m_full & (px.index <= pd.Timestamp(IS_END)),
             "OOS": px.index >= pd.Timestamp(OOS_START)}
    _, spyref, v2ref = build_refs(px, masks)
    sc, above, vol20 = score(px, vol_scale=False)
    el = above & (vol20 < MAXVOL) & px.notna()
    names = [c for c in px.columns if c != "SPY"]
    G2 = run_draws(px, spyref, v2ref, masks, sc, el, names, draws=25)
    A = GRIDS["U56"][GRIDS["U56"].draw < 25].select_dtypes(include=[float]).values
    B = G2.select_dtypes(include=[float]).values
    d = float(np.nanmax(np.abs(A - B))) if A.shape == B.shape else np.inf
    gates["G6"] = d == 0.0
    P(f"G6  determinism (first 25 U56 draws rebuilt): max|d| {d:.3e}   -> "
      f"{'PASS' if gates['G6'] else 'FAIL'}")
    dump(pd.concat([GRIDS[nm].assign(panel=nm) for nm in PANELS], ignore_index=True)
         .query("cost == 10.0")[["panel", "draw", "book", "cost", "CAGR", "Sharpe", "MaxDD",
                                 "H1", "H2", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                 f"pass4b@{FLOOR0:.2f}", "pass4a", "gross_mean"]], "draws.csv")
    P("")
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  "
      + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items())))
    P(f"elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return D, S, W


if __name__ == "__main__":
    main()
