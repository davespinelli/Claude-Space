#!/usr/bin/env python3
"""Idea 910 (lane C, 2026-09-15) -- is there an EX-ANTE proxy for the DDWIN beta that is not
CIRCULAR?

THE QUESTION (queue, 2026-09-15)
  Idea 867 asked whether PROTOCOL 4b's DD leg

      DD leg    MaxDD(book) >= 0.60 * MaxDD(SPY)          (both negative; pass = shallower)

  is the constraint `beta <= 0.60` in a costume.  It answered NO for the three beta estimators
  anyone can compute ex ante (FULL / DOWN / ROLL agree with the DD leg on only 0.679-0.983 of
  books) -- but it found ONE estimator that does reach the bar:

      DDWIN   beta measured INSIDE the book's own peak-to-trough max-drawdown window
              B136 agreement 0.983, best-case 1.000, 0 of 109 matched pairs disagreeing

  and dismissed it as circular: the window is defined by the very drawdown the leg is testing.
  The queue asks whether some FORWARD-COMPUTABLE statistic -- a downside beta on a
  vol-conditioned subsample, a tail beta, a conditional-drawdown beta -- reaches the same
  agreement without that circularity.

WHAT "EX ANTE" MEANS HERE (stated before any number is read)
  A statistic is EX ANTE for this run iff its conditioning set is a function of MARKET data
  (SPY's path) and of the book's returns, but NEVER of the book's own equity-curve extremum.
  That is exactly the dependence 867 flagged.  DDWIN is the only estimator below that fails it,
  and it is carried as the CEILING, not as a candidate.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  PROXY (the queue's own first dial), 11 levels, every one reported:
           FULL     OLS beta of daily net book returns on SPY over the window   (867's reference)
           DOWN     the same restricted to days SPY < 0                         (867)
           ROLL     median of 252d rolling OLS betas                            (867)
           MAXROLL  MAX of the same 252d rolling betas ("worst beta you ever ran")
           EWMA     median of the exponentially-weighted beta path (halflife 252d)
           SEMI     downside semibeta  E[r*m*1{m<0}] / E[m^2*1{m<0}]
           TAIL10   OLS on the days SPY sits in its own worst return decile
           HIVOL    OLS on the days SPY's TRAILING 20d realised vol is top-quartile
                    (the queue's "downside beta at a vol-conditioned subsample")
           SPYDD    OLS inside SPY's OWN peak-to-trough max-drawdown window
                    (the queue's "conditional-drawdown beta" -- market-defined, so the SAME
                     days for every book on a panel: a drawdown window with no circularity)
           SPYDD10  OLS on the union of days SPY sits >= 10% below its running peak
           DDWIN    [CIRCULAR CEILING, not a candidate] the book's own peak-to-trough window
  TUNED 2  PANEL (the queue's own second dial), 3 levels: U56, B136, SMALL.
  REPORTED AXES (nothing is fitted on them; every point published):
           family (4) x mode (3) x theta (3, ROW has none) x gross (4) = 112 real books,
           + ZEROSIG (4 rungs) + RANDGATE (3 seeds x 4 rungs) = 128 traded books per panel,
           x 3 windows (FULL / IS / OOS) x 11 proxies x 2 POPULATIONS (see below).

THE POPULATION CONTROL (asked FIRST, because it may dispose of the question)
  867's committed `.agree.csv` reads DDWIN on n = 64 / 60 / 112 books against n = 112 / 112 / 112
  for the other three: DDWIN is UNDEFINED wherever a book's peak-to-trough window is shorter than
  20 trading days, which is most de-grossed books on the large-cap panels.  So 867's 0.983 is a
  number on a DIFFERENT AND SMALLER population than the 0.857 it is quoted against.  Before any
  proxy is searched for, this run re-reads every estimator on BOTH populations:
      ALL     all 112 real books on the panel/window
      DDSUB   the subset where DDWIN is defined  (867's own DDWIN population)
  If FULL reaches DDWIN's agreement on DDSUB, there is no DDWIN effect left to proxy.

PRE-REGISTERED BARS (fixed before the run; both directions reported)
  BAR-A  "reaches the same agreement" (the queue's words), read on the FULL window, DDSUB
         population, per panel:  agree >= agree(DDWIN)  AND  best_agree >= best_agree(DDWIN)
         AND matched-pair disagreement = 0.
  BAR-B  "and is usable": the qualifying proxy must survive rule 8 -- chosen on 2009-2016 only,
         its OOS agreement read once, bar 0.95 -- and its IS-only book selector read on OOS.

HYPOTHESES
  H0  DDWIN's edge over FULL is a POPULATION effect, not an estimator effect.
  H1  At least one ex-ante proxy clears BAR-A on at least one panel.
  H2  (upper bound) with the cap fitted on the answer, some ex-ante proxy reaches DDWIN's
      best-case agreement.
  H3  Some ex-ante proxy reproduces DDWIN's matched-pair exactness (0 disagreeing pairs).
  H4  The honest walk-forward form of DDWIN -- beta measured inside the book's IS drawdown
      window, used to predict the OOS DD leg -- beats FULL measured the same way.  If DDWIN is
      circular and nothing more, H4 FAILS.
  H5  (rule 8, books) an IS-only proxy-cap selector reaches 4a or 4b out of sample.

GATES (all printed before any hypothesis number)
  G1  TREND/ROW at g=0.75 == baseline.rules_v2_weights elementwise
  G2  the fast runner == engine.backtest on returns and turnover
  G3  the committed U56 triples (SPY, RULES v2) reproduce
  G4  867's committed .agree.csv reproduces -- agree / best_agree / beta_star for
      FULL/DOWN/ROLL/DDWIN x 3 panels on the FULL window, 36 published numbers
  G5  determinism (rebuild U56, compare)
  G6  the analytic ray: on the zero-signal book g x SPY EVERY proxy must read g, because a pure
      SPY blend has the same beta on every subsample.  This gates all 11 implementations at once.

PROTOCOL: 10 bps, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.
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
DD10 = 0.10                        # SPYDD10's market-drawdown depth

# ---- TUNED DIAL 1: the proxy ------------------------------------------------------------------
EXANTE = ["FULL", "DOWN", "ROLL", "MAXROLL", "EWMA", "SEMI", "TAIL10", "HIVOL", "SPYDD", "SPYDD10"]
PROXIES = EXANTE + ["DDWIN"]       # DDWIN carried as the circular CEILING
# ---- TUNED DIAL 2: the panel ------------------------------------------------------------------
PANELS = ["U56", "B136", "SMALL"]

# ---- reported axes ----------------------------------------------------------------------------
FAMILIES = ["TREND", "VOL", "MOM", "DISP"]
MODES = ["ROW", "AGG", "HYB"]
THETAS = [0.20, 0.40, 0.60]
GROSSES = [0.25, 0.50, 0.75, 1.00]
RAND_SEEDS = [9101, 9102, 9103]
POPS = ["ALL", "DDSUB"]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
PARENT_AGREE = ROOT / "research" / "backtests" / "2026-09-15_is-the-4b-DD-CAP-just-a-BETA-CAP_B.agree.csv"

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
# runner -- the record's vectorised equivalent of engine.backtest (gated at G1/G2)
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
        # market-state conditioners, one per window (never book-specific)
        self.cond = {w: market_conditioners(self.spy[m]) for w, m in self.masks.items()}


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
# the proxies -- TUNED DIAL 1
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
    """Boolean day-masks that depend ONLY on SPY's path over this window. Computed once per
    (panel, window) and shared by every book -- that is what makes them non-circular."""
    m = np.asarray(m, float)
    out = {}
    out["DOWN"] = m < 0.0
    # TAIL10: SPY's own worst return decile
    if len(m) >= MINOBS:
        q = np.quantile(m, 0.10)
        out["TAIL10"] = m <= q
    else:
        out["TAIL10"] = np.zeros(len(m), bool)
    # HIVOL: SPY trailing 20d realised vol, shifted one day (known at the open of day t)
    v = pd.Series(m).rolling(VOLWIN).std().shift(1)
    thr = v.quantile(0.75)
    out["HIVOL"] = (v >= thr).fillna(False).values if np.isfinite(thr) else np.zeros(len(m), bool)
    # SPYDD: SPY's own peak-to-trough max-drawdown window
    pk, tr = _dd_window(m)
    sp = np.zeros(len(m), bool)
    if tr - pk >= MINOBS:
        sp[pk: tr + 1] = True
    out["SPYDD"] = sp
    # SPYDD10: every day SPY sits >= 10% below its running peak
    eq = np.cumprod(1.0 + m)
    out["SPYDD10"] = (eq / np.maximum.accumulate(eq) - 1.0) <= -DD10
    return out


def proxies_all(r, m, cond):
    """All 11 readings of one book's beta over one window. r, m already windowed; cond is the
    panel/window's market-state mask dict from market_conditioners()."""
    out = {}
    out["FULL"] = _ols_beta(r, m)
    for key in ("DOWN", "TAIL10", "HIVOL", "SPYDD", "SPYDD10"):
        sel = cond[key]
        out[key] = _ols_beta(r[sel], m[sel]) if sel.sum() >= MINOBS else np.nan
    # rolling family -- one pass serves ROLL, MAXROLL
    if len(r) >= ROLLWIN + 10:
        rs, ms = pd.Series(r), pd.Series(m)
        b = rs.rolling(ROLLWIN).cov(ms) / ms.rolling(ROLLWIN).var()
        b = b.replace([np.inf, -np.inf], np.nan).dropna()
        out["ROLL"] = float(b.median()) if len(b) else np.nan
        out["MAXROLL"] = float(b.max()) if len(b) else np.nan
    else:
        out["ROLL"] = out["MAXROLL"] = np.nan
    # EWMA beta path, halflife 252d, median after a full halflife of data
    if len(r) >= ROLLWIN + 10:
        rs, ms = pd.Series(r), pd.Series(m)
        be = rs.ewm(halflife=EWMA_HL, min_periods=ROLLWIN).cov(ms) / \
            ms.ewm(halflife=EWMA_HL, min_periods=ROLLWIN).var()
        be = be.replace([np.inf, -np.inf], np.nan).dropna()
        out["EWMA"] = float(be.median()) if len(be) else np.nan
    else:
        out["EWMA"] = np.nan
    # SEMI: downside semibeta (no mean removal), Bollerslev-style
    dn = m < 0.0
    if dn.sum() >= MINOBS:
        den = float((m[dn] ** 2).sum())
        out["SEMI"] = float((r[dn] * m[dn]).sum() / den) if den > 0 else np.nan
    else:
        out["SEMI"] = np.nan
    # DDWIN -- the CIRCULAR ceiling (867's definition, unchanged, for G4)
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
    """(meta, net-returns array) for every traded book on this panel. Book objects are NOT
    retained -- only the T-length return vectors, so SMALL's 716 columns stay in memory."""
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


