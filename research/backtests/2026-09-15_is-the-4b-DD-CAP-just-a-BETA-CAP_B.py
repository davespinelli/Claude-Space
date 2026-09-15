#!/usr/bin/env python3
"""Idea 867 (lane B, 2026-09-15) -- is the 4b DD CAP just a BETA CAP?

THE QUESTION (queue, 2026-09-15)
  Ideas 662, 866 and 676 each found the same thing from a different side: de-grossing buys
  drawdown and pays CAGR.  If that is ALL the DD leg sees, then PROTOCOL 4b's

      DD cap    MaxDD(book) >= 0.60 * MaxDD(SPY)

  is not a test of a book at all -- it is a monotone read of the book's realised SPY beta,
  i.e. the constraint `beta <= 0.60` wearing a drawdown costume.  The queue asks: regress
  every shelf book's MaxDD on its own SPY beta and report the RESIDUAL -- does anything
  survive beta?

  The equivalence is EXACT on one ray and that is what makes the question sharp.  A zero-signal
  book g x SPY has beta = g identically and MaxDD = (the g-blend of SPY's own path), so on the
  cash/SPY ray the DD cap IS the beta cap, with no error at all (gate G4 proves this, it is not
  assumed).  The whole question is whether REAL books depart from that ray by enough to flip
  the leg.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  BETA ESTIMATOR (the queue's own first dial), 4 levels, every one reported:
           FULL  OLS beta of daily net book returns on SPY, over the window
           DOWN  the same restricted to days SPY < 0 (downside beta)
           ROLL  median of 252d rolling OLS betas
           DDWIN beta measured INSIDE the book's own peak-to-trough max-drawdown window
  TUNED 2  PANEL (the queue's own second dial), 3 levels: U56, B136, SMALL.
  REPORTED AXES (nothing below is fitted on them; every point published in .books.csv):
           family (4) x mode (3) x theta (3 where the mode reads breadth) x gross (4)
           = 112 books per panel, + ZEROSIG (4 rungs) + RANDGATE (3 seeds x 4 rungs)
           = 384 traded books x 3 windows (FULL / IS / OOS) x 4 beta estimators.

THE BOOK POPULATION (the machinery is the record's, unchanged from idea 677's lane-B script)
  ROW  hold each name passing its own gate at gross/N of NAV, rest in CASH
       (TREND/ROW at g=0.75 IS RULES v2 -- gate G1).
  AGG  know only the breadth b_t = (#passing)/(#priced): hold the WHOLE priced panel equal
       weighted at `gross` when b_t >= theta, else all cash.
  HYB  the ROW book, switched off on days when b_t < theta.
  families  TREND (200d MA +/-3% band), VOL (vol20 < 0.60), MOM (12-1 > 0),
            DISP (60d idiosyncratic vol below the panel's own cross-sectional mean).
  controls  ZEROSIG = g x SPY (the ray on which the two caps coincide exactly)
            RANDGATE = a seeded per-name random gate at 50% breadth.

PRE-REGISTERED HYPOTHESES (fixed before any number below was read)
  H1  MONOTONE READ.  |Spearman(beta, MaxDD)| >= 0.90 within panel, at a majority of the
      4 x 3 (estimator, panel) grid points.  This is the queue's literal claim.
  H2  SUBSTITUTION AT THE PROTOCOL'S OWN NUMBER.  The beta cap `beta <= 0.60` reproduces the
      DD leg's PASS/FAIL verdict on >= 95% of books.
  H2b BEST-CASE SUBSTITUTION.  Even with beta* chosen to MAXIMISE agreement (the most
      favourable beta cap that exists), agreement stays >= 95%.
  H3  BETA-MATCHED DISAGREEMENT.  Among book pairs matched to |dbeta| <= 0.02 within a panel,
      the share that DISAGREE on the DD leg is <= 5%.  This is the sharpest form: if the leg
      is a beta cap, two books at the same beta cannot land on opposite sides of it.
  H4  RESIDUAL IS NOISE (rule 8).  The residual MaxDD - f(beta) does not walk forward:
      Spearman(residual_IS, residual_OOS) < +0.30.
  H5  CAPITAL (rule 8).  An IS-only chooser on the DD RESIDUAL does no better out of sample
      than an IS-only chooser on beta alone -- if the residual is nothing, it cannot pick.

  The queue's hypothesis is CONFIRMED if H1, H2, H2b, H3 and H4 all hold.  Any one of them
  failing means the DD leg carries information beta does not.

PROTOCOL
  2  10 bps per unit turnover, weights at close t applied t+1 (LAG=1), weekly, no leverage
     (max gross rung 1.00).  Cost rungs 0 / 10 / 25 bps reported for the headline agreement.
  3  every reported book compared to RULES v2 (live) and to SPY buy-and-hold, same sample.
  4  BOTH KEEP paths evaluated, at every (estimator, panel) grid point.
  8  WALK-FORWARD: every fit, every residual and every chooser decision is computed on
     2009-2016 ALONE; 2017-2026 is read ONCE.
  9  SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists; every CAGR and drawdown
     LEVEL is optimistic.  The agreement rates and matched-pair contrasts are same-tape
     comparisons between books on one panel and are unaffected.

GATES (run and printed BEFORE any result number is read)
  G1  TREND/ROW at gross 0.75 IS baseline.rules_v2_weights (max |weight| and |return| dev).
  G2  fast Book.at() == engine.backtest on a representative book (returns AND turnover).
  G3  SPY and RULES v2 on U56 reproduce their committed triples
      (15.16%/0.8861/-33.72% and 8.63%/1.2018/-12.05%).
  G4  ZEROSIG at rung g has FULL beta == g and MaxDD/MaxDD(SPY) == g, both to tolerance --
      the analytic ray on which the DD cap and the beta cap are the SAME constraint.
  G5  DETERMINISM: the whole book grid rebuilt twice, max |dSharpe| and max |dbeta|.

Outputs beside this script: .console.txt .books.csv .agree.csv .matched.csv
                            .residual.csv .walkforward.csv .result.md
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                        # PROTOCOL 2
FREQ = "W"
LAG = 1
BAND = 0.03                        # RULES v2 clause 2
MAXVOL = 0.60                      # rules_v1_weights' committed max_vol
VOLWIN = 20
DISPWIN = 60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70    # PROTOCOL 4b
COSTRUNGS = [0.0, 10.0, 25.0]
ROLLWIN = 252
MATCH_TOL = 0.02                   # H3's beta-matching tolerance
AGREE_BAR = 0.95                   # H2 / H2b bar
RHO_BAR = 0.30                     # H4 bar
SPEARMAN_BAR = 0.90                # H1 bar

# ---- TUNED DIAL 1: beta estimator -------------------------------------------------------------
ESTIMATORS = ["FULL", "DOWN", "ROLL", "DDWIN"]
# ---- TUNED DIAL 2: panel ----------------------------------------------------------------------
PANELS = ["U56", "B136", "SMALL"]

# ---- reported axes ----------------------------------------------------------------------------
FAMILIES = ["TREND", "VOL", "MOM", "DISP"]
MODES = ["ROW", "AGG", "HYB"]
THETAS = [0.20, 0.40, 0.60]
GROSSES = [0.25, 0.50, 0.75, 1.00]
RAND_SEEDS = [8671, 8672, 8673]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015

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
# runner -- the record's vectorised equivalent of engine.backtest (gated at G2)
# ================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
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
        self.start = self.idx[WARMUP]
        self.m_full = self.idx >= self.start
        self.m_is = self.m_full & (self.idx <= pd.Timestamp(IS_END))
        self.m_oos = self.idx >= pd.Timestamp(OOS_START)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.masks = {"FULL": self.m_full, "IS": self.m_is, "OOS": self.m_oos}


class Book:
    """One book's gross-1.0 weights, pre-reduced so any gross rung costs O(T) + O(|reb| x N)."""

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
        del A, AR, Ap

    def at(self, g: float, cost=COST):
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


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


