#!/usr/bin/env python3
"""Idea 912 (cloud, 2026-09-15) -- is the record's whole DD-LEG literature a 2020 CONTAINMENT
fact?

THE QUESTION (queue, 2026-09-15)
  Idea 910 measured that 92.9% of U56 books and 89.3% of B136 books have their ENTIRE
  peak-to-trough decline contained inside SPY's own 24-day 2020 drawdown window (median Jaccard
  0.854 / 0.708), against 0.0% on SMALL.  Every DD-leg result the record has published on the
  large-cap panels may therefore be ONE EPISODE read 112 times.  The queue asks: re-run 867's and
  910's agreement tables with 2020 excised and report which survive.

WHAT IS BEING TESTED (the two committed tables, restated as bars before any number is read)
  867  `2026-09-15_is-the-4b-DD-CAP-just-a-BETA-CAP_B.agree.csv`
       K5  the DD leg is a high-R2 read of beta:  |Spearman(beta_FULL, MaxDD)| in 0.69-0.97 on
           the large-cap panels
       K6  and still NOT a beta cap:  agreement of `beta<=0.60` with the DD leg spans
           0.679-0.983 over the 336 real books
       K1  DDWIN (beta inside the book's OWN peak-to-trough window) reaches the bar on U56:
           agree 0.9531, best 0.9844
       K2  and on B136: agree 0.9833, best 1.0000, 0 of 109 matched pairs disagreeing
  910  `2026-09-15_ex-ante-proxy-for-the-DDWIN-beta_C.agree.csv` / `.barA.csv` / `.overlap.csv`
       K3  U56 / ROLL clears BAR-A: agree 0.9844, best 1.0000, 0 of 146 pairs disagreeing
       K4  B136 / SPYDD clears BAR-A: agree 1.0000, best 1.0000, 0 of 130 pairs disagreeing
       K7  the H0 decomposition has POPULATION negative and ESTIMATOR positive on U56 and B136
       K8  containment shares 0.9286 / 0.8929 / 0.0000 and median Jaccard 0.854 / 0.708 / 0.054
       K9  0 of 30 ex-ante (proxy x panel) cells clear the 0.95 rule-8 OOS agreement bar

WHAT "EXCISED" MEANS HERE (convention stated before any number is read)
  An excision DELETES the episode's days from the STATISTIC, not from the tape.  Every book is
  traded, rebalanced and charged exactly as in 867 and 910 -- weekly, t+1, 10 bps, on the full
  price history -- and then the excised days are dropped from the daily net-return vector before
  CAGR / Sharpe / MaxDD / every beta is computed, for the books, for SPY and for RULES v2 alike.
  This is a RE-READING of the same tape with one episode's days removed, not a counterfactual
  re-simulation of a world without 2020: re-simulating would move every rebalance date and change
  what is being compared.  Consequences that are stated, not hidden:
    - MaxDD is measured on a SPLICED equity curve, so a decline that straddles the excision is
      read as two shallower ones.  That is the intended operation: it is what "excise the episode"
      must mean for a path statistic.
    - the 252d rolling and EWMA betas (ROLL / MAXROLL / EWMA) also straddle the splice.
    - 2020 lies entirely in the OOS half (2017-2026), so the IS half is INVARIANT to every
      excision below.  Gate G9 checks that invariance is exact, which is what makes the IS-only
      rule-8 chooser identical across excisions and the OOS change attributable to the episode.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  EXCISION WINDOW (the queue's own first dial), 5 levels, every one reported:
           NONE    control -- must reproduce 867 and 910 exactly (gates G4/G5/G6)
           SPYDD   SPY's own FULL-window argmin peak-to-trough window (the 24 days 910 measured;
                   computed per panel, printed with its dates)
           CRASH   2020-02-19 .. 2020-04-30   (the decline plus its recovery leg)
           H1_20   2020-01-01 .. 2020-06-30
           CAL20   2020-01-01 .. 2020-12-31   (the whole calendar year)
  TUNED 2  PANEL (the queue's own second dial), 3 levels: U56, B136, SMALL.
  REPORTED AXES (nothing fitted on them; every point published):
           family (4) x mode (3) x theta (3, ROW has none) x gross (4) = 112 real books
           + ZEROSIG (4 rungs) + RANDGATE (3 seeds x 4 rungs) = 128 traded books per panel,
           x 3 windows (FULL / IS / OOS) x 11 proxies x 2 populations (ALL / DDSUB).

HYPOTHESES (bars fixed before the run; both directions reported)
  H_STRUCT  is containment a 2020 fact or a MARKET-EPISODE fact?  After excising 2020, SPY has a
            different worst decline; if the containment share stays >= 0.70 around THAT episode,
            the record's DD-leg agreement is structural (books' declines sit inside the market's,
            whichever episode it is) and not a 2020 artefact.
  H_AGREE   867's and 910's agreement headlines (K1-K4) BREAK under excision.  A claim SURVIVES
            iff its own committed bar still holds at every excision level.
  H_LEG     the DD leg's pass SET is an episode fact: share of books whose `leg_DDCAP` flips
            between NONE and the excision.  Bar: > 0.50 flipping = the leg is the episode.
  H_4b      the full-sample 4b pass census moves materially under excision (nothing selected).
  H_WF      (rule 8, required) IS-only choosers picked on 2009-2016, OOS 2017-2026 read once, at
            every excision, both KEEP paths, against SPY and RULES v2 in the SAME excised window.

GATES (all printed before any result number)
  G1  TREND/ROW at g=0.75 == baseline.rules_v2_weights elementwise
  G2  the fast runner == engine.backtest on returns and turnover
  G3  the committed U56 triples (SPY, RULES v2) at EXCISION=NONE
  G4  867's committed .agree.csv reproduces at EXCISION=NONE
  G5  910's committed .agree.csv reproduces at EXCISION=NONE -- all 11 proxies x 3 panels x 2
      populations on the FULL window, 132 published numbers
  G6  910's committed .overlap.csv containment shares reproduce at EXCISION=NONE
  G7  determinism (rebuild U56, compare)
  G8  the analytic ray: on the zero-signal book g x SPY every proxy must read g AT EVERY
      EXCISION -- a pure SPY blend has the same beta on every subsample, spliced or not.  This
      gates all 11 implementations against the excision code at once.
  G9  IS-window invariance: no excision touches 2009-2016, so every IS number must be unchanged
      to 0.  This is the gate that makes the rule-8 comparison legitimate.
  SMALL CAVEAT, declared: 867 and 910 built SMALL from `load_universe(small=True)` WITHOUT the
  `max_1d_move >= 1.0` drop.  This lane's standing data rule drops those 52 tickers first, so the
  run's SMALL panel is NOT byte-comparable to theirs.  A fourth panel SMALLRAW (undropped) is
  therefore built for G4/G5/G6 only, so the gates are read on the same construction they were
  published on, and every headline number below is on the dropped panel.

PROTOCOL: 10 bps, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown LEVEL
below is optimistic -- the books' and the comparands' alike.  The agreement tables, the flip
counts and the containment shares are same-tape statistics and are unaffected.
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
from engine import backtest, rebalance_mask  # noqa: E402

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
BETA_CAP = 0.60                    # the substitution 867 tested
ROLLWIN = 252
EWMA_HL = 252
MINOBS = 20                        # 867's own minimum for a beta
MATCH_TOL = 0.02                   # 867's beta-matching tolerance
AGREE_BAR = 0.95
DD10 = 0.10
CONTAIN_BAR = 0.70                 # H_STRUCT
FLIP_BAR = 0.50                    # H_LEG

# ---- TUNED DIAL 1: the excision window --------------------------------------------------------
EXCISIONS = ["NONE", "SPYDD", "CRASH", "H1_20", "CAL20"]
EXC_DATES = {"CRASH": ("2020-02-19", "2020-04-30"),
             "H1_20": ("2020-01-01", "2020-06-30"),
             "CAL20": ("2020-01-01", "2020-12-31")}
# ---- TUNED DIAL 2: the panel ------------------------------------------------------------------
PANELS = ["U56", "B136", "SMALL"]
GATE_PANEL = "SMALLRAW"            # built for G4/G5/G6 only (867/910's SMALL construction)

# ---- reported axes ----------------------------------------------------------------------------
FAMILIES = ["TREND", "VOL", "MOM", "DISP"]
MODES = ["ROW", "AGG", "HYB"]
THETAS = [0.20, 0.40, 0.60]
GROSSES = [0.25, 0.50, 0.75, 1.00]
RAND_SEEDS = [9101, 9102, 9103]
POPS = ["ALL", "DDSUB"]
WINDOWS = ["FULL", "IS", "OOS"]

EXANTE = ["FULL", "DOWN", "ROLL", "MAXROLL", "EWMA", "SEMI", "TAIL10", "HIVOL", "SPYDD", "SPYDD10"]
PROXIES = EXANTE + ["DDWIN"]       # DDWIN carried as the circular CEILING

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
A867 = ROOT / "research" / "backtests" / "2026-09-15_is-the-4b-DD-CAP-just-a-BETA-CAP_B.agree.csv"
A910 = ROOT / "research" / "backtests" / "2026-09-15_ex-ante-proxy-for-the-DDWIN-beta_C.agree.csv"
O910 = ROOT / "research" / "backtests" / "2026-09-15_ex-ante-proxy-for-the-DDWIN-beta_C.overlap.csv"

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
# runner -- 910's vectorised equivalent of engine.backtest, unchanged (gated at G1/G2)
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
        self.wins = {"FULL": self.m_full, "IS": self.m_is, "OOS": self.m_oos}
        # ---- TUNED DIAL 1 materialised: one keep-mask per excision level -----------------
        self.keep, self.excinfo = {}, {}
        for e in EXCISIONS:
            k, info = self._keep(e)
            self.keep[e], self.excinfo[e] = k, info
        # masks and market conditioners per (excision, window)
        self.masks, self.cond = {}, {}
        for e in EXCISIONS:
            for w in WINDOWS:
                m = self.wins[w] & self.keep[e]
                self.masks[(e, w)] = m
                self.cond[(e, w)] = market_conditioners(self.spy[m])

    def _keep(self, exc):
        keep = np.ones(self.T, bool)
        if exc == "NONE":
            return keep, "(control: nothing excised)"
        if exc == "SPYDD":
            pos = np.flatnonzero(self.m_full)
            pk, tr = _dd_window(self.spy[self.m_full])
            drop = pos[pk: tr + 1]
            keep[drop] = False
            return keep, (f"SPY argmin peak-to-trough {self.idx[drop[0]].date()} .. "
                          f"{self.idx[drop[-1]].date()}  ({len(drop)}d)")
        a, b = EXC_DATES[exc]
        drop = (self.idx >= pd.Timestamp(a)) & (self.idx <= pd.Timestamp(b))
        keep[drop] = False
        return keep, f"calendar {a} .. {b}  ({int(drop.sum())}d)"


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
    return bool(all(legs4b(s, spy).values()))


# ================================================================================================
# the proxies -- 910's definitions, unchanged
# ================================================================================================
def _ols_beta(r, m):
    r, m = np.asarray(r, float), np.asarray(m, float)
    if len(r) < MINOBS:
        return np.nan
    v = m.var(ddof=1)
    return float(np.cov(r, m, ddof=1)[0, 1] / v) if v > 0 else np.nan


def _dd_window(r):
    """(peak, trough) index of the deepest peak-to-trough decline of the equity curve of r."""
    eq = np.cumprod(1.0 + np.asarray(r, float))
    dd = eq / np.maximum.accumulate(eq) - 1.0
    tr = int(np.argmin(dd))
    pk = int(np.argmax(eq[: tr + 1])) if tr > 0 else 0
    return pk, tr


def market_conditioners(m):
    """Boolean day-masks that depend ONLY on SPY's path over this (excision, window).  Computed
    once and shared by every book -- that is what makes them non-circular."""
    m = np.asarray(m, float)
    out = {}
    out["DOWN"] = m < 0.0
    if len(m) >= MINOBS:
        q = np.quantile(m, 0.10)
        out["TAIL10"] = m <= q
    else:
        out["TAIL10"] = np.zeros(len(m), bool)
    v = pd.Series(m).rolling(VOLWIN).std().shift(1)
    thr = v.quantile(0.75)
    out["HIVOL"] = (v >= thr).fillna(False).values if np.isfinite(thr) else np.zeros(len(m), bool)
    pk, tr = _dd_window(m)
    sp = np.zeros(len(m), bool)
    if tr - pk >= MINOBS:
        sp[pk: tr + 1] = True
    out["SPYDD"] = sp
    eq = np.cumprod(1.0 + m)
    out["SPYDD10"] = (eq / np.maximum.accumulate(eq) - 1.0) <= -DD10
    return out


def proxies_all(r, m, cond):
    """All 11 readings of one book's beta over one (excision, window)."""
    out = {}
    out["FULL"] = _ols_beta(r, m)
    for key in ("DOWN", "TAIL10", "HIVOL", "SPYDD", "SPYDD10"):
        sel = cond[key]
        out[key] = _ols_beta(r[sel], m[sel]) if sel.sum() >= MINOBS else np.nan
    if len(r) >= ROLLWIN + 10:
        rs, ms = pd.Series(r), pd.Series(m)
        b = rs.rolling(ROLLWIN).cov(ms) / ms.rolling(ROLLWIN).var()
        b = b.replace([np.inf, -np.inf], np.nan).dropna()
        out["ROLL"] = float(b.median()) if len(b) else np.nan
        out["MAXROLL"] = float(b.max()) if len(b) else np.nan
    else:
        out["ROLL"] = out["MAXROLL"] = np.nan
    if len(r) >= ROLLWIN + 10:
        rs, ms = pd.Series(r), pd.Series(m)
        be = rs.ewm(halflife=EWMA_HL, min_periods=ROLLWIN).cov(ms) / \
            ms.ewm(halflife=EWMA_HL, min_periods=ROLLWIN).var()
        be = be.replace([np.inf, -np.inf], np.nan).dropna()
        out["EWMA"] = float(be.median()) if len(be) else np.nan
    else:
        out["EWMA"] = np.nan
    dn = m < 0.0
    if dn.sum() >= MINOBS:
        den = float((m[dn] ** 2).sum())
        out["SEMI"] = float((r[dn] * m[dn]).sum() / den) if den > 0 else np.nan
    else:
        out["SEMI"] = np.nan
    pk, tr = _dd_window(r)
    out["DDWIN"] = _ols_beta(r[pk: tr + 1], m[pk: tr + 1]) if tr - pk >= MINOBS else np.nan
    out["_ddlen"] = float(tr - pk + 1)
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
# the book grid
# ================================================================================================
def build_books(pan: Panel):
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
            out.append((md, r))
        del bk
    return out


