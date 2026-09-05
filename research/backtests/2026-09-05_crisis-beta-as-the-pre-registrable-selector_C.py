#!/usr/bin/env python3
"""QUEUE idea 113 — crisis-beta-as-the-pre-registrable-selector (lane C, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 99 measured a -1.03 slope of overlay value on the year's SPY MaxDD, i.e. an overlay's
payoff is a linear function of an observable that does not need the OOS window to estimate.
Test whether 'argmax IS Sharpe + estimated crisis beta x a stated drawdown budget' picks better
OOS than plain rule 8 across the same 44 cells, and whether it beats the +0.015 ceiling rule 8
already leaves.  Max 2 params."

THE OBJECT UNDER TEST
---------------------
Idea 99's T2 regression says: for a grid point p, its per-year value over the no-overlay control,
d_y(p) = Sharpe_y(p) - Sharpe_y(null), falls roughly linearly in that year's SPY drawdown, with
slope about -1.0 (SPY MaxDD is negative, so a deeper-drawdown year pays the overlay MORE).
Define that point's CRISIS BETA as the negative of its own such slope, fitted on IS YEARS ONLY:

    beta_IS(p) = -OLS_slope( d_y(p)  ~  SPY_MaxDD_y ),   y in the IS calendar years

beta_IS > 0 means "this arm pays more the worse the year is".  Nothing in beta_IS touches the OOS
window.  The first-order forecast of the arm's value in a deployment window whose average annual
SPY drawdown is B deeper than the IS window's is then d_IS(p) + beta_IS(p) * B, so the selector is

    S_crisis(B):  argmax over the grid of  [ IS_Sharpe(p) + beta_IS(p) * B ]

B is THE STATED DRAWDOWN BUDGET, in MaxDD units (B = 0.10 means "assume the window we are about
to trade averages 10pp deeper annual SPY drawdowns than 2009-2016 did").  B = 0 is EXACTLY
PROTOCOL rule 8 as written, so the selectors are nested and the test is a clean one-sided
question: does any B > 0 pick better arms out of sample than B = 0?

PRE-REGISTERED SELECTORS (declared before any number was computed)
------------------------------------------------------------------
  S_sharpe      argmax IS Sharpe                       <- PROTOCOL rule 8; identical to B=0
  S_crisis005   argmax IS Sharpe + beta_IS * 0.05      <- the queue's proposal, small budget
  S_crisis010   argmax IS Sharpe + beta_IS * 0.10      <-   "          "     , medium budget
  S_crisis020   argmax IS Sharpe + beta_IS * 0.20      <-   "          "     , large budget
  S_anti010     argmax IS Sharpe - beta_IS * 0.10      <- FALSIFICATION control: the same dial
                                                          turned the wrong way.  If +B and -B
                                                          both help, the dial is noise, not
                                                          crisis beta.
  S_null        the no-overlay point (overlay parameter = 0)   <- does ANY selection beat none?
  S_oracle      argmax OOS Sharpe                      <- the unreachable ceiling; reported for
                                                          regret only, never claimed as a rule.
IS = 2009-01-13 .. 2016-12-31.  OOS = 2017-01-01 .. 2026-09-04, touched by S_oracle alone (which
is labelled as cheating everywhere it appears).  Tie-break in every selector: SMALLEST overlay
parameter, so no selector wins on argmax ordering.

TUNED (2, per PROTOCOL rule 4): the drawdown budget B (4 levels incl. 0) x the overlay parameter
(4-5 levels per grid).  Universe, base book, cost rung, which overlay, and the beta estimator's
window are reported controls, never selected on.  ALL grid points are written to .grid.csv and
printed.

WHY A HORSE RACE ALONE WOULD NOT SETTLE IT — the two diagnostics that do
------------------------------------------------------------------------
  T1  IS BETA STABLE?   corr(beta_IS, beta_OOS) across non-null grid points.  A selector using
      beta_IS can only work if beta_IS predicts the same point's OOS beta.
  T2  DOES BETA PREDICT PAYOFF?  cross-sectional OLS/Spearman of realised d_OOS on beta_IS.  If
      beta_IS carries no information about OOS value, S_crisis cannot beat rule 8 for any B and
      any apparent win is grid noise.
These are computed on every non-null point and reported whatever the horse race says.

ROBUSTNESS ARM (declared, not tuned): the annual estimator has only 7 IS years.  beta is
re-estimated on the 28 IS QUARTERS (d_q vs the SPY MaxDD inside that quarter) and the whole
selector census is re-run on it.  The verdict is taken from the PRE-REGISTERED ANNUAL estimator;
if the quarterly arm reverses it, that is reported as a headline, not buried.

CELLS: 6 overlay grids x 2 base books (top20, ewall) x 2 universes (u56, broad) x 2 cost rungs
(10, 25 bps), weekly cadence = 44 cells (crypto does not exist on the broad panel).  Same cells
as ideas 99 and 109 so the numbers are comparable.

CRYPTO CAVEAT: BTC-USD starts 2014-09-17, so the crypto grid's IS window holds barely two years
of crypto and its beta_IS is fitted on ~2 usable years.  Reported in and out of every pooled
statistic.

Both KEEP paths evaluated for every pick: 4a (Sharpe > RULES v1 in both halves, MaxDD no worse)
and 4b (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's), plus
4b evaluated on the OOS window alone, which is the honest test of a selector.

SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
The bias is identical across selectors, which is what this run compares.

COST NOTE: engine.backtest applies costs as `gross - turnover * bps/1e4` with the holdings path
independent of bps, so each weight matrix is run ONCE at 0 bps and both rungs derived exactly.
Asserted at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17.
It hits every grid point, every selector and every beta identically.

Deterministic, standalone:
    python research/backtests/2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

FREQ = "W"
COSTS = (10, 25)
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BUDGETS = (0.05, 0.10, 0.20)      # the stated drawdown budgets B; B=0 is rule 8 itself
ANTI_B = 0.10                     # falsification control uses the middle budget
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30                  # pre-set, not tuned
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
YEARS = list(range(2010, 2027))   # 2009 is partial (eval starts 2009-01-13); 2026 partial, flagged
IS_YEARS = [y for y in YEARS if y <= 2016]
OOS_YEARS = [y for y in YEARS if y >= 2017]
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- gates and books
def _band_above(px, w):
    """200d gate with hysteresis: enter above MA*(1+w), exit below MA*(1-w). w=0 -> plain 200d."""
    ma = px.rolling(200).mean()
    up = (px > ma * (1 + w))
    dn = (px < ma * (1 - w))
    st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                      index=px.index, columns=px.columns)
    return st.ffill().fillna(0.0) > 0.5


def _elig(px, band=0.0, stop=None):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = _band_above(px, band) & (vol20 < 0.60)
    if stop is not None:
        dd = px / px.rolling(126).max() - 1.0
        m = m & (dd > -stop)
    return m


def book(px, kind, band=0.0, stop=None, gross=BOOK_GROSS, n=20):
    s, _, _ = score(px, vol_scale=False)
    m = _elig(px, band, stop)
    if kind == "top20":
        rank = s.where(m).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
    else:                                          # ewall
        w = (m & s.notna()).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = (1.0 / vol.replace(0.0, np.nan))
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def _regross(w, g=1.00):
    tot = w.sum(axis=1)
    return w.mul((g / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- the six overlay grids
def overlay(px, kind, grid, p):
    if grid == "sleeve":
        E = book(px, kind)
        return _regross((1 - p) * E + p * sleeve_weights(px, S4), 1.00)
    if grid == "band":
        return book(px, kind, band=p)
    if grid == "breadth":
        E = book(px, kind)
        above = _band_above(px, 0.0).drop(columns=["SPY"], errors="ignore")
        br = above.mean(axis=1)
        mult = pd.Series(np.where(br < BREADTH_B, 1.0 - p, 1.0), index=px.index)
        return E.mul(mult, axis=0)
    if grid == "stop":
        return book(px, kind, stop=None if p is None else p)
    if grid == "gross":
        return book(px, kind, gross=p)
    if grid == "crypto":
        E = book(px, kind, gross=BOOK_GROSS * (1 - p))
        if p == 0.0:
            return E
        c = [t for t in CRYPTO if t in px.columns]
        avail = px[c].notna().astype(float)
        k = avail.sum(axis=1)
        cw = avail.div(k.where(k > 0), axis=0).fillna(0.0) * (BOOK_GROSS * p)
        out = E.copy()
        out[c] = out[c].values + cw.values
        return out
    raise ValueError(grid)


GRIDS = {
    "sleeve":  [0.00, 0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.02, 0.03, 0.05, 0.08],
    "breadth": [0.00, 0.25, 0.50, 0.75, 1.00],
    "stop":    [None, 0.25, 0.20, 0.15, 0.10],
    "crypto":  [0.00, 0.02, 0.05, 0.10],
    "gross":   [0.75, 0.50, 1.00, 1.25],          # first entry = incumbent = "no overlay"
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}
# idea 99's a-priori labels, carried over unchanged so the two runs line up
APRIORI = {"sleeve": "defensive", "band": "defensive", "breadth": "defensive",
           "stop": "defensive", "crypto": "offensive", "gross": "mixed"}


def pkey(grid, p):
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p
    if grid == "gross":
        return abs(p - 0.75)
    return float(p)


# ---------------------------------------------------------------- metrics helpers
def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def sharpe_on(r, a, b):
    s = r.loc[a:b] if (a or b) else r
    if len(s) < 20:
        return np.nan
    return metrics(s)["Sharpe"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, idd = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
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


def ols(x, y):
    """slope, intercept, pearson r on the finite pairs (nan,nan,nan if <3 usable points)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3 or np.nanstd(x[m]) < 1e-12:
        return np.nan, np.nan, np.nan
    b, a = np.polyfit(x[m], y[m], 1)
    r = np.corrcoef(x[m], y[m])[0, 1]
    return b, a, r