def legs4b(s, spy):
    return dict(H1=bool(s["H1"] > spy["H1"]), H2=bool(s["H2"] > spy["H2"]),
                DDCAP=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGRFLOOR=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4b(s, spy):
    L = legs4b(s, spy)
    return bool(all(L.values()))


# ================================================================================================
# beta estimators -- TUNED DIAL 1
# ================================================================================================
def _ols_beta(r, m):
    r, m = np.asarray(r, float), np.asarray(m, float)
    if len(r) < 20:
        return np.nan
    v = m.var(ddof=1)
    return float(np.cov(r, m, ddof=1)[0, 1] / v) if v > 0 else np.nan


def betas_all(r, m):
    """All four TUNED-1 readings of one book's beta over one window. r, m already windowed."""
    out = {}
    out["FULL"] = _ols_beta(r, m)
    dn = m < 0
    out["DOWN"] = _ols_beta(r[dn], m[dn]) if dn.sum() >= 20 else np.nan
    if len(r) >= ROLLWIN + 10:
        rs = pd.Series(r)
        ms = pd.Series(m)
        cov = rs.rolling(ROLLWIN).cov(ms)
        var = ms.rolling(ROLLWIN).var()
        out["ROLL"] = float((cov / var).dropna().median())
    else:
        out["ROLL"] = np.nan
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    tr = int(np.argmin(dd))
    pk = int(np.argmax(eq[: tr + 1])) if tr > 0 else 0
    out["DDWIN"] = _ols_beta(r[pk: tr + 1], m[pk: tr + 1]) if tr - pk >= 20 else np.nan
    return out


# ================================================================================================
# gate families -> per-name boolean IN(i,t)  (the record's definitions, unchanged)
# ================================================================================================
def gate_in(px, family, seed=None):
    priced = px.notna()
    if family == "TREND":
        g = band_state(px, BAND)
    elif family == "VOL":
        vol = px.pct_change().rolling(VOLWIN).std() * np.sqrt(252)
        g = vol < MAXVOL
    elif family == "MOM":
        g = (px.shift(21) / px.shift(252) - 1.0) > 0.0
    elif family == "DISP":
        r = px.pct_change()
        idio = r.sub(r.mean(axis=1), axis=0).rolling(DISPWIN).std() * np.sqrt(252)
        g = idio.lt(idio.mean(axis=1), axis=0)
    elif family == "RANDGATE":
        rng = np.random.default_rng(seed)
        g = pd.DataFrame(rng.random(px.shape) < 0.5, index=px.index, columns=px.columns)
    else:
        raise ValueError(family)
    return g.fillna(False) & priced


def ew_panel(px):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return priced.astype(float).div(n, axis=0).fillna(0.0)


def book_w1(ew, inb, b, mode, theta):
    if mode == "ROW":
        return ew.where(inb, 0.0).values
    on = (b >= theta).astype(float)
    if mode == "AGG":
        return ew.mul(on, axis=0).values
    return ew.where(inb, 0.0).mul(on, axis=0).values


# ================================================================================================
# gates
# ================================================================================================
def run_gates(panels):
    P("=" * 96)
    P("GATES (printed before any result number is read)")
    P("=" * 96)
    ok = {}

    pan = panels["U56"]
    px = pan.px
    ew = ew_panel(px)
    inb = gate_in(px, "TREND")
    W1 = book_w1(ew, inb, None, "ROW", 0.0)
    w_ref = rules_v2_weights(px, band=BAND, gross=0.75).values
    dw = float(np.nanmax(np.abs(W1 * 0.75 - w_ref)))
    bk = Book(pan, W1)
    r_fast, t_fast = bk.at(0.75)
    res_eng = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75), cost_bps=COST, freq=FREQ)
    dr = float(np.nanmax(np.abs(r_fast - res_eng["returns"].values)))
    ok["G1"] = dw < 1e-12
    P(f"G1  TREND/ROW g=0.75 == rules_v2_weights   max|dw| {dw:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")

    dt = float(np.nanmax(np.abs(t_fast - res_eng["turnover"].values)))
    ok["G2"] = dr < 1e-10 and dt < 1e-10
    P(f"G2  fast Book.at == engine.backtest        max|dr| {dr:.3e}  max|dturn| {dt:.3e}   "
      f"-> {'PASS' if ok['G2'] else 'FAIL'}")

    m = pan.m_full
    spy_t = fmet(pan.spy[m])
    v2_t = fmet(r_fast[m])
    d1 = (abs(spy_t[0] - SPY_U56[0]), abs(spy_t[1] - SPY_U56[1]), abs(spy_t[2] - SPY_U56[2]))
    d2 = (abs(v2_t[0] - V2_U56[0]), abs(v2_t[1] - V2_U56[1]), abs(v2_t[2] - V2_U56[2]))
    ok["G3"] = (d1[0] < TOL_C and d1[1] < TOL_S and d1[2] < TOL_D
                and d2[0] < TOL_C and d2[1] < TOL_S and d2[2] < TOL_D)
    P(f"G3  committed triples on U56   SPY {spy_t[0]:.4%}/{spy_t[1]:.4f}/{spy_t[2]:.4%}  "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%})")
    P(f"                              v2  {v2_t[0]:.4%}/{v2_t[1]:.4f}/{v2_t[2]:.4%}  "
      f"(committed {V2_U56[0]:.2%}/{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> {'PASS' if ok['G3'] else 'FAIL'}")

    # G4 -- the analytic ray: ZEROSIG beta == g and MaxDD ratio == g
    Z = np.zeros((pan.T, pan.N))
    Z[:, list(px.columns).index("SPY")] = 1.0
    zb = Book(pan, Z)
    rows = []
    for g in GROSSES:
        rz, _ = zb.at(g, cost=0.0)
        bt = betas_all(rz[m], pan.spy[m])["FULL"]
        _, _, ddz = fmet(rz[m])
        rows.append((g, bt, ddz / spy_t[2]))
    mb = max(abs(b - g) for g, b, _ in rows)
    mr = max(abs(rr - g) for g, _, rr in rows)
    ok["G4"] = mb < 0.02 and mr < 0.06
    P("G4  ZEROSIG ray (g x SPY, 0 bps)   " + "   ".join(
        f"g={g:.2f} beta={b:.3f} ddratio={rr:.3f}" for g, b, rr in rows))
    P(f"      max|beta-g| {mb:.3e}   max|ddratio-g| {mr:.3e}   -> {'PASS' if ok['G4'] else 'FAIL'}")
    return ok, rows