def score_books(pan: Panel, books):
    """One row per (book, window): metrics + all 11 proxies + the 4b legs."""
    ref = {}
    for win, m in pan.masks.items():
        ref[("SPY", win)] = pack(pan.spy[m])
    ew = ew_panel(pan.px)
    inb = gate_in(pan.px, "TREND")
    v2 = Book(pan, book_w1(ew, inb, None, "ROW", 0.0)).at(0.75, COST)[0]
    for win, m in pan.masks.items():
        ref[("V2", win)] = pack(v2[m])

    rows = []
    for md, r in books:
        for win, m in pan.masks.items():
            rw, mw = r[m], pan.spy[m]
            s = pack(rw)
            bt = proxies_all(rw, mw, pan.cond[win])
            spy = ref[("SPY", win)]
            L = legs4b(s, spy)
            row = dict(md)
            row.update(window=win, **{k: s[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")})
            row.update({f"beta_{k}": bt[k] for k in PROXIES})
            row.update(ddwin_len=bt["_ddlen"],
                       dd_ratio=s["MaxDD"] / spy["MaxDD"],
                       leg_DDCAP=L["DDCAP"], leg_CAGR=L["CAGRFLOOR"],
                       leg_H1=L["H1"], leg_H2=L["H2"],
                       pass4b=bool(all(L.values())),
                       pass4a=pass4a(s, ref[("V2", win)]))
            rows.append(row)
    return pd.DataFrame(rows), ref


# ================================================================================================
# agreement machinery
# ================================================================================================
def best_cap(beta, truth):
    """Cap fitted ON THE ANSWER: the threshold c maximising agreement of (beta <= c) with truth.
    Reported as an UPPER BOUND, never as a usable rule."""
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


def agree_row(panel, window, popn, proxy, beta, truth, maxdd):
    ok = np.isfinite(beta)
    n = int(ok.sum())
    if n < 5:
        return dict(panel=panel, window=window, popn=popn, proxy=proxy, n=n)
    b, t, d = beta[ok], truth[ok], maxdd[ok]
    pred = b <= BETA_CAP
    bc, ba = best_cap(beta, truth)
    # matched pairs: |dbeta| <= MATCH_TOL, disagreeing on the DD leg
    B = b[:, None] - b[None, :]
    M = np.triu(np.abs(B) <= MATCH_TOL, 1)
    npair = int(M.sum())
    dis = int((M & (t[:, None] != t[None, :])).sum())
    dmax = float(np.abs(d[:, None] - d[None, :])[M].max()) if npair else np.nan
    return dict(panel=panel, window=window, popn=popn, proxy=proxy, n=n,
                dd_pass=int(t.sum()), beta_pass=int(pred.sum()),
                agree=float((pred == t).mean()),
                TP=int((pred & t).sum()), FP=int((pred & ~t).sum()),
                FN=int((~pred & t).sum()), TN=int((~pred & ~t).sum()),
                beta_star=bc, best_agree=ba,
                spearman=spearman(b, d),
                n_pairs=npair, n_disagree=dis,
                pair_disagree=(dis / npair if npair else np.nan),
                max_dMaxDD_in_pair=dmax)


def flips4b(sub, proxy):
    """Books where swapping `beta <= 0.60` for the DD leg flips the WHOLE 4b verdict."""
    b = sub[f"beta_{proxy}"].values
    ok = np.isfinite(b)
    other = sub["leg_H1"].values & sub["leg_H2"].values & sub["leg_CAGR"].values
    dd = sub["leg_DDCAP"].values
    pred = b <= BETA_CAP
    flip = ok & other & (dd != pred)
    return int(flip.sum()), int((ok & dd & other).sum()), int(ok.sum())


# ================================================================================================
# gates
# ================================================================================================
def run_gates(panels):
    P("=" * 100)
    P("GATES (printed before any result number is read)")
    P("=" * 100)
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

    m = pan.m_full
    spy_t = fmet(pan.spy[m])
    v2_t = fmet(r_fast[m])
    d1 = tuple(abs(spy_t[i] - SPY_U56[i]) for i in range(3))
    d2 = tuple(abs(v2_t[i] - V2_U56[i]) for i in range(3))
    ok["G3"] = (d1[0] < TOL_C and d1[1] < TOL_S and d1[2] < TOL_D
                and d2[0] < TOL_C and d2[1] < TOL_S and d2[2] < TOL_D)
    P(f"G3  committed U56 triples   SPY {spy_t[0]:.4%}/{spy_t[1]:.4f}/{spy_t[2]:.4%}  "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%})")
    P(f"                            v2  {v2_t[0]:.4%}/{v2_t[1]:.4f}/{v2_t[2]:.4%}  "
      f"(committed {V2_U56[0]:.2%}/{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> {'PASS' if ok['G3'] else 'FAIL'}")

    # G6 -- the analytic ray: every proxy of g x SPY must read g
    Z = np.zeros((pan.T, pan.N))
    Z[:, list(px.columns).index("SPY")] = 1.0
    zb = Book(pan, Z)
    worst, detail = 0.0, []
    for g in GROSSES:
        rz, _ = zb.at(g, cost=0.0)
        bt = proxies_all(rz[m], pan.spy[m], pan.cond["FULL"])
        for k in PROXIES:
            if np.isfinite(bt[k]):
                worst = max(worst, abs(bt[k] - g))
        detail.append((g, {k: bt[k] for k in PROXIES}))
    ok["G6"] = worst < 0.03
    P(f"G6  ZEROSIG ray (g x SPY, 0 bps): every proxy must read g   max|beta-g| over "
      f"{len(GROSSES)}x{len(PROXIES)} = {worst:.3e}   -> {'PASS' if ok['G6'] else 'FAIL'}")
    for g, d in detail:
        P("      g=%.2f  " % g + "  ".join(f"{k}={d[k]:.3f}" for k in PROXIES if np.isfinite(d[k])))
    return ok, zb


def gate_parent(B):
    """G4 -- reproduce idea 867's committed .agree.csv (36 published numbers)."""
    if not PARENT_AGREE.exists():
        P("G4  parent .agree.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(PARENT_AGREE)
    rows, worst = [], 0.0
    for _, pr in par.iterrows():
        sub = B[(B.panel == pr.panel) & (B.window == "FULL") & (~B.family.str.startswith(("ZEROSIG", "RANDGATE")))]
        beta = sub[f"beta_{pr.estimator}"].values
        truth = sub["leg_DDCAP"].values
        ok = np.isfinite(beta)
        n = int(ok.sum())
        pred = beta[ok] <= BETA_CAP
        ag = float((pred == truth[ok]).mean())
        bc, ba = best_cap(beta, truth)
        d = dict(panel=pr.panel, estimator=pr.estimator,
                 n_parent=int(pr.n), n_here=n,
                 agree_parent=float(pr.agree), agree_here=ag,
                 best_parent=float(pr.best_agree), best_here=ba,
                 bstar_parent=float(pr.beta_star), bstar_here=bc)
        d["d_agree"] = abs(d["agree_here"] - d["agree_parent"])
        d["d_best"] = abs(d["best_here"] - d["best_parent"])
        d["d_bstar"] = abs(d["bstar_here"] - d["bstar_parent"])
        d["d_n"] = abs(n - int(pr.n))
        worst = max(worst, d["d_agree"], d["d_best"])
        rows.append(d)
    G = pd.DataFrame(rows)
    passed = bool((G.d_n == 0).all() and worst < 1e-9)
    P(f"G4  867's committed .agree.csv reproduced: {len(G)} rows, worst |d_agree| "
      f"{G.d_agree.max():.3e}, worst |d_best| {G.d_best.max():.3e}, worst |d_beta*| "
      f"{G.d_bstar.max():.3e}, n mismatches {int((G.d_n != 0).sum())}   -> "
      f"{'PASS' if passed else 'FAIL'}")
    for _, r in G.iterrows():
        P(f"      {r.panel:6s} {r.estimator:8s} n {int(r.n_here):3d}/{int(r.n_parent):3d}  "
          f"agree {r.agree_here:.4f}/{r.agree_parent:.4f}  best {r.best_here:.4f}/{r.best_parent:.4f}"
          f"  beta* {r.bstar_here:.3f}/{r.bstar_parent:.3f}")
    return passed, G


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 910 (lane C, 2026-09-15) -- is there an EX-ANTE proxy for the DDWIN beta that is not")
    P("                                 CIRCULAR?")
    P("=" * 100)
    P(f"TUNED 1 proxy ({len(PROXIES)} levels, all reported): {PROXIES}")
    P(f"        ex ante = {EXANTE}")
    P("        DDWIN is the CIRCULAR CEILING, carried for comparison, never a candidate")
    P(f"TUNED 2 panel: {PANELS}")
    P(f"reported axes: family {FAMILIES} x mode {MODES} x theta {THETAS} x gross {GROSSES}")
    P(f"                + ZEROSIG + RANDGATE{RAND_SEEDS};  cost {COST:.0f} bps, {FREQ}, LAG {LAG}")
    P(f"populations: {POPS}  (DDSUB = the books where DDWIN is defined -- 867's own population)")
    P(f"PRE-REGISTERED BAR-A: agree >= DDWIN's AND best_agree >= DDWIN's AND 0 disagreeing pairs,")
    P(f"                      read on FULL window / DDSUB population, per panel.")
    P(f"PRE-REGISTERED BAR-B: rule 8 -- proxy chosen on IS, OOS agreement read once, bar {AGREE_BAR}")
    P("")

    panels = {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        panels[nm] = Panel(nm, px)
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  "
          f"{px.index[0].date()} .. {px.index[-1].date()}  eval from {panels[nm].start.date()}")
    P("")

    gates, _ = run_gates(panels)

    P("")
    P("=" * 100)
    P("BUILDING THE BOOK GRID")
    P("=" * 100)
    allb, refs, book_rets = [], {}, {}
    for nm in PANELS:
        t = time.time()
        bk = build_books(panels[nm])
        df, ref = score_books(panels[nm], bk)
        refs[nm] = ref
        allb.append(df)
        book_rets[nm] = bk
        P(f"  {nm:6s} {len(bk):4d} books  {len(df):5d} book-windows  ({time.time()-t:.1f}s)")
    B = pd.concat(allb, ignore_index=True)
    del allb

    bk2 = build_books(panels["U56"])
    d2, _ = score_books(panels["U56"], bk2)
    a = B[B.panel == "U56"].reset_index(drop=True)
    ds = float(np.nanmax(np.abs(a["Sharpe"].values - d2["Sharpe"].values)))
    db = float(np.nanmax(np.abs(a["beta_SPYDD"].values - d2["beta_SPYDD"].values)))
    gates["G5"] = ds < 1e-12 and db < 1e-12
    P(f"G5  DETERMINISM  max|dSharpe| {ds:.3e}  max|dbeta_SPYDD| {db:.3e}   "
      f"-> {'PASS' if gates['G5'] else 'FAIL'}")
    del bk2, d2, a

    P("")
    gates["G4"], G4 = gate_parent(B)
    P("")
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  " + "  ".join(
        f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items())))
    if not all(gates.values()):
        P("  *** a gate FAILED -- every number below is reported with that caveat ***")
    dump(B, "books.csv")
    dump(G4, "gate867.csv")

    real = B[~B.family.str.startswith(("ZEROSIG", "RANDGATE"))].copy()
    P("")
    P(f"book grid: {B.panel.nunique()} panels, {len(B)} book-windows, "
      f"{len(B[B.window=='FULL'])} traded books "
      f"({len(real[real.window=='FULL'])} real, {len(B[B.window=='FULL'])-len(real[real.window=='FULL'])} control)")

    # --------------------------------------------------------------------------------------
    # H0 -- the POPULATION control
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("H0  IS DDWIN's EDGE AN ESTIMATOR EFFECT OR A POPULATION EFFECT?")
    P("=" * 100)
    rows = []
    for nm in PANELS:
        for win in ("FULL", "IS", "OOS"):
            sub = real[(real.panel == nm) & (real.window == win)]
            ddok = np.isfinite(sub["beta_DDWIN"].values)
            for popn in POPS:
                s = sub if popn == "ALL" else sub[ddok]
                for pr in PROXIES:
                    rows.append(agree_row(nm, win, popn, pr,
                                          s[f"beta_{pr}"].values.astype(float),
                                          s["leg_DDCAP"].values.astype(bool),
                                          s["MaxDD"].values.astype(float)))
    A = pd.DataFrame(rows)
    dump(A, "agree.csv")

    F = A[A.window == "FULL"]
    P("")
    P("median DDWIN peak-to-trough length (trading days), FULL window, real books:")
    for nm in PANELS:
        sub = real[(real.panel == nm) & (real.window == "FULL")]
        ok = np.isfinite(sub["beta_DDWIN"].values)
        P(f"   {nm:6s} defined {int(ok.sum()):3d} of {len(sub):3d} books   "
          f"median len {np.median(sub['ddwin_len'].values):.0f}d   "
          f"defined-subset median len {np.median(sub['ddwin_len'].values[ok]):.0f}d   "
          f"mean gross defined {sub['gross'].values[ok].mean():.3f} vs undefined "
          f"{sub['gross'].values[~ok].mean():.3f}")
    P("")
    P("  agreement with the DD leg at the FIXED cap beta <= 0.60, FULL window")
    P(f"  {'panel':6s} {'proxy':8s} | {'ALL':>22s} | {'DDSUB':>22s}")
    P(f"  {'':6s} {'':8s} | {'n':>4s} {'agree':>7s} {'best':>7s} | {'n':>4s} {'agree':>7s} {'best':>7s}")
    for nm in PANELS:
        for pr in PROXIES:
            a1 = F[(F.panel == nm) & (F["popn"] == "ALL") & (F.proxy == pr)]
            a2 = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == pr)]
            if a1.empty or a2.empty:
                continue
            r1, r2 = a1.iloc[0], a2.iloc[0]
            P(f"  {nm:6s} {pr:8s} | {int(r1.n):4d} {r1.agree:7.4f} {r1.best_agree:7.4f} | "
              f"{int(r2.n):4d} {r2.agree:7.4f} {r2.best_agree:7.4f}"
              + ("   <-- CIRCULAR CEILING" if pr == "DDWIN" else ""))
    P("")
    for nm in PANELS:
        f_all = F[(F.panel == nm) & (F["popn"] == "ALL") & (F.proxy == "FULL")].iloc[0]
        f_sub = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == "FULL")].iloc[0]
        d_sub = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == "DDWIN")].iloc[0]
        gap_pop = f_sub.agree - f_all.agree
        gap_est = d_sub.agree - f_sub.agree
        P(f"  {nm:6s} DECOMPOSITION of DDWIN({d_sub.agree:.4f}) - FULL_ALL({f_all.agree:.4f}) = "
          f"{d_sub.agree-f_all.agree:+.4f}  =  POPULATION {gap_pop:+.4f}  +  ESTIMATOR {gap_est:+.4f}")
    P("")

    # --------------------------------------------------------------------------------------
    # H1 / H2 / H3 -- BAR-A
    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("H1 / H2 / H3  BAR-A: does ANY ex-ante proxy reach DDWIN on its OWN population?")
    P("=" * 100)
    barA = []
    for nm in PANELS:
        d = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == "DDWIN")].iloc[0]
        P("")
        P(f"  {nm}  (DDSUB, n={int(d.n)}):  DDWIN agree {d.agree:.4f}  best {d.best_agree:.4f}  "
          f"pairs {int(d.n_disagree)}/{int(d.n_pairs)} disagreeing  rho {d.spearman:+.3f}")
        P(f"    {'proxy':8s} {'agree':>7s} {'best':>7s} {'beta*':>7s} {'rho':>7s} "
          f"{'pairs dis':>12s} {'maxdDD':>8s}  BAR-A")
        for pr in EXANTE:
            r = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == pr)]
            if r.empty:
                continue
            r = r.iloc[0]
            q = bool(r.agree >= d.agree - 1e-12 and r.best_agree >= d.best_agree - 1e-12
                     and r.n_disagree == 0)
            barA.append(dict(panel=nm, proxy=pr, agree=r.agree, best_agree=r.best_agree,
                             n_disagree=int(r.n_disagree), n_pairs=int(r.n_pairs),
                             ddwin_agree=d.agree, ddwin_best=d.best_agree,
                             ddwin_disagree=int(d.n_disagree), qualifies=q))
            P(f"    {pr:8s} {r.agree:7.4f} {r.best_agree:7.4f} {r.beta_star:7.3f} "
              f"{r.spearman:+7.3f} {int(r.n_disagree):5d}/{int(r.n_pairs):<6d} "
              f"{r.max_dMaxDD_in_pair:7.1%}  {'QUALIFIES' if q else '-'}")
    BA = pd.DataFrame(barA)
    dump(BA, "barA.csv")
    nq = int(BA.qualifies.sum())
    P("")
    P(f"  BAR-A RESULT: {nq} of {len(BA)} (proxy x panel) cells qualify.")
    if nq:
        for _, r in BA[BA.qualifies].iterrows():
            P(f"     {r.panel} / {r.proxy}: agree {r.agree:.4f} >= {r.ddwin_agree:.4f}, "
              f"best {r.best_agree:.4f} >= {r.ddwin_best:.4f}, {int(r.n_disagree)} disagreeing pairs")

    # best ex-ante proxy per panel on the ALL population (the population that matters for a rule)
    P("")
    P("  and on the population a REAL rule would face (ALL 112 books, FULL window):")
    P(f"    {'panel':6s} {'best ex-ante proxy':>20s} {'agree':>8s} | {'FULL':>8s} | "
      f"{'DDWIN(own pop)':>15s}")
    for nm in PANELS:
        sub = F[(F.panel == nm) & (F["popn"] == "ALL") & (F.proxy.isin(EXANTE))]
        b = sub.loc[sub.agree.idxmax()]
        f0 = F[(F.panel == nm) & (F["popn"] == "ALL") & (F.proxy == "FULL")].iloc[0]
        d0 = F[(F.panel == nm) & (F["popn"] == "DDSUB") & (F.proxy == "DDWIN")].iloc[0]
        P(f"    {nm:6s} {b.proxy:>20s} {b.agree:8.4f} | {f0.agree:8.4f} | {d0.agree:15.4f}")

    # --------------------------------------------------------------------------------------
    # 4b flips
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("DOES THE SUBSTITUTION REACH 4b?  (books whose WHOLE 4b verdict flips under `beta<=0.60`)")
    P("=" * 100)
    frows = []
    for nm in PANELS:
        sub = real[(real.panel == nm) & (real.window == "FULL")]
        line = []
        for pr in PROXIES:
            f, actual, nn = flips4b(sub, pr)
            frows.append(dict(panel=nm, proxy=pr, flips=f, actual_4b_pass=actual, n_defined=nn))
            line.append(f"{pr} {f}/{nn}")
        P(f"  {nm:6s} actual 4b passes {int(sub.pass4b.sum()):3d} of {len(sub):3d}   " + "  ".join(line))
    FL = pd.DataFrame(frows)
    dump(FL, "flips.csv")

    # --------------------------------------------------------------------------------------
    # MECHANISM -- why SPYDD reaches DDWIN: the two windows are the SAME EPISODE
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("MECHANISM  how much of a book's OWN drawdown window is SPY's OWN drawdown window?")
    P("           (Jaccard overlap of the two day-sets; reported, never tuned)")
    P("=" * 100)
    orows = []
    for nm in PANELS:
        pan = panels[nm]
        for win, m in pan.masks.items():
            mw = pan.spy[m]
            spk, str_ = _dd_window(mw)
            sset = set(range(spk, str_ + 1))
            for md, r in book_rets[nm]:
                if str(md["family"]).startswith(("ZEROSIG", "RANDGATE")):
                    continue
                rw = r[m]
                bpk, btr = _dd_window(rw)
                bset = set(range(bpk, btr + 1))
                inter = len(sset & bset)
                uni = len(sset | bset)
                orows.append(dict(panel=nm, window=win,
                                  family=md["family"], mode=md["mode"], theta=md["theta"],
                                  gross=md["gross"],
                                  jaccard=(inter / uni if uni else np.nan),
                                  book_len=btr - bpk + 1, spy_len=str_ - spk + 1,
                                  contained=float(inter == (btr - bpk + 1))))
    OV = pd.DataFrame(orows)
    dump(OV, "overlap.csv")
    P("")
    P(f"  {'panel':6s} {'window':6s} {'median Jaccard':>15s} {'share contained in SPY DD':>27s} "
      f"{'SPY DD len':>11s}")
    for nm in PANELS:
        for win in ("FULL", "IS", "OOS"):
            o = OV[(OV.panel == nm) & (OV.window == win)]
            P(f"  {nm:6s} {win:6s} {o.jaccard.median():15.3f} {o.contained.mean():27.3f} "
              f"{int(o.spy_len.iloc[0]):11d}")
    P("")
    P("  read: where a book's own peak-to-trough IS (inside) the market's, SPYDD and DDWIN are")
    P("  reading the SAME DAYS, so SPYDD inherits DDWIN's agreement AND DDWIN's in-window")
    P("  dependence.  The circularity is relocated to the market, not removed.")

    # --------------------------------------------------------------------------------------
    # H4 -- the HONEST walk-forward form of DDWIN (rule 8, part a)
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("H4 / RULE 8 (a)  THE NON-CIRCULAR FORM OF DDWIN: measure beta on 2009-2016, predict the")
    P("                 2017-2026 DD leg.  Every proxy chosen on IS, read ONCE on OOS.")
    P("=" * 100)
    wrows = []
    for nm in PANELS:
        IS = real[(real.panel == nm) & (real.window == "IS")].reset_index(drop=True)
        OS = real[(real.panel == nm) & (real.window == "OOS")].reset_index(drop=True)
        key = ["family", "mode", "theta", "gross"]
        J = IS.merge(OS, on=["panel"] + key, suffixes=("_is", "_oos"))
        for pr in PROXIES:
            bi = J[f"beta_{pr}_is"].values.astype(float)
            to = J["leg_DDCAP_oos"].values.astype(bool)
            ti = J["leg_DDCAP_is"].values.astype(bool)
            ok = np.isfinite(bi)
            if ok.sum() < 5:
                continue
            # cap fitted on IS only, then applied OOS untouched
            c_is, a_is = best_cap(bi, ti)
            pred_oos = bi[ok] <= c_is
            a_oos_fit = float((pred_oos == to[ok]).mean())
            a_oos_060 = float(((bi[ok] <= BETA_CAP) == to[ok]).mean())
            # how well does the IS beta even predict the OOS beta of the same estimator
            bo = J[f"beta_{pr}_oos"].values.astype(float)
            wrows.append(dict(panel=nm, proxy=pr, n=int(ok.sum()),
                              cap_IS=c_is, agree_IS_fit=a_is,
                              agree_OOS_at_IScap=a_oos_fit, agree_OOS_at_060=a_oos_060,
                              rho_beta_IS_OOS=spearman(bi, bo),
                              rho_betaIS_ddOOS=spearman(bi, J["MaxDD_oos"].values.astype(float)),
                              exante=(pr in EXANTE)))
    W = pd.DataFrame(wrows)
    dump(W, "wfproxy.csv")
    P("")
    P(f"  {'panel':6s} {'proxy':8s} {'n':>4s} {'cap_IS':>7s} {'agreeIS':>8s} {'agreeOOS':>9s} "
      f"{'@0.60':>7s} {'rho(bIS,bOOS)':>14s} {'rho(bIS,ddOOS)':>15s}")
    for _, r in W.iterrows():
        P(f"  {r.panel:6s} {r.proxy:8s} {int(r.n):4d} {r.cap_IS:7.3f} {r.agree_IS_fit:8.4f} "
          f"{r.agree_OOS_at_IScap:9.4f} {r.agree_OOS_at_060:7.4f} {r.rho_beta_IS_OOS:+14.3f} "
          f"{r.rho_betaIS_ddOOS:+15.3f}" + ("" if r.exante else "   <-- circular"))
    P("")
    for nm in PANELS:
        w = W[W.panel == nm]
        if w.empty:
            continue
        dd = w[w.proxy == "DDWIN"]
        ex = w[w.exante]
        b = ex.loc[ex.agree_OOS_at_IScap.idxmax()]
        P(f"  {nm:6s} H4: DDWIN_IS->OOS {float(dd.agree_OOS_at_IScap.iloc[0]):.4f} "
          f"(n={int(dd.n.iloc[0])})  vs FULL_IS->OOS "
          f"{float(w[w.proxy=='FULL'].agree_OOS_at_IScap.iloc[0]):.4f}  "
          f"vs best ex-ante {b.proxy} {b.agree_OOS_at_IScap:.4f}   "
          f"(bar {AGREE_BAR}: {'clears' if b.agree_OOS_at_IScap >= AGREE_BAR else 'MISSES'})")

    # --------------------------------------------------------------------------------------
    # RULE 8 (b) -- the BOOKS, both KEEP paths
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("RULE 8 (b)  THE BOOKS: IS-only choosers on 2009-2016, OOS 2017-2026 read ONCE.")
    P("            10 bps, t+1, weekly.  BOTH KEEP PATHS evaluated (PROTOCOL 4a and 4b).")
    P("=" * 100)
    brows = []
    for nm in PANELS:
        IS = real[(real.panel == nm) & (real.window == "IS")].reset_index(drop=True)
        OS = real[(real.panel == nm) & (real.window == "OOS")].reset_index(drop=True)
        key = ["family", "mode", "theta", "gross"]
        J = IS.merge(OS, on=["panel"] + key, suffixes=("_is", "_oos"))
        spy_o, v2_o = refs[nm][("SPY", "OOS")], refs[nm][("V2", "OOS")]
        # the best ex-ante proxy on THIS panel, chosen on IS agreement only
        w = W[(W.panel == nm) & (W.exante)]
        bestpr = str(w.loc[w.agree_IS_fit.idxmax()].proxy) if len(w) else "FULL"
        cap_is = float(w.loc[w.agree_IS_fit.idxmax()].cap_IS) if len(w) else BETA_CAP
        sel = {
            "IS_SHARPE": np.ones(len(J), bool),
            "IS_DDCAP": J["leg_DDCAP_is"].values.astype(bool),
            f"IS_PROXYCAP[{bestpr}@0.60]": (J[f"beta_{bestpr}_is"].values <= BETA_CAP),
            f"IS_PROXYCAP[{bestpr}@IScap]": (J[f"beta_{bestpr}_is"].values <= cap_is),
            "IS_DDWINCAP[circular]": (J["beta_DDWIN_is"].values <= BETA_CAP),
        }
        for chooser, mask in sel.items():
            mask = np.asarray(mask, bool) & np.isfinite(J["Sharpe_is"].values)
            if not mask.any():
                brows.append(dict(panel=nm, chooser=chooser, book="(empty selection)"))
                continue
            cand = J[mask]
            pick = cand.loc[cand["Sharpe_is"].idxmax()]
            s = dict(CAGR=pick["CAGR_oos"], Sharpe=pick["Sharpe_oos"], MaxDD=pick["MaxDD_oos"],
                     H1=pick["H1_oos"], H2=pick["H2_oos"])
            th = "" if not np.isfinite(pick["theta"]) else f"/th={pick['theta']:.1f}"
            brows.append(dict(
                panel=nm, chooser=chooser,
                book=f"{pick['family']}/{pick['mode']}{th}/g={pick['gross']:.2f}",
                n_cand=int(mask.sum()),
                OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                OOS_H1=s["H1"], OOS_H2=s["H2"],
                pass4a=pass4a(s, v2_o), pass4b=pass4b(s, spy_o),
                **{f"leg_{k}": v for k, v in legs4b(s, spy_o).items()}))
    WF = pd.DataFrame(brows)
    dump(WF, "walkforward.csv")
    P("")
    P(f"  {'panel':6s} {'chooser':28s} {'book':30s} {'cand':>5s} {'CAGR':>8s} {'Shrp':>6s} "
      f"{'MaxDD':>8s} {'H1/H2':>13s} {'4a':>3s} {'4b':>3s}")
    for _, r in WF.iterrows():
        if "OOS_CAGR" not in r or not np.isfinite(r.get("OOS_CAGR", np.nan)):
            P(f"  {r.panel:6s} {r.chooser:28s} {r.book}")
            continue
        P(f"  {r.panel:6s} {r.chooser:28s} {r.book:30s} {int(r.n_cand):5d} {r.OOS_CAGR:8.2%} "
          f"{r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%} {r.OOS_H1:6.3f}/{r.OOS_H2:6.3f} "
          f"{'y' if r.pass4a else 'n':>3s} {'y' if r.pass4b else 'n':>3s}")
    P("")
    P("  comparands, SAME OOS window:")
    for nm in PANELS:
        sp, v2 = refs[nm][("SPY", "OOS")], refs[nm][("V2", "OOS")]
        P(f"    {nm:6s} SPY {sp['CAGR']:7.2%} / {sp['Sharpe']:.3f} / {sp['MaxDD']:7.2%} "
          f"(halves {sp['H1']:.3f}/{sp['H2']:.3f})    "
          f"RULES v2 (live) {v2['CAGR']:7.2%} / {v2['Sharpe']:.3f} / {v2['MaxDD']:7.2%} "
          f"(halves {v2['H1']:.3f}/{v2['H2']:.3f})")
    n4a, n4b = int(WF.get("pass4a", pd.Series(dtype=bool)).sum()), int(WF.get("pass4b", pd.Series(dtype=bool)).sum())
    ntot = int(WF["OOS_CAGR"].notna().sum()) if "OOS_CAGR" in WF else 0
    P("")
    P(f"  RULE 8 SUMMARY: 4a {n4a} of {ntot}   4b {n4b} of {ntot}")

    # --------------------------------------------------------------------------------------
    # verdict
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    P(f"  H0 population control: see the decomposition above.")
    P(f"  H1/H2/H3 BAR-A: {nq} of {len(BA)} ex-ante (proxy x panel) cells reach DDWIN.")
    wex = W[W.exante]
    P(f"  H4 rule 8 (a): best ex-ante OOS agreement "
      f"{wex.agree_OOS_at_IScap.max():.4f} against bar {AGREE_BAR}; "
      f"DDWIN_IS->OOS {W[W.proxy=='DDWIN'].agree_OOS_at_IScap.max():.4f}")
    P(f"  H5 rule 8 (b): 4a {n4a} of {ntot}, 4b {n4b} of {ntot}")
    P("")
    P(f"elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
