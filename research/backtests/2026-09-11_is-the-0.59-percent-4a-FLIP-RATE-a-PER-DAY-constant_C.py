#!/usr/bin/env python3
"""
IDEA 683 -- is-the-0.59-percent-4a-FLIP-RATE-a-PER-DAY-constant                    (lane C)
==========================================================================================

THE QUEUE'S QUESTION (verbatim)
-------------------------------
  idea 516 found two calendar days of price drift flip 0.59% of 4a passes and 0.07% of 4b
  passes over 153,429 book-rows, i.e. a published KEEP has a decay rate.  Measure the flip
  rate as a function of vintage distance using the git history of data/prices.csv, and
  report the horizon at which a committed 4b pass is more likely than not to have moved.
  Max 2 params (horizon ladder, claim set).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)  : P1 HORIZON d (the vintage-distance rung) and P2 CLAIM SET (which family of
               book-rows the flip rate is measured over: ALL / BAND / CAND / FLAT).
  NOT TUNED  : cost 10 bps (PROTOCOL 2); cadences W and M; band grid, n grid, vol-cap grid
               and gross ladder -- all are the record's OWN committed dials, restated, never
               chosen by looking at an outcome; warm-up 260 rows; IS/OOS split
               2016-12-31 / 2017-01-01 (PROTOCOL 8); the 4a/4b legs exactly as PROTOCOL 4
               and baseline.compare state them.

WHY IDEA 516's NUMBER CANNOT ANSWER ITS OWN QUESTION
----------------------------------------------------
  516 measured ONE interval (2026-09-08 -> 2026-09-10) by re-executing committed scripts.
  That conflates three different things which decay at completely different speeds:
     (R) RESTATEMENT   historical cells in prices.csv change under you (splits, dividend
                       adjustment, vendor revision).  Mean-reverting-ish, no direction.
     (E) EXTENSION     the panel gains trailing days.  Directional: the sample the verdict
                       is computed on is literally a different sample.
     (X) CORPUS/CODE   the record itself grew, and on 2026-09-04 the price cache changed
                       its INDEX CONVENTION (commit c006b43 aligned crypto to equity days,
                       6,060 rows -> 4,698).  Not price drift at all.
  This run separates them at source by re-adjudicating ONE FIXED BOOK GRID -- no committed
  artefacts, no re-execution, no corpus -- on every price vintage git holds.

THE THREE CHANNELS
------------------
  B  "AS PUBLISHED"  the 8 real git vintages of data/prices.csv, each read on ITS OWN full
                     sample, exactly as a researcher that day would have.  d = calendar days
                     between the two vintages.  d in {1,2,3,4,5,6,7}.  Contains R + E + X.
  R  "RESTATEMENT"   the same 8 vintages, both members of a pair restricted to the
                     INTERSECTION of their date indexes.  Same sample, moved values.  Pure R.
  E  "EXTENSION"     pseudo-vintages built by truncating the NEWEST panel by k trading days,
                     k in {1,2,3,5,10,21,42,63,126,252}, compared against the untruncated
                     panel.  Pure E, and the only channel that reaches past 7 days, which is
                     all the git history there is.  It carries NO restatement by construction;
                     channel R measures separately how much that omits.
  B ~ R (+) E at the overlapping rungs is reported as a consistency check, not assumed.

  Gate G7 asserts the identity that makes E legitimate: every indicator in this grid is
  backward-looking, so weights computed on the full panel and then truncated are EXACTLY the
  weights computed on the truncated panel.  Truncation is therefore a real vintage, not an
  approximation.

THE CLAIM SET (848 book-rows, P2)
---------------------------------
  BAND   band in {0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.08,0.10,0.12} x gross x freq   160
  CAND   n in {3,5,8,10,12,15,20,25,30,40} x volscale{on,off} x volcap{0.60,off}
                                            x gross x freq                            640
  FLAT   EWELIG (equal-weight every eligible name) x volcap x gross x freq              32
         SPYBH  (g x SPY, the zero-signal exposure control) x gross x freq               16
  gross in {0.20,0.35,0.50,0.60,0.75,0.85,0.95,1.00} (idea 668's committed ladder), freq
  in {W,M}.  BAND(0.03, 0.75, W) IS the live RULES v2 book -- gate G2.

WHAT IS REPORTED AT EVERY RUNG
------------------------------
  4a pass / 4b pass counts, flip counts, and the two conditional rates the queue names:
     DECAY(4a|d) = P(a row that PASSED 4a in the older vintage FAILS in the newer)
     DECAY(4b|d) = same for 4b
  plus BIRTH rates (fail -> pass), and the BINDING MARGIN: each leg's slack divided by that
  leg's cross-sectional sd over the grid on the newest panel, binding margin = min over legs.
  A flip is exactly "drift exceeded the binding margin", so the margin distribution plus the
  measured per-rung drift scale is what an extrapolation to an unobserved horizon can use.

RULE 8 (PROTOCOL 8), RUN ON EVERY VINTAGE
-----------------------------------------
  Parameters chosen on 2009-2016 IS only (argmax IS Sharpe over the 848-row grid), the
  2017-2026 half read once.  OOS CAGR/Sharpe/MaxDD of the pick are reported against the
  RULES v2 baseline and against SPY on every vintage and every horizon rung, and the
  PICK-FLIP rate (does the vintage change which book rule 8 selects?) is reported as a
  function of d -- the sharpest form of the queue's question, since the pick is the single
  decision the protocol actually makes.

PANEL (PROTOCOL 9 survivorship)
-------------------------------
  U56 -- research/universe.json via data/prices.csv, the ONLY panel with a daily git
  history (prices_broad.csv and the small panel are weekly/static, so they carry no
  vintage ladder at all; that is a limit of this run, stated, not hidden).  Current
  constituents only: every LEVEL here is biased upward.  The claims are about DIFFERENCES
  between vintages of the same panel, which survivorship biases far less than a level.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
--------------------------------------------------------------------
  G1  fast_backtest == engine.backtest @ 10 bps on the live panel        bar 1e-12
  G2  BAND(0.03, 0.75, W) weights == baseline.rules_v2_weights           bar 0.0 (exact)
  G3  idea 516's committed headline reproduces from its OWN keepflips.csv (read, not
      re-typed): 26 artefacts, 153,429 rows, 4a 3,366->3,368 / 20 flips, 4b 14,732->14,741
      / 11 flips, 13 artefacts with >=1 flip, rates 0.594% and 0.0747%
  G4  the git vintage inventory is exactly the 8 commits git reports for data/prices.csv,
      and the newest vintage is byte-identical to data/prices.csv on disk
  G5  weights(g) == g * weights(1.00) exactly, every family                bar 0.0
  G6  4a/4b verdict functions agree with baseline.compare's own 4a formula on the live book
  G7  TRUNCATION IDENTITY: weights(px[:T-k])  ==  weights(px)[:T-k]        bar 0.0 (exact)

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated at every grid point on every vintage and all points are
  reported.  Nothing is promoted on a flip-rate result: this run measures the DECAY of the
  record's verdicts, it does not propose a book.  The expected and correct outcome is an
  ANSWERED/KILL with a number and a stated horizon.
"""
import subprocess
import sys
import time
import warnings
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                       # PROTOCOL 2
BAND0, GROSS0, FREQ0 = 0.03, 0.75, "W"      # RULES v2 clauses 2/3 and cadence
MAXVOL = 0.60                     # RULES v1/v2 eligibility cap
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
EXCLUDE = {"BTC-USD", "ETH-USD"}

GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]     # idea 668's committed ladder
BANDS = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12]
NS = [3, 5, 8, 10, 12, 15, 20, 25, 30, 40]
FREQS = ["W", "M"]
TRUNCS = [1, 2, 3, 5, 10, 21, 42, 63, 126, 252]                 # P1, channel E (trading days)

# idea 516's COMMITTED headline, for G3 (re-derived from its own keepflips.csv, never re-typed
# as a result -- these are the target values the file must reproduce)
I516 = dict(artefacts=26, rows=153429, a_com=3366, a_new=3368, a_flip=20,
            b_com=14732, b_new=14741, b_flip=11, with_flip=13)
I516_FILE = ("2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-"
             "published-numbers_B.keepflips.csv")

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 1.  ENGINE  (vectorised equivalent of engine.backtest, asserted against it in G1)
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ0, cost=COST):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
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
    gross_r = (held * rets).sum(axis=1)
    return pd.Series(gross_r - turn * cost / 1e4, index=idx)


class Ctx:
    """Per-(panel, freq) precompute so the 8 gross rungs of a book cost O(T) each instead of
    a full T x N rebuild.  Asserted against the plain fast_backtest in G8 at every rung."""

    def __init__(self, prices, freq):
        idx = prices.index
        self.idx = idx
        self.rets = prices.pct_change().fillna(0.0).values
        m = rebalance_mask(idx, freq).values
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        T = len(idx)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), C[:-1]])

    def run(self, weights, grosses, cost=COST):
        wt = weights.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values
        W0, W0p = wt[self.s0], wt[self.s0p]
        h1 = W0 * (self.Cp / self.Cp[self.s0])
        hp1 = W0p * (self.Cp / self.Cp[self.s0p])
        hp1[self.reb[0]] = 0.0
        S, Sp = h1.sum(axis=1), hp1.sum(axis=1)
        Wsum, Wsump = W0.sum(axis=1), W0p.sum(axis=1)
        A = (h1 * self.rets).sum(axis=1)
        wt_reb, hp_reb = wt[self.reb], hp1[self.reb]
        Sp_reb, Wsump_reb = Sp[self.reb], Wsump[self.reb]
        out = {}
        for g in grosses:
            V = g * S + (1.0 - g * Wsum)
            Vp = g * Sp_reb + (1.0 - g * Wsump_reb)
            turn = np.zeros(len(self.idx))
            turn[self.reb] = np.abs(g * wt_reb - (g * hp_reb) / Vp[:, None]).sum(axis=1)
            out[g] = pd.Series(g * A / V - turn * cost / 1e4, index=self.idx)
        return out


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def cagr_dd(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    dd = (eq / eq.cummax() - 1).min()
    return (eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan), dd


def metric_block(r):
    """Full-sample + halves + OOS, the seven numbers 4a and 4b are decided on."""
    c, d = cagr_dd(r)
    h = len(r) // 2
    o = r.loc[OOS_START:]
    oc, od = cagr_dd(o) if len(o) > 20 else (np.nan, np.nan)
    i = r.loc[:IS_END]
    return dict(CAGR=c, Sharpe=sharpe(r), MaxDD=d, H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                IS_Sharpe=sharpe(i) if len(i) > 20 else np.nan,
                OOS_CAGR=oc, OOS_Sharpe=sharpe(o) if len(o) > 20 else np.nan, OOS_MaxDD=od)


# ================================================================================================
# 2.  THE CLAIM SET  (P2)
# ================================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def build_books(px):
    """Return {key: weights_at_gross_1.00}.  Gross is applied later by a scalar multiply
    (G5), so the expensive part -- the indicators -- is computed once per vintage."""
    sc_on, above, vol20 = score(px, vol_scale=True)
    sc_off, _, _ = score(px, vol_scale=False)
    ew1 = ew_gross(px, 1.0)
    W = {}
    for b in BANDS:
        W[("BAND", b, None, None)] = ew1.where(band_state(px, b) & px.notna(), 0.0)
    for n in NS:
        for vs, sc in (("VS", sc_on), ("NOVS", sc_off)):
            for cap, mv in (("CAP", MAXVOL), ("NOCAP", 9.99)):
                elig = sc.where(above & (vol20 < mv))
                sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
                k = sel.sum(axis=1).replace(0, np.nan)
                W[("CAND", n, vs, cap)] = sel.div(k, axis=0).fillna(0.0)
    for cap, mv in (("CAP", MAXVOL), ("NOCAP", 9.99)):
        e = (above & (vol20 < mv) & px.notna()).astype(float)
        W[("EWELIG", None, None, cap)] = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    spy = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    spy["SPY"] = 1.0
    W[("SPYBH", None, None, None)] = spy
    return W


def book_rows(W):
    """The 848 (family, params, gross, freq) rows -- the claim set, fixed across vintages."""
    rows = []
    for key, w in W.items():
        for g in GROSSES:
            for f in FREQS:
                rows.append((key, g, f, w))
    return rows


def family_of(key):
    fam = key[0]
    return "BAND" if fam == "BAND" else ("CAND" if fam == "CAND" else "FLAT")


def keystr(key, g, f):
    return f"{key[0]}|{key[1]}|{key[2]}|{key[3]}|g{g:.2f}|{f}"


# ================================================================================================
# 3.  VERDICTS  (PROTOCOL 4, exactly)
# ================================================================================================
def legs(m, base, old, spy):
    """Signed slack on every leg.  Positive == the leg passes.
    a*  : PROTOCOL 4a against the LIVE book (RULES v2), which is what 4a means today.
    v*  : the SAME 4a legs against RULES v1, the pre-2026-09-06 live book that
          baseline.compare still prints for continuity.  Not a third tuned parameter: it is
          the record's own second baseline, and it is reported because 4a-vs-v2 turns out to
          be EMPTY on this grid (see the console), which would leave the queue's headline
          statistic -- a rate whose denominator is '4a passes' -- undefined at source."""
    return dict(
        a1=m["H1"] - base["H1"], a2=m["H2"] - base["H2"],
        a3=m["MaxDD"] - base["MaxDD"],                       # >=0 means "no worse"
        v1=m["H1"] - old["H1"], v2=m["H2"] - old["H2"], v3=m["MaxDD"] - old["MaxDD"],
        b1=m["H1"] - spy["H1"], b2=m["H2"] - spy["H2"], b3=m["OOS_Sharpe"] - spy["OOS_Sharpe"],
        b4=0.60 * abs(spy["MaxDD"]) - abs(m["MaxDD"]),
        b5=m["CAGR"] - 0.70 * spy["CAGR"],
    )


A_LEGS, V_LEGS = ["a1", "a2", "a3"], ["v1", "v2", "v3"]
B_LEGS = ["b1", "b2", "b3", "b4", "b5"]
# comparator per leg, exactly as PROTOCOL 4 / baseline.compare word them: Sharpe legs are
# STRICT ("Sharpe > ..."), the two cap/floor legs are NON-STRICT ("no worse than", "<=", ">=").
STRICT = {"a1": True, "a2": True, "a3": False, "v1": True, "v2": True, "v3": False,
          "b1": True, "b2": True, "b3": True, "b4": False, "b5": False}


def _ok(L, keys):
    if any(np.isnan(L[k]) for k in keys):
        return False
    return all((L[k] > 0) if STRICT[k] else (L[k] >= 0) for k in keys)


def verdicts(L):
    return _ok(L, A_LEGS), _ok(L, V_LEGS), _ok(L, B_LEGS)


# ================================================================================================
# 4.  VINTAGES
# ================================================================================================
def git_vintages():
    out = subprocess.run(["git", "log", "--format=%H %ad", "--date=short", "--",
                          "data/prices.csv"], cwd=ROOT, capture_output=True, text=True).stdout
    v = []
    for ln in out.strip().split("\n"):
        h, d = ln.split()
        v.append((h, pd.Timestamp(d)))
    return v[::-1]                                           # oldest first


def read_vintage(h):
    raw = subprocess.run(["git", "show", f"{h}:data/prices.csv"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    px = pd.read_csv(StringIO(raw), index_col=0, parse_dates=True).sort_index()
    return px.dropna(how="all").ffill()


def prep(px, cols):
    px = px.reindex(columns=cols)
    return px.loc["2008-01-01":].dropna(how="all").ffill()


# ================================================================================================
# 5.  EVALUATE ONE PANEL  -> DataFrame of 848 rows
# ================================================================================================
def evaluate(px, tag):
    if len(px) <= WARM + 300:
        return None
    W = build_books(px)
    start = px.index[WARM]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    spy = metric_block(spy_r)
    ctx = {f: Ctx(px, f) for f in FREQS}
    base = metric_block(fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ0).loc[start:])
    old = metric_block(fast_backtest(px, rules_v1_weights(px), FREQ0).loc[start:])
    recs = []
    for key, w in W.items():
        for f in FREQS:
            rs = ctx[f].run(w, GROSSES)
            for g in GROSSES:
                m = metric_block(rs[g].loc[start:])
                L = legs(m, base, old, spy)
                p4a, p4v, p4b = verdicts(L)
                recs.append(dict(vintage=tag, row=keystr(key, g, f), family=family_of(key),
                                 gross=g, freq=f, pass4a=int(p4a), pass4a_v1=int(p4v),
                                 pass4b=int(p4b), **m, **L))
    df = pd.DataFrame(recs)
    for c, v in (("spy_Sharpe", spy["Sharpe"]), ("spy_CAGR", spy["CAGR"]),
                 ("spy_MaxDD", spy["MaxDD"]), ("spy_OOS_Sharpe", spy["OOS_Sharpe"]),
                 ("spy_OOS_CAGR", spy["OOS_CAGR"]), ("spy_OOS_MaxDD", spy["OOS_MaxDD"]),
                 ("base_Sharpe", base["Sharpe"]), ("base_OOS_Sharpe", base["OOS_Sharpe"]),
                 ("base_OOS_CAGR", base["OOS_CAGR"]), ("base_OOS_MaxDD", base["OOS_MaxDD"]),
                 ("n_rows_panel", len(px)), ("last", str(px.index[-1].date()))):
        df[c] = v
    return df


# ================================================================================================
# 6.  GATES
# ================================================================================================
def gates(px_live):
    P("=" * 96)
    P("PRE-REGISTERED GATES")
    P("=" * 96)
    ok = True

    w = rules_v2_weights(px_live, BAND0, GROSS0)
    a = fast_backtest(px_live, w, FREQ0)
    b = backtest(px_live, w, cost_bps=COST, freq=FREQ0)["returns"]
    d1 = float((a - b).abs().max())
    P(f"  G1  fast_backtest == engine.backtest        max|d| = {d1:.3e}   bar 1e-12   "
      f"{'PASS' if d1 < 1e-12 else 'FAIL'}")
    ok &= d1 < 1e-12

    W = build_books(px_live)
    d2 = float((GROSS0 * W[("BAND", BAND0, None, None)] - w).abs().max().max())
    P(f"  G2  BAND(0.03,0.75) == rules_v2_weights     max|d| = {d2:.3e}   bar 0.0     "
      f"{'PASS' if d2 == 0.0 else 'FAIL'}")
    ok &= d2 == 0.0

    kf = pd.read_csv(OUT / I516_FILE)
    got = dict(artefacts=len(kf), rows=int(kf.n_rows.sum()),
               a_com=int(kf.pass4a_com.sum()), a_new=int(kf.pass4a_new.sum()),
               a_flip=int(kf.flip4a.sum()), b_com=int(kf.pass4b_com.sum()),
               b_new=int(kf.pass4b_new.sum()), b_flip=int(kf.flip4b.sum()),
               with_flip=int(((kf.flip4a + kf.flip4b) > 0).sum()))
    g3 = got == I516
    P(f"  G3  idea 516 headline re-derived from its own keepflips.csv                  "
      f"{'PASS' if g3 else 'FAIL'}")
    P(f"        {got}")
    P(f"        idea 516's published rates: 4a {got['a_flip']/got['a_com']:.4%}  "
      f"4b {got['b_flip']/got['b_com']:.4%}   (queue quotes 0.59% / 0.07%)")
    ok &= g3

    V = git_vintages()
    disk = (ROOT / "data" / "prices.csv").read_text()
    newest = subprocess.run(["git", "show", f"{V[-1][0]}:data/prices.csv"], cwd=ROOT,
                            capture_output=True, text=True).stdout
    g4 = len(V) == 8 and disk == newest
    P(f"  G4  git vintage inventory                   n = {len(V)}   newest == data/prices.csv "
      f"on disk: {disk == newest}   {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    # G5 compares the scalar-multiply path this run USES against an INDEPENDENT construction
    # of the same book at that gross (baseline.rules_v2_weights' own gross argument, and
    # ew_gross' own g argument), so it is not a tautology.
    d5 = 0.0
    for g in GROSSES:
        d5 = max(d5, float((g * W[("BAND", BAND0, None, None)]
                            - rules_v2_weights(px_live, BAND0, g)).abs().max().max()))
        d5 = max(d5, float((g * ew_gross(px_live, 1.0) - ew_gross(px_live, g)).abs().max().max()))
    r_half = fast_backtest(px_live, 0.5 * W[("BAND", BAND0, None, None)], FREQ0)
    r_one = fast_backtest(px_live, 1.0 * W[("BAND", BAND0, None, None)], FREQ0)
    g5 = d5 == 0.0 and not r_half.equals(r_one)
    P(f"  G5  weights(g) == g*weights(1.00) exactly   max|d| = {d5:.3e}   bar 0.0     "
      f"{'PASS' if g5 else 'FAIL'}   (and the returns DO differ across g: "
      f"{not r_half.equals(r_one)})")
    ok &= g5

    # G6 runs BOTH verdict implementations over the WHOLE 848-row grid on the live panel and
    # demands exact agreement on every row -- baseline.compare's inline 4a formula, verbatim.
    live_eval = evaluate(px_live, "G6")
    theirs = ((live_eval.a1 > 0) & (live_eval.a2 > 0) & (live_eval.a3 >= 0)).astype(int)
    g6 = bool((theirs == live_eval.pass4a).all())
    P(f"  G6  4a verdict fn == baseline.compare's     agree on {int((theirs == live_eval.pass4a).sum())}"
      f"/{len(live_eval)} rows   {'PASS' if g6 else 'FAIL'}")
    P(f"        live grid: 4a(vs RULES v2) {int(live_eval.pass4a.sum())} passes, "
      f"4a(vs RULES v1) {int(live_eval.pass4a_v1.sum())}, "
      f"4b {int(live_eval.pass4b.sum())}, of {len(live_eval)} book-rows")
    ok &= g6

    k = 63
    trunc = px_live.iloc[:-k]
    Wt = build_books(trunc)
    d7 = max(float((Wt[kk] - W[kk].iloc[:-k]).abs().max().max()) for kk in Wt)
    P(f"  G7  TRUNCATION IDENTITY weights            max|d| = {d7:.3e}   bar 0.0     "
      f"{'PASS' if d7 == 0.0 else 'FAIL'}")
    ok &= d7 == 0.0

    d8 = 0.0
    cx = Ctx(px_live, FREQ0)
    rs = cx.run(W[("CAND", 20, "NOVS", "CAP")], GROSSES)
    for g in GROSSES:
        d8 = max(d8, float((rs[g] - fast_backtest(px_live, g * W[("CAND", 20, "NOVS", "CAP")],
                                                  FREQ0)).abs().max()))
    P(f"  G8  Ctx multi-gross == fast_backtest        max|d| = {d8:.3e}   bar 1e-12   "
      f"{'PASS' if d8 < 1e-12 else 'FAIL'}   (all {len(GROSSES)} rungs)")
    ok &= d8 < 1e-12

    P(f"\n  ALL GATES: {'PASS' if ok else 'FAIL'}")
    assert ok, "a pre-registered gate failed -- no number below may be read"
    return V, got


# ================================================================================================
# 7.  FLIP ACCOUNTING
# ================================================================================================
def pair_stats(old, new, d, channel, label, d_td=None):
    """old/new: 848-row frames on the SAME row keys.  Returns one dict per claim set.
    d    = calendar days between the two COMMITS (the queue's 'vintage distance').
    d_td = trading rows the newer panel has that the older does not.  Reported alongside d
           because the two are not the same: the record has two pairs of SAME-DAY commits
           whose panels differ by a trading day, so d=0 does not mean 'no new data'."""
    m = old.merge(new, on="row", suffixes=("_o", "_n"))
    assert len(m) == len(old) == len(new)
    if d_td is None:
        d_td = int(new.n_rows_panel.iloc[0] - old.n_rows_panel.iloc[0])
    out = []
    for cs in ["ALL", "BAND", "CAND", "FLAT"]:
        s = m if cs == "ALL" else m[m.family_o == cs]
        if not len(s):
            continue
        rec = dict(channel=channel, claim_set=cs, d=d, d_td=d_td, label=label, n=len(s))
        for tag in ("4a", "4a_v1", "4b"):
            o, n = s[f"pass{tag}_o"], s[f"pass{tag}_n"]
            rec[f"pass{tag}_o"] = int(o.sum())
            rec[f"pass{tag}_n"] = int(n.sum())
            rec[f"flip{tag}"] = int((o != n).sum())
            rec[f"decay{tag}"] = int(((o == 1) & (n == 0)).sum())
            rec[f"birth{tag}"] = int(((o == 0) & (n == 1)).sum())
            rec[f"decay{tag}_rate"] = rec[f"decay{tag}"] / o.sum() if o.sum() else np.nan
            rec[f"flip{tag}_rate"] = rec[f"flip{tag}"] / len(s)
        out.append(rec)
    return out


def margin_frame(df, sd):
    """Binding margin: each leg's slack / that leg's cross-sectional sd on the newest panel."""
    a = pd.concat([df[k] / sd[k] for k in V_LEGS], axis=1).min(axis=1)
    b = pd.concat([df[k] / sd[k] for k in B_LEGS], axis=1).min(axis=1)
    return a, b


# ================================================================================================
# 8.  MAIN
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 96)
    P("IDEA 683 -- is-the-0.59-percent-4a-FLIP-RATE-a-PER-DAY-constant        (lane C)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   panel U56 (data/prices.csv)   "
      f"cost {COST:.0f} bps   PROTOCOL 2/4/8/9")
    P("=" * 96)
    P()

    raw_live = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    cols = [c for c in raw_live.columns if c not in EXCLUDE]
    px_live = prep(raw_live, cols)
    V, i516 = gates(px_live)

    # ---------------- vintage inventory ----------------
    P()
    P("=" * 96)
    P("VINTAGE INVENTORY  (git log -- data/prices.csv, oldest first)")
    P("=" * 96)
    panels, inv = {}, []
    for h, dt in V:
        px = prep(read_vintage(h), cols)
        tag = f"{dt.date()}_{h[:7]}"
        panels[tag] = px
        inv.append(dict(vintage=tag, commit=h[:7], commit_date=str(dt.date()), rows=len(px),
                        last=str(px.index[-1].date()), cols=px.shape[1]))
    inv = pd.DataFrame(inv)
    newest_tag = inv.vintage.iloc[-1]
    ref_dt = pd.Timestamp(inv.commit_date.iloc[-1])
    inv["d_days"] = [(ref_dt - pd.Timestamp(x)).days for x in inv.commit_date]
    # the 2026-09-04 index-convention fix (commit c006b43) is a CODE break, not price drift
    inv["index_convention"] = np.where(inv.rows > 5000, "CALENDAR(pre-fix)", "EQUITY")
    P(inv.to_string(index=False))
    dump(inv, "vintages")
    P()
    P("  NOTE: the two 2026-09-03 vintages carry the PRE-FIX CALENDAR-DAY index (6,060/6,059")
    P("  raw rows vs 4,698 after commit c006b43 aligned crypto to equity days on 2026-09-04).")
    P("  Every pair that crosses that commit is tagged INDEX-BREAK and reported separately;")
    P("  it is channel X (code), not channel R (price drift).")

    # cell-level drift, newest as reference
    P()
    P("  CELL-LEVEL DRIFT vs the newest vintage (common index, common columns):")
    base_px = panels[newest_tag]
    drift = []
    for tag, px in panels.items():
        idx = px.index.intersection(base_px.index)
        x, y = px.loc[idx, cols], base_px.loc[idx, cols]
        both = x.notna() & y.notna()
        rel = ((x - y).abs() / y.abs().clip(lower=1e-9))[both]
        ncell = int(both.sum().sum())
        drift.append(dict(vintage=tag,
                          d_days=int(inv.set_index("vintage").d_days[tag]),
                          common_rows=len(idx), cells=ncell,
                          changed=int((rel > 1e-9).sum().sum()),
                          share_changed=float((rel > 1e-9).sum().sum()) / ncell,
                          median_rel=float(np.nanmedian(rel.values[rel.values > 1e-9]))
                          if (rel > 1e-9).any().any() else 0.0,
                          max_rel=float(np.nanmax(rel.values)) if ncell else 0.0))
    drift = pd.DataFrame(drift)
    P(drift.to_string(index=False, float_format=lambda x: f"{x:.6g}"))
    dump(drift, "drift")

    # ---------------- channel B / R : real vintages ----------------
    P()
    P("=" * 96)
    P("EVALUATING THE CLAIM SET ON EVERY VINTAGE")
    P("=" * 96)
    ev_own = {}
    for tag, px in panels.items():
        t = time.time()
        ev_own[tag] = evaluate(px, tag)
        P(f"  {tag}  rows={len(px):5d}  last={px.index[-1].date()}  "
          f"books={len(ev_own[tag])}  4a/v2={int(ev_own[tag].pass4a.sum()):4d}  "
          f"4a/v1={int(ev_own[tag].pass4a_v1.sum()):4d}  "
          f"4b={int(ev_own[tag].pass4b.sum()):4d}   ({time.time()-t:.1f}s)")
    grid = pd.concat(ev_own.values(), ignore_index=True)
    dump(grid, "grid")

    # common-index (pure restatement) evaluation, each pair against the newest
    P()
    P("  channel R (common index, pure restatement) -- each vintage vs the newest on their")
    P("  shared date index, so the SAMPLE is identical and only the VALUES moved:")
    ev_com = {}
    for tag, px in panels.items():
        idx = px.index.intersection(base_px.index)
        ev_com[tag] = (evaluate(px.loc[idx], tag + "|R"),
                       evaluate(base_px.loc[idx], newest_tag + "|R:" + tag))
        P(f"    {tag}  common rows={len(idx)}")

    # ---------------- channel E : truncation ladder ----------------
    P()
    P("  channel E (truncation of the newest panel) -- pure sample EXTENSION, the only")
    P("  channel that reaches past the 7 calendar days git actually holds:")
    ev_tr = {}
    for k in TRUNCS:
        t = time.time()
        ev_tr[k] = evaluate(base_px.iloc[:-k], f"TRUNC-{k}")
        P(f"    k={k:4d} trading days  rows={len(base_px)-k}  "
          f"last={base_px.index[-k-1].date()}  4a/v2={int(ev_tr[k].pass4a.sum()):4d}  "
          f"4a/v1={int(ev_tr[k].pass4a_v1.sum()):4d}  "
          f"4b={int(ev_tr[k].pass4b.sum()):4d}   ({time.time()-t:.1f}s)")
    full = ev_own[newest_tag]

    # ---------------- flip accounting ----------------
    P()
    P("=" * 96)
    P("P1 x P2 GRID -- FLIP AND DECAY RATES AT EVERY HORIZON RUNG, EVERY CLAIM SET")
    P("=" * 96)
    rows = []
    tags = list(panels)
    dd = inv.set_index("vintage").d_days.to_dict()
    conv = inv.set_index("vintage").index_convention.to_dict()
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            o, n = tags[i], tags[j]
            d = dd[o] - dd[n]
            brk = "INDEX-BREAK" if conv[o] != conv[n] else "clean"
            rows += [dict(r, pair=f"{o}->{n}", note=brk)
                     for r in pair_stats(ev_own[o], ev_own[n], d, "B", brk)]
    for tag in tags:
        if tag == newest_tag:
            continue
        a, b = ev_com[tag]
        d = dd[tag]
        brk = "INDEX-BREAK" if conv[tag] != conv[newest_tag] else "clean"
        rows += [dict(r, pair=f"{tag}->{newest_tag}", note=brk)
                 for r in pair_stats(a, b, d, "R", brk)]
    for k in TRUNCS:
        d = int(round(k * 365 / 252))
        rows += [dict(r, pair=f"TRUNC-{k}->full", note=f"k={k}td")
                 for r in pair_stats(ev_tr[k], full, d, "E", f"k={k}td", d_td=k)]
    flips = pd.DataFrame(rows)
    dump(flips, "flips")

    for ch, name in (("B", "AS PUBLISHED (R+E+X)"), ("R", "RESTATEMENT only"),
                     ("E", "EXTENSION only")):
        P()
        P(f"  --- channel {ch}: {name} ---")
        s = flips[(flips.channel == ch) & (flips.claim_set == "ALL")]
        if ch == "B":
            s = s[s.note == "clean"]
            P("      (INDEX-BREAK pairs excluded here, reported separately below)")
        agg = s.groupby("d").agg(
            pairs=("n", "size"), n=("n", "sum"), d_td=("d_td", "max"),
            pass4a_o=("pass4a_o", "sum"), flip4a=("flip4a", "sum"),
            pass4av1_o=("pass4a_v1_o", "sum"), decay4av1=("decay4a_v1", "sum"),
            birth4av1=("birth4a_v1", "sum"), flip4av1=("flip4a_v1", "sum"),
            pass4b_o=("pass4b_o", "sum"), decay4b=("decay4b", "sum"),
            birth4b=("birth4b", "sum"), flip4b=("flip4b", "sum")).reset_index()
        agg["decay4av1_rate"] = agg.decay4av1 / agg.pass4av1_o
        agg["decay4b_rate"] = agg.decay4b / agg.pass4b_o
        agg["flip4av1_rate"] = agg.flip4av1 / agg.n
        agg["flip4b_rate"] = agg.flip4b / agg.n
        P(agg.to_string(index=False, float_format=lambda x: f"{x:.5f}"))

    P()
    P("  --- INDEX-BREAK pairs (channel X: the 2026-09-04 calendar->equity index fix) ---")
    s = flips[(flips.channel == "B") & (flips.claim_set == "ALL") & (flips.note == "INDEX-BREAK")]
    if len(s):
        P(s[["pair", "d", "n", "pass4a_v1_o", "pass4a_v1_n", "flip4a_v1", "pass4b_o",
             "pass4b_n", "flip4b", "flip4a_v1_rate", "flip4b_rate"]].to_string(
                 index=False, float_format=lambda x: f"{x:.5f}"))

    P()
    P("  --- P2 (claim set) x P1 (horizon), channel E ---")
    P("  decay4b_rate:")
    P(flips[flips.channel == "E"].pivot_table(index="d", columns="claim_set",
                                              values="decay4b_rate").to_string(
        float_format=lambda x: f"{x:.5f}"))
    P("  decay4a_v1_rate:")
    P(flips[flips.channel == "E"].pivot_table(index="d", columns="claim_set",
                                              values="decay4a_v1_rate").to_string(
        float_format=lambda x: f"{x:.5f}"))
    P()
    P("  --- P2 (claim set) x P1 (horizon), channel R ---")
    P("  decay4b_rate:")
    P(flips[flips.channel == "R"].pivot_table(index="d", columns="claim_set",
                                              values="decay4b_rate").to_string(
        float_format=lambda x: f"{x:.5f}"))
    P("  decay4a_v1_rate:")
    P(flips[flips.channel == "R"].pivot_table(index="d", columns="claim_set",
                                              values="decay4a_v1_rate").to_string(
        float_format=lambda x: f"{x:.5f}"))

    # ---------------- binding margins ----------------
    P()
    P("=" * 96)
    P("BINDING MARGINS  (leg slack / that leg's cross-sectional sd on the newest panel)")
    P("=" * 96)
    sd = {k: float(full[k].std()) for k in A_LEGS + V_LEGS + B_LEGS}
    P("  leg sd on the newest panel: " + "  ".join(f"{k}={v:.4f}" for k, v in sd.items()))
    ma, mb = margin_frame(full, sd)
    full_m = full.assign(margin4a_v1=ma, margin4b=mb)
    pa, pb = full_m[full_m.pass4a_v1 == 1], full_m[full_m.pass4b == 1]
    P(f"  4a(v1) passers on the newest panel: n={len(pa)}   median binding margin "
      f"{pa.margin4a_v1.median():.4f}   q10 {pa.margin4a_v1.quantile(.10):.4f}")
    P(f"  4b     passers on the newest panel: n={len(pb)}   median binding margin "
      f"{pb.margin4b.median():.4f}   q10 {pb.margin4b.quantile(.10):.4f}")
    P("  WHICH LEG BINDS on the newest panel's 4b passers:")
    bind = pd.concat([pb[k] / sd[k] for k in B_LEGS], axis=1)
    bind.columns = B_LEGS
    P("    " + bind.idxmin(axis=1).value_counts().to_string().replace("\n", "\n    "))

    P()
    P("  margin DRIFT scale by horizon (median |delta binding margin| over rows passing in")
    P("  the older panel) -- a flip is exactly 'drift exceeded the margin':")
    mrows = []
    for ch, pairs in (("R", [(ev_com[t][0], ev_com[t][1], dd[t], t) for t in tags
                             if t != newest_tag]),
                      ("E", [(ev_tr[k], full, int(round(k * 365 / 252)), f"k={k}") for k in TRUNCS])):
        for o, n, d, lab in pairs:
            oa, ob = margin_frame(o, sd)
            na, nb = margin_frame(n, sd)
            o2 = o.assign(ma=oa.values, mb=ob.values)
            n2 = n.assign(ma=na.values, mb=nb.values)
            mm = o2[["row", "ma", "mb", "pass4a_v1", "pass4b"]].merge(
                n2[["row", "ma", "mb"]], on="row", suffixes=("_o", "_n"))
            da = (mm.ma_n - mm.ma_o).abs()
            db = (mm.mb_n - mm.mb_o).abs()
            mrows.append(dict(channel=ch, label=lab, d=d,
                              drift4av1_med=float(da[mm.pass4a_v1 == 1].median()),
                              drift4b_med=float(db[mm.pass4b == 1].median()),
                              drift4av1_p90=float(da[mm.pass4a_v1 == 1].quantile(.90)),
                              drift4b_p90=float(db[mm.pass4b == 1].quantile(.90))))
    mdf = pd.DataFrame(mrows)
    P(mdf.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    dump(mdf, "margins")

    # ---------------- the horizon the queue asks for ----------------
    P()
    P("=" * 96)
    P("THE HORIZON:  at what d is a committed 4b pass more likely than not to have MOVED?")
    P("=" * 96)
    for tag in ("4b", "4a_v1"):
        P(f"  --- verdict {tag} ---")
        for ch in ("E", "R", "B"):
            s = flips[(flips.channel == ch) & (flips.claim_set == "ALL")]
            if ch == "B":
                s = s[s.note == "clean"]
            if not len(s):
                continue
            agg = s.groupby("d").agg(dec=(f"decay{tag}", "sum"),
                                     tot=(f"pass{tag}_o", "sum")).reset_index()
            agg["rate"] = agg.dec / agg.tot
            hit = agg[agg.rate >= 0.5]
            cross = int(hit.d.iloc[0]) if len(hit) else None
            P(f"    channel {ch}: max observed decay rate {agg.rate.max():.4f} at "
              f"d={int(agg.d[agg.rate.idxmax()])}   crosses 0.50 at "
              f"d={cross if cross is not None else 'NEVER within the ladder'}")
            pos = agg[(agg.rate > 0) & (agg.d > 0)]
            if len(pos) >= 3 and cross is None:
                sl, ic = np.polyfit(np.log(pos.d.astype(float)), np.log(pos.rate), 1)
                dstar = float(np.exp((np.log(0.5) - ic) / sl)) if sl > 0 else np.nan
                P(f"        log-log fit rate ~ {np.exp(ic):.3e} * d^{sl:.3f} "
                  f"(n={len(pos)} rungs)  ->  rate=0.50 at d = {dstar:,.0f} calendar days "
                  f"({dstar/365:.1f} years).  EXTRAPOLATION beyond the ladder, stated as such.")
    P()
    P("  WHY A SYMMETRIC-DRIFT MODEL CANNOT REACH 0.50: restatement moves a margin without")
    P("  direction, so P(flip|pass) = P(drift < -margin) -> 0.50 only as the drift scale ->")
    P("  infinity and never exceeds it.  Only the EXTENSION channel, which changes the sample")
    P("  the verdict is about, can carry a decay rate past 0.50.  That is the substantive")
    P("  answer to the queue's framing, and it is reported, not asserted: see channel R's")
    P("  measured asymptote above.")

    # ---------------- rule 8 ----------------
    P()
    P("=" * 96)
    P("RULE 8 (PROTOCOL 8) -- IS 2009-2016 argmax Sharpe, OOS 2017-2026 read once")
    P("=" * 96)
    r8 = []
    for tag, df in list(ev_own.items()) + [(f"TRUNC-{k}", ev_tr[k]) for k in TRUNCS]:
        w = df.loc[df.IS_Sharpe.idxmax()]
        r8.append(dict(vintage=tag, pick=w.row, IS_Sharpe=w.IS_Sharpe,
                       OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe, OOS_MaxDD=w.OOS_MaxDD,
                       base_OOS_CAGR=w.base_OOS_CAGR, base_OOS_Sharpe=w.base_OOS_Sharpe,
                       base_OOS_MaxDD=w.base_OOS_MaxDD,
                       spy_OOS_CAGR=w.spy_OOS_CAGR, spy_OOS_Sharpe=w.spy_OOS_Sharpe,
                       spy_OOS_MaxDD=w.spy_OOS_MaxDD,
                       pass4a=int(w.pass4a), pass4a_v1=int(w.pass4a_v1), pass4b=int(w.pass4b)))
    r8 = pd.DataFrame(r8)
    P(r8.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(r8, "walkforward")
    P()
    P(f"  PICK-FLIP: {r8.pick.nunique()} distinct picks over {len(r8)} vintages/rungs.")
    for ch, sub in (("real git vintages", r8[~r8.vintage.str.startswith("TRUNC")]),
                    ("truncation ladder", r8[r8.vintage.str.startswith("TRUNC")])):
        P(f"    {ch}: {sub.pick.nunique()} distinct of {len(sub)}  "
          f"-> pick-flip share {1 - (sub.pick == sub.pick.mode().iloc[0]).mean():.4f}")
    ref = r8[r8.vintage == newest_tag].iloc[0]
    P(f"  reference (newest vintage) pick: {ref.pick}")
    P(f"    OOS  CAGR {ref.OOS_CAGR:.2%}  Sharpe {ref.OOS_Sharpe:.3f}  MaxDD {ref.OOS_MaxDD:.2%}")
    P(f"    RULES v2 baseline OOS  CAGR {ref.base_OOS_CAGR:.2%}  Sharpe {ref.base_OOS_Sharpe:.3f}"
      f"  MaxDD {ref.base_OOS_MaxDD:.2%}")
    P(f"    SPY OOS                CAGR {ref.spy_OOS_CAGR:.2%}  Sharpe {ref.spy_OOS_Sharpe:.3f}"
      f"  MaxDD {ref.spy_OOS_MaxDD:.2%}")
    P(f"    4a(vs RULES v2) {bool(ref.pass4a)}   4a(vs RULES v1) {bool(ref.pass4a_v1)}   "
      f"4b {bool(ref.pass4b)}")

    # ---------------- calibration against idea 516 ----------------
    P()
    P("=" * 96)
    P("CALIBRATION AGAINST IDEA 516's PUBLISHED TWO-DAY NUMBER")
    P("=" * 96)
    s = flips[(flips.channel == "B") & (flips.claim_set == "ALL") & (flips.d == 2)
              & (flips.note == "clean")]
    if len(s):
        def rate(num, den):
            return num / den if den else np.nan
        a = rate(s.flip4a_v1.sum(), s.pass4a_v1_o.sum())
        b = rate(s.flip4b.sum(), s.pass4b_o.sum())
        P(f"  this run, d=2 calendar days, as-published, {int(s.n.sum())} book-row comparisons:")
        P(f"    4a(v2) passes in the whole claim set = {int(s.pass4a_o.sum())}  "
          f"-> the queue's denominator is EMPTY at source on this grid")
        P(f"    4a(v1) flips / passes = {int(s.flip4a_v1.sum())} / {int(s.pass4a_v1_o.sum())} "
          f"= {a:.4%}      idea 516 published {i516['a_flip']/i516['a_com']:.4%}")
        P(f"    4b     flips / passes = {int(s.flip4b.sum())} / {int(s.pass4b_o.sum())} "
          f"= {b:.4%}      idea 516 published {i516['b_flip']/i516['b_com']:.4%}")
        P("  516's population is committed ARTEFACT TABLES re-executed (a column-name proxy,")
        P("  its own stated upper bound); this run's is a fixed book grid re-adjudicated at")
        P("  source.  The two are not the same estimand and are not expected to agree to the")
        P("  digit; the comparison is published so a reader can see the gap.")

    P()
    P(f"done in {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