# ================================================================================================
# the book grid
# ================================================================================================
def build_books(pan: Panel, tag=""):
    """Returns list of (meta dict, returns array) for every traded book on this panel."""
    px = pan.px
    ew = ew_panel(px)
    priced = px.notna()
    npriced = priced.sum(axis=1).replace(0, np.nan)
    specs = []
    for fam in FAMILIES:
        inb = gate_in(px, fam)
        b = (inb.sum(axis=1) / npriced).fillna(0.0)
        specs.append((dict(family=fam, mode="ROW", theta=np.nan), book_w1(ew, inb, b, "ROW", 0.0)))
        for mode in ("AGG", "HYB"):
            for th in THETAS:
                specs.append((dict(family=fam, mode=mode, theta=th), book_w1(ew, inb, b, mode, th)))
    for sd in RAND_SEEDS:
        inb = gate_in(px, "RANDGATE", seed=sd)
        b = (inb.sum(axis=1) / npriced).fillna(0.0)
        specs.append((dict(family=f"RANDGATE{sd}", mode="ROW", theta=np.nan),
                      book_w1(ew, inb, b, "ROW", 0.0)))
    Z = np.zeros((pan.T, pan.N))
    Z[:, list(px.columns).index("SPY")] = 1.0
    specs.append((dict(family="ZEROSIG", mode="ROW", theta=np.nan), Z))

    out = []
    for meta, W1 in specs:
        bk = Book(pan, W1)
        for g in GROSSES:
            r, turn = bk.at(g, COST)
            md = dict(panel=pan.name, **meta, gross=g)
            md["turn_yr"] = float(turn[pan.m_full].sum() / (pan.m_full.sum() / 252.0))
            out.append((md, r, bk))
        del bk
    return out


