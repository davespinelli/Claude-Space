#!/usr/bin/env python3
"""Idea 618 — is the INTERCEPT of the width law a DEFENSIVE-SLEEVE statistic?   (lane C, 2026-09-10)

QUEUE 618: "idea 613 replicated width = intercept(panel, book, sleeve) - slope x drag on a CASH
sleeve 403 never ran, and the intercept moved a long way with the sleeve (u56/TOP20 mean width
6.90 on ETF3 vs 4.35 on CASH; broad/EWALL 3.67 vs 0.06) while the slope barely moved (-0.923 vs
-0.847; -0.930 vs -0.374).  Sweep the sleeve asset set itself and ask whether the intercept is a
property of the sleeve's own drawdown behaviour rather than of the panel.  Max 2 params (sleeve
set, f)."

WHAT IS ACTUALLY BEING TESTED
  H1 (variance)  Across (panel, book, sleeve) cells, the width law's INTERCEPT is carried by the
                 SLEEVE label, not the (panel, book) label.  Falsifiable: fit intercept on sleeve
                 dummies alone and on panel-x-book dummies alone and compare R^2.  If the panel
                 term wins, the queue's premise is wrong.
  H2 (the ask)   The sleeve term is specifically a DRAWDOWN statistic of the sleeve held ALONE:
                 rho(intercept, sleeve's own MaxDD) is large and stable, and beats the rival
                 sleeve statistics (CAGR, Sharpe, vol, corr-to-book, crash cushion) that a
                 reader could equally have named.  Falsifiable by running all six side by side —
                 this is the leg that can kill "it is a drawdown statistic" while H1 still holds.
  H3 (slope)     613's claim that the SLOPE barely moves with the sleeve.  Falsifiable: measure
                 the dispersion of slope across sleeves inside a (panel, book) cell against the
                 dispersion of intercept in the same cell, in comparable units.
  H4 (KEEP)      Both PROTOCOL 4 paths on every arm-row, and PROTOCOL 8 with (f, sleeve) — the
                 queue's own two parameters — chosen on 2009-2016 alone.

AXES AND WHAT IS SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
  The queue names the two tuned parameters and both are swept in full with every point reported:
    P1 SLEEVE SET : 10 pre-registered sleeves spanning the standalone-drawdown range from 0%
                    (CASH) to a full equity drawdown (SPY1), listed in SLEEVES below.
    P2 f          : the blend fraction, uniform 0.00-0.50 step 0.05 (11 points), 403/613's own
                    dial and the dial whose 4b window IS the width being measured.
  Everything else is a REPORTED axis and is never selected on: panels, books, the lambda
  turnover instrument (idea 137's, verbatim), and the six cost rungs.  The ONLY place anything
  is chosen is PROTOCOL rule 8, where (f, sleeve) is picked on 2009-2016 by four pre-registered
  selectors and 2017-2026 is read exactly once.

WHY THE DRAG AXIS IS CLEAN HERE
  base_to (the cell's f=0 turnover) does not depend on the sleeve at all — at f=0 every sleeve
  collapses to the same book — so the drag axis is IDENTICAL across sleeves inside a
  (panel, book, lambda) cell.  Any movement of the fitted intercept across sleeves is therefore
  a movement of the LEVEL of the width law, not a re-scaling of its x-axis.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 idea 613's four published level numbers reproduced off its committed .windows.csv
     (u56/TOP20 6.90 ETF3 vs 4.35 CASH; broad/EWALL 3.67 vs 0.06) and its two published slope
     pairs (-0.923/-0.847 and -0.930/-0.374).
  G4 sleeve invariance of base_to at f=0 (the paragraph above, measured not assumed).
  G5 the numpy metric core (CAGR/Sharpe/MaxDD) vs `engine.metrics` on a live 10 bps series.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): both panels are current constituents.
  * SMALL439 is EXCLUDED and the exclusion is content, not a gap: it prices no ETF, so 9 of the
    10 sleeves do not exist on it, and idea 613 already found both of its cells INERT (width 0
    at all 48 grid points), so it can contribute no intercept.
  * The sleeve assets are also INVESTABLE names in both panels (403/613's own convention), so
    the TOP20 book can hold a sleeve asset on its own account.  Carried, not fixed.
  * lambda can only LOWER turnover, so the drag axis is one-sided.
  * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * 40 cells is a small population for a rank correlation; the exact permutation p-value over
    sleeve labels is reported beside every headline rho for that reason.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .windows.csv,
.fits.csv, .sleeves.csv, .h2.csv, .walkforward.csv next to itself.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, compare  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-the-INTERCEPT-of-the-width-law-a-DEFENSIVE-SLEEVE-statistic_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I613_WIN = OUT / "2026-09-10_publish-DRAG-not-TURNOVER-beside-every-window-width-claim_cloud.windows.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")                       # idea 94's harness: composite / vol20 / gate_mask
FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60                     # 4b CAGR floor / DD cap fractions of SPY

FSTEP = 0.05
FS = [round(FSTEP * i, 2) for i in range(11)]                 # P2, uniform, never chosen
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]    # idea 137's ladder, verbatim
BOOKS = ["TOP20", "EWALL"]
NTOP = 20
PANELS = ["u56", "broad"]
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

# P1 — the SLEEVE SET, pre-registered to span the standalone-drawdown range end to end.
# CASH is 613's own new sleeve; ETF3 is 403/613's; SPY1 is the null-defensive control.
SLEEVES = {
    "CASH":  [],                       # de-gross to (1-f), zero yield: MaxDD 0 by construction
    "SHY":   ["SHY"],                  # 1-3y treasuries
    "IEF":   ["IEF"],                  # 7-10y treasuries
    "TLT":   ["TLT"],                  # 20y+ treasuries
    "GLD":   ["GLD"],                  # gold
    "UUP":   ["UUP"],                  # dollar
    "ETF3":  ["TLT", "GLD", "UUP"],    # idea 100/104/403/613's sleeve, verbatim
    "BOND2": ["TLT", "IEF"],           # duration-only
    "DEFEQ": ["XLU", "XLP"],           # defensive EQUITY: low beta, full equity drawdown
    "SPY1":  ["SPY"],                  # the market itself: a "sleeve" with no defensive content
}
SLEEVE_ORDER = list(SLEEVES)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# vectorised runner (segment-exact reproduction of engine.backtest at zero cost) — idea 613's
# =====================================================================================
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    idx = px.index
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# =====================================================================================
# books and sleeves (403/613's constructions, verbatim)
# =====================================================================================
def smooth(W, lam):
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


def book_weights(px, book, investable):
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (GROSS / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's defensive sleeve, verbatim: momentum vote x risk parity over the assets.
    With one asset risk parity is identically 1.0, so a single-name sleeve is that name held on
    its own momentum vote — the same construction, not a different one."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f, sleeve):
    """f = the DIAL.  CASH: hold (1-f) of the base book, rest in zero-yield cash (the record's
    de-gross convention).  Any asset sleeve: idea 134/138/403's blend, (1-f)*base + f*sleeve
    rescaled to GROSS per day."""
    if f == 0.0:
        return base_W
    if sleeve == "CASH":
        return base_W * (1.0 - f)
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def sleeve_alone(px, sleeve, sl_W):
    """The sleeve held ALONE at GROSS — the f=1 endpoint of the same blend.  This is the series
    every 'sleeve's own X' statistic in H2 is read off.  CASH alone is a flat zero series."""
    if sleeve == "CASH":
        return pd.Series(0.0, index=px.index)
    raw = sl_W.mul((GROSS / sl_W.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
    return fast_bt(px, raw)[0]


# =====================================================================================
# numpy metric core (gate G5 checks it against engine.metrics to machine precision)
# =====================================================================================
def fmet(a: np.ndarray):
    """(CAGR, Sharpe, MaxDD) off a raw daily-return array — engine.metrics' algebra, no pandas.
    engine.metrics uses pandas .std() (ddof=1), reproduced here."""
    eq = np.cumprod(1.0 + a)
    yrs = len(a) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(a.std(ddof=1) * np.sqrt(252.0))
    sh = float(a.mean() * 252.0 / vol) if vol else np.nan
    return float(cagr), sh, dd


def fsh(a: np.ndarray):
    vol = float(a.std(ddof=1) * np.sqrt(252.0))
    return float(a.mean() * 252.0 / vol) if vol else np.nan


# =====================================================================================
# metric helpers
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def _rank(a: np.ndarray) -> np.ndarray:
    """Average ranks, ties shared — pandas' .rank() default, in numpy."""
    order = np.argsort(a, kind="mergesort")
    r = np.empty(len(a), float)
    r[order] = np.arange(1, len(a) + 1, dtype=float)
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        if j > i:
            r[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    return r


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or len(set(a[ok])) < 2 or len(set(b[ok])) < 2:
        return np.nan
    return float(np.corrcoef(_rank(a[ok]), _rank(b[ok]))[0, 1])


def perm_p_sleeve(df, xcol, ycol, nperm=5000, seed=7):
    """Permutation p over SLEEVE LABELS.  The predictor is a per-(panel, sleeve) constant while
    the outcome varies by cell, so the exchangeable unit is the SLEEVE LABEL, not the cell row —
    a row-shuffled p-value here would be badly anti-conservative.  One relabelling is drawn and
    applied IDENTICALLY in every panel, preserving the design.  Two-sided on |rho|; 10! = 3.6e6
    labellings, so a fixed-seed draw of `nperm` is used and its size is reported."""
    sl = sorted(df.sleeve.unique())
    xmap = df.groupby(["panel", "sleeve"])[xcol].first().to_dict()
    y = df[ycol].values.astype(float)
    pan, slv = df.panel.values, df.sleeve.values
    obs = spearman(df[xcol].values, y)
    if not np.isfinite(obs):
        return np.nan, obs, 0
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(nperm):
        q = rng.permutation(len(sl))
        m = {sl[i]: sl[q[i]] for i in range(len(sl))}
        xp = np.array([xmap[(pan[k], m[slv[k]])] for k in range(len(y))], float)
        v = spearman(xp, y)
        if np.isfinite(v) and abs(v) >= abs(obs) - 1e-12:
            hit += 1
    return hit / nperm, obs, nperm


def window_of(sub, col="pass4b"):
    """Window statistics over ONE cell's uniform f grid (613's, verbatim)."""
    d = sub.sort_values("f")
    p = d[col].values.astype(bool)
    nv = d["f"].values
    best = cur = 0
    blo = bhi = clo = np.nan
    for i, ok in enumerate(p):
        if ok:
            if cur == 0:
                clo = nv[i]
            cur += 1
            if cur > best:
                best, blo, bhi = cur, clo, nv[i]
        else:
            cur = 0
    return dict(n_pass=int(p.sum()), w_pts=int(best),
                w_units=(best - 1) * FSTEP if best > 0 else 0.0,
                f_lo=blo, f_hi=bhi, is_empty=bool(p.sum() == 0))


def ols(x, y):
    """width = a + b*drag.  Returns (a, b, R2) with a = the INTERCEPT this idea is about."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or x.std() == 0:
        return (float(y.mean()) if len(y) else np.nan), 0.0, np.nan
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss = ((y - y.mean()) ** 2).sum()
    return float(a), float(b), (1.0 - ((y - yh) ** 2).sum() / ss) if ss > 0 else np.nan


def r2_dummies(y, labels):
    """R^2 of the one-way group-mean fit — the share of intercept variance a label carries.
    Cells whose target is undefined (an INERT cell has no rank slope) are dropped, and the
    number kept is returned beside the number so a dropped cell can never be read as a zero."""
    d = pd.DataFrame(dict(y=np.asarray(y, float), g=list(labels))).dropna()
    if len(d) < 3:
        return np.nan, len(d)
    fit = d.groupby("g").y.transform("mean")
    ss = ((d.y - d.y.mean()) ** 2).sum()
    return (float(1.0 - ((d.y - fit) ** 2).sum() / ss) if ss > 0 else np.nan), len(d)


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, px in panels.items():
        inv = list(px.columns)
        W = book_weights(px, "TOP20", inv)
        start = px.index[260]
        r_f, t_f = fast_bt(px, W)
        e0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        d_r = float((r_f.loc[start:] - e0["returns"].loc[start:]).abs().max())
        d_t = float((t_f.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        e25 = backtest(px, W, cost_bps=25.0, freq=FREQ)
        d_c = float(((r_f - t_f * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest   max|dr| {d_r:.3e}   max|dturnover| {d_t:.3e}")
        say(f"  G2 {pk:>5}: rung identity vs live 25 bps max|dr| {d_c:.3e}")
        ok &= (d_r < 1e-12) and (d_t < 1e-12) and (d_c < 1e-12)
        # G5 the numpy metric core (the only thing the 21k-row grid is read with) vs engine.metrics
        rr = (r_f - t_f * 10.0 / 1e4).loc[start:]
        cg, sh, dd = fmet(rr.values)
        me = metrics(rr)
        d5 = max(abs(cg - me["CAGR"]), abs(sh - me["Sharpe"]), abs(dd - me["MaxDD"]),
                 abs(fsh(rr.values[:len(rr) // 2]) - metrics(rr.iloc[:len(rr) // 2])["Sharpe"]))
        say(f"  G5 {pk:>5}: numpy metric core vs engine.metrics  max|d| {d5:.3e}")
        ok &= d5 < 1e-12

    # G3 — idea 613's own published levels and slopes, off its committed artefact.
    if I613_WIN.exists():
        w = pd.read_csv(I613_WIN)
        tgt = {("u56", "TOP20", "ETF3"): 6.90, ("u56", "TOP20", "CASH"): 4.35,
               ("broad", "EWALL", "ETF3"): 3.67, ("broad", "EWALL", "CASH"): 0.06}
        slo = {("u56", "TOP20", "ETF3"): -0.923, ("u56", "TOP20", "CASH"): -0.847,
               ("broad", "EWALL", "ETF3"): -0.930, ("broad", "EWALL", "CASH"): -0.374}
        good = 0
        for k, want in tgt.items():
            g = w[(w.panel == k[0]) & (w.book == k[1]) & (w.sleeve == k[2])]
            got = float(g.w_pts.mean())
            gots = spearman(g.w_pts.values, g.drag.values)
            hit = abs(got - want) <= 0.02 and (not np.isfinite(slo[k]) or abs(gots - slo[k]) <= 0.02)
            good += int(hit)
            say(f"  G3 {k[0]:>5} {k[1]:>5} {k[2]:>5}: mean w_pts {got:.2f} (613 published {want:.2f})"
                f"   rho(w,drag) {gots:+.3f} (613 published {slo[k]:+.3f})   {'OK' if hit else 'MISMATCH'}")
        ok &= (good == 4)
    else:
        say("  G3 SKIPPED: idea 613 .windows.csv not found")
        ok = False
    say(f"  GATES(1-3) {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# the grid, one panel at a time
# =====================================================================================
def run_panel(pk, px):
    inv = list(px.columns)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars_full = bars_of(spy, "full")
    bars_is = bars_of(spy, "IS")
    v2r, v2t = fast_bt(px, rules_v2_weights(px))
    v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
    say(f"\n  panel {pk}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"evaluated from {start.date()}")
    say(f"    SPY bars: H1 {bars_full['s1']:.3f}  H2 {bars_full['s2']:.3f}  "
        f"OOS {bars_full['soos']:.3f}  MaxDD {bars_full['sdd']:.1%}  CAGR {bars_full['scagr']:.2%}")

    missing = [s for s, a in SLEEVES.items() if any(t not in px.columns for t in a)]
    if missing:
        say(f"    sleeves not priced on this panel (EXCLUDED, reported): {missing}")
    sl_names = [s for s in SLEEVE_ORDER if s not in missing]

    # --- the sleeve's OWN behaviour, held alone at GROSS (H2's predictors) -------------
    slW = {s: (None if s == "CASH" else sleeve_weights(px, SLEEVES[s])) for s in sl_names}
    top_r = fast_bt(px, book_weights(px, "TOP20", inv))[0].loc[start:]
    srows = []
    for s in sl_names:
        r = sleeve_alone(px, s, slW[s]).loc[start:]
        m, mi = metrics(r), metrics(r.loc[:IS_END])
        q = top_r.quantile(0.05)
        cush = float(r[top_r <= q].mean()) * 1e4          # bps/day on the book's worst 5% days
        cush_is = float(r.loc[:IS_END][top_r.loc[:IS_END] <= top_r.loc[:IS_END].quantile(0.05)].mean()) * 1e4
        srows.append(dict(panel=pk, sleeve=s, assets="+".join(SLEEVES[s]) or "-",
                          sl_CAGR=m["CAGR"], sl_Sharpe=m["Sharpe"], sl_MaxDD=m["MaxDD"],
                          sl_vol=float(r.std() * np.sqrt(252)),
                          sl_corr=float(r.corr(top_r)) if r.std() > 0 else 0.0,
                          sl_cush=cush,
                          sl_CAGR_IS=mi["CAGR"], sl_Sharpe_IS=mi["Sharpe"], sl_MaxDD_IS=mi["MaxDD"],
                          sl_cush_IS=cush_is))
    SS = pd.DataFrame(srows)
    say("\n    the SLEEVE HELD ALONE at gross %.2f (zero cost, full sample) — H2's predictors:" % GROSS)
    say("    " + SS.drop(columns=["panel", "sl_CAGR_IS", "sl_Sharpe_IS", "sl_MaxDD_IS", "sl_cush_IS"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # index positions for the numpy core (identical slices to the pandas ones)
    idx = v2[0.0].index
    n = len(idx)
    hF = n // 2
    iIS = int((idx <= pd.Timestamp(IS_END)).sum())
    iOOS = int(np.searchsorted(idx.values, np.datetime64(pd.Timestamp(OOS_START))))
    hIS = iIS // 2
    v2b = {}
    for c in RUNGS:                        # the 4a comparand, once per rung
        a = v2[c].values
        _, _, d = fmet(a)
        v2b[c] = (fsh(a[:hF]), fsh(a[hF:]), d)

    rows, series = [], {}
    for book in BOOKS:
        raw = book_weights(px, book, inv)
        for lam in LAMBDAS:
            base = smooth(raw, lam)
            r_f0, t_f0 = fast_bt(px, base)                      # f = 0, sleeve-independent
            r_f0 = r_f0.loc[start:].values
            t_f0 = t_f0.loc[start:].values
            base_to_cell = float(t_f0.sum() / (n / 252))
            for sleeve in sl_names:
                for f in FS:
                    if f == 0.0:
                        r0, t0 = r_f0, t_f0
                    else:
                        rr, tt = fast_bt(px, blend(base, slW[sleeve], f, sleeve))
                        r0, t0 = rr.loc[start:].values, tt.loc[start:].values
                    series[(book, sleeve, lam, f)] = (r0, t0)
                    arm_to = float(t0.sum() / (n / 252))
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        cg, sh, dd = fmet(r)
                        h1, h2 = fsh(r[:hF]), fsh(r[hF:])
                        oos = fsh(r[iOOS:])
                        ri = r[:iIS]
                        cgi, shi, ddi = fmet(ri)
                        mg = dict(H1=h1 - bars_full["s1"], H2=h2 - bars_full["s2"],
                                  OOS=oos - bars_full["soos"],
                                  DD=DELTA * abs(bars_full["sdd"]) - abs(dd),
                                  CAGR=cg - PHI * bars_full["scagr"])
                        mgi = dict(H1=fsh(ri[:hIS]) - bars_is["s1"],
                                   H2=fsh(ri[hIS:]) - bars_is["s2"],
                                   DD=DELTA * abs(bars_is["sdd"]) - abs(ddi),
                                   CAGR=cgi - PHI * bars_is["scagr"])
                        b1, b2, bdd = v2b[c]
                        rows.append(dict(
                            panel=pk, book=book, sleeve=sleeve, lam=lam, f=f, cost=c,
                            base_to=base_to_cell, drag=base_to_cell * c / 1e4, arm_to=arm_to,
                            CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2, OOSs=oos,
                            **{f"m_{k}": mg[k] for k in BARS5},
                            m_min=min(mg[k] for k in BARS5),
                            pass4b=all(mg[k] > 0 for k in BARS5),
                            pass4a=bool(h1 > b1 and h2 > b2 and dd >= bdd),
                            IS_pass4b=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                            IS_Sharpe=shi, IS_MaxDD=ddi))
    return pd.DataFrame(rows), series, SS, v2, idx


def walkforward(pk, px, G, series, SS, v2):
    """PROTOCOL 8 — (f, sleeve), the queue's OWN two parameters, chosen on 2009-2016 alone."""
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    idx = spy.index
    spy_o = spy.loc[OOS_START:]
    mo = metrics(spy_o)
    bars_o = dict(s1=metrics(spy_o.iloc[:len(spy_o) // 2])["Sharpe"],
                  s2=metrics(spy_o.iloc[len(spy_o) // 2:])["Sharpe"],
                  sdd=mo["MaxDD"], scagr=mo["CAGR"], soos=mo["Sharpe"])
    isdd = SS.set_index("sleeve").sl_MaxDD_IS.to_dict()      # IS-only, no OOS leakage
    iscg = SS.set_index("sleeve").sl_CAGR_IS.to_dict()
    wf = []
    for (book, lam), sub0 in G[G.panel == pk].groupby(["book", "lam"]):
        for c in RUNGS:
            sub = sub0[sub0.cost == c]
            picks = {"S0_ISsharpe": sub.loc[sub.IS_Sharpe.idxmax()]}
            scr = sub[sub.IS_pass4b]
            picks["S1_IS4b"] = (scr.loc[scr.IS_Sharpe.idxmax()] if len(scr)
                                else sub.loc[sub.IS_Sharpe.idxmax()])
            # the queue's own hypothesis, as a selector: take the sleeve with the SHALLOWEST
            # standalone IS drawdown, then the best IS-Sharpe f inside it.  These three are
            # restricted to f > 0 — a sleeve selector that is allowed to pick f = 0 answers a
            # different question (whether to buy a sleeve at all), and at f = 0 every sleeve is
            # the SAME book, so the pick would carry no sleeve information.  S4 is their
            # like-for-like comparand: the same f > 0 restriction, sleeve chosen by IS Sharpe.
            pos = sub[sub.f > 0]
            sdd_best = min(isdd, key=lambda s: abs(isdd[s]))
            s2 = pos[pos.sleeve == sdd_best]
            picks["S2_minSleeveDD"] = s2.loc[s2.IS_Sharpe.idxmax()]
            scg_best = max(iscg, key=lambda s: iscg[s])
            s3 = pos[pos.sleeve == scg_best]
            picks["S3_maxSleeveCAGR"] = s3.loc[s3.IS_Sharpe.idxmax()]
            picks["S4_ISsharpe_fpos"] = pos.loc[pos.IS_Sharpe.idxmax()]
            for sname, p in picks.items():
                r0, t0 = series[(book, str(p.sleeve), float(p.lam), float(p.f))]
                r = (pd.Series(r0, index=idx) - pd.Series(t0, index=idx) * c / 1e4).loc[OOS_START:]
                m = metrics(r)
                h = len(r) // 2
                o4b = dict(H1=metrics(r.iloc[:h])["Sharpe"] - bars_o["s1"],
                           H2=metrics(r.iloc[h:])["Sharpe"] - bars_o["s2"],
                           OOS=m["Sharpe"] - bars_o["soos"],
                           DD=DELTA * abs(bars_o["sdd"]) - abs(m["MaxDD"]),
                           CAGR=m["CAGR"] - PHI * bars_o["scagr"])
                v2o = v2[c].loc[OOS_START:]
                mv = metrics(v2o)  # engine.metrics on the OOS slice, not the numpy core
                wf.append(dict(panel=pk, book=book, lam=lam, cost=c, selector=sname,
                               f=float(p.f), sleeve=str(p.sleeve),
                               OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                               SPY_CAGR=mo["CAGR"], SPY_Sharpe=mo["Sharpe"], SPY_MaxDD=mo["MaxDD"],
                               V2_CAGR=mv["CAGR"], V2_Sharpe=mv["Sharpe"], V2_MaxDD=mv["MaxDD"],
                               beats_SPY=bool(m["Sharpe"] > mo["Sharpe"]),
                               beats_V2=bool(m["Sharpe"] > mv["Sharpe"]),
                               OOS_4b=all(v > 0 for v in o4b.values()),
                               OOS_4a=pass4a(r, v2o)))
    return pd.DataFrame(wf)


def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 618 — is the INTERCEPT of the width law a DEFENSIVE-SLEEVE statistic?   (lane C)")
    say("=" * 100)
    say(f"tuned parameter 1 (SLEEVE SET): {SLEEVE_ORDER} — all reported")
    say(f"tuned parameter 2 (f)         : {FS} — uniform, fully enumerated, never chosen")
    say(f"reported axes: panels {PANELS}; books {BOOKS}; lambda {LAMBDAS}; rungs {RUNGS} bps")
    say(f"weekly, t+1, gross {GROSS}; IS <= {IS_END}, OOS >= {OOS_START}; "
        f"4b bars = {BARS5} with CAGR floor {PHI} x SPY and DD cap {DELTA} x SPY")
    say("SMALL439 excluded: it prices no ETF (9 of 10 sleeves do not exist on it) and idea 613")
    say("  already found both of its cells INERT (width 0 at all 48 points).")

    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    if not gates(panels):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    say()
    say("=" * 100)
    say("THE GRID (2 panels x 2 books x 10 sleeves x 8 lambdas x 11 f, read at 6 rungs)")
    say("=" * 100)
    G, SSl, WF = [], [], []
    for pk in PANELS:
        px = panels[pk]
        g, ser, ss, v2, _ = run_panel(pk, px)
        G.append(g)
        SSl.append(ss)
        WF.append(walkforward(pk, px, g, ser, ss, v2))
        del ser
    G = pd.concat(G, ignore_index=True)
    SS = pd.concat(SSl, ignore_index=True)
    WF = pd.concat(WF, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    SS.to_csv(OUT / f"{STEM}.sleeves.csv", index=False)
    nsim = G[["panel", "book", "sleeve", "lam", "f"]].drop_duplicates().shape[0]
    say(f"\n  {len(G)} arm-rows ({nsim} weight paths x {len(RUNGS)} rungs).")

    # --- G4: the drag axis is sleeve-invariant -------------------------------------
    piv = G[G.f == 0].pivot_table(index=["panel", "book", "lam"], columns="sleeve", values="base_to")
    dmax = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    say(f"  G4 base_to at f=0 is sleeve-invariant: max spread across sleeves {dmax:.3e} "
        f"({'PASS' if dmax < 1e-12 else 'FAIL'})")

    # --- windows -------------------------------------------------------------------
    W = []
    for (pk, book, sleeve, lam, c), sub in G.groupby(["panel", "book", "sleeve", "lam", "cost"]):
        w = window_of(sub)
        base_to = float(sub.base_to.iloc[0])
        W.append(dict(panel=pk, book=book, sleeve=sleeve, lam=lam, cost=c, base_to=base_to,
                      drag=base_to * c / 1e4, **w, best_margin=float(sub.m_min.max()),
                      binding=min(BARS5, key=lambda k: sub.loc[sub.m_min.idxmax(), "m_" + k])))
    W = pd.DataFrame(W)
    W.to_csv(OUT / f"{STEM}.windows.csv", index=False)

    # --- fits: width = intercept - slope x drag, one fit per (panel, book, sleeve) ---
    say()
    say("-" * 100)
    say("THE LAW, CELL BY CELL — width = a + b x drag over the 48 (lambda, rung) points")
    say("-" * 100)
    say("  a0    = mean width at cost 0 (drag = 0 exactly): the DIRECT intercept measurement")
    say("  a_ols = OLS intercept over all 48 points;  b = OLS slope (width per unit drag)")
    say("  rho   = within-cell Spearman(width, drag) — the 'slope' the queue quotes from 613")
    fits = []
    for (pk, book, sl), sub in W.groupby(["panel", "book", "sleeve"]):
        a, b, r2 = ols(sub.drag.values, sub.w_pts.values)
        a0 = float(sub[sub.cost == 0].w_pts.mean())
        fits.append(dict(panel=pk, book=book, sleeve=sl, a0=a0, a_ols=a, b_ols=b,
                         b_norm=(b / a0 if a0 else np.nan), R2=r2,
                         rho=spearman(sub.w_pts.values, sub.drag.values),
                         mean_w=float(sub.w_pts.mean()), rng=int(sub.w_pts.max() - sub.w_pts.min()),
                         n_empty=int(sub.is_empty.sum()), n=len(sub)))
    F = pd.DataFrame(fits)
    F = F.merge(SS, on=["panel", "sleeve"], how="left")
    F.to_csv(OUT / f"{STEM}.fits.csv", index=False)
    show = ["panel", "book", "sleeve", "a0", "a_ols", "b_ols", "b_norm", "R2", "rho", "mean_w", "rng",
            "n_empty", "sl_MaxDD", "sl_CAGR", "sl_Sharpe", "sl_vol", "sl_corr", "sl_cush"]
    say(F[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # --- H1 variance decomposition ---------------------------------------------------
    say()
    say("-" * 100)
    say(f"H1 — WHOSE statistic is the intercept?  one-way R^2 on {len(F)} cells")
    say("-" * 100)
    for tgt in ("a0", "a_ols", "b_ols", "b_norm", "rho"):
        y = F[tgt].values
        rs, n = r2_dummies(y, F.sleeve)
        rp, _ = r2_dummies(y, F.panel)
        rb, _ = r2_dummies(y, F.book)
        rpb, _ = r2_dummies(y, F.panel + "/" + F.book)
        say(f"  {tgt:>6}: R^2(sleeve label) {rs:6.3f}   R^2(panel) {rp:6.3f}   "
            f"R^2(book) {rb:6.3f}   R^2(panel x book) {rpb:6.3f}   n={n:>2}   "
            f"--> {'SLEEVE' if rs > rpb else 'PANELxBOOK'} carries it")
    say("  (R^2 here is the share of ACROSS-CELL variance a single label explains; the two")
    say("   labels are not nested, so the two numbers are directly comparable.)")

    # --- H2 the ask: WHICH sleeve statistic? ------------------------------------------
    say()
    say("-" * 100)
    say("H2 (THE ASK) — is the sleeve term a DRAWDOWN statistic?  six rival sleeve columns")
    say("-" * 100)
    preds = ["sl_MaxDD", "sl_CAGR", "sl_Sharpe", "sl_vol", "sl_corr", "sl_cush"]
    cellkeys = [(pk, bk) for pk in PANELS for bk in BOOKS]
    say(f"  {'predictor':>10} {'rho pooled':>11} {'perm p':>8} {'n':>4} " +
        "".join(f"{pk + '/' + bk:>14}" for pk, bk in cellkeys))
    h2rows = []
    nperm = 0
    for pcol in preds:
        rp_, obs, nperm = perm_p_sleeve(F.dropna(subset=[pcol, "a0"]), pcol, "a0",
                                        nperm=5000, seed=7)
        cells = []
        for pk, bk in cellkeys:
            sub = F[(F.panel == pk) & (F.book == bk)]
            cells.append(spearman(sub[pcol].values, sub.a0.values))
        nused = int(F[[pcol, "a0"]].notna().all(axis=1).sum())
        h2rows.append(dict(predictor=pcol, rho_pooled=obs, perm_p=rp_, n=nused,
                           **{f"{pk}/{bk}": cells[i] for i, (pk, bk) in enumerate(cellkeys)}))
        say(f"  {pcol:>10} {obs:>+11.3f} {rp_:>8.4f} {nused:>4} " +
            "".join(f"{c:>+14.3f}" for c in cells))
    H2 = pd.DataFrame(h2rows)
    H2.to_csv(OUT / f"{STEM}.h2.csv", index=False)
    say(f"  (perm p = {nperm} random sleeve-label relabellings, fixed seed; the sleeve statistic")
    say("   is a per-sleeve constant so the sleeve LABEL is the only exchangeable unit.)")
    best = H2.loc[H2.rho_pooled.abs().idxmax()]
    say(f"  --> strongest pooled predictor of the intercept: {best.predictor} "
        f"(|rho| {abs(best.rho_pooled):.3f});  sl_MaxDD reads "
        f"{float(H2.loc[H2.predictor=='sl_MaxDD','rho_pooled'].iloc[0]):+.3f}")
    say()
    say("  ROBUSTNESS 1 — the same six columns against the OLS intercept a_ols, and against the")
    say("  cell's mean width, so the answer cannot be an artefact of reading the intercept at")
    say("  the zero rung alone:")
    say(f"  {'predictor':>10} {'rho(a0)':>9} {'rho(a_ols)':>11} {'rho(mean_w)':>12}")
    for pcol in preds:
        say(f"  {pcol:>10} {spearman(F[pcol].values, F.a0.values):>+9.3f} "
            f"{spearman(F[pcol].values, F.a_ols.values):>+11.3f} "
            f"{spearman(F[pcol].values, F.mean_w.values):>+12.3f}")
    say()
    say("  ROBUSTNESS 2 — CASH dropped.  CASH's MaxDD is 0 by CONSTRUCTION, not by measurement,")
    say("  so it is the one point that could manufacture a drawdown correlation on its own:")
    FX = F[F.sleeve != "CASH"]
    say(f"  {'predictor':>10} {'rho(a0) ex-CASH':>16} {'perm p':>8} {'n':>4}")
    for pcol in preds:
        rpx, obsx, _ = perm_p_sleeve(FX.dropna(subset=[pcol, "a0"]), pcol, "a0",
                                     nperm=5000, seed=7)
        say(f"  {pcol:>10} {obsx:>+16.3f} {rpx:>8.4f} "
            f"{int(FX[[pcol, 'a0']].notna().all(axis=1).sum()):>4}")

    # --- H3 slope stability ------------------------------------------------------------
    say()
    say("-" * 100)
    say("H3 — does the SLOPE move with the sleeve as much as the INTERCEPT does?")
    say("-" * 100)
    say(f"  {'panel':>6} {'book':>6} {'a0 range':>10} {'a0 sd/mean':>11} {'b range':>10} "
        f"{'b sd/mean':>11} {'rho range':>10}")
    for (pk, bk), sub in F.groupby(["panel", "book"]):
        say(f"  {pk:>6} {bk:>6} {sub.a0.max()-sub.a0.min():>10.3f} "
            f"{sub.a0.std()/max(abs(sub.a0.mean()),1e-9):>11.3f} "
            f"{sub.b_ols.max()-sub.b_ols.min():>10.3f} "
            f"{sub.b_ols.std()/max(abs(sub.b_ols.mean()),1e-9):>11.3f} "
            f"{sub.rho.max()-sub.rho.min():>10.3f}")
    say("  The queue's own 'slope' is the within-cell rho(width, drag) it quotes from 613")
    say("  (-0.923 vs -0.847; -0.930 vs -0.374).  b_ols is the same slope in RAW width units and")
    say("  therefore scales with the level; b_norm = b_ols / a0 removes that scaling.")
    say(f"  {'panel':>6} {'book':>6} {'b_norm range':>13} {'b_norm sd/mean':>15}")
    for (pk, bk), sub in F.groupby(["panel", "book"]):
        say(f"  {pk:>6} {bk:>6} {sub.b_norm.max()-sub.b_norm.min():>13.3f} "
            f"{sub.b_norm.std()/max(abs(sub.b_norm.mean()),1e-9):>15.3f}")
    say(f"  pooled coefficient of variation: intercept a0 "
        f"{F.a0.std()/max(abs(F.a0.mean()),1e-9):.3f}   slope b "
        f"{F.b_ols.std()/max(abs(F.b_ols.mean()),1e-9):.3f}   b_norm "
        f"{F.b_norm.std()/max(abs(F.b_norm.mean()),1e-9):.3f}   rank slope rho "
        f"{F.rho.std()/max(abs(F.rho.mean()),1e-9):.3f}")

    # --- KEEP paths ---------------------------------------------------------------------
    say()
    say("-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both, on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                               : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>4}  4b {int(s.pass4b.sum()):>4}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    say("  4b passes at PROTOCOL's own 10 bps rung, by sleeve:")
    s10 = G[G.cost == 10]
    for sl, sub in s10.groupby("sleeve"):
        say(f"    {sl:>6}: 4b {int(sub.pass4b.sum()):>4} / {len(sub)}   "
            f"4a {int(sub.pass4a.sum()):>3}   BOTH {int((sub.pass4a & sub.pass4b).sum()):>3}")

    # --- rule 8 --------------------------------------------------------------------------
    say()
    say("-" * 100)
    say("RULE 8 (PROTOCOL 8) — (f, sleeve) chosen on 2009-2016 ONLY, 2017-2026 read once")
    say("-" * 100)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("selector").agg(
        picks=("f", "size"), median_f=("f", "median"),
        modal_sleeve=("sleeve", lambda s: s.mode().iloc[0]),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        beats_V2=("beats_V2", "sum"), OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say()
    for pk in PANELS:
        s = WF[(WF.panel == pk) & (WF.cost == 10)]
        say(f"  {pk:>6} @10 bps  SPY OOS: CAGR {s.SPY_CAGR.iloc[0]:.2%}  Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f}  MaxDD {s.SPY_MaxDD.iloc[0]:.1%}   |   RULES v2 OOS: "
            f"CAGR {s.V2_CAGR.iloc[0]:.2%}  Sharpe {s.V2_Sharpe.iloc[0]:.3f}  "
            f"MaxDD {s.V2_MaxDD.iloc[0]:.1%}")
        for sn, g in s.groupby("selector"):
            say(f"          {sn:>17}: OOS CAGR {g.OOS_CAGR.mean():.2%}  Sharpe "
                f"{g.OOS_Sharpe.mean():.3f}  MaxDD {g.OOS_MaxDD.mean():.1%}  "
                f"4b {int(g.OOS_4b.sum())}/{len(g)}  4a {int(g.OOS_4a.sum())}/{len(g)}  "
                f"sleeves {sorted(set(g.sleeve))}")

    # --- the reference arm, through baseline.compare (PROTOCOL 3), pre-registered ---------
    say()
    say("-" * 100)
    say("PROTOCOL 3 — 403/613's OWN arm through baseline.compare (u56, TOP20, ETF3, f=0.25,")
    say("lambda=1.00, 10 bps).  Pre-registered as the continuity reference; NOT chosen here.")
    say("-" * 100)
    pxu = panels["u56"]
    slw = sleeve_weights(pxu, SLEEVES["ETF3"])
    ref = compare("618 ref: u56 TOP20 + ETF3 f=0.25 (403/613's arm)",
                  lambda p: blend(book_weights(p, "TOP20", list(p.columns)), slw, 0.25, "ETF3"),
                  pxu, freq=FREQ, cost_bps=10)
    for ln in ref["table"].to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
        LOG.append(ln)
    LOG.append("Verdict (4a): " + ref["verdict"])

    say()
    say("=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