def spearman(x, y):
    s = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(s) < 3:
        return np.nan
    return float(s["x"].rank().corr(s["y"].rank()))


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- selectors
SELECTORS = (["S_sharpe"] + [f"S_crisis{int(b*1000):03d}" for b in BUDGETS]
             + [f"S_anti{int(ANTI_B*1000):03d}", "S_null", "S_oracle"])
SEL_B = {"S_sharpe": 0.0, "S_null": None, "S_oracle": None,
         f"S_anti{int(ANTI_B*1000):03d}": -ANTI_B}
SEL_B.update({f"S_crisis{int(b*1000):03d}": b for b in BUDGETS})


def select(sub, how, betacol):
    """sub: all grid points of one cell (a DataFrame).  Returns the chosen row."""
    s = sub.sort_values("pkey")
    if how == "S_null":
        return s[s["is_null"]].iloc[0]
    if how == "S_oracle":
        return s.loc[[s["OOS_Sharpe"].idxmax()]].iloc[0]
    b = SEL_B[how]
    obj = s["IS_Sharpe"] + b * s[betacol].fillna(0.0)   # a point whose beta cannot be fitted is
    return s.loc[[obj.idxmax()]].iloc[0]                # scored as beta=0, i.e. rule 8 treatment


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())          # keeps BTC/ETH so the crypto grid can run
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    print(f"[data] u56 {u56.shape[1]} cols (incl. {[t for t in CRYPTO if t in u56.columns]}), "
          f"broad {broad.shape[1]} cols")
    print(f"[pre-registered] selectors {SELECTORS}")
    print(f"[pre-registered] beta_IS(p) = -slope( d_y(p) ~ SPY_MaxDD_y ) on IS years {IS_YEARS}")
    print(f"[pre-registered] budgets B = {BUDGETS} (B=0 is rule 8); anti-control at -{ANTI_B}")
    print(f"[pre-registered] IS <= {IS_END} · OOS >= {SPLIT} · tie-break = smallest overlay param\n")

    st0 = u56.index[260]
    w0 = book(u56, "top20")
    r0 = backtest(u56, w0, cost_bps=0.0, freq=FREQ)
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], 10)
                 - backtest(u56, w0, cost_bps=10, freq=FREQ)["returns"].loc[st0:]).abs().max())
    print(f"[check] cost linearity max |derived - direct| at 10 bps = {err:.2e}")
    assert err < 1e-12

    # quarters, for the robustness estimator
    QUARTERS = [(f"{y}Q{q}", f"{y}-{3*q-2:02d}-01",
                 f"{y}-{3*q:02d}-{'31' if q in (1, 4) else '30'}")
                for y in YEARS for q in (1, 2, 3, 4)]
    IS_Q = [q for q, a, _ in QUARTERS if int(q[:4]) <= 2016]
    OOS_Q = [q for q, a, _ in QUARTERS if int(q[:4]) >= 2017]

    records, refs, spy_year, spy_qtr = [], {}, {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto)
        spy_year[tag] = {}
        for y in YEARS:
            s = spy_r.loc[f"{y}-01-01":f"{y}-12-31"]
            spy_year[tag][y] = (np.nan if len(s) < 20 else
                                float(((1 + s).cumprod() / (1 + s).cumprod().cummax() - 1).min()))
        spy_qtr[tag] = {}
        for qn, a, b in QUARTERS:
            s = spy_r.loc[a:b]
            spy_qtr[tag][qn] = (np.nan if len(s) < 20 else
                                float(((1 + s).cumprod() / (1 + s).cumprod().cummax() - 1).min()))

        print("=" * 122)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers | eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": full_row(net(bgr, bto, 10)), "SPY": spy}).T))
        print("SPY MaxDD by calendar year (the selector's only exogenous input):")
        print("  " + "  ".join(f"{y}:{spy_year[tag][y]:+.1%}" for y in YEARS))
        isd = np.nanmean([spy_year[tag][y] for y in IS_YEARS])
        osd = np.nanmean([spy_year[tag][y] for y in OOS_YEARS])
        print(f"  mean annual SPY MaxDD: IS {isd:+.1%} · OOS {osd:+.1%} · "
              f"realised budget B* = {isd - osd:+.3f}")

        for grid, params in GRIDS.items():
            if grid == "crypto" and not all(t in px.columns for t in CRYPTO):
                print(f"  [skip] grid={grid} on {tag}: crypto tickers absent from this panel")
                continue
            for kind in ("top20", "ewall"):
                for p in params:
                    w = overlay(px, kind, grid, p)
                    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                    gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    gross = float(w.loc[start:].sum(axis=1).mean())
                    turn = float(to.sum() / (len(gr) / 252))
                    for bps in COSTS:
                        r = net(gr, to, bps)
                        row = full_row(r)
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind,
                                   param=("none" if p is None else p), cost_bps=bps,
                                   Gross=gross, Turn_yr=turn, apriori=APRIORI[grid],
                                   pkey=pkey(grid, p), is_null=(p == NULL_P[grid]))
                        for y in YEARS:
                            row[f"SH_y_{y}"] = sharpe_on(r, f"{y}-01-01", f"{y}-12-31")
                        for qn, a, b in QUARTERS:
                            row[f"SH_q_{qn}"] = sharpe_on(r, a, b)
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    CELL = ["universe", "grid", "book", "cost_bps"]

    # ------------------------------------------------------------ crisis betas, per grid point
    beta_rows = []
    for cell, sub in G.groupby(CELL, sort=False):
        tag = cell[0]
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub.iterrows():
            dy = {y: r[f"SH_y_{y}"] - nullrow[f"SH_y_{y}"] for y in YEARS}
            dq = {q: r[f"SH_q_{q}"] - nullrow[f"SH_q_{q}"] for q, _, _ in QUARTERS}
            b_is, _, r_is = ols([spy_year[tag][y] for y in IS_YEARS], [dy[y] for y in IS_YEARS])
            b_os, _, r_os = ols([spy_year[tag][y] for y in OOS_YEARS], [dy[y] for y in OOS_YEARS])
            bq_is, _, rq_is = ols([spy_qtr[tag][q] for q in IS_Q], [dq[q] for q in IS_Q])
            bq_os, _, _ = ols([spy_qtr[tag][q] for q in OOS_Q], [dq[q] for q in OOS_Q])
            beta_rows.append(dict(
                universe=cell[0], grid=cell[1], book=cell[2], cost_bps=cell[3],
                param=r["param"], pkey=r["pkey"], is_null=bool(r["is_null"]), apriori=r["apriori"],
                beta_IS=-b_is, beta_OOS=-b_os, betafit_r_IS=r_is,
                betaQ_IS=-bq_is, betaQ_OOS=-bq_os, betafitQ_r_IS=rq_is,
                d_IS=r["IS_Sharpe"] - nullrow["IS_Sharpe"],
                d_OOS=r["OOS_Sharpe"] - nullrow["OOS_Sharpe"]))
    B = pd.DataFrame(beta_rows)
    G = G.merge(B[CELL + ["param", "beta_IS", "beta_OOS", "betaQ_IS", "betaQ_OOS",
                          "betafit_r_IS", "d_IS", "d_OOS"]], on=CELL + ["param"], how="left")
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    B.to_csv(OUT.with_suffix(".betas.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv · betas -> {OUT.name}.betas.csv")

    # ------------------------------------------------------------ (1) every grid point
    print("\n" + "=" * 122)
    print("### (1) EVERY GRID POINT (10 bps shown; 25 bps in .grid.csv)\n")
    for (tag, grid, kind), sub in G[G.cost_bps == 10].groupby(["universe", "grid", "book"],
                                                              sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}  (apriori {APRIORI[grid]})")
        print(fmt(sub.set_index("param")[["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD",
                                          "IS_Sharpe", "beta_IS", "beta_OOS", "d_IS", "d_OOS",
                                          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                          "4a", "4b", "4b_oos"]]))
        print()

    # ------------------------------------------------------------ (2) T1/T2 diagnostics
    print("=" * 122)
    print("### (2) IS THE SELECTOR'S INPUT EVEN INFORMATIVE?  T1 beta stability, T2 beta -> payoff\n")
    nn = B[~B.is_null].copy()
    diag = []
    for label, sel in (("ALL grids", nn), ("excl. crypto", nn[nn.grid != "crypto"]),
                       ("defensive only", nn[nn.apriori == "defensive"])):
        b1, _, r1 = ols(sel.beta_IS, sel.beta_OOS)
        b2, _, r2 = ols(sel.beta_IS, sel.d_OOS)
        b3, _, r3 = ols(sel.d_IS, sel.d_OOS)
        diag.append(dict(sample=label, n=len(sel),
                         mean_beta_IS=sel.beta_IS.mean(), mean_beta_OOS=sel.beta_OOS.mean(),
                         T1_slope=b1, T1_r=r1, T1_spearman=spearman(sel.beta_IS, sel.beta_OOS),
                         T2_slope=b2, T2_r=r2, T2_spearman=spearman(sel.beta_IS, sel.d_OOS),
                         ctrl_dIS_dOOS_r=r3,
                         ctrl_dIS_spearman=spearman(sel.d_IS, sel.d_OOS)))
    DG = pd.DataFrame(diag).set_index("sample")
    print(fmt(DG))
    DG.to_csv(OUT.with_suffix(".diagnostics.csv"))
    print("\nT1: does IS-fitted crisis beta predict the SAME point's OOS crisis beta?")
    print("T2: does IS-fitted crisis beta predict the point's realised OOS value d_OOS?")
    print("ctrl: for reference, how well plain IS value d_IS predicts d_OOS (what rule 8 uses).")
    print("\nBeta by a-priori label (idea 99's taxonomy), 10 bps:")
    print(fmt(nn[nn.cost_bps == 10].groupby(["apriori", "universe"])
              [["beta_IS", "beta_OOS", "betafit_r_IS", "d_IS", "d_OOS"]].mean()))

    # ------------------------------------------------------------ (3) selector census
    print("\n" + "=" * 122)
    print("### (3) THE SELECTOR CENSUS — each selector's pick per cell, and its OOS outcome\n")
    picks = []
    for cell, sub in G.groupby(CELL, sort=False):
        tag = cell[0]
        spy, _, _ = refs[tag]
        best_oos = sub["OOS_Sharpe"].max()
        for arm, betacol in (("annual", "beta_IS"), ("quarterly", "betaQ_IS")):
            for how in SELECTORS:
                if arm == "quarterly" and how in ("S_null", "S_oracle", "S_sharpe"):
                    continue                      # identical by construction; run once
                r = select(sub, how, betacol)
                picks.append(dict(universe=cell[0], grid=cell[1], book=cell[2], cost_bps=cell[3],
                                  arm=arm, selector=how, param=r["param"],
                                  beta_IS=r["beta_IS"], IS_Sharpe=r["IS_Sharpe"],
                                  OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                                  OOS_MaxDD=r["OOS_MaxDD"], CAGR=r["CAGR"], Sharpe=r["Sharpe"],
                                  MaxDD=r["MaxDD"], H1=r["H1"], H2=r["H2"],
                                  regret=r["OOS_Sharpe"] - best_oos,
                                  full_4a=bool(r["4a"]), full_4b=bool(r["4b"]),
                                  oos_4b=bool(r["4b_oos"]), apriori=r["apriori"],
                                  spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                  spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    P = pd.DataFrame(picks)
    P.to_csv(OUT.with_suffix(".picks.csv"), index=False)
    A = P[P.arm == "annual"]
    print("--- PRE-REGISTERED (annual) estimator; every cell, every selector")
    print(fmt(A.set_index(CELL + ["selector"])[
        ["param", "beta_IS", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "regret", "full_4b", "oos_4b"]]))

    # ------------------------------------------------------------ (4) does the dial ever move?
    print("\n" + "=" * 122)
    print("### (4) DOES THE BUDGET EVER CHANGE THE PICK?  If S_crisis == S_sharpe it is not a rule.\n")
    piv = A.pivot_table(index=CELL, columns="selector", values="param", aggfunc="first")
    ncell = len(piv)
    same = pd.DataFrame({s: (piv[s].astype(str) == piv["S_sharpe"].astype(str))
                         for s in SELECTORS if s not in ("S_sharpe",)})
    print(piv.to_string())
    print(f"\nOf {ncell} cells, each selector picks the SAME point as rule 8 (S_sharpe) in:")
    for s in same.columns:
        print(f"  {s:<14} {int(same[s].sum()):>3}/{ncell} ({same[s].mean():.0%})  "
              f"differs in {int((~same[s]).sum())}")

    # ------------------------------------------------------------ (5) headline OOS comparison
    print("\n" + "=" * 122)
    print("### (5) OUT-OF-SAMPLE OUTCOME BY SELECTOR (2017-2026; only S_oracle ever saw it)\n")
    for label, sel in (("ALL grids", A), ("excl. crypto (short IS window)", A[A.grid != "crypto"]),
                       ("defensive grids only", A[A.apriori == "defensive"])):
        agg = sel.groupby("selector").agg(
            n=("param", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
            OOS_MaxDD=("OOS_MaxDD", "mean"), regret=("regret", "mean"),
            full_4a=("full_4a", "sum"), full_4b=("full_4b", "sum"), oos_4b=("oos_4b", "sum"),
            beats_SPY_OOS=("OOS_Sharpe",
                           lambda s: int((s.values > sel.loc[s.index, "spy_OOS_Sharpe"].values).sum())),
        ).reindex(SELECTORS)
        print(f"--- {label}   (SPY OOS Sharpe u56/broad "
              f"{refs['u56'][0]['OOS_Sharpe']:.3f}/{refs['broad'][0]['OOS_Sharpe']:.3f}, "
              f"OOS CAGR {refs['u56'][0]['OOS_CAGR']:.2%}, OOS MaxDD {refs['u56'][0]['OOS_MaxDD']:.1%})")
        print(fmt(agg))
        print()

    # paired, cell by cell, vs rule 8
    print("Paired vs rule 8 (S_sharpe), same cell, PRE-REGISTERED annual estimator:")
    base = A[A.selector == "S_sharpe"].set_index(CELL)
    pair = []
    for s in SELECTORS:
        if s == "S_sharpe":
            continue
        a = A[A.selector == s].set_index(CELL)
        d = a["OOS_Sharpe"] - base["OOS_Sharpe"]
        differs = a["param"].astype(str) != base["param"].astype(str)
        pair.append(dict(selector=s, n_differ=int(differs.sum()),
                         dOOS_Sharpe_all=d.mean(),
                         dOOS_Sharpe_differ=d[differs].mean() if differs.any() else np.nan,
                         dOOS_CAGR_all=(a["OOS_CAGR"] - base["OOS_CAGR"]).mean(),
                         dOOS_MaxDD_all=(a["OOS_MaxDD"] - base["OOS_MaxDD"]).mean(),
                         better=int((d > 1e-12).sum()), worse=int((d < -1e-12).sum()),
                         d4b=int((a["full_4b"].astype(int) - base["full_4b"].astype(int)).sum()),
                         d4b_oos=int((a["oos_4b"].astype(int) - base["oos_4b"].astype(int)).sum())))
    PR = pd.DataFrame(pair).set_index("selector")
    print(fmt(PR))
    PR.to_csv(OUT.with_suffix(".paired.csv"))
    ceiling = -base["OOS_Sharpe"].sub(A[A.selector == "S_oracle"].set_index(CELL)["OOS_Sharpe"]).mean()
    print(f"\nCEILING: mean regret of rule 8 vs the OOS oracle = {ceiling:+.4f} of OOS Sharpe.")
    print("Any selector's gain over rule 8 must be read against that ceiling.")

    # per-grid detail
    print("\nPer-grid mean dOOS_Sharpe vs rule 8 (annual estimator):")
    rows = []
    for s in SELECTORS:
        if s == "S_sharpe":
            continue
        a = A[A.selector == s].set_index(CELL)
        rows.append((a["OOS_Sharpe"] - base["OOS_Sharpe"]).groupby(level="grid").mean().rename(s))
    print(fmt(pd.concat(rows, axis=1)))

    # ------------------------------------------------------------ (6) robustness arm
    print("\n" + "=" * 122)
    print("### (6) ROBUSTNESS ARM — beta re-estimated on 28 IS QUARTERS instead of 7 IS years\n")
    Q = P[P.arm == "quarterly"]
    agg = Q.groupby("selector").agg(
        n=("param", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), regret=("regret", "mean"),
        full_4b=("full_4b", "sum"), oos_4b=("oos_4b", "sum"))
    print(fmt(agg))
    qpair = []
    for s in sorted(set(Q.selector)):
        a = Q[Q.selector == s].set_index(CELL)
        d = a["OOS_Sharpe"] - base["OOS_Sharpe"]
        differs = a["param"].astype(str) != base["param"].astype(str)
        qpair.append(dict(selector=s, n_differ=int(differs.sum()), dOOS_Sharpe_all=d.mean(),
                          better=int((d > 1e-12).sum()), worse=int((d < -1e-12).sum()),
                          d4b=int((a["full_4b"].astype(int) - base["full_4b"].astype(int)).sum())))
    print("\nPaired vs rule 8:")
    print(fmt(pd.DataFrame(qpair).set_index("selector")))
    b1, _, r1 = ols(nn.betaQ_IS, nn.betaQ_OOS)
    b2, _, r2 = ols(nn.betaQ_IS, nn.d_OOS)
    print(f"\nQuarterly-estimator diagnostics on {len(nn)} non-null points: "
          f"T1 slope {b1:+.3f} r {r1:+.3f} · T2 slope {b2:+.3f} r {r2:+.3f}")

    # ------------------------------------------------------------ (7) the KEEP paths
    print("\n" + "=" * 122)
    print("### (7) KEEP PATHS 4a AND 4b FOR EVERY SELECTOR'S PICKS (annual estimator)\n")
    kp = A.groupby("selector").agg(cells=("param", "size"), pass_4a=("full_4a", "sum"),
                                   pass_4b=("full_4b", "sum"), pass_4b_oos=("oos_4b", "sum")
                                   ).reindex(SELECTORS)
    print(fmt(kp))
    print("\n4b-passing picks in full (annual estimator):")
    w4b = A[A.full_4b]
    print(fmt(w4b.set_index(CELL + ["selector"])[["param", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]])
          if len(w4b) else "  (none)")

    # ------------------------------------------------------------ (8) verdict
    print("\n" + "=" * 122)
    print("### (8) VERDICT INPUTS\n")
    b1, _, r1 = ols(nn.beta_IS, nn.beta_OOS)
    b2, _, r2 = ols(nn.beta_IS, nn.d_OOS)
    b3, _, r3 = ols(nn.d_IS, nn.d_OOS)
    print(f"T1 beta stability  : slope {b1:+.3f} r {r1:+.3f} spearman "
          f"{spearman(nn.beta_IS, nn.beta_OOS):+.3f}  (n={len(nn)} non-null points)")
    print(f"T2 beta -> d_OOS   : slope {b2:+.3f} r {r2:+.3f} spearman "
          f"{spearman(nn.beta_IS, nn.d_OOS):+.3f}")
    print(f"ctrl d_IS -> d_OOS : slope {b3:+.3f} r {r3:+.3f} spearman "
          f"{spearman(nn.d_IS, nn.d_OOS):+.3f}")
    best = PR["dOOS_Sharpe_all"].drop(index=["S_oracle"], errors="ignore")
    print(f"\nBest budget by mean dOOS Sharpe vs rule 8: {best.idxmax()} at "
          f"{best.max():+.4f}; anti-control S_anti{int(ANTI_B*1000):03d} at "
          f"{PR.loc[f'S_anti{int(ANTI_B*1000):03d}', 'dOOS_Sharpe_all']:+.4f}; ceiling {ceiling:+.4f}")
    print(f"4b pass count vs rule 8's {int(kp.loc['S_sharpe', 'pass_4b'])}: "
          + ", ".join(f"{s} {int(kp.loc[s, 'pass_4b'])}" for s in SELECTORS if s != "S_sharpe"))
    print("\nDone.")


if __name__ == "__main__":
    main()