def score_books(pan: Panel, books):
    """One row per (book, window): metrics + all four betas + the 4b legs."""
    rows = []
    ref = {}
    for win, m in pan.masks.items():
        ref[("SPY", win)] = pack(pan.spy[m])
    # RULES v2 (live) on this panel
    ew = ew_panel(pan.px)
    inb = gate_in(pan.px, "TREND")
    v2 = Book(pan, book_w1(ew, inb, None, "ROW", 0.0)).at(0.75, COST)[0]
    for win, m in pan.masks.items():
        ref[("V2", win)] = pack(v2[m])

    for md, r, _ in books:
        for win, m in pan.masks.items():
            rw, mw = r[m], pan.spy[m]
            s = pack(rw)
            bt = betas_all(rw, mw)
            spy = ref[("SPY", win)]
            L = legs4b(s, spy)
            row = dict(md)
            row.update(window=win, **{k: s[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")})
            row.update({f"beta_{k}": v for k, v in bt.items()})
            row.update(dd_ratio=s["MaxDD"] / spy["MaxDD"],
                       leg_DDCAP=L["DDCAP"], leg_CAGR=L["CAGRFLOOR"],
                       leg_H1=L["H1"], leg_H2=L["H2"],
                       pass4b=bool(all(L.values())),
                       pass4a=pass4a(s, ref[("V2", win)]))
            rows.append(row)
    return pd.DataFrame(rows), ref


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 96)
    P("IDEA 867 (lane B, 2026-09-15) -- is the 4b DD CAP just a BETA CAP?")
    P("=" * 96)
    P(f"TUNED 1 beta estimator: {ESTIMATORS}")
    P(f"TUNED 2 panel:          {PANELS}")
    P(f"reported axes: family {FAMILIES} x mode {MODES} x theta {THETAS} x gross {GROSSES}")
    P(f"                + ZEROSIG + RANDGATE{RAND_SEEDS};  cost {COST:.0f} bps, {FREQ}, LAG {LAG}")
    P("")

    panels = {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        panels[nm] = Panel(nm, px)
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  "
          f"{px.index[0].date()} .. {px.index[-1].date()}  eval from {panels[nm].start.date()}")
    P("")

    gates, zray = run_gates(panels)

    P("")
    P("=" * 96)
    P("BUILDING THE BOOK GRID")
    P("=" * 96)
    allb, refs, kept = [], {}, {}
    for nm in PANELS:
        t = time.time()
        bk = build_books(panels[nm])
        df, ref = score_books(panels[nm], bk)
        refs[nm] = ref
        kept[nm] = bk
        allb.append(df)
        P(f"  {nm:6s} {len(bk):4d} books  {len(df):5d} book-windows  ({time.time()-t:.1f}s)")
    B = pd.concat(allb, ignore_index=True)

    # determinism gate G5 -- rebuild U56 and compare
    bk2 = build_books(panels["U56"])
    d2, _ = score_books(panels["U56"], bk2)
    a = B[B.panel == "U56"].reset_index(drop=True)
    ds = float(np.nanmax(np.abs(a["Sharpe"].values - d2["Sharpe"].values)))
    db = float(np.nanmax(np.abs(a["beta_FULL"].values - d2["beta_FULL"].values)))
    gates["G5"] = ds < 1e-12 and db < 1e-12
    P(f"G5  DETERMINISM  max|dSharpe| {ds:.3e}  max|dbeta| {db:.3e}   "
      f"-> {'PASS' if gates['G5'] else 'FAIL'}")
    del bk2, d2
    P("")
    P(f"GATES: {sum(gates.values())} of {len(gates)} PASS  " + "  ".join(
        f"{k}={'PASS' if v else 'FAIL'}" for k, v in gates.items()))
    if not all(gates.values()):
        P("  *** a gate FAILED -- every number below is reported with that caveat ***")

    dump(B, "books.csv")
    real = B[~B.family.str.startswith(("ZEROSIG", "RANDGATE"))]
    P("")
    P(f"book grid: {B.panel.nunique()} panels, {len(B)} book-windows, "
      f"{len(B[B.window=='FULL'])} traded books ({len(real[real.window=='FULL'])} real, "
      f"{len(B[B.window=='FULL'])-len(real[real.window=='FULL'])} control)")

    # --------------------------------------------------------------------------------------
    # H1 -- is MaxDD a monotone read of beta?
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 96)
    P("H1  MONOTONE READ -- Spearman(beta, MaxDD) within panel, ALL 4 x 3 grid points")
    P("=" * 96)
    P(f"{'window':7s} {'panel':6s} " + " ".join(f"{e:>9s}" for e in ESTIMATORS)
      + "    (bar |rho| >= %.2f)" % SPEARMAN_BAR)
    h1rows = []
    for win in ("FULL", "IS", "OOS"):
        for pn in PANELS:
            sub = real[(real.window == win) & (real.panel == pn)]
            cells = []
            for e in ESTIMATORS:
                x, y = sub[f"beta_{e}"], sub["MaxDD"]
                ok = x.notna() & y.notna()
                rho = float(x[ok].rank().corr(y[ok].rank())) if ok.sum() > 5 else np.nan
                cells.append(rho)
                h1rows.append(dict(window=win, panel=pn, estimator=e, spearman=rho,
                                   n=int(ok.sum()), pass_bar=bool(abs(rho) >= SPEARMAN_BAR)))
            P(f"{win:7s} {pn:6s} " + " ".join(f"{c:9.3f}" for c in cells))
    H1 = pd.DataFrame(h1rows)
    nfull = H1[H1.window == "FULL"]
    h1_hits = int(nfull.pass_bar.sum())
    P(f"  FULL-window grid points clearing |rho| >= {SPEARMAN_BAR:.2f}: {h1_hits} of {len(nfull)}"
      f"   -> H1 {'HOLDS' if h1_hits > len(nfull)/2 else 'FAILS'}")
    # R2 and residual spread of the linear read
    P("")
    P(f"{'panel':6s} {'est':6s} {'R2':>7s} {'resid SD (pp of DD)':>21s} {'DD spread (pp)':>16s}")
    r2rows = []
    for pn in PANELS:
        for e in ESTIMATORS:
            sub = real[(real.window == "FULL") & (real.panel == pn)]
            x, y = sub[f"beta_{e}"].values, sub["MaxDD"].values
            ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() < 5:
                continue
            A = np.vstack([x[ok], np.ones(ok.sum())]).T
            coef, *_ = np.linalg.lstsq(A, y[ok], rcond=None)
            res = y[ok] - A @ coef
            r2 = 1.0 - res.var() / y[ok].var()
            r2rows.append(dict(panel=pn, estimator=e, slope=coef[0], intercept=coef[1],
                               R2=r2, resid_sd=res.std(), dd_sd=y[ok].std()))
            P(f"{pn:6s} {e:6s} {r2:7.3f} {res.std()*100:21.2f} {y[ok].std()*100:16.2f}")
    R2 = pd.DataFrame(r2rows)

    # --------------------------------------------------------------------------------------
    # H2 / H2b -- does a beta cap reproduce the DD leg's verdict?
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 96)
    P("H2  SUBSTITUTION -- does `beta <= 0.60` reproduce the DD leg PASS/FAIL?")
    P("    H2b the BEST beta* that exists (agreement maximised over a 0.001 grid)")
    P("=" * 96)
    P(f"{'panel':6s} {'est':6s} {'n':>4s} {'DDpass':>7s} {'b<=.60':>7s} {'agree':>7s} "
      f"{'TP':>4s} {'FP':>4s} {'FN':>4s} {'TN':>4s} | {'beta*':>6s} {'best agree':>10s}")
    agrows = []
    grid = np.arange(0.0, 2.001, 0.001)
    for pn in PANELS:
        for e in ESTIMATORS:
            sub = real[(real.window == "FULL") & (real.panel == pn)]
            x, y = sub[f"beta_{e}"].values, sub["leg_DDCAP"].values.astype(bool)
            ok = np.isfinite(x)
            x, y = x[ok], y[ok]
            pred = x <= DD_CAP
            TP = int((pred & y).sum()); FP = int((pred & ~y).sum())
            FN = int((~pred & y).sum()); TN = int((~pred & ~y).sum())
            agree = (TP + TN) / len(y)
            best_a, best_b = -1, np.nan
            for bb in grid:
                a = ((x <= bb) == y).mean()
                if a > best_a:
                    best_a, best_b = a, bb
            agrows.append(dict(panel=pn, estimator=e, n=len(y), dd_pass=int(y.sum()),
                               beta_pass=int(pred.sum()), agree=agree, TP=TP, FP=FP, FN=FN, TN=TN,
                               beta_star=best_b, best_agree=best_a))
            P(f"{pn:6s} {e:6s} {len(y):4d} {int(y.sum()):7d} {int(pred.sum()):7d} {agree:7.3f} "
              f"{TP:4d} {FP:4d} {FN:4d} {TN:4d} | {best_b:6.3f} {best_a:10.3f}")
    AG = pd.DataFrame(agrows)
    dump(AG, "agree.csv")
    h2 = int((AG.agree >= AGREE_BAR).sum())
    h2b = int((AG.best_agree >= AGREE_BAR).sum())
    P(f"  H2  cells with agreement >= {AGREE_BAR:.2f} at beta<=0.60 : {h2} of {len(AG)}"
      f"   -> H2  {'HOLDS' if h2 > len(AG)/2 else 'FAILS'}")
    P(f"  H2b cells with BEST-CASE agreement >= {AGREE_BAR:.2f}     : {h2b} of {len(AG)}"
      f"   -> H2b {'HOLDS' if h2b > len(AG)/2 else 'FAILS'}")
    P(f"  best-case agreement: min {AG.best_agree.min():.3f}  median {AG.best_agree.median():.3f} "
      f" max {AG.best_agree.max():.3f}")

    # MARGIN diagnostic -- why a 0.87-0.92 R2 read still cannot reproduce a BINARY leg
    P("")
    P("  MARGIN DIAGNOSTIC -- the DD leg is a bar, and a bar is flipped by the RESIDUAL, not by R2.")
    P(f"  {'panel':6s} {'est':6s} {'resid SD (pp)':>13s} {'|margin| med (pp)':>17s} "
      f"{'share |margin| < 1 resid SD':>27s}")
    mgrows = []
    for pn in PANELS:
        sub = real[(real.window == "FULL") & (real.panel == pn)]
        spy = refs[pn][("SPY", "FULL")]
        marg = (sub["MaxDD"].values - DD_CAP * spy["MaxDD"])           # + = passes, - = fails
        for e in ESTIMATORS:
            x, y = sub[f"beta_{e}"].values, sub["MaxDD"].values
            ok = np.isfinite(x) & np.isfinite(y)
            A = np.vstack([x[ok], np.ones(int(ok.sum()))]).T
            coef, *_ = np.linalg.lstsq(A, y[ok], rcond=None)
            sd = float((y[ok] - A @ coef).std())
            inside = float((np.abs(marg[ok]) < sd).mean())
            mgrows.append(dict(panel=pn, estimator=e, resid_sd=sd,
                               margin_med=float(np.median(np.abs(marg[ok]))), share_inside=inside))
            P(f"  {pn:6s} {e:6s} {sd*100:13.2f} {np.median(np.abs(marg[ok]))*100:17.2f} "
              f"{inside:27.3f}")
    MG = pd.DataFrame(mgrows)

    # does the substitution CHANGE the 4b verdict, or only the leg?
    P("")
    P("  DOES THE DISAGREEMENT REACH 4b? -- books where `beta<=0.60` and the DD leg differ AND")
    P("  the other three 4b legs (H1, H2, CAGR floor) all pass, i.e. the swap flips the 4b verdict:")
    flips = []
    for pn in PANELS:
        sub = real[(real.window == "FULL") & (real.panel == pn)]
        other = sub["leg_H1"] & sub["leg_H2"] & sub["leg_CAGR"]
        for e in ESTIMATORS:
            x = sub[f"beta_{e}"].values
            ok = np.isfinite(x)
            dis = (x <= DD_CAP) != sub["leg_DDCAP"].values.astype(bool)
            n_flip = int((dis & other.values & ok).sum())
            n_4b = int((sub["pass4b"].values & ok).sum())
            flips.append(dict(panel=pn, estimator=e, n_flip=n_flip, n_4b_pass=n_4b,
                              n_books=int(ok.sum())))
            P(f"  {pn:6s} {e:6s}  4b verdict flipped by the swap: {n_flip:3d} of {int(ok.sum()):3d} books"
              f"   (actual 4b passes {n_4b})")
    FL = pd.DataFrame(flips)

    # cost-rung robustness of the headline agreement (FULL beta, all panels pooled)
    P("")
    P("  COST RUNG check of the headline agreement (FULL estimator, pooled real books):")
    costrows = []
    for c in COSTRUNGS:
        accs = []
        for pn in PANELS:
            pan = panels[pn]
            m = pan.m_full
            spy = pack(pan.spy[m])
            for md, _, bkobj in kept[pn]:
                if str(md["family"]).startswith(("ZEROSIG", "RANDGATE")):
                    continue
                rr, _ = bkobj.at(md["gross"], c)
                s = pack(rr[m])
                bt = betas_all(rr[m], pan.spy[m])["FULL"]
                accs.append(((bt <= DD_CAP) == (s["MaxDD"] >= DD_CAP * spy["MaxDD"])))
        costrows.append(dict(cost_bps=c, agree=float(np.mean(accs)), n=len(accs)))
        P(f"    {c:5.1f} bps   agreement {np.mean(accs):.3f}  (n={len(accs)})")
    CR = pd.DataFrame(costrows)

    # --------------------------------------------------------------------------------------
    # H3 -- beta-matched pairs
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 96)
    P(f"H3  BETA-MATCHED PAIRS -- among books within |dbeta| <= {MATCH_TOL:.2f} on the same panel,")
    P("    how often do the two land on OPPOSITE sides of the DD leg?")
    P("=" * 96)
    P(f"{'panel':6s} {'est':6s} {'pairs':>8s} {'disagree':>9s} {'rate':>7s} "
      f"{'max |dMaxDD| within a matched pair (pp)':>40s}")
    mrows = []
    for pn in PANELS:
        for e in ESTIMATORS:
            sub = real[(real.window == "FULL") & (real.panel == pn)]
            x = sub[f"beta_{e}"].values
            y = sub["leg_DDCAP"].values.astype(bool)
            d = sub["MaxDD"].values
            ok = np.isfinite(x)
            x, y, d = x[ok], y[ok], d[ok]
            n = len(x)
            i, j = np.triu_indices(n, 1)
            close = np.abs(x[i] - x[j]) <= MATCH_TOL
            i, j = i[close], j[close]
            npair = len(i)
            dis = int((y[i] != y[j]).sum())
            maxdd = float(np.abs(d[i] - d[j]).max()) if npair else np.nan
            rate = dis / npair if npair else np.nan
            mrows.append(dict(panel=pn, estimator=e, pairs=npair, disagree=dis, rate=rate,
                              max_dMaxDD=maxdd))
            P(f"{pn:6s} {e:6s} {npair:8d} {dis:9d} {rate:7.3f} {maxdd*100:40.2f}")
    MP = pd.DataFrame(mrows)
    dump(MP, "matched.csv")
    h3 = int((MP.rate <= 0.05).sum())
    P(f"  H3 cells with matched-pair disagreement <= 5%: {h3} of {len(MP)}"
      f"   -> H3 {'HOLDS' if h3 > len(MP)/2 else 'FAILS'}")

    # --------------------------------------------------------------------------------------
    # H4 -- does the beta residual walk forward?  (rule 8)
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 96)
    P("H4  RESIDUAL PERSISTENCE (rule 8) -- fit MaxDD ~ beta on 2009-2016 ONLY, read 2017-2026")
    P("=" * 96)
    P(f"{'panel':6s} {'est':6s} {'n':>4s} {'rho(res_IS,res_OOS)':>20s} {'rho(dd_IS,dd_OOS)':>18s} "
      f"{'rho(beta_IS,beta_OOS)':>22s}")
    rrows = []
    for pn in PANELS:
        for e in ESTIMATORS:
            ii = real[(real.window == "IS") & (real.panel == pn)].reset_index(drop=True)
            oo = real[(real.window == "OOS") & (real.panel == pn)].reset_index(drop=True)
            key = ["family", "mode", "theta", "gross"]
            mg = ii.merge(oo, on=["panel"] + key, suffixes=("_is", "_oos"))
            xi, yi = mg[f"beta_{e}_is"].values, mg["MaxDD_is"].values
            xo, yo = mg[f"beta_{e}_oos"].values, mg["MaxDD_oos"].values
            ok = np.isfinite(xi) & np.isfinite(xo)
            xi, yi, xo, yo = xi[ok], yi[ok], xo[ok], yo[ok]
            A = np.vstack([xi, np.ones(len(xi))]).T
            coef, *_ = np.linalg.lstsq(A, yi, rcond=None)     # FIT ON IS ONLY (rule 8)
            res_is = yi - A @ coef
            res_oos = yo - (np.vstack([xo, np.ones(len(xo))]).T @ coef)   # SAME coefficients
            rho = float(pd.Series(res_is).rank().corr(pd.Series(res_oos).rank()))
            rdd = float(pd.Series(yi).rank().corr(pd.Series(yo).rank()))
            rbt = float(pd.Series(xi).rank().corr(pd.Series(xo).rank()))
            rrows.append(dict(panel=pn, estimator=e, n=len(xi), rho_resid=rho,
                              rho_maxdd=rdd, rho_beta=rbt,
                              slope_is=coef[0], intercept_is=coef[1]))
            P(f"{pn:6s} {e:6s} {len(xi):4d} {rho:20.3f} {rdd:18.3f} {rbt:22.3f}")
    RS = pd.DataFrame(rrows)
    dump(RS, "residual.csv")
    h4 = int((RS.rho_resid < RHO_BAR).sum())
    P(f"  H4 cells with rho(residual) < {RHO_BAR:.2f}: {h4} of {len(RS)}"
      f"   -> H4 {'HOLDS (residual is noise)' if h4 > len(RS)/2 else 'FAILS (residual persists)'}")

    # --------------------------------------------------------------------------------------
    # H5 / RULE 8 ON THE BOOKS -- three IS-only choosers, OOS read once
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 96)
    P("RULE 8 ON THE BOOKS -- IS-only choosers (2009-2016), OOS (2017-2026) read ONCE")
    P("=" * 96)
    wf = []
    for pn in PANELS:
        pan = panels[pn]
        ii = real[(real.window == "IS") & (real.panel == pn)].reset_index(drop=True)
        oo = real[(real.window == "OOS") & (real.panel == pn)].reset_index(drop=True)
        key = ["family", "mode", "theta", "gross"]
        mg = ii.merge(oo, on=["panel"] + key, suffixes=("_is", "_oos"))
        spy_o, v2_o = refs[pn][("SPY", "OOS")], refs[pn][("V2", "OOS")]
        spy_f = refs[pn][("SPY", "FULL")]
        for e in ESTIMATORS:
            x, y = mg[f"beta_{e}_is"].values, mg["MaxDD_is"].values
            ok = np.isfinite(x) & np.isfinite(y)
            A = np.vstack([x[ok], np.ones(int(ok.sum()))]).T
            coef, *_ = np.linalg.lstsq(A, y[ok], rcond=None)
            r = np.full(len(mg), np.nan)
            r[ok] = y[ok] - A @ coef
            mg[f"resid_is_{e}"] = r
        choosers = {
            "IS_SHARPE": mg["Sharpe_is"].values,                 # the record's standard selector
            "IS_LOWBETA": -mg["beta_FULL_is"].values,            # beta alone
            "IS_DDRESID": -mg["resid_is_FULL"].values,           # shallower DD than beta predicts
            "IS_MAXDD": mg["MaxDD_is"].values,                   # shallowest IS DD outright
        }
        for cname, v in choosers.items():
            k = int(np.nanargmax(v))
            row = mg.iloc[k]
            s = dict(CAGR=row["CAGR_oos"], Sharpe=row["Sharpe_oos"], MaxDD=row["MaxDD_oos"],
                     H1=row["H1_oos"], H2=row["H2_oos"])
            L = legs4b(s, spy_o)
            wf.append(dict(panel=pn, chooser=cname,
                           book=f"{row['family']}/{row['mode']}/th={row['theta']}/g={row['gross']:.2f}",
                           beta_is=row["beta_FULL_is"], beta_oos=row["beta_FULL_oos"],
                           OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                           OOS_H1=s["H1"], OOS_H2=s["H2"],
                           p4a=pass4a(s, v2_o), p4b=bool(all(L.values())), **{f"leg_{k2}": v2
                                                                              for k2, v2 in L.items()}))
        wf.append(dict(panel=pn, chooser="SPY", book="buy-and-hold",
                       beta_is=1.0, beta_oos=1.0,
                       OOS_CAGR=spy_o["CAGR"], OOS_Sharpe=spy_o["Sharpe"], OOS_MaxDD=spy_o["MaxDD"],
                       OOS_H1=spy_o["H1"], OOS_H2=spy_o["H2"], p4a=False, p4b=False,
                       leg_H1=False, leg_H2=False, leg_DDCAP=False, leg_CAGRFLOOR=False))
        wf.append(dict(panel=pn, chooser="RULESv2", book="live baseline",
                       beta_is=np.nan, beta_oos=np.nan,
                       OOS_CAGR=v2_o["CAGR"], OOS_Sharpe=v2_o["Sharpe"], OOS_MaxDD=v2_o["MaxDD"],
                       OOS_H1=v2_o["H1"], OOS_H2=v2_o["H2"],
                       p4a=False, p4b=pass4b(v2_o, spy_o),
                       **{f"leg_{k2}": v2 for k2, v2 in legs4b(v2_o, spy_o).items()}))
        _ = spy_f
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward.csv")
    P(f"{'panel':6s} {'chooser':11s} {'book':44s} {'bIS':>5s} {'bOOS':>5s} "
      f"{'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1/H2':>13s} {'4a':>3s} {'4b':>3s}")
    for _, r in WF.iterrows():
        P(f"{r['panel']:6s} {r['chooser']:11s} {str(r['book'])[:44]:44s} "
          f"{r['beta_is'] if np.isfinite(r['beta_is']) else float('nan'):5.2f} "
          f"{r['beta_oos'] if np.isfinite(r['beta_oos']) else float('nan'):5.2f} "
          f"{r['OOS_CAGR']:9.2%} {r['OOS_Sharpe']:7.3f} {r['OOS_MaxDD']:8.2%} "
          f"{r['OOS_H1']:6.3f}/{r['OOS_H2']:6.3f} "
          f"{'Y' if r['p4a'] else 'n':>3s} {'Y' if r['p4b'] else 'n':>3s}")

    res_wins = 0
    for pn in PANELS:
        a = WF[(WF.panel == pn) & (WF.chooser == "IS_DDRESID")]["OOS_Sharpe"].iloc[0]
        b = WF[(WF.panel == pn) & (WF.chooser == "IS_LOWBETA")]["OOS_Sharpe"].iloc[0]
        res_wins += int(a > b)
    P(f"  H5  DDRESID chooser beats LOWBETA chooser on OOS Sharpe at {res_wins} of {len(PANELS)} panels"
      f"   -> H5 {'HOLDS (residual picks nothing)' if res_wins <= len(PANELS)/2 else 'FAILS (residual picks)'}")

    # --------------------------------------------------------------------------------------
    # verdict
    # --------------------------------------------------------------------------------------
    hold = dict(H1=h1_hits > len(nfull) / 2, H2=h2 > len(AG) / 2, H2b=h2b > len(AG) / 2,
                H3=h3 > len(MP) / 2, H4=h4 > len(RS) / 2, H5=res_wins <= len(PANELS) / 2)
    P("")
    P("=" * 96)
    P("VERDICT")
    P("=" * 96)
    for k, v in hold.items():
        P(f"  {k:4s} {'HOLDS' if v else 'FAILS'}")
    conf = all(hold[k] for k in ("H1", "H2", "H2b", "H3", "H4"))
    P(f"  queue hypothesis (the DD cap IS a beta cap): "
      f"{'CONFIRMED' if conf else 'REFUTED -- the DD leg carries information beta does not'}")
    n4b = int(WF[WF.chooser.isin(list(choosers))].p4b.sum())
    n4a = int(WF[WF.chooser.isin(list(choosers))].p4a.sum())
    P(f"  OOS KEEP paths over the {len(PANELS)*len(choosers)} rule-8 picks: 4a {n4a}, 4b {n4b}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P("")
    P(f"total {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    dump(pd.concat([MG.assign(kind="margin"), FL.assign(kind="flip")], ignore_index=True), "margin.csv")
    return dict(gates=gates, H1=H1, R2=R2, AG=AG, MP=MP, RS=RS, WF=WF, CR=CR, MG=MG, FL=FL,
                hold=hold, zray=zray, conf=conf)


if __name__ == "__main__":
    main()