def score_books(pan: Panel, books, excisions):
    """One row per (book, excision, window): metrics + all 11 proxies + the 4b legs."""
    ref = {}
    ew = ew_panel(pan.px)
    inb = gate_in(pan.px, "TREND")
    v2 = Book(pan, book_w1(ew, inb, None, "ROW", 0.0)).at(0.75, COST)[0]
    for e in excisions:
        for w in WINDOWS:
            m = pan.masks[(e, w)]
            ref[("SPY", e, w)] = pack(pan.spy[m])
            ref[("V2", e, w)] = pack(v2[m])
    rows = []
    for md, r in books:
        for e in excisions:
            for w in WINDOWS:
                m = pan.masks[(e, w)]
                rw, mw = r[m], pan.spy[m]
                s = pack(rw)
                bt = proxies_all(rw, mw, pan.cond[(e, w)])
                spy = ref[("SPY", e, w)]
                L = legs4b(s, spy)
                row = dict(md)
                row.update(excision=e, window=w,
                           **{k: s[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")})
                row.update({f"beta_{k}": bt[k] for k in PROXIES})
                row.update(ddwin_len=bt["_ddlen"], ndays=int(m.sum()),
                           dd_ratio=s["MaxDD"] / spy["MaxDD"],
                           leg_DDCAP=L["DDCAP"], leg_CAGR=L["CAGRFLOOR"],
                           leg_H1=L["H1"], leg_H2=L["H2"],
                           pass4b=bool(all(L.values())),
                           pass4a=pass4a(s, ref[("V2", e, w)]))
                rows.append(row)
    return pd.DataFrame(rows), ref


# ================================================================================================
# agreement machinery -- 867/910's, unchanged
# ================================================================================================
def best_cap(beta, truth):
    ok = np.isfinite(beta)
    b, t = beta[ok], truth[ok]
    if len(b) < 5:
        return np.nan, np.nan
    order = np.sort(np.unique(b))
    cands = np.concatenate([[order[0] - 1e-6], (order[:-1] + order[1:]) / 2.0, [order[-1] + 1e-6]])
    best, bc = -1.0, np.nan
    for c in cands:
        a = float(((b <= c) == t).mean())
        if a > best:
            best, bc = a, float(c)
    return bc, best


def spearman(a, b):
    s = pd.DataFrame({"a": np.asarray(a, float), "b": np.asarray(b, float)}).dropna()
    if len(s) < 5:
        return np.nan
    return float(s["a"].rank().corr(s["b"].rank()))


def agree_row(panel, excision, window, popn, proxy, beta, truth, maxdd):
    ok = np.isfinite(beta)
    n = int(ok.sum())
    if n < 5:
        return dict(panel=panel, excision=excision, window=window, popn=popn, proxy=proxy, n=n)
    b, t, d = beta[ok], truth[ok], maxdd[ok]
    pred = b <= BETA_CAP
    bc, ba = best_cap(beta, truth)
    B = b[:, None] - b[None, :]
    M = np.triu(np.abs(B) <= MATCH_TOL, 1)
    npair = int(M.sum())
    dis = int((M & (t[:, None] != t[None, :])).sum())
    dmax = float(np.abs(d[:, None] - d[None, :])[M].max()) if npair else np.nan
    return dict(panel=panel, excision=excision, window=window, popn=popn, proxy=proxy, n=n,
                dd_pass=int(t.sum()), beta_pass=int(pred.sum()),
                agree=float((pred == t).mean()),
                TP=int((pred & t).sum()), FP=int((pred & ~t).sum()),
                FN=int((~pred & t).sum()), TN=int((~pred & ~t).sum()),
                beta_star=bc, best_agree=ba, spearman=spearman(b, d),
                n_pairs=npair, n_disagree=dis,
                pair_disagree=(dis / npair if npair else np.nan),
                max_dMaxDD_in_pair=dmax)


# ================================================================================================
# containment (910's MECHANISM block, re-run per excision)
# ================================================================================================
def overlap_rows(pan: Panel, books, excisions):
    rows = []
    for e in excisions:
        for w in WINDOWS:
            m = pan.masks[(e, w)]
            mw = pan.spy[m]
            spk, str_ = _dd_window(mw)
            sset = set(range(spk, str_ + 1))
            for md, r in books:
                if str(md["family"]).startswith(("ZEROSIG", "RANDGATE")):
                    continue
                bpk, btr = _dd_window(r[m])
                bset = set(range(bpk, btr + 1))
                inter, uni = len(sset & bset), len(sset | bset)
                rows.append(dict(panel=pan.name, excision=e, window=w,
                                 family=md["family"], mode=md["mode"], theta=md["theta"],
                                 gross=md["gross"],
                                 jaccard=(inter / uni if uni else np.nan),
                                 book_len=btr - bpk + 1, spy_len=str_ - spk + 1,
                                 contained=float(inter == (btr - bpk + 1))))
    return rows


# ================================================================================================
# gates
# ================================================================================================
def run_gates(panels):
    P("=" * 110)
    P("GATES (printed before any result number is read)")
    P("=" * 110)
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
    dt = float(np.nanmax(np.abs(t_fast - res_eng["turnover"].values)))
    ok["G1"] = dw < 1e-12
    P(f"G1  TREND/ROW g=0.75 == rules_v2_weights   max|dw| {dw:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")
    ok["G2"] = dr < 1e-10 and dt < 1e-10
    P(f"G2  fast Book.at == engine.backtest        max|dr| {dr:.3e}  max|dturn| {dt:.3e}   "
      f"-> {'PASS' if ok['G2'] else 'FAIL'}")

    m = pan.masks[("NONE", "FULL")]
    spy_t, v2_t = fmet(pan.spy[m]), fmet(r_fast[m])
    d1 = tuple(abs(spy_t[i] - SPY_U56[i]) for i in range(3))
    d2 = tuple(abs(v2_t[i] - V2_U56[i]) for i in range(3))
    ok["G3"] = all(d < t for d, t in zip(d1, (TOL_C, TOL_S, TOL_D))) and \
        all(d < t for d, t in zip(d2, (TOL_C, TOL_S, TOL_D)))
    P(f"G3  committed U56 triples @ NONE   SPY {spy_t[0]:.4%}/{spy_t[1]:.4f}/{spy_t[2]:.4%}  "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%})")
    P(f"                                   v2  {v2_t[0]:.4%}/{v2_t[1]:.4f}/{v2_t[2]:.4%}  "
      f"(committed {V2_U56[0]:.2%}/{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> "
      f"{'PASS' if ok['G3'] else 'FAIL'}")

    # G8 -- the analytic ray, AT EVERY EXCISION
    Z = np.zeros((pan.T, pan.N))
    Z[:, list(px.columns).index("SPY")] = 1.0
    zb = Book(pan, Z)
    worst, wcell = 0.0, ""
    for e in EXCISIONS:
        me = pan.masks[(e, "FULL")]
        for g in GROSSES:
            rz, _ = zb.at(g, cost=0.0)
            bt = proxies_all(rz[me], pan.spy[me], pan.cond[(e, "FULL")])
            for k in PROXIES:
                if np.isfinite(bt[k]) and abs(bt[k] - g) > worst:
                    worst, wcell = abs(bt[k] - g), f"{e}/g={g:.2f}/{k}"
    ok["G8"] = worst < 0.03
    P(f"G8  ZEROSIG ray at EVERY excision: every proxy of g x SPY must read g   "
      f"max|beta-g| over {len(EXCISIONS)}x{len(GROSSES)}x{len(PROXIES)} = {worst:.3e} ({wcell})"
      f"   -> {'PASS' if ok['G8'] else 'FAIL'}")
    return ok


def gate_867(B):
    if not A867.exists():
        P("G4  867's .agree.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(A867)
    rows = []
    for _, pr in par.iterrows():
        pn = GATE_PANEL if pr.panel == "SMALL" else pr.panel
        sub = B[(B.panel == pn) & (B.excision == "NONE") & (B.window == "FULL")
                & (~B.family.str.startswith(("ZEROSIG", "RANDGATE")))]
        beta = sub[f"beta_{pr.estimator}"].values.astype(float)
        truth = sub["leg_DDCAP"].values.astype(bool)
        okm = np.isfinite(beta)
        ag = float(((beta[okm] <= BETA_CAP) == truth[okm]).mean())
        _, ba = best_cap(beta, truth)
        rows.append(dict(panel=pr.panel, panel_here=pn, estimator=pr.estimator,
                         n_parent=int(pr.n), n_here=int(okm.sum()),
                         agree_parent=float(pr.agree), agree_here=ag,
                         best_parent=float(pr.best_agree), best_here=ba,
                         d_agree=abs(ag - float(pr.agree)),
                         d_best=abs(ba - float(pr.best_agree)),
                         d_n=abs(int(okm.sum()) - int(pr.n))))
    G = pd.DataFrame(rows)
    w = G[(G.d_n == 0) & (G.d_agree < 1e-9) & (G.d_best < 1e-9)]
    passed = len(w) == len(G)
    P(f"G4  867's committed .agree.csv @ NONE: {len(w)} of {len(G)} rows reproduce exactly  "
      f"(worst |d_agree| {G.d_agree.max():.3e}, worst |d_best| {G.d_best.max():.3e}, "
      f"n mismatches {int((G.d_n != 0).sum())})   -> {'PASS' if passed else 'FAIL'}")
    for _, r in G.iterrows():
        P(f"      {r.panel:6s}->{r.panel_here:8s} {r.estimator:8s} n {int(r.n_here):3d}/"
          f"{int(r.n_parent):3d}  agree {r.agree_here:.4f}/{r.agree_parent:.4f}  "
          f"best {r.best_here:.4f}/{r.best_parent:.4f}")
    return passed, G


def gate_910(A):
    if not A910.exists():
        P("G5  910's .agree.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(A910)
    par = par[par.window == "FULL"]
    rows = []
    for _, pr in par.iterrows():
        pn = GATE_PANEL if pr.panel == "SMALL" else pr.panel
        h = A[(A.panel == pn) & (A.excision == "NONE") & (A.window == "FULL")
              & (A["popn"] == pr["popn"]) & (A.proxy == pr.proxy)]
        if h.empty:
            continue
        h = h.iloc[0]
        rows.append(dict(panel=pr.panel, panel_here=pn, popn=pr["popn"], proxy=pr.proxy,
                         n_parent=int(pr.n), n_here=int(h.n),
                         agree_parent=float(pr.agree), agree_here=float(h.agree),
                         best_parent=float(pr.best_agree), best_here=float(h.best_agree),
                         dis_parent=int(pr.n_disagree), dis_here=int(h.n_disagree),
                         d_agree=abs(float(h.agree) - float(pr.agree)),
                         d_best=abs(float(h.best_agree) - float(pr.best_agree)),
                         d_n=abs(int(h.n) - int(pr.n)),
                         d_dis=abs(int(h.n_disagree) - int(pr.n_disagree))))
    G = pd.DataFrame(rows)
    w = G[(G.d_n == 0) & (G.d_agree < 1e-9) & (G.d_best < 1e-9) & (G.d_dis == 0)]
    passed = len(w) == len(G)
    P(f"G5  910's committed .agree.csv @ NONE: {len(w)} of {len(G)} (panel x popn x proxy) rows "
      f"reproduce exactly on agree / best_agree / n / n_disagree   "
      f"(worst |d_agree| {G.d_agree.max():.3e}, worst |d_best| {G.d_best.max():.3e})   -> "
      f"{'PASS' if passed else 'FAIL'}")
    bad = G[(G.d_n != 0) | (G.d_agree >= 1e-9) | (G.d_best >= 1e-9) | (G.d_dis != 0)]
    for _, r in bad.iterrows():
        P(f"      MISMATCH {r.panel:6s}->{r.panel_here:8s} {r['popn']:6s} {r.proxy:8s} "
          f"n {int(r.n_here)}/{int(r.n_parent)}  agree {r.agree_here:.4f}/{r.agree_parent:.4f}  "
          f"best {r.best_here:.4f}/{r.best_parent:.4f}  dis {int(r.dis_here)}/{int(r.dis_parent)}")
    return passed, G


def gate_overlap(OV):
    if not O910.exists():
        P("G6  910's .overlap.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(O910)
    rows = []
    for pn in ["U56", "B136", "SMALL"]:
        for w in WINDOWS:
            p = par[(par.panel == pn) & (par.window == w)]
            h = OV[(OV.panel == (GATE_PANEL if pn == "SMALL" else pn))
                   & (OV.excision == "NONE") & (OV.window == w)]
            if p.empty or h.empty:
                continue
            rows.append(dict(panel=pn, window=w,
                             contain_parent=float(p.contained.mean()),
                             contain_here=float(h.contained.mean()),
                             jacc_parent=float(p.jaccard.median()),
                             jacc_here=float(h.jaccard.median()),
                             spylen_parent=int(p.spy_len.iloc[0]),
                             spylen_here=int(h.spy_len.iloc[0])))
    G = pd.DataFrame(rows)
    G["d_contain"] = (G.contain_here - G.contain_parent).abs()
    G["d_jacc"] = (G.jacc_here - G.jacc_parent).abs()
    passed = bool((G.d_contain < 1e-9).all() and (G.d_jacc < 1e-9).all()
                  and (G.spylen_here == G.spylen_parent).all())
    P(f"G6  910's committed .overlap.csv @ NONE: {len(G)} (panel x window) cells, worst "
      f"|d contained| {G.d_contain.max():.3e}, worst |d median Jaccard| {G.d_jacc.max():.3e}   "
      f"-> {'PASS' if passed else 'FAIL'}")
    for _, r in G.iterrows():
        P(f"      {r.panel:6s} {r.window:5s} contained {r.contain_here:.4f}/{r.contain_parent:.4f}"
          f"  medJ {r.jacc_here:.4f}/{r.jacc_parent:.4f}  SPY DD len "
          f"{int(r.spylen_here)}/{int(r.spylen_parent)}")
    return passed, G


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 110)
    P("IDEA 912 (cloud, 2026-09-15) -- is the record's whole DD-LEG literature a 2020")
    P("                               CONTAINMENT fact?")
    P("=" * 110)
    P(f"TUNED 1 excision window ({len(EXCISIONS)} levels, all reported): {EXCISIONS}")
    P(f"TUNED 2 panel: {PANELS}   (+ {GATE_PANEL}, gates G4/G5/G6 only)")
    P(f"reported axes: family {FAMILIES} x mode {MODES} x theta {THETAS} x gross {GROSSES}")
    P(f"                + ZEROSIG + RANDGATE{RAND_SEEDS};  {len(PROXIES)} proxies, {POPS} "
      f"populations, {WINDOWS} windows")
    P(f"                cost {COST:.0f} bps, {FREQ}, LAG {LAG}, warm-up {WARMUP}d, "
      f"IS <= {IS_END} / OOS >= {OOS_START}")
    P("EXCISION CONVENTION: days are deleted from the STATISTIC, not from the tape -- books trade,")
    P("  rebalance and pay costs on the full history, then the excised days are dropped from the")
    P("  daily return vector before CAGR / Sharpe / MaxDD / every beta, for books, SPY and RULES")
    P("  v2 alike.  MaxDD is therefore read on a SPLICED curve; that is what excising an episode")
    P("  must mean for a path statistic.  Stated, not hidden.")
    P(f"BARS: H_STRUCT containment >= {CONTAIN_BAR}; H_AGREE each committed bar re-read at every")
    P(f"      excision; H_LEG flip share > {FLIP_BAR}; H_WF rule 8 with both KEEP paths.")
    P("")

    panels = {}
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = sorted(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True)),
                   (GATE_PANEL, dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in set(bad)]]
        panels[nm] = Panel(nm, px)
        P(f"panel {nm:8s} {px.shape[0]} days x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}  eval from {panels[nm].start.date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv); "
      f"{GATE_PANEL} keeps them, which is 867's and 910's construction")
    P("")
    P("excision windows as materialised on each panel:")
    for nm in PANELS + [GATE_PANEL]:
        for e in EXCISIONS:
            if e == "NONE":
                continue
            k = panels[nm].keep[e]
            nfull = int((panels[nm].m_full & ~k).sum())
            noos = int((panels[nm].m_oos & ~k).sum())
            nis = int((panels[nm].m_is & ~k).sum())
            P(f"  {nm:8s} {e:6s} {panels[nm].excinfo[e]:58s} dropped FULL {nfull:4d} "
              f"IS {nis:3d} OOS {noos:4d}")
    P("")

    gates = run_gates(panels)

    P("")
    P("=" * 110)
    P("BUILDING THE BOOK GRID")
    P("=" * 110)
    allb, refs, book_rets, ovr = [], {}, {}, []
    for nm in PANELS + [GATE_PANEL]:
        t = time.time()
        exc = EXCISIONS if nm in PANELS else ["NONE"]
        bk = build_books(panels[nm])
        df, ref = score_books(panels[nm], bk, exc)
        refs[nm] = ref
        allb.append(df)
        book_rets[nm] = bk
        ovr += overlap_rows(panels[nm], bk, exc)
        P(f"  {nm:8s} {len(bk):4d} books x {len(exc)} excisions  {len(df):6d} book-rows  "
          f"({time.time()-t:.1f}s)")
    B = pd.concat(allb, ignore_index=True)
    OV = pd.DataFrame(ovr)
    del allb, ovr
    # one string key per book spec (theta is NaN on ROW, which no index/merge can align on)
    B["bkey"] = (B.family.astype(str) + "|" + B["mode"].astype(str) + "|"
                 + B.theta.map(lambda x: "na" if not np.isfinite(x) else f"{x:.2f}") + "|"
                 + B.gross.map(lambda x: f"{x:.2f}"))

    # G7 determinism
    bk2 = build_books(panels["U56"])
    d2, _ = score_books(panels["U56"], bk2, EXCISIONS)
    a = B[B.panel == "U56"].reset_index(drop=True)
    ds = float(np.nanmax(np.abs(a["Sharpe"].values - d2["Sharpe"].values)))
    db = float(np.nanmax(np.abs(a["beta_ROLL"].values - d2["beta_ROLL"].values)))
    gates["G7"] = ds < 1e-12 and db < 1e-12
    P(f"G7  DETERMINISM  max|dSharpe| {ds:.3e}  max|dbeta_ROLL| {db:.3e}   "
      f"-> {'PASS' if gates['G7'] else 'FAIL'}")
    del bk2, d2, a

    # G9 IS invariance
    isrows = B[(B.window == "IS") & (B.panel.isin(PANELS))]
    base = isrows[isrows.excision == "NONE"].set_index(["panel", "bkey"])
    worst = 0.0
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2"] + [f"beta_{k}" for k in PROXIES]
    for e in EXCISIONS[1:]:
        cur = isrows[isrows.excision == e].set_index(["panel", "bkey"]).reindex(base.index)
        d = (cur[cols].astype(float) - base[cols].astype(float)).abs().to_numpy()
        worst = max(worst, float(np.nanmax(d)))
    gates["G9"] = worst == 0.0
    P(f"G9  IS-window invariance (no excision touches 2009-2016): max|d| over "
      f"{len(cols)} statistics x {len(EXCISIONS)-1} excisions = {worst:.3e}   -> "
      f"{'PASS' if gates['G9'] else 'FAIL'}")

    real = B[~B.family.str.startswith(("ZEROSIG", "RANDGATE"))].copy()

    # agreement tables -- the object the queue asked to re-run
    P("")
    rows = []
    for nm in PANELS + [GATE_PANEL]:
        for e in (EXCISIONS if nm in PANELS else ["NONE"]):
            for w in WINDOWS:
                sub = real[(real.panel == nm) & (real.excision == e) & (real.window == w)]
                ddok = np.isfinite(sub["beta_DDWIN"].values)
                for popn in POPS:
                    s = sub if popn == "ALL" else sub[ddok]
                    for pr in PROXIES:
                        rows.append(agree_row(nm, e, w, popn, pr,
                                              s[f"beta_{pr}"].values.astype(float),
                                              s["leg_DDCAP"].values.astype(bool),
                                              s["MaxDD"].values.astype(float)))
    A = pd.DataFrame(rows)

    P("")
    gates["G4"], G4 = gate_867(B)
    P("")
    gates["G5"], G5 = gate_910(A)
    P("")
    gates["G6"], G6 = gate_overlap(OV)
    P("")
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  " + "  ".join(
        f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items())))
    if not all(gates.values()):
        P("  *** a gate FAILED -- every number below is reported with that caveat ***")
    P("")
    dump(B, "books.csv")
    dump(A, "agree.csv")
    dump(OV, "overlap.csv")
    dump(pd.concat([G4.assign(gate="G4_867"), G5.assign(gate="G5_910")], ignore_index=True)
         if len(G4) and len(G5) else pd.DataFrame(), "gates.csv")

    # ============================================================================================
    # H_STRUCT -- is containment a 2020 fact or a market-episode fact?
    # ============================================================================================
    P("")
    P("=" * 110)
    P("H_STRUCT  IS CONTAINMENT A 2020 FACT OR A MARKET-EPISODE FACT?")
    P("          after excising 2020, SPY has a DIFFERENT worst decline; does the containment")
    P("          share reappear around THAT one?")
    P("=" * 110)
    P(f"  {'panel':6s} {'excision':8s} {'window':6s} {'SPY DD':>8s} {'SPY DD win':>22s} "
      f"{'medJ':>6s} {'contained':>10s} {'len':>4s}")
    srows = []
    for nm in PANELS:
        for e in EXCISIONS:
            for w in WINDOWS:
                o = OV[(OV.panel == nm) & (OV.excision == e) & (OV.window == w)]
                pan = panels[nm]
                m = pan.masks[(e, w)]
                dates = pan.idx[m]
                mw = pan.spy[m]
                pk, tr = _dd_window(mw)
                _, _, sdd = fmet(mw)
                srows.append(dict(panel=nm, excision=e, window=w, spy_MaxDD=sdd,
                                  spy_dd_start=str(dates[pk].date()),
                                  spy_dd_end=str(dates[tr].date()),
                                  spy_dd_len=int(tr - pk + 1),
                                  med_jaccard=float(o.jaccard.median()),
                                  contained=float(o.contained.mean())))
                r = srows[-1]
                P(f"  {nm:6s} {e:8s} {w:6s} {sdd:8.2%} "
                  f"{r['spy_dd_start']+'..'+r['spy_dd_end']:>22s} {r['med_jaccard']:6.3f} "
                  f"{r['contained']:10.3f} {r['spy_dd_len']:4d}")
    S = pd.DataFrame(srows)
    dump(S, "containment.csv")
    P("")
    for nm in PANELS:
        f = S[(S.panel == nm) & (S.window == "FULL")]
        base = float(f[f.excision == "NONE"].contained.iloc[0])
        exc = f[f.excision != "NONE"]
        P(f"  {nm:6s} FULL-window contained: NONE {base:.3f} -> " + "  ".join(
            f"{r.excision} {r.contained:.3f}" for _, r in exc.iterrows())
          + f"   H_STRUCT ({CONTAIN_BAR:.2f} bar): "
          + ("HOLDS at every excision" if (exc.contained >= CONTAIN_BAR).all()
             else f"holds at {int((exc.contained >= CONTAIN_BAR).sum())} of {len(exc)}"))

    # ============================================================================================
    # H_AGREE -- the committed tables, re-read at every excision
    # ============================================================================================
    P("")
    P("=" * 110)
    P("H_AGREE  867's AND 910's AGREEMENT TABLES, RE-READ AT EVERY EXCISION")
    P("=" * 110)
    P("")
    P("  agreement with the DD leg at the FIXED cap beta <= 0.60, FULL window, DDSUB population")
    P(f"  {'panel':6s} {'proxy':8s} " + " ".join(f"{e:>16s}" for e in EXCISIONS))
    for nm in PANELS:
        for pr in PROXIES:
            cells = []
            for e in EXCISIONS:
                r = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                      & (A["popn"] == "DDSUB") & (A.proxy == pr)]
                cells.append(f"{float(r.iloc[0].agree):.4f}/{int(r.iloc[0].n_disagree):3d}"
                             if not r.empty and np.isfinite(r.iloc[0].get("agree", np.nan))
                             else f"{'--':>8s}")
            P(f"  {nm:6s} {pr:8s} " + " ".join(f"{c:>16s}" for c in cells)
              + ("   <-- CIRCULAR CEILING" if pr == "DDWIN" else ""))
    P("    (cell = agree / n_disagreeing matched pairs)")

    # BAR-A re-run at every excision
    P("")
    P("  BAR-A (910's own bar: agree >= DDWIN's AND best_agree >= DDWIN's AND 0 disagreeing")
    P("  pairs, FULL window / DDSUB), re-run at every excision:")
    barA = []
    for nm in PANELS:
        for e in EXCISIONS:
            d = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                  & (A["popn"] == "DDSUB") & (A.proxy == "DDWIN")]
            if d.empty or not np.isfinite(d.iloc[0].get("agree", np.nan)):
                continue
            d = d.iloc[0]
            for pr in EXANTE:
                r = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                      & (A["popn"] == "DDSUB") & (A.proxy == pr)]
                if r.empty or not np.isfinite(r.iloc[0].get("agree", np.nan)):
                    continue
                r = r.iloc[0]
                q = bool(r.agree >= d.agree - 1e-12 and r.best_agree >= d.best_agree - 1e-12
                         and r.n_disagree == 0)
                barA.append(dict(panel=nm, excision=e, proxy=pr, n=int(r.n), agree=r.agree,
                                 best_agree=r.best_agree, n_disagree=int(r.n_disagree),
                                 n_pairs=int(r.n_pairs), ddwin_agree=d.agree,
                                 ddwin_best=d.best_agree, ddwin_disagree=int(d.n_disagree),
                                 qualifies=q))
    BA = pd.DataFrame(barA)
    dump(BA, "barA.csv")
    P(f"  {'panel':6s} {'excision':8s} {'n':>4s} {'DDWIN agree/best/dis':>24s} "
      f"{'qualifying ex-ante proxies':>44s}")
    for nm in PANELS:
        for e in EXCISIONS:
            s = BA[(BA.panel == nm) & (BA.excision == e)]
            if s.empty:
                continue
            q = s[s.qualifies]
            P(f"  {nm:6s} {e:8s} {int(s.n.iloc[0]):4d} "
              f"{f'{s.ddwin_agree.iloc[0]:.4f}/{s.ddwin_best.iloc[0]:.4f}/{int(s.ddwin_disagree.iloc[0])}':>24s} "
              f"{(', '.join(q.proxy) if len(q) else '(none)'):>44s}")
    P("")
    P(f"  BAR-A totals: " + "  ".join(
        f"{e} {int(BA[BA.excision==e].qualifies.sum())}/{len(BA[BA.excision==e])}"
        for e in EXCISIONS if len(BA[BA.excision == e])))

    # the survival table -- the queue's actual question
    P("")
    P("=" * 110)
    P("WHICH COMMITTED CLAIMS SURVIVE?  (each claim re-read against ITS OWN committed bar)")
    P("=" * 110)
    surv = []

    def add(claim, panel, excision, stat, bar_txt, ok, committed):
        surv.append(dict(claim=claim, panel=panel, excision=excision, value=stat,
                         committed=committed, bar=bar_txt, survives=bool(ok)))

    for e in EXCISIONS:
        # K1 / K2 -- DDWIN reaches the bar on the large-cap panels
        for nm, comm in (("U56", 0.9531), ("B136", 0.9833)):
            r = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                  & (A["popn"] == "DDSUB") & (A.proxy == "DDWIN")]
            v = float(r.iloc[0].agree) if not r.empty and np.isfinite(r.iloc[0].get("agree", np.nan)) else np.nan
            dis = int(r.iloc[0].n_disagree) if not r.empty and np.isfinite(r.iloc[0].get("agree", np.nan)) else -1
            add(f"K{'1' if nm=='U56' else '2'} DDWIN reaches {AGREE_BAR} on {nm}", nm, e,
                v, f"agree >= {AGREE_BAR}", np.isfinite(v) and v >= AGREE_BAR, comm)
            if nm == "B136":
                add("K2b DDWIN B136 has 0 disagreeing pairs", nm, e, dis,
                    "n_disagree == 0", dis == 0, 0)
        # K3 / K4 -- 910's two qualifying ex-ante cells
        for nm, pr, comm in (("U56", "ROLL", 0.9844), ("B136", "SPYDD", 1.0000)):
            s = BA[(BA.panel == nm) & (BA.excision == e) & (BA.proxy == pr)]
            q = bool(s.iloc[0].qualifies) if not s.empty else False
            v = float(s.iloc[0].agree) if not s.empty else np.nan
            add(f"K{'3' if pr=='ROLL' else '4'} {nm}/{pr} clears BAR-A", nm, e, v,
                "BAR-A qualifies", q, comm)
        # K5 -- the DD leg is a high-R2 read of beta
        for nm, lo, hi in (("U56", 0.69, 0.97), ("B136", 0.69, 0.97)):
            r = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                  & (A["popn"] == "ALL") & (A.proxy == "FULL")]
            v = abs(float(r.iloc[0].spearman)) if not r.empty else np.nan
            add(f"K5 |rho(beta_FULL, MaxDD)| in [{lo},{hi}] on {nm}", nm, e, v,
                f"{lo} <= |rho| <= {hi}", np.isfinite(v) and lo <= v <= hi, np.nan)
        # K6 -- and still NOT a beta cap: agreement span over the real books
        sub = A[(A.excision == e) & (A.window == "FULL") & (A["popn"] == "ALL")
                & (A.panel.isin(PANELS)) & (A.proxy.isin(["FULL", "DOWN", "ROLL"]))]
        lo, hi = float(sub.agree.min()), float(sub.agree.max())
        add("K6 ex-ante agreement span stays below 1.0 (not a beta cap)", "all", e, hi,
            "max agree < 1.0", hi < 1.0 - 1e-12, 0.983)
        # K7 -- the H0 decomposition signs
        for nm in ("U56", "B136"):
            fa = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                   & (A["popn"] == "ALL") & (A.proxy == "FULL")]
            fs = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                   & (A["popn"] == "DDSUB") & (A.proxy == "FULL")]
            dd = A[(A.panel == nm) & (A.excision == e) & (A.window == "FULL")
                   & (A["popn"] == "DDSUB") & (A.proxy == "DDWIN")]
            if fa.empty or fs.empty or dd.empty or not np.isfinite(dd.iloc[0].get("agree", np.nan)):
                continue
            gp = float(fs.iloc[0].agree) - float(fa.iloc[0].agree)
            ge = float(dd.iloc[0].agree) - float(fs.iloc[0].agree)
            add(f"K7 {nm} POPULATION < 0 and ESTIMATOR > 0", nm, e, gp,
                "pop < 0 and est > 0", gp < 0 and ge > 0, np.nan)
        # K8 -- containment
        for nm, comm in (("U56", 0.9286), ("B136", 0.8929), ("SMALL", 0.0)):
            r = S[(S.panel == nm) & (S.excision == e) & (S.window == "FULL")]
            v = float(r.iloc[0].contained) if not r.empty else np.nan
            add(f"K8 containment share on {nm}", nm, e, v,
                f"within 0.05 of committed {comm:.4f}",
                np.isfinite(v) and abs(v - comm) <= 0.05, comm)
    SV = pd.DataFrame(surv)
    dump(SV, "survival.csv")
    P("")
    P(f"  {'claim':58s} " + " ".join(f"{e:>9s}" for e in EXCISIONS))
    for cl in SV.claim.unique():
        s = SV[SV.claim == cl]
        cells = []
        for e in EXCISIONS:
            x = s[s.excision == e]
            cells.append(("  --  " if x.empty else
                          ("SURVIVES" if bool(x.iloc[0].survives) else " BREAKS ")))
        P(f"  {cl:58s} " + " ".join(f"{c:>9s}" for c in cells))
    P("")
    nb = SV[SV.excision != "NONE"]
    P(f"  SURVIVAL SUMMARY: of {len(nb)} (claim x excision) cells outside the control, "
      f"{int(nb.survives.sum())} survive ({nb.survives.mean():.1%}).")
    P(f"  at the control (NONE): {int(SV[SV.excision=='NONE'].survives.sum())} of "
      f"{len(SV[SV.excision=='NONE'])} -- this is the reproduction check on the claims themselves.")

    # ============================================================================================
    # H_LEG -- does the DD leg's pass SET survive?
    # ============================================================================================
    P("")
    P("=" * 110)
    P("H_LEG / H_4b  DOES THE DD LEG'S PASS SET SURVIVE?  (every real book, nothing selected)")
    P("=" * 110)
    frows = []
    for nm in PANELS:
        for w in WINDOWS:
            b0 = real[(real.panel == nm) & (real.excision == "NONE") & (real.window == w)] \
                .set_index("bkey", drop=False)
            for e in EXCISIONS:
                b1 = real[(real.panel == nm) & (real.excision == e) & (real.window == w)] \
                    .set_index("bkey", drop=False).reindex(b0.index)
                fl = (b0.leg_DDCAP.values != b1.leg_DDCAP.values)
                f4 = (b0.pass4b.values != b1.pass4b.values)
                frows.append(dict(panel=nm, window=w, excision=e, n=len(b0),
                                  dd_pass_NONE=int(b0.leg_DDCAP.sum()),
                                  dd_pass_here=int(b1.leg_DDCAP.sum()),
                                  dd_flip=int(fl.sum()), dd_flip_share=float(fl.mean()),
                                  p4b_NONE=int(b0.pass4b.sum()), p4b_here=int(b1.pass4b.sum()),
                                  p4b_flip=int(f4.sum()), p4b_flip_share=float(f4.mean()),
                                  p4a_NONE=int(b0.pass4a.sum()), p4a_here=int(b1.pass4a.sum())))
    FL = pd.DataFrame(frows)
    dump(FL, "legflips.csv")
    P("")
    P(f"  {'panel':6s} {'window':6s} {'excision':8s} {'DDleg pass':>16s} {'flips':>12s} "
      f"{'4b pass':>14s} {'4b flips':>12s} {'4a pass':>14s}")
    for _, r in FL.iterrows():
        P(f"  {r.panel:6s} {r.window:6s} {r.excision:8s} "
          f"{f'{int(r.dd_pass_NONE)}->{int(r.dd_pass_here)}':>16s} "
          f"{f'{int(r.dd_flip)}/{int(r.n)} {r.dd_flip_share:.3f}':>12s} "
          f"{f'{int(r.p4b_NONE)}->{int(r.p4b_here)}':>14s} "
          f"{f'{int(r.p4b_flip)}/{int(r.n)} {r.p4b_flip_share:.3f}':>12s} "
          f"{f'{int(r.p4a_NONE)}->{int(r.p4a_here)}':>14s}")
    P("")
    nz = FL[(FL.excision != "NONE") & (FL.window == "FULL")]
    P(f"  H_LEG (bar: flip share > {FLIP_BAR} = the leg is the episode): max flip share on the "
      f"FULL window {nz.dd_flip_share.max():.3f} ({int((nz.dd_flip_share > FLIP_BAR).sum())} of "
      f"{len(nz)} cells above the bar)")

    # ============================================================================================
    # H_WF -- RULE 8: the books, both KEEP paths
    # ============================================================================================
    P("")
    P("=" * 110)
    P("H_WF / RULE 8  THE BOOKS: IS-only choosers on 2009-2016, OOS 2017-2026 read ONCE, at")
    P("               EVERY excision.  10 bps, t+1, weekly.  BOTH KEEP PATHS (PROTOCOL 4a/4b).")
    P("               The IS half carries no 2020 days (G9), so the chooser is IDENTICAL across")
    P("               excisions and every OOS move below is the episode.")
    P("=" * 110)
    brows = []
    for nm in PANELS:
        for e in EXCISIONS:
            IS = real[(real.panel == nm) & (real.excision == e) & (real.window == "IS")] \
                .reset_index(drop=True)
            OS = real[(real.panel == nm) & (real.excision == e) & (real.window == "OOS")] \
                .reset_index(drop=True)
            J = IS.merge(OS, on=["panel", "bkey", "family", "mode", "gross"],
                         suffixes=("_is", "_oos"))
            spy_o, v2_o = refs[nm][("SPY", e, "OOS")], refs[nm][("V2", e, "OOS")]
            sel = {
                "IS_SHARPE": np.ones(len(J), bool),
                "IS_DDCAP": J["leg_DDCAP_is"].values.astype(bool),
                "IS_ROLLCAP[<=0.60]": (J["beta_ROLL_is"].values <= BETA_CAP),
                "IS_SPYDDCAP[<=0.60]": (J["beta_SPYDD_is"].values <= BETA_CAP),
                "IS_DDWINCAP[circular]": (J["beta_DDWIN_is"].values <= BETA_CAP),
            }
            for chooser, mask in sel.items():
                mask = np.asarray(mask, bool) & np.isfinite(J["Sharpe_is"].values)
                if not mask.any():
                    brows.append(dict(panel=nm, excision=e, chooser=chooser,
                                      book="(empty selection)"))
                    continue
                cand = J[mask]
                pick = cand.loc[cand["Sharpe_is"].idxmax()]
                s = dict(CAGR=pick["CAGR_oos"], Sharpe=pick["Sharpe_oos"],
                         MaxDD=pick["MaxDD_oos"], H1=pick["H1_oos"], H2=pick["H2_oos"])
                th = "" if not np.isfinite(pick["theta_is"]) else f"/th={pick['theta_is']:.1f}"
                brows.append(dict(
                    panel=nm, excision=e, chooser=chooser,
                    book=f"{pick['family']}/{pick['mode']}{th}/g={pick['gross']:.2f}",
                    n_cand=int(mask.sum()),
                    OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                    OOS_H1=s["H1"], OOS_H2=s["H2"],
                    SPY_CAGR=spy_o["CAGR"], SPY_Sharpe=spy_o["Sharpe"], SPY_MaxDD=spy_o["MaxDD"],
                    V2_CAGR=v2_o["CAGR"], V2_Sharpe=v2_o["Sharpe"], V2_MaxDD=v2_o["MaxDD"],
                    pass4a=pass4a(s, v2_o), pass4b=pass4b(s, spy_o),
                    **{f"leg_{k}": v for k, v in legs4b(s, spy_o).items()}))
    WF = pd.DataFrame(brows)
    dump(WF, "walkforward.csv")
    P("")
    P(f"  {'panel':6s} {'exc':6s} {'chooser':22s} {'book':26s} {'cand':>5s} {'CAGR':>8s} "
      f"{'Shrp':>6s} {'MaxDD':>8s} {'H1/H2':>13s} {'4a':>3s} {'4b':>3s}")
    for _, r in WF.iterrows():
        if "OOS_CAGR" not in r or not np.isfinite(r.get("OOS_CAGR", np.nan)):
            P(f"  {r.panel:6s} {r.excision:6s} {r.chooser:22s} {r.book}")
            continue
        P(f"  {r.panel:6s} {r.excision:6s} {r.chooser:22s} {r.book:26s} {int(r.n_cand):5d} "
          f"{r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%} "
          f"{r.OOS_H1:6.3f}/{r.OOS_H2:6.3f} {'y' if r.pass4a else 'n':>3s} "
          f"{'y' if r.pass4b else 'n':>3s}")
    P("")
    P("  comparands, SAME OOS window, SAME excision:")
    P(f"  {'panel':6s} {'exc':6s} {'SPY CAGR/Sharpe/MaxDD':>34s} "
      f"{'RULES v2 (live) CAGR/Sharpe/MaxDD':>36s}")
    for nm in PANELS:
        for e in EXCISIONS:
            sp, v2 = refs[nm][("SPY", e, "OOS")], refs[nm][("V2", e, "OOS")]
            a = "%7.2f%% / %.3f / %7.2f%%" % (100 * sp["CAGR"], sp["Sharpe"], 100 * sp["MaxDD"])
            b = "%7.2f%% / %.3f / %7.2f%%" % (100 * v2["CAGR"], v2["Sharpe"], 100 * v2["MaxDD"])
            P(f"  {nm:6s} {e:6s} {a:>34s} {b:>36s}")
    P("")
    P("  full-window comparands (for the leaderboard rows), SAME excision:")
    for nm in PANELS:
        for e in EXCISIONS:
            sp, v2 = refs[nm][("SPY", e, "FULL")], refs[nm][("V2", e, "FULL")]
            P(f"    {nm:6s} {e:6s} SPY {sp['CAGR']:7.2%} / {sp['Sharpe']:.3f} / {sp['MaxDD']:7.2%} "
              f"(halves {sp['H1']:.3f}/{sp['H2']:.3f})   RULES v2 {v2['CAGR']:7.2%} / "
              f"{v2['Sharpe']:.3f} / {v2['MaxDD']:7.2%} (halves {v2['H1']:.3f}/{v2['H2']:.3f})")
    ok = WF["OOS_CAGR"].notna() if "OOS_CAGR" in WF else pd.Series(dtype=bool)
    P("")
    P(f"  RULE 8 SUMMARY by excision:")
    for e in EXCISIONS:
        w = WF[(WF.excision == e) & ok]
        if w.empty:
            continue
        P(f"    {e:6s} 4a {int(w.pass4a.sum())} of {len(w)}   4b {int(w.pass4b.sum())} of {len(w)}"
          f"   (books passing 4b: " + (", ".join(f"{r.panel}/{r.chooser}"
                                                 for _, r in w[w.pass4b].iterrows()) or "none") + ")")

    # ============================================================================================
    # verdict
    # ============================================================================================
    P("")
    P("=" * 110)
    P("VERDICT")
    P("=" * 110)
    for nm in PANELS:
        f = S[(S.panel == nm) & (S.window == "FULL")]
        P(f"  H_STRUCT {nm:6s} containment " + " ".join(
            f"{r.excision}={r.contained:.3f}" for _, r in f.iterrows()))
    P(f"  H_AGREE  {int(nb.survives.sum())} of {len(nb)} committed (claim x excision) cells "
      f"survive outside the control")
    P(f"  H_LEG    max DD-leg flip share (FULL window) {nz.dd_flip_share.max():.3f} "
      f"against a {FLIP_BAR} bar")
    P(f"  H_4b     FULL-window 4b census by excision: " + "  ".join(
        f"{e} " + "/".join(str(int(FL[(FL.excision==e)&(FL.window=='FULL')&(FL.panel==p)].p4b_here.iloc[0]))
                           for p in PANELS) for e in EXCISIONS) + "   (U56/B136/SMALL of 112)")
    P(f"  H_WF     rule 8: " + "  ".join(
        f"{e} 4a {int(WF[(WF.excision==e)&ok].pass4a.sum())}/4b "
        f"{int(WF[(WF.excision==e)&ok].pass4b.sum())}" for e in EXCISIONS))
    P("")
    P("SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops "
      f"the {len(bad)} tickers")
    P("  with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and drawdown LEVEL above "
      "is")
    P("  optimistic -- the books' and the comparands' alike.  The agreement tables, flip counts "
      "and")
    P("  containment shares are same-tape statistics and are unaffected.")
    P("")
    P(f"elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
