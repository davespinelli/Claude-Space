#!/usr/bin/env python3
"""Idea 579 (lane C, 2026-09-09) - does-the-DRAWDOWN-a-vol-cap-BUYS-ever-clear-the-4b-DD-LEG-on-its-own.

QUESTION
--------
Idea 314 found that a vol cap CUTS MaxDD in 41 of 48 capped books (median +2.08 pp, best
+8.53) while 47 of 48 LOSE Sharpe and 48 of 48 LOSE CAGR.  Ideas 527/530/531 found DD is the
most-cited SOLE cut in PROTOCOL 4b.  Idea 311's committed grid makes the population exact: at
gross 0.75, of its 36 pre-registered books (6 forms x 3 panels x 2 cadences), **16 fail 4b on
the DD leg ALONE** (8 on U56, 8 on B136) and 3 already pass.  Those 16 are books whose edge
legs (H1, H2, OOS Sharpe vs SPY) and CAGR floor ALL clear and which are held out of 4b by
drawdown and nothing else.

So ask the queue's question directly and at its sharpest: is there any DD-BUYING CLAUSE whose
CAGR cost is small enough that the CLAUSED PAIR clears 4b where the unclaused parent fails?
If none, the 4b DD leg cannot be BOUGHT and must be read as a constraint on the BOOK FORM.

The test has a null that the record has not previously priced the clauses against: plain
STATIC DE-GROSS (hold k of the book, rest in cash at 0%).  Cash buys drawdown mechanically -
MaxDD and CAGR both scale ~linearly in k - so a signal-based clause is only worth anything if
it buys the SAME drawdown for LESS CAGR.  Every clause cell is therefore also priced at
MATCHED MaxDD against its own parent's dense cash ladder (edge = CAGR_clause - CAGR_cash at
the clause's own MaxDD).  A positive edge is a real DD purchase; a negative edge means the
clause is a worse way to hold cash.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the CLAUSE FAMILY and its DIAL.  The parent
book form, the panel and the cadence are REPORTED axes, not tuned: the parents are idea 311's
pre-registered six-form menu at its committed gross 0.75, taken as given.  Every grid point of
every axis is written to .grid.csv.

THE CLAUSE MENU (6 families, 47 dial points; all overlays - they can only REMOVE risk)
  CASH(k)      hold k of the parent, rest in cash at 0%.  k = 0.05 .. 1.00 by 0.05 (20 pts).
               THE NULL: the mechanical price of drawdown.
  VOLCAP(c)    drop names whose trailing 60d annualised vol exceeds c; dropped weight goes to
               CASH, never re-spread.  c in {0.20,0.25,0.30,0.40,0.50,0.60}.  Idea 314's clause.
  VT(t)        scale the parent's gross by min(1, t / realised 60d vol of the parent's own
               traded returns, lagged 1d).  Scales DOWN only.  t in {0.06,...,0.20} (6 pts).
  MKT(w)       hold the parent only while SPY > its own w-day MA, else cash.  w in {50,...,250}.
  DDSTOP(d)    hold cash while the parent's own realised drawdown (lagged 1d) is worse than
               -d, re-enter when it recovers past -d/2 (hysteresis).  d in {0.05,...,0.30}.
  BREADTH(b)   hold the parent only while the panel's fraction of priced names above their own
               200d MA is >= b, else cash.  b in {0.30,...,0.70}.

PRE-REGISTERED HYPOTHESES (written before any clause was run)
-------------------------------------------------------------
H_MAIN   : NO (parent, clause, dial) cell clears all five 4b legs where the unclaused parent
           fails 4b.  A single passer refutes it and is a KEEP-candidate.
H_DDONLY : among the 16 parents that fail 4b on the DD leg ALONE, no clause cell repairs the
           DD leg without breaking a Sharpe leg or the CAGR floor.  This is the strongest
           form of the queue's question: these books need ONLY drawdown.
H_CASH   : no clause family has a positive MEDIAN matched-DD edge, i.e. no signal buys
           drawdown more cheaply than plain cash.  (If one does, the DD leg is buyable in
           principle even if no cell clears 4b.)
H_MONO   : DD gain is monotone in each family's own INTENSITY dial in >= 90% of adjacent dial
           pairs - these clauses are DIALS, not signals, so their drawdown purchase should be
           ordered by the dial and not by what the dial selects.  Scored over the five
           intensity families only; MKT's dial is a LOOKBACK WINDOW, not an intensity, so it
           carries no a-priori ordering and is reported but excluded from the bar.
H_OOS    : (rule 8) neither walk-forward selector's IS-chosen pair clears 4b out of sample.

RULE 8 (walk-forward, required, run regardless of verdict): the clause family and dial are
chosen on 2010/2011-2016 ONLY and 2017-2026 is then read ONCE.
  WF-A  the overfitter's pick: max IS Sharpe over every cell in the menu.
  WF-B  the DD-buyer's pick: among cells clearing all five IS-restated 4b legs, the one with
        the largest IS matched-DD edge.
Both report OOS CAGR/Sharpe/MaxDD against the RULES v2 baseline run on the SAME panel and
against SPY, plus the OOS-restated 4b legs.

Costs 10 bps per unit turnover, weights decided at close t and applied t+1 (engine convention),
no shorting, no leverage (every clause scales gross DOWN only; parents are at gross 0.75).
Both KEEP paths are evaluated on every cell: 4a vs RULES v2 on the same panel, 4b vs SPY.

SURVIVORSHIP: B136 (research/universe_broad.json) and the small panel are CURRENT constituents
only, so every level on those two panels is biased UP relative to what was investable in 2010.
Small-panel names with max_1d_move >= 1.0 in data/small_meta.csv are dropped first, per the
record's convention, leaving 439.

GATES (all must pass, or their deviation is reported, before any finding is read)
---------------------------------------------------------------------------------
G1  the numpy runner == engine.backtest on a CLAUSED book, on all three panels, returns AND
    turnover, bar 1e-12.
G2  idea 311's 36 committed g=0.75 rows (3 panels x 6 forms x 2 cadences, 6 metric columns
    each) reproduce.  Bar 1e-9 on B136 and SMALL439 (static committed caches).  U56 is read
    through data/prices.csv, which the price job refreshes daily and which idea 312/311
    documented as revised (<= 5.1e-5 relative); its bar is therefore 5e-3 ABSOLUTE and the
    measured deviation is reported, not hidden.
G3  NULL-DIAL IDENTITY: every clause at its no-op dial reproduces its parent's return path
    exactly (bar 1e-15), i.e. the clause plumbing is a pure overlay and cannot move a book
    on its own.
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
MA_WIN = 200
VOL_WIN = 60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"          # idea 311's PARENT_END, so G2 is comparable
CADENCES = ["W", "M"]
GFIX = 0.75                        # idea 311's committed gross for the parent menu
WARM = 260                         # warm-up rows skipped before ANY metric (record convention)
PARENT = "2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.grid.csv"
G1_TOL = 1e-12
G2_TOL = {"B136": 1e-9, "SMALL439": 1e-9, "U56": 5e-3}
G3_TOL = 1e-15
MONO_BAR = 0.90                    # H_MONO

FORMS = ["EWall", "MA-RS", "MA-DG", "TOP20", "TOP10", "MA20"]
CASH_GRID = [round(0.05 * i, 2) for i in range(1, 21)]          # 0.05 .. 1.00
VOLCAP_GRID = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60]
VT_GRID = [0.06, 0.08, 0.10, 0.12, 0.15, 0.20]
MKT_GRID = [50, 100, 150, 200, 250]
DDSTOP_GRID = [0.05, 0.10, 0.15, 0.20, 0.30]
BREADTH_GRID = [0.30, 0.40, 0.50, 0.60, 0.70]
FAMILIES = ["CASH", "VOLCAP", "VT", "MKT", "DDSTOP", "BREADTH"]
GRIDS = {"CASH": CASH_GRID, "VOLCAP": VOLCAP_GRID, "VT": VT_GRID,
         "MKT": MKT_GRID, "DDSTOP": DDSTOP_GRID, "BREADTH": BREADTH_GRID}
# H_MONO: +1 if a HIGHER dial should give a BETTER (less negative) MaxDD, -1 if worse.
# MKT is None: its dial is a lookback window, not an intensity - reported, excluded from the bar.
MONO_SIGN = {"CASH": -1.0, "VOLCAP": -1.0, "VT": -1.0, "DDSTOP": -1.0, "BREADTH": +1.0,
             "MKT": None}

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1).  Idea 311/312/575's runner."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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


class Cadence:
    """Everything in fast_backtest that depends only on (prices, freq), precomputed once.

    Lets a menu of books on the same panel be run with 4 array ops each instead of 10, which
    is what makes 1,700+ clause cells affordable.  Asserted identical to engine.backtest in G1.
    """

    def __init__(self, prices, freq):
        idx = prices.index
        self.idx = idx
        self.rets = prices.pct_change().fillna(0.0).values
        mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
        mask[0] = True
        T, N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        Cp = np.vstack([np.ones((1, N)), C[:-1]])
        self.reb = np.flatnonzero(mask)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.D = Cp / Cp[self.s0]
        self.Dp = Cp / Cp[self.s0p]

    def run(self, w, cost_bps=COST):
        """w is the UNSHIFTED weight array (decided at close t); the shift is applied here."""
        wt = np.empty_like(w)
        wt[0] = 0.0
        wt[1:] = w[:-1]
        W0 = wt[self.s0]
        h = W0 * self.D
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.Dp
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(len(wt))
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        port = (held * self.rets).sum(axis=1) - turn * cost_bps / 1e4
        return pd.Series(port, index=self.idx), pd.Series(turn, index=self.idx)


# ------------------------------------------------------------------------- helpers
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def legs_4b(r, spy, sub=False):
    """The five PROTOCOL 4b legs as booleans (idea 311's function, verbatim).

    sub=False: full sample; H1/H2 are its halves, the third Sharpe leg is post-2017 Sharpe.
    sub=True:  r and spy are already ONE window; the third leg is that window's own Sharpe.
    """
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    sh_r = m["Sharpe"] if sub else metrics(r.loc[OOS_START:])["Sharpe"]
    sh_s = ms["Sharpe"] if sub else metrics(spy.loc[OOS_START:])["Sharpe"]
    return dict(H1=bool(a1 > s1), H2=bool(a2 > s2), OOS=bool(sh_r > sh_s),
                DD=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_str(lg):
    f = [k for k, v in lg.items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels
def small_tradables(pxs):
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return [c for c in pxs.columns if c != "SPY" and c not in bad]


def real_panels():
    """Idea 311's three panels, built exactly as it built them (so G2 is a real gate)."""
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    s_stk = small_tradables(pxs)
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


# ------------------------------------------------------- the PARENT book-form menu
def form_weights(name, px, tradable, g, sc=None):
    """Idea 311's PRE-REGISTERED menu of unlevered book-forms, verbatim (see G2).

    EWall   every priced tradable name, equal weight, gross g            (NO-EDGE CONTROL)
    MA-RS   200d gate, re-spread over survivors at gross g               (gate, gross held)
    MA-DG   200d gate, de-grossed: gated-out weight goes to CASH         (gate, gross floats)
    TOP20   top 20 by RULES' composite score, equal weight, gross g      (ranked)
    TOP10   top 10 by the same score                                     (ranked, concentrated)
    MA20    200d gate INTERSECT top 20 by score, re-spread at gross g    (gate + ranked)
    """
    e = _priced(px, tradable) > 0
    if name == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if name == "MA-RS":
        return _ew(ma, g)
    if name == "MA-DG":
        n = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(n, axis=0).fillna(0.0)
    s = (score(px, vol_scale=False)[0] if sc is None else sc).where(e)
    if name in ("TOP20", "TOP10"):
        k = 20 if name == "TOP20" else 10
        return _ew(s.rank(axis=1, ascending=False) <= k, g)
    if name == "MA20":
        return _ew(s.where(ma).rank(axis=1, ascending=False) <= 20, g)
    raise ValueError(name)


# ------------------------------------------------------------------ the CLAUSE menu
def dd_path(r):
    """Realised drawdown of a return path, LAGGED one day (causal at the decision close)."""
    eq = (1.0 + r).cumprod()
    return (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)


def hyst_gate(dd, d):
    """DDSTOP state: OUT once dd < -d, back IN once dd > -d/2; IN before either fires."""
    raw = pd.Series(np.nan, index=dd.index)
    raw = raw.mask(dd < -d, 0.0).mask(dd > -d / 2.0, 1.0)
    return raw.ffill().fillna(1.0).values


def clause_scale(fam, dial, ctx, parent_ret):
    """Return (row_scale, col_mask) for a clause.  row_scale is a T-vector in [0,1]; col_mask
    is a T x N 0/1 array or None.  Every clause only ever REMOVES weight (gross scales DOWN).

    dial=None is the NULL DIAL: the clause becomes the identity overlay (gate G3)."""
    T = ctx["T"]
    one = np.ones(T)
    if fam == "CASH":
        return (one if dial is None else one * float(dial)), None
    if fam == "VOLCAP":
        return one, (None if dial is None else (ctx["vol"] <= float(dial)))
    if fam == "VT":
        if dial is None:
            return one, None
        rv = (parent_ret.rolling(VOL_WIN).std() * np.sqrt(252)).shift(1)
        sc = (float(dial) / rv.clip(lower=1e-6)).clip(upper=1.0).fillna(1.0).values
        return sc, None
    if fam == "MKT":
        return (one if dial is None else ctx["mkt"][int(dial)]), None
    if fam == "DDSTOP":
        return (one if dial is None else hyst_gate(dd_path(parent_ret), float(dial))), None
    if fam == "BREADTH":
        return (one if dial is None else (ctx["breadth"] >= float(dial)).astype(float)), None
    raise ValueError(fam)


def apply_clause(w, fam, dial, ctx, parent_ret):
    rs, cm = clause_scale(fam, dial, ctx, parent_ret)
    out = w if cm is None else w * cm
    return out * rs[:, None]


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 579  does-the-DRAWDOWN-a-vol-cap-BUYS-ever-clear-the-4b-DD-LEG-on-its-own  (lane C, 2026-09-09)")
    P("=" * 118)
    P("Idea 311's 36 committed g=0.75 books: 16 fail PROTOCOL 4b on the DD leg ALONE, 3 pass.")
    P("Ask whether ANY DD-buying clause repairs the DD leg cheaply enough that the PAIR clears 4b.")
    P("Tuned: CLAUSE FAMILY x DIAL (2 params).  Parent form, panel and cadence are reported axes.")
    P("Every clause cell is ALSO priced at MATCHED MaxDD against its own parent's dense CASH ladder:")
    P("a signal clause is only worth anything if it buys the same drawdown for less CAGR than cash.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only - levels there are biased UP.")
    P("")

    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    order = ["U56", "B136", SMALLK]
    par = pd.read_csv(OUT / PARENT)
    par = par[par.gross == GFIX]

    ref, cad_ctx, panel_ctx = {}, {}, {}
    for nm in order:
        px, tr = panels[nm]
        st = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[st:]
        ref[nm] = dict(start=st, spy=spy, v2=v2)
        sc = score(px, vol_scale=False)[0]
        e = _priced(px, tr) > 0
        ma = above_ma(px) & e
        breadth = (ma.sum(axis=1) / e.sum(axis=1).replace(0, np.nan)).fillna(0.0).values
        vol = (px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)).reindex(
            columns=px.columns).fillna(np.inf).values
        spy_px = px["SPY"]
        mkt = {w: (spy_px > spy_px.rolling(w).mean()).astype(float).values for w in MKT_GRID}
        panel_ctx[nm] = dict(px=px, tr=tr, sc=sc, T=len(px), vol=vol, breadth=breadth, mkt=mkt)
        for c in CADENCES:
            cad_ctx[(nm, c)] = Cadence(px, c)
        P(f"panel {nm:<9}: {len(tr):>3} tradable, {px.shape[1]:>3} cols, "
          f"{px.index[0].date()} .. {px.index[-1].date()}, {len(px)} rows, metrics from {st.date()}")
    P("")

    # -------------------------------------------------------------------------- GATES
    P("-" * 118)
    P("GATES")
    P("-" * 118)
    g1max = 0.0
    for nm in order:
        px, tr = panels[nm]
        ctx = panel_ctx[nm]
        w = form_weights("MA20", px, tr, GFIX, ctx["sc"])
        pr = cad_ctx[(nm, "W")].run(w.values)[0]
        wc = apply_clause(w.values, "VOLCAP", 0.40, ctx, pr)
        wc = apply_clause(wc, "CASH", 0.80, ctx, pr)
        wcdf = pd.DataFrame(wc, index=px.index, columns=px.columns)
        a_r, a_t = cad_ctx[(nm, "W")].run(wc)
        b = backtest(px, wcdf, cost_bps=COST, freq="W")
        d_r = float((a_r - b["returns"]).abs().max())
        d_t = float((a_t - b["turnover"]).abs().max())
        g1max = max(g1max, d_r, d_t)
        P(f"G1 {nm:<9} numpy runner == engine.backtest on VOLCAP(0.40)+CASH(0.80) MA20/W : "
          f"max|dret| {d_r:.3e}  max|dturn| {d_t:.3e}")
    P(f"G1 max over panels {g1max:.3e} vs bar {G1_TOL:.0e}  -> {'PASS' if g1max < G1_TOL else 'FAIL'}")
    assert g1max < G1_TOL, "G1"

    P("")
    g2rows, g2max = [], {}
    for nm in order:
        px, tr = panels[nm]
        ctx = panel_ctx[nm]
        st = ref[nm]["start"]
        sub = par[par.panel == nm]
        dmax, nrep = 0.0, 0
        for _, prow in sub.iterrows():
            w = form_weights(prow["form"], px, tr, GFIX, ctx["sc"])
            r = cad_ctx[(nm, prow["cadence"])].run(w.values)[0].loc[st:]
            m = rowify(r)
            for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"):
                dmax = max(dmax, abs(m[k] - float(prow[k])))
            nrep += 1
        g2max[nm] = dmax
        ok = dmax < G2_TOL[nm]
        g2rows.append(dict(panel=nm, rows=nrep, max_abs_dev=dmax, bar=G2_TOL[nm], passed=ok))
        P(f"G2 {nm:<9} idea 311's {nrep} committed g=0.75 rows x 6 cols reproduce : "
          f"max|d| {dmax:.3e}  bar {G2_TOL[nm]:.0e}  -> {'PASS' if ok else 'FAIL'}")
    pd.DataFrame(g2rows).to_csv(OUT / f"{STAMP}.gates.csv", index=False)
    for nm in order:
        assert g2max[nm] < G2_TOL[nm], f"G2 {nm}"
    if g2max["U56"] > 1e-9:
        P(f"    NOTE: U56 deviates by {g2max['U56']:.3e} because data/prices.csv is refreshed daily "
          f"(idea 312/311 documented this revision).  B136 and {SMALLK} are static caches and are exact.")

    P("")
    g3max = 0.0
    nm = "B136"
    px, tr = panels[nm]
    ctx = panel_ctx[nm]
    w = form_weights("TOP20", px, tr, GFIX, ctx["sc"]).values
    pr = cad_ctx[(nm, "W")].run(w)[0]
    for fam in FAMILIES:
        wn = apply_clause(w, fam, None, ctx, pr)
        rn = cad_ctx[(nm, "W")].run(wn)[0]
        d = float((rn - pr).abs().max())
        g3max = max(g3max, d)
        P(f"G3 null-dial identity {fam:<8} on TOP20/W/B136 : max|dret| {d:.3e}")
    P(f"G3 max {g3max:.3e} vs bar {G3_TOL:.0e}  -> {'PASS' if g3max < G3_TOL else 'FAIL'}")
    assert g3max < G3_TOL, "G3"
    P("")

    # ------------------------------------------------------------------------- the bar
    P("-" * 118)
    P("THE BAR (SPY and RULES v2 on each panel's own trading days, from row 260)")
    P("-" * 118)
    for nm in order:
        spy, v2 = ref[nm]["spy"], ref[nm]["v2"]
        ms, s1, s2 = metrics(spy), *halves(spy)
        mso = metrics(spy.loc[OOS_START:])
        mv, b1, b2 = metrics(v2), *halves(v2)
        P(f"{nm:<9} SPY   CAGR {ms['CAGR']:.4f}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.4f}"
          f"  H1 {s1:.4f}  H2 {s2:.4f}  OOS_Sharpe {mso['Sharpe']:.4f}")
        P(f"{'':<9} 4b bars: H1 > {s1:.4f}, H2 > {s2:.4f}, OOS > {mso['Sharpe']:.4f}, "
          f"MaxDD >= {0.60 * ms['MaxDD']:.4f}, CAGR >= {0.70 * ms['CAGR']:.4f}")
        P(f"{'':<9} RULESv2 CAGR {mv['CAGR']:.4f}  Sharpe {mv['Sharpe']:.4f}  MaxDD {mv['MaxDD']:.4f}"
          f"  H1 {b1:.4f}  H2 {b2:.4f}")
    P("")

    # ---------------------------------------------------------------------- the sweep
    P("-" * 118)
    P("A  THE PARENTS  (idea 311's six forms at gross 0.75; every grid point)")
    P("-" * 118)
    P(f"{'panel':<9} {'form':<6} {'cad':<3} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} "
      f"{'H1':>7} {'H2':>7} {'OOSsh':>7}  {'fail4b':<20} {'4a':<5}")
    rows, prow_by = [], {}
    for nm in order:
        px, tr = panels[nm]
        ctx = panel_ctx[nm]
        st, spy, v2 = ref[nm]["start"], ref[nm]["spy"], ref[nm]["v2"]
        for form in FORMS:
            w = form_weights(form, px, tr, GFIX, ctx["sc"]).values
            for cad in CADENCES:
                cc = cad_ctx[(nm, cad)]
                pret_full, ptn = cc.run(w)
                r = pret_full.loc[st:]
                d = rowify(r, ptn.loc[st:])
                lg = legs_4b(r, spy)
                lgi = legs_4b(r.loc[:IS_END], spy.loc[:IS_END], sub=True)
                d.update(panel=nm, form=form, cadence=cad, family="PARENT", dial=np.nan,
                         clause="PARENT", **{f"L_{k}": v for k, v in lg.items()},
                         fail4b=fail_str(lg), keep4b=all(lg.values()), keep4a=keep_4a(r, v2),
                         IS_keep4b=all(lgi.values()), IS_fail4b=fail_str(lgi),
                         dd_gain_pp=0.0, cagr_cost_pp=0.0, cash_edge_pp=np.nan,
                         IS_cash_edge_pp=np.nan)
                rows.append(d)
                prow_by[(nm, form, cad)] = dict(row=d, ret=pret_full, legs=lg)
                P(f"{nm:<9} {form:<6} {cad:<3} {d['CAGR']:>8.4f} {d['Sharpe']:>7.4f} "
                  f"{d['MaxDD']:>8.4f} {d['H1']:>7.4f} {d['H2']:>7.4f} {d['OOS_Sharpe']:>7.4f}  "
                  f"{fail_str(lg):<20} {str(keep_4a(r, v2)):<5}")
    P("")

    P("-" * 118)
    P("B  THE CLAUSE SWEEP  (6 families x 47 dials x 36 parents = 1,692 cells; all written to .grid.csv)")
    P("-" * 118)
    for nm in order:
        px, tr = panels[nm]
        ctx = panel_ctx[nm]
        st, spy, v2 = ref[nm]["start"], ref[nm]["spy"], ref[nm]["v2"]
        for form in FORMS:
            w = form_weights(form, px, tr, GFIX, ctx["sc"]).values
            for cad in CADENCES:
                cc = cad_ctx[(nm, cad)]
                pinfo = prow_by[(nm, form, cad)]
                pret, prow = pinfo["ret"], pinfo["row"]
                spy_is = spy.loc[:IS_END]
                cash_dd, cash_cagr, cash_isdd, cash_iscagr = [], [], [], []
                cells = []
                for fam in FAMILIES:
                    for dial in GRIDS[fam]:
                        wc = apply_clause(w, fam, dial, ctx, pret)
                        rr, tt = cc.run(wc)
                        r = rr.loc[st:]
                        d = rowify(r, tt.loc[st:])
                        lg = legs_4b(r, spy)
                        lgi = legs_4b(r.loc[:IS_END], spy_is, sub=True)
                        d.update(panel=nm, form=form, cadence=cad, family=fam, dial=float(dial),
                                 clause=f"{fam}({dial})",
                                 **{f"L_{k}": v for k, v in lg.items()},
                                 fail4b=fail_str(lg), keep4b=all(lg.values()),
                                 keep4a=keep_4a(r, v2),
                                 IS_keep4b=all(lgi.values()), IS_fail4b=fail_str(lgi),
                                 dd_gain_pp=100.0 * (d["MaxDD"] - prow["MaxDD"]),
                                 cagr_cost_pp=100.0 * (prow["CAGR"] - d["CAGR"]))
                        if fam == "CASH":
                            cash_dd.append(d["MaxDD"])
                            cash_cagr.append(d["CAGR"])
                            cash_isdd.append(d["IS_MaxDD"])
                            cash_iscagr.append(d["IS_CAGR"])
                        cells.append(d)
                o = np.argsort(cash_dd)
                cx, cy = np.asarray(cash_dd)[o], np.asarray(cash_cagr)[o]
                oi = np.argsort(cash_isdd)
                ix, iy = np.asarray(cash_isdd)[oi], np.asarray(cash_iscagr)[oi]
                for d in cells:
                    x, xi = d["MaxDD"], d["IS_MaxDD"]
                    d["cash_edge_pp"] = (np.nan if not (cx[0] <= x <= cx[-1])
                                         else 100.0 * (d["CAGR"] - float(np.interp(x, cx, cy))))
                    d["IS_cash_edge_pp"] = (np.nan if not (ix[0] <= xi <= ix[-1])
                                            else 100.0 * (d["IS_CAGR"] - float(np.interp(xi, ix, iy))))
                rows.extend(cells)
        P(f"  {nm} done  ({time.time() - t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    CL = G[G.family != "PARENT"]
    P(f"grid: {len(G)} rows ({len(CL)} clause cells + {len(G) - len(CL)} parents) -> {STAMP}.grid.csv")
    P("")

    # ------------------------------------------------------------------- H_MAIN
    P("-" * 118)
    P("C  H_MAIN  does any clause cell clear 4b where its unclaused parent fails?")
    P("-" * 118)
    fails = {k for k, v in prow_by.items() if not v["legs"] or not all(v["legs"].values())}
    CL_fp = CL[[(r.panel, r.form, r.cadence) in fails for r in CL.itertuples()]]
    passers = CL_fp[CL_fp.keep4b]
    P(f"parents failing 4b: {len(fails)} of 36;  clause cells under them: {len(CL_fp)}")
    P(f"clause cells clearing all five 4b legs under a FAILING parent: {len(passers)}"
      f"  -> H_MAIN {'REFUTED' if len(passers) else 'HOLDS'}")
    if len(passers):
        P(passers[["panel", "form", "cadence", "clause", "CAGR", "Sharpe", "MaxDD",
                   "H1", "H2", "OOS_Sharpe", "cash_edge_pp"]].to_string(index=False))
    P(f"clause cells clearing 4a (vs RULES v2 on the same panel): {int(CL.keep4a.sum())} of {len(CL)}")
    P(f"clause cells clearing 4b anywhere (failing or passing parent): {int(CL.keep4b.sum())} of {len(CL)}")
    P("")

    # ------------------------------------------------------------------- H_DDONLY
    P("-" * 118)
    P("D  H_DDONLY  the 16 parents held out of 4b by the DD leg ALONE")
    P("-" * 118)
    ddonly = [k for k, v in prow_by.items() if v["row"]["fail4b"] == "DD"]
    P(f"parents failing 4b on DD alone: {len(ddonly)}")
    P(f"{'panel':<9} {'form':<6} {'cad':<3} {'MaxDD':>8} {'DDbar':>8} {'gap_pp':>7} | "
      f"{'cells':>5} {'DDfix':>5} {'DDfix&4b':>8} {'CASH':>6} {'SIGNAL':>6} {'S>cash':>6} "
      f"{'best clause repairing DD':<22} {'its fail4b':<14}")
    dd_rows = []
    for k in ddonly:
        nm, form, cad = k
        prow = prow_by[k]["row"]
        spy = ref[nm]["spy"]
        bar = 0.60 * metrics(spy)["MaxDD"]
        sub = CL[(CL.panel == nm) & (CL.form == form) & (CL.cadence == cad)]
        fix = sub[sub.L_DD]
        fix4b = fix[fix.keep4b]
        cash4b = int((fix4b.family == "CASH").sum())
        sig4b = fix4b[fix4b.family != "CASH"]
        beats = int((sig4b.cash_edge_pp > 0).sum())     # a SIGNAL 4b pass cash cannot match
        best = fix.sort_values("CAGR", ascending=False).head(1)
        bl = best.iloc[0]["clause"] if len(best) else "-"
        bf = best.iloc[0]["fail4b"] if len(best) else "-"
        P(f"{nm:<9} {form:<6} {cad:<3} {prow['MaxDD']:>8.4f} {bar:>8.4f} "
          f"{100 * (prow['MaxDD'] - bar):>7.2f} | {len(sub):>5} {len(fix):>5} {len(fix4b):>8} "
          f"{cash4b:>6} {len(sig4b):>6} {beats:>6} {bl:<22} {bf:<14}")
        dd_rows.append(dict(panel=nm, form=form, cadence=cad, MaxDD=prow["MaxDD"], dd_bar=bar,
                            gap_pp=100 * (prow["MaxDD"] - bar), cells=len(sub), dd_fixed=len(fix),
                            dd_fixed_and_4b=len(fix4b), cash_4b=cash4b, signal_4b=len(sig4b),
                            signal_4b_beating_cash=beats, best_clause=bl, best_fail4b=bf))
    dd_df = pd.DataFrame(dd_rows)
    dd_df.to_csv(OUT / f"{STAMP}.ddonly.csv", index=False)
    nfix = int(dd_df.dd_fixed.gt(0).sum()) if len(dd_df) else 0
    n4b = int(dd_df.dd_fixed_and_4b.gt(0).sum()) if len(dd_df) else 0
    ncash = int(dd_df.cash_4b.gt(0).sum()) if len(dd_df) else 0
    nsig = int(dd_df.signal_4b.gt(0).sum()) if len(dd_df) else 0
    nbeat = int(dd_df.signal_4b_beating_cash.gt(0).sum()) if len(dd_df) else 0
    P(f"DD-only parents with >=1 clause that REPAIRS the DD leg          : {nfix} of {len(ddonly)}")
    P(f"DD-only parents with >=1 clause that repairs DD AND still clears 4b: {n4b} of {len(ddonly)}"
      f"  -> H_DDONLY {'REFUTED' if n4b else 'HOLDS'}")
    P(f"  ... of which repaired by PLAIN CASH alone (the null)           : {ncash} of {len(ddonly)}")
    P(f"  ... repaired by a SIGNAL clause                                : {nsig} of {len(ddonly)}")
    P(f"  ... repaired by a SIGNAL clause CASH CANNOT MATCH at its own MaxDD: {nbeat} of {len(ddonly)}")
    if len(dd_df):
        brk = CL[[(r.panel, r.form, r.cadence) in set(ddonly) and r.L_DD for r in CL.itertuples()]]
        P(f"of the {len(brk)} DD-repairing cells under those parents, what broke instead:")
        P("   " + brk.fail4b.value_counts().to_string().replace("\n", "\n   "))
    P("")

    # ------------------------------------------------------------------- H_CASH
    P("-" * 118)
    P("E  H_CASH  the matched-MaxDD price of drawdown: does any signal beat plain cash?")
    P("-" * 118)
    P("edge = CAGR(clause) - CAGR(cash ladder interpolated to the clause's OWN MaxDD), in pp/yr.")
    P(f"{'family':<9} {'cells':>6} {'median':>9} {'mean':>9} {'p90':>9} {'max':>9} {'>0':>7} "
      f"{'med dd_gain_pp':>15} {'med cagr_cost_pp':>17}")
    fam_rows = []
    for fam in FAMILIES:
        s = CL[CL.family == fam]
        e = s.cash_edge_pp.dropna()
        row = dict(family=fam, cells=len(s), edge_median=e.median(), edge_mean=e.mean(),
                   edge_p90=e.quantile(0.90), edge_max=e.max(),
                   share_positive=float((e > 0).mean()) if len(e) else np.nan,
                   dd_gain_pp_median=s.dd_gain_pp.median(),
                   cagr_cost_pp_median=s.cagr_cost_pp.median())
        fam_rows.append(row)
        P(f"{fam:<9} {len(s):>6} {e.median():>9.3f} {e.mean():>9.3f} {e.quantile(0.90):>9.3f} "
          f"{e.max():>9.3f} {(e > 0).mean():>7.1%} {s.dd_gain_pp.median():>15.3f} "
          f"{s.cagr_cost_pp.median():>17.3f}")
    fam_df = pd.DataFrame(fam_rows)
    fam_df.to_csv(OUT / f"{STAMP}.family.csv", index=False)
    pos = fam_df[(fam_df.family != "CASH") & (fam_df.edge_median > 0)]
    P(f"signal families with POSITIVE median matched-DD edge: {len(pos)} of {len(FAMILIES) - 1}"
      f"  -> H_CASH {'REFUTED' if len(pos) else 'HOLDS'}")
    if len(pos):
        P("   " + ", ".join(f"{r.family} {r.edge_median:+.3f}" for r in pos.itertuples()))
    P("")

    # ------------------------------------------------------------------- H_MONO
    P("-" * 118)
    P("F  H_MONO  is the drawdown purchase ordered by the dial (a dial) or by what it selects?")
    P("-" * 118)
    mono_rows = []
    for fam in FAMILIES:
        gd = [float(x) for x in GRIDS[fam]]
        sgn = MONO_SIGN[fam]
        ok = tot = 0
        for (nm, form, cad) in prow_by:
            s = CL[(CL.family == fam) & (CL.panel == nm) & (CL.form == form) & (CL.cadence == cad)]
            v = s.set_index("dial").reindex(gd).MaxDD.values
            for i in range(len(v) - 1):
                tot += 1
                if sgn is not None:
                    ok += int(sgn * (v[i + 1] - v[i]) >= -1e-12)
        share = (ok / tot if tot else np.nan) if sgn is not None else np.nan
        mono_rows.append(dict(family=fam, pairs=tot, monotone=ok, share=share,
                              in_bar=sgn is not None))
        if sgn is None:
            P(f"{fam:<9} dial is a LOOKBACK WINDOW, not an intensity - no a-priori ordering; "
              f"{tot} adjacent pairs reported, excluded from the bar")
        else:
            dirn = "worsening as the dial loosens" if sgn < 0 else "improving as the dial tightens"
            P(f"{fam:<9} adjacent dial pairs with MaxDD {dirn}: {ok}/{tot} = {share:.1%}")
    mono_df = pd.DataFrame(mono_rows)
    mono_df.to_csv(OUT / f"{STAMP}.mono.csv", index=False)
    worst = float(mono_df[mono_df.in_bar].share.min())
    P(f"min share over the five INTENSITY families {worst:.1%} vs bar {MONO_BAR:.0%}"
      f"  -> H_MONO {'HOLDS' if worst >= MONO_BAR else 'FAILS'}")
    P("")

    # ------------------------------------------------------------------- rule 8
    P("-" * 118)
    P("G  RULE 8  WALK-FORWARD - clause family and dial chosen on IS only, OOS read ONCE")
    P("-" * 118)
    P("Selection reads ONLY the IS columns of the same .grid.csv (2010/2011-2016); the winning")
    P("cell's weights are then rebuilt once and its OOS window read a single time.")
    wf_rows = []
    for nm in order:
        px, tr = panels[nm]
        ctx = panel_ctx[nm]
        st, spy, v2 = ref[nm]["start"], ref[nm]["spy"], ref[nm]["v2"]
        spy_oos = spy.loc[OOS_START:]
        cdf = CL[CL.panel == nm].reset_index(drop=True)
        picks = [("WF-A max IS Sharpe", int(cdf.IS_Sharpe.idxmax()))]
        elig = cdf[cdf.IS_keep4b & cdf.IS_cash_edge_pp.notna()]
        picks.append(("WF-B max IS matched-DD edge among IS-4b passers",
                      int(elig.IS_cash_edge_pp.idxmax()) if len(elig) else -1))
        for tag, i in picks:
            if i < 0:
                P(f"{nm:<9} {tag}: NO cell clears all five IS 4b legs - selector empty.")
                wf_rows.append(dict(panel=nm, selector=tag, pick="(empty)"))
                continue
            c = cdf.loc[i].to_dict()
            cc = cad_ctx[(nm, c["cadence"])]
            wp = form_weights(c["form"], px, tr, GFIX, ctx["sc"]).values
            dial = int(c["dial"]) if c["family"] == "MKT" else c["dial"]
            wc = apply_clause(wp, c["family"], dial, ctx, prow_by[(nm, c["form"], c["cadence"])]["ret"])
            r = cc.run(wc)[0].loc[st:]
            ro, rf = r.loc[OOS_START:], r
            mo, mfull = metrics(ro), metrics(rf)
            lo = legs_4b(ro, spy_oos, sub=True)
            lf = legs_4b(rf, spy)
            bo, so = metrics(v2.loc[OOS_START:]), metrics(spy_oos)
            # OOS matched-MaxDD edge: rebuild THIS parent's cash ladder on the OOS window only
            # and price the pick against it there.  Tests whether WF-B's own selection statistic
            # survives out of sample, which is the real "can drawdown be BOUGHT" question.
            odd, ocg = [], []
            for k in CASH_GRID:
                rk = cc.run(wp * k)[0].loc[st:].loc[OOS_START:]
                mk = metrics(rk)
                odd.append(mk["MaxDD"])
                ocg.append(mk["CAGR"])
            oo = np.argsort(odd)
            ox, oy = np.asarray(odd)[oo], np.asarray(ocg)[oo]
            oedge = (np.nan if not (ox[0] <= mo["MaxDD"] <= ox[-1])
                     else 100.0 * (mo["CAGR"] - float(np.interp(mo["MaxDD"], ox, oy))))
            rb = float(abs(metrics(rf.loc[:IS_END])["Sharpe"] - c["IS_Sharpe"]))
            ee = c["IS_cash_edge_pp"]
            P(f"{nm:<9} {tag}")
            P(f"{'':<9}   pick {c['form']}/{c['cadence']} + {c['clause']:<14} "
              f"IS Sharpe {c['IS_Sharpe']:.4f}  IS MaxDD {c['IS_MaxDD']:.4f}  "
              f"IS edge {('nan' if pd.isna(ee) else f'{ee:+.3f}')} pp  IS 4b {c['IS_keep4b']}"
              f"  (rebuild check |dIS_Sharpe| {rb:.2e})")
            assert rb < 1e-12, "walk-forward rebuild does not match its own grid row"
            P(f"{'':<9}   OOS      CAGR {mo['CAGR']:.4f}  Sharpe {mo['Sharpe']:.4f}  "
              f"MaxDD {mo['MaxDD']:.4f}   OOS 4b legs fail: {fail_str(lo)}")
            P(f"{'':<9}   matched-MaxDD edge vs its own parent's CASH ladder: "
              f"IS {('nan' if pd.isna(ee) else f'{ee:+.3f}')} pp -> "
              f"OOS {('nan' if pd.isna(oedge) else f'{oedge:+.3f}')} pp"
              f"   (positive = the clause bought drawdown more cheaply than cash)")
            P(f"{'':<9}   RULES v2 CAGR {bo['CAGR']:.4f}  Sharpe {bo['Sharpe']:.4f}  "
              f"MaxDD {bo['MaxDD']:.4f}")
            P(f"{'':<9}   SPY      CAGR {so['CAGR']:.4f}  Sharpe {so['Sharpe']:.4f}  "
              f"MaxDD {so['MaxDD']:.4f}")
            P(f"{'':<9}   full-sample 4b fail: {fail_str(lf)}   4a vs RULES v2: {keep_4a(rf, v2)}")
            wf_rows.append(dict(panel=nm, selector=tag, pick=f"{c['form']}/{c['cadence']}+{c['clause']}",
                                IS_Sharpe=c["IS_Sharpe"], IS_MaxDD=c["IS_MaxDD"],
                                IS_cash_edge_pp=c["IS_cash_edge_pp"], IS_keep4b=c["IS_keep4b"],
                                OOS_cash_edge_pp=oedge,
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                OOS_fail4b=fail_str(lo), OOS_keep4b=all(lo.values()),
                                base_OOS_CAGR=bo["CAGR"], base_OOS_Sharpe=bo["Sharpe"],
                                base_OOS_MaxDD=bo["MaxDD"], spy_OOS_CAGR=so["CAGR"],
                                spy_OOS_Sharpe=so["Sharpe"], spy_OOS_MaxDD=so["MaxDD"],
                                full_fail4b=fail_str(lf), full_keep4a=keep_4a(rf, v2)))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    oos_keep = int(wf.get("OOS_keep4b", pd.Series(dtype=bool)).fillna(False).sum())
    P(f"walk-forward picks clearing 4b OUT OF SAMPLE: {oos_keep} of {len(wf)}"
      f"  -> H_OOS {'REFUTED' if oos_keep else 'HOLDS'}")
    ed = wf.dropna(subset=["IS_cash_edge_pp", "OOS_cash_edge_pp"]) if "OOS_cash_edge_pp" in wf else wf.iloc[:0]
    if len(ed):
        keptsign = int(((ed.IS_cash_edge_pp > 0) & (ed.OOS_cash_edge_pp > 0)).sum())
        P(f"walk-forward picks whose matched-MaxDD edge over cash KEEPS ITS SIGN out of sample: "
          f"{keptsign} of {len(ed)}  (median IS {ed.IS_cash_edge_pp.median():+.3f} pp -> "
          f"median OOS {ed.OOS_cash_edge_pp.median():+.3f} pp)")
    P("")

    # ------------------------------------------------------------------- verdict
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    P(f"H_MAIN   no clause cell clears 4b under a failing parent      : "
      f"{'HOLDS' if not len(passers) else 'REFUTED'}  ({len(passers)}/{len(CL_fp)})")
    P(f"H_DDONLY no clause repairs DD-only parents without breaking a leg: "
      f"{'HOLDS' if not n4b else 'REFUTED'}  ({n4b}/{len(ddonly)})")
    P(f"H_CASH   no signal family beats plain cash at matched MaxDD   : "
      f"{'HOLDS' if not len(pos) else 'REFUTED'}  ({len(pos)}/{len(FAMILIES) - 1})")
    P(f"H_MONO   drawdown purchase is dial-ordered                    : "
      f"{'HOLDS' if worst >= MONO_BAR else 'FAILS'}  (min {worst:.1%})")
    P(f"H_OOS    no walk-forward pick clears 4b out of sample         : "
      f"{'HOLDS' if not oos_keep else 'REFUTED'}  ({oos_keep}/{len(wf)})")
    verdict = "KEEP-candidate" if len(passers) else "KILL"
    P(f"PROTOCOL verdict for the CLAUSE FAMILY: {verdict}")
    P(f"4a passes over the {len(CL)} clause cells: {int(CL.keep4a.sum())}; "
      f"4b passes: {int(CL.keep4b.sum())} (of which under an already-passing parent: "
      f"{int(CL.keep4b.sum()) - len(passers)})")
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
