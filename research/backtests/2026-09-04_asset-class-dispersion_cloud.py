#!/usr/bin/env python3
"""QUEUE idea 73 — asset-class-dispersion (cloud, 2026-09-04).

Question
--------
Idea 10 killed the ETF-only book with a clean but unexplained number: at matched
construction, days and gross, the 36-ETF panel had LOWER vol than the same book on
the 56-name list in 10 of 10 pairs and still lost Sharpe in 20 of 20, because return
fell more than risk did (-6.15%/yr, t to -5.31).  Idea 73 proposes the mechanism:
a RANKED book can only earn what the cross-section offers it, so if 12-1 momentum
is tightly bunched inside a panel there is nothing for the ranking to pick, and the
book collapses onto its own equal-weight control while still paying the turnover.

That makes a falsifiable prediction with a natural dependent variable.  The right
thing to measure is not the book's Sharpe (which mixes in the panel's beta, its
drift and its survivorship) but the RANKING PREMIUM — the ranked book minus the
unranked equal-weight-all-eligible book on the SAME panel, same gate, same gross,
same days.  Everything except the ranking cancels.  If dispersion is the mechanism,
the premium should track dispersion; if it does not, idea 10's ETF result is about
asset class and the "dispersion floor" has no place in RULES.

Three tests, in increasing order of how much confounding they remove:
  (A) CROSS-PANEL.  Seven panels spanning ETFs, mega-caps, large caps and sub-$2B
      names.  Weakest test: panel identity confounds dispersion with asset class,
      sample and survivorship, and there are only seven points.
  (B) WITHIN-PANEL, ACROSS TIME.  Sort each panel's weeks into quintiles of its own
      TRAILING dispersion (known at the close before the week — no look-ahead) and
      measure the ranked-minus-unranked excess inside each quintile.  Panel identity
      is held fixed; only the regime varies.
  (C) WITHIN-PANEL, ACROSS COMPOSITION.  Draw 150 random 36-name sub-panels from the
      136-name broad list (matching ETF36's size), run the same two books on each,
      and regress the draw's ranking premium on the draw's own dispersion.  Asset
      class, sample and gate are identical across draws; dispersion varies only by
      which names are in the panel.  This is the test that can actually separate
      "dispersion" from "ETFs".

Design (PROTOCOL rules 1-8)
---------------------------
Panels   : U56 / ETF36 / ETF24 / STK20 (research/universe.json, idea 10's split),
           B136 / BSTK100 (research/universe_broad.json), SMALL439 (the sub-$2B panel,
           with the 44 tickers whose max_1d_move >= 1.0 dropped per data/small_meta.csv).
           SPY is joined to every panel as a BENCHMARK ONLY and is never tradable in
           the stock-leg or small panels.
Books    : `EWall`   — equal-weight every 200d/vol20-eligible name at 75% gross (no
                       ranking at all): the unranked control.
           `CANDg-n` — top-n of the same eligible set by the composite WITHOUT the
                       /sqrt(vol20) term, equal-weighted to the SAME 75% gross.  This
                       is the arm the idea's question needs, because it differs from
                       EWall only in which eligible names are held.
           `CAND-n`  — idea 2's literal construction, 75%/n per name.  Reported for
                       continuity with ideas 2/10/55, but on a panel with fewer than n
                       eligible names it is the unranked book at reduced gross, so its
                       "premium" is mostly de-grossing and must not be read as ranking.
Params   : ONE tuned dimension, n in {5, 10, 20}.  The panel is the subject of the
           idea, not a tuned parameter, and every panel x n cell is printed.
Costs    : 5 / 10 / 25 bps; 10 bps is the PROTOCOL cost and the one verdicts are read
           at.  Costs are applied analytically (returns(c) = gross - turnover*c/1e4),
           exact because the held path does not depend on cost_bps and asserted below.
Execution: weights decided at close t, applied at t+1 (engine), weekly, long-only.
Rule 8   : (panel, n) chosen on 2009-2016 only under two rules fixed BEFORE any OOS
           number is read; 2017-2026 evaluated untouched.

SURVIVORSHIP: every panel is current constituents, one-directional, and it is WORST
on SMALL439 and STK20 (a mega-cap list is mega-cap because it won).  It inflates the
level of every CAGR here.  The ranking premium is much less exposed — both books hold
the same survivors on the same days from the same gate — but not immune: survivorship
flatters the beaten-down cohort's absent losers, which is exactly the cohort a ranked
book underweights, so it biases the premium DOWNWARD on the small panel.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

GROSS = 0.75
MAX_VOL = 0.60
NS = [5, 10, 20]
COSTS = [5, 10, 25]
PROTO_COST = 10
FREQ = "W"
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
N_DRAWS = 150
DRAW_SIZE = 36
SEED = 20260904
SCRIPT = "research/backtests/2026-09-04_asset-class-dispersion_cloud.py"


# ---------------------------------------------------------------- panels
def build_panels():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    g = {k: [t for t in v if t not in crypto] for k, v in U.items()}
    etf36 = g["broad"] + g["sectors"] + g["bonds_fx_commod"]
    etf24 = g["broad"] + g["sectors"]
    stk20 = g["megacap"]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small = [c for c in pxs.columns if c != "SPY" and c not in bad]

    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    def sub(px, cols):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(cols)

    return {
        "U56": sub(px56, list(px56.columns)),
        "ETF36": sub(px56, etf36),
        "ETF24": sub(px56, etf24),
        "STK20": sub(px56, stk20),
        "B136": sub(px136, [c for c in px136.columns if c != "SPY"]),
        "BSTK100": sub(px136, b_stk),
        "SMALL439": sub(pxs, small),
    }


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def elig_mask(px, tradable):
    _, above, vol20 = score(px)
    mk = above & (vol20 < MAX_VOL)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        mk = mk.copy()
        mk[drop] = False
    return mk


def w_ewall(px, tradable):
    e = elig_mask(px, tradable).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def w_cand(px, tradable, n):
    """Idea 2's literal construction: GROSS/n per name, so the book runs BELOW full gross
    whenever fewer than n names are eligible."""
    rank = composite(px).where(elig_mask(px, tradable)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def w_candg(px, tradable, n):
    """Top-n, equal-weighted to FULL gross across the names actually selected.

    This is the arm the idea needs.  On a small panel the literal CAND-n book is not a
    ranking at all — with 13.2 names eligible on average, STK20's `CAND-n20` holds every
    eligible name at GROSS/20 each, i.e. it is the unranked book at 49% gross, and idea 66
    showed gross alone moves CAGR and MaxDD hard with no Sharpe content.  Comparing that
    to a 75%-gross EWall measures de-grossing, not selection.  Normalising to full gross
    makes CAND minus EWall a pure ranking contrast: identical gate, identical gross,
    identical days, differing only in WHICH eligible names are held.
    """
    rank = composite(px).where(elig_mask(px, tradable)).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


# ---------------------------------------------------------------- dispersion
def dispersion(px, tradable):
    """Cross-sectional spread of the 12-1 momentum signal among ELIGIBLE names, per day.

    Three measures because no single one is obviously right: std is the natural scale
    parameter, IQR is robust to the one runaway name, and the D1-D10 gap is literally
    what a top-n ranked book tries to harvest.  All are computed from data available at
    the close (12-1 momentum uses shift(21)/shift(252)), so they can condition a trade.
    fwd_disp is the cross-sectional std of the NEXT 21 days' return — forward-looking,
    reported for description only and never used to choose anything.
    """
    mom = px.shift(21) / px.shift(252) - 1
    e = elig_mask(px, tradable)
    mo = mom.where(e)
    q1, q3 = mo.quantile(0.25, axis=1), mo.quantile(0.75, axis=1)
    d1 = mo.apply(lambda r: r.nlargest(max(int(r.count() * 0.1), 1)).mean(), axis=1)
    d10 = mo.apply(lambda r: r.nsmallest(max(int(r.count() * 0.1), 1)).mean(), axis=1)
    fwd = (px.shift(-21) / px - 1).where(e)
    return pd.DataFrame({"disp_std": mo.std(axis=1), "disp_iqr": q3 - q1,
                         "disp_d1d10": d1 - d10, "fwd_disp": fwd.std(axis=1),
                         "n_elig": e.sum(axis=1)})


# ---------------------------------------------------------------- stats helpers
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def paired_t(a, b):
    d = (a - b).dropna()
    sd = d.std()
    if not np.isfinite(sd) or sd == 0:
        return 0.0, 0.0
    return float(d.mean() * 252), float(d.mean() / (sd / np.sqrt(len(d))))


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, np.nan
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    r = np.corrcoef(rx, ry)[0, 1]
    t = r * np.sqrt((len(x) - 2) / max(1 - r ** 2, 1e-12))
    return float(r), float(t)


def ols(x, y):
    """slope, t(slope), R2 — plain OLS with a constant."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3:
        return np.nan, np.nan, np.nan
    X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (n - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    ss = ((y - y.mean()) ** 2).sum()
    return float(beta[1]), float(beta[1] / se if se else np.nan), float(1 - resid @ resid / ss if ss else np.nan)


def at_cost(gross, turn, bps):
    return gross - turn * bps / 1e4


def turn_per_yr(t):
    return t.sum() / (len(t) / 252)


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r)
    h1, h2 = halves(r)
    _, _, bdd = m(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def run(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


# ---------------------------------------------------------------- main
def main():
    panels = build_panels()

    # -------- harness
    print("HARNESS CHECKS")
    px56, trad56 = panels["U56"]
    st = px56.index[260]
    gr, tu = run(px56, w_cand(px56, trad56, 20), st)
    real = backtest(px56, w_cand(px56, trad56, 20), cost_bps=PROTO_COST,
                    freq=FREQ)["returns"].loc[st:]
    err = float((at_cost(gr, tu, PROTO_COST) - real).abs().max())
    print(f"  analytic-cost identity vs engine cost_bps=10: max abs daily diff {err:.2e} "
          f"({'OK' if err < 1e-12 else 'MISMATCH'})")
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 2 KEEP row (U56/CAND-n20): {c:.1%}/{s:.3f}/{dd:.1%}   [published 12.7%/1.093/-18.3%]")
    gr2, tu2 = run(px56, w_ewall(px56, trad56), st)
    c, s, dd = m(at_cost(gr2, tu2, PROTO_COST))
    print(f"  idea 28/4 EWall control (U56):  {c:.1%}/{s:.3f}/{dd:.1%}   [published 10.4%/1.05/-15.9%]")
    pxE, tradE = panels["ETF36"]
    grE, tuE = run(pxE, w_cand(pxE, tradE, 20), pxE.index[260])
    c, s, dd = m(at_cost(grE, tuE, PROTO_COST))
    print(f"  idea 10 ETF36/CAND-n20:         {c:.1%}/{s:.3f}/{dd:.1%}   [published 6.8%/0.817/-15.2%]")
    for nm in panels:
        p = panels[nm][0]
        y = p.index.to_series().groupby(p.index.year).count()
        if y.loc[2015:2024].max() > 300:
            sys.exit(f"!! CALENDAR-DAY INDEX in {nm} — aborting")
    print("  trading-day index confirmed on all 7 panels")

    # -------- per-panel grid
    rows = []
    RET = {}
    DISP = {}
    print(f"\n{'=' * 150}\nPANEL GRID at 5/10/25 bps — every panel x arm printed. "
          f"`prem` = this arm's Sharpe minus the SAME panel's unranked EWall book.\n" + "=" * 150)
    for nm, (px, trad) in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        sc, ss, sdd = m(spy)
        s1, s2 = halves(spy)
        _, ss_o, _ = m(spy.loc[OOS_START:])
        base_v1 = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST,
                           freq=FREQ)["returns"].loc[start:]
        d = dispersion(px, trad).loc[start:]
        DISP[nm] = d
        arms = ({"EWall": w_ewall(px, trad)}
                | {f"CANDg-n{n}": w_candg(px, trad, n) for n in NS}
                | {f"CAND-n{n}": w_cand(px, trad, n) for n in NS})
        G = {a: run(px, w, start) for a, w in arms.items()}
        INV = {a: float(backtest(px, w, cost_bps=0.0, freq=FREQ)["weights"].loc[start:].sum(axis=1).mean())
               for a, w in arms.items()}
        print(f"\n{nm}: {len(trad)} tradable, {start.date()} -> {px.index[-1].date()}, "
              f"mean eligible {d.n_elig.mean():.1f} | SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} "
              f"halves {s1:.3f}/{s2:.3f} OOS {ss_o:.3f}")
        print(f"  dispersion (12-1 mom among eligible): std {d.disp_std.mean():.4f}  "
              f"IQR {d.disp_iqr.mean():.4f}  D1-D10 {d.disp_d1d10.mean():.4f}  "
              f"fwd21d-ret std {d.fwd_disp.mean():.4f}")
        print(f"  {'arm':<11}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'turn':>7}{'inv':>7}"
              f"{'H1':>7}/{'H2':<6}{'OOS':>7}{'prem':>8}{'annΔ':>8}{'t':>7}   verdict")
        ew_by_cost = {c: at_cost(*G["EWall"], c) for c in COSTS}
        for a in arms:
            for cost in COSTS:
                r = at_cost(*G[a], cost)
                RET[(nm, a, cost)] = r
                cg, sh, dd_ = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                ew = ew_by_cost[cost]
                prem = sh - m(ew)[1]
                ann, t = paired_t(r, ew)
                v4a = fail4a(r, base_v1)
                v4b = fail4b(r, spy, oos, ss_o)
                v = ("KEEP 4a" if not v4a else "KILL 4a") + "/" + \
                    ("KEEP 4b" if not v4b else "KILL 4b(" + ",".join(v4b) + ")")
                mark = " <-" if cost == PROTO_COST else ""
                print(f"  {a:<11}{cost:5d}{cg:8.1%}{sh:8.3f}{dd_:8.1%}{turn_per_yr(G[a][1]):6.1f}x"
                      f"{INV[a]:7.1%}{h1:7.3f}/{h2:<6.3f}{oos:7.3f}{prem:+8.3f}{ann * 100:+8.2f}"
                      f"{t:+7.2f}   {v}{mark}")
                if cost == PROTO_COST:
                    rows.append(dict(panel=nm, arm=a, kind=a.split("-")[0],
                                     n=(0 if a == "EWall" else int(a.split("-n")[1])),
                                     cagr=cg, sharpe=sh, dd=dd_, h1=h1, h2=h2, oos=oos,
                                     prem=prem, ann=ann, t=t, turn=turn_per_yr(G[a][1]),
                                     inv=INV[a], pass4a=not v4a, pass4b=not v4b,
                                     disp_std=d.disp_std.mean(), disp_iqr=d.disp_iqr.mean(),
                                     disp_d1d10=d.disp_d1d10.mean(), fwd=d.fwd_disp.mean()))
    df = pd.DataFrame(rows)

    # -------- (A) cross-panel
    print(f"\n{'=' * 150}\n(A) CROSS-PANEL — does the ranking premium track dispersion across "
          f"panels?  (7 panels; the weakest of the three tests)\n" + "=" * 150)
    print("  Premium = arm Sharpe minus the same panel's EWall Sharpe at 10 bps.  CANDg is the")
    print("  gross-normalised ranked book (the clean contrast); CAND is idea 2's literal GROSS/n")
    print("  book, whose premium on a small panel is mostly de-grossing — both are shown.")
    print(f"  {'panel':<10}{'n_elig':>8}{'disp_std':>10}{'disp_iqr':>10}{'D1-D10':>10}{'fwd_std':>10}"
          + "".join(f"{'CANDg n' + str(n):>11}" for n in NS)
          + "".join(f"{'CAND n' + str(n):>11}" for n in NS) + f"{'EWall Sh':>10}")
    for nm in panels:
        sl = df[df.panel == nm]
        e = sl[sl.arm == "EWall"].iloc[0]
        ne = DISP[nm].n_elig.mean()
        print(f"  {nm:<10}{ne:8.1f}{e.disp_std:10.4f}{e.disp_iqr:10.4f}{e.disp_d1d10:10.4f}"
              f"{e.fwd:10.4f}"
              + "".join(f"{sl[(sl.n == n) & (sl.kind == 'CANDg')].iloc[0].prem:+11.3f}" for n in NS)
              + "".join(f"{sl[(sl.n == n) & (sl.kind == 'CAND')].iloc[0].prem:+11.3f}" for n in NS)
              + f"{e.sharpe:10.3f}")
    for kind in ("CANDg", "CAND"):
        for meas in ("disp_std", "disp_iqr", "disp_d1d10", "fwd"):
            line = f"  Spearman(mean {meas}, {kind} premium) across panels:"
            for n in NS:
                sl = df[(df.n == n) & (df.kind == kind)]
                r, t = spearman(sl[meas], sl.prem)
                line += f"   n={n}: rho {r:+.3f} (t {t:+.2f})"
            print(line)
    print("  NOTE: a panel whose mean eligible count is below n cannot rank at all at that n — "
          "the\n        top-n IS the eligible set, so CANDg-n collapses onto EWall by construction.")

    # -------- (B) within-panel, across time
    print(f"\n{'=' * 150}\n(B) WITHIN-PANEL, ACROSS TIME — weeks sorted into quintiles of the "
          f"panel's OWN trailing dispersion (known at the prior close).\n"
          f"    Value shown is the ranked (CANDg-n10, gross-matched) minus unranked (EWall) return, annualised, "
          f"inside each quintile, at 10 bps.\n" + "=" * 150)
    print(f"  {'panel':<10}{'measure':<12}" + "".join(f"{'Q' + str(q):>10}" for q in range(1, 6))
          + f"{'Q5-Q1':>10}{'t(Q5-Q1)':>10}{'mono?':>8}")
    pooled = {mz: [] for mz in ("disp_std", "disp_d1d10")}
    for nm, (px, trad) in panels.items():
        d = DISP[nm]
        r = RET[(nm, "CANDg-n10", PROTO_COST)] - RET[(nm, "EWall", PROTO_COST)]
        for meas in ("disp_std", "disp_d1d10"):
            cond = d[meas].shift(1).reindex(r.index)          # strictly prior information
            q = pd.qcut(cond, 5, labels=False, duplicates="drop")
            cells = [r[q == i] for i in range(5)]
            mus = [float(c.mean() * 252 * 100) if len(c) else np.nan for c in cells]
            a, b = cells[4], cells[0]
            diff = a.mean() - b.mean()
            se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            t = float(diff / se) if se else np.nan
            mono = all(mus[i] <= mus[i + 1] for i in range(4))
            pooled[meas].append((nm, mus[4] - mus[0], t))
            print(f"  {nm:<10}{meas:<12}" + "".join(f"{v:10.2f}" for v in mus)
                  + f"{mus[4] - mus[0]:10.2f}{t:10.2f}{'yes' if mono else 'no':>8}")
    for meas, lst in pooled.items():
        pos = sum(1 for _, dd_, _ in lst if dd_ > 0)
        sig = sum(1 for _, _, t in lst if abs(t) > 2)
        print(f"  POOLED {meas}: Q5-Q1 positive in {pos} of {len(lst)} panels, "
              f"|t|>2 in {sig}; mean Q5-Q1 {np.mean([d_ for _, d_, _ in lst]):+.2f}pp/yr")

    # -------- panel-year pooled regression
    print(f"\n  PANEL-YEAR REGRESSION — one point per (panel, calendar year): "
          f"y = ranked-minus-unranked return that year, x = that year's mean dispersion.")
    print("    Reported twice: POOLED (which still contains the between-panel variation test A")
    print("    already showed is uninformative) and WITHIN (panel fixed effects — x and y demeaned")
    print("    by panel, so only year-to-year variation inside a panel identifies the slope).")
    for meas in ("disp_std", "disp_d1d10"):
        X, Y, P = [], [], []
        for nm in panels:
            d = DISP[nm]
            r = RET[(nm, "CANDg-n10", PROTO_COST)] - RET[(nm, "EWall", PROTO_COST)]
            for y in sorted(set(r.index.year)):
                rr, dd_ = r[r.index.year == y], d[d.index.year == y][meas]
                if len(rr) > 100:
                    X.append(dd_.mean())
                    Y.append(float((1 + rr).prod() - 1) * 100)
                    P.append(nm)
        b, t, r2 = ols(X, Y)
        rho, rt = spearman(X, Y)
        print(f"    {meas:<12} POOLED n={len(X):3d}  slope {b:+8.2f} pp per unit  t {t:+6.2f}  "
              f"R2 {r2:6.3f}   Spearman {rho:+.3f} (t {rt:+.2f})")
        dfp = pd.DataFrame({"x": X, "y": Y, "p": P})
        xw = dfp.x - dfp.groupby("p").x.transform("mean")
        yw = dfp.y - dfp.groupby("p").y.transform("mean")
        bw, tw, r2w = ols(xw, yw)
        rw, rtw = spearman(xw, yw)
        print(f"    {meas:<12} WITHIN n={len(X):3d}  slope {bw:+8.2f} pp per unit  t {tw:+6.2f}  "
              f"R2 {r2w:6.3f}   Spearman {rw:+.3f} (t {rtw:+.2f})")

    # -------- (C) random sub-panels
    print(f"\n{'=' * 150}\n(C) WITHIN-PANEL, ACROSS COMPOSITION — {N_DRAWS} random {DRAW_SIZE}-name "
          f"sub-panels of B136 (ETF36's size), same gate, same days, same gross.\n"
          f"    Asset class and sample are held fixed; only WHICH names are in the panel varies, "
          f"so dispersion is the only thing moving.\n" + "=" * 150)
    px136, trad136 = panels["B136"]
    start = px136.index[260]
    names = sorted(trad136)
    rng = np.random.default_rng(SEED)
    dx, dy, dew, dcand = [], [], [], []
    for i in range(N_DRAWS):
        pick = list(rng.choice(names, DRAW_SIZE, replace=False))
        cols = list(dict.fromkeys(pick + ["SPY"]))
        p = px136[cols]
        tr = set(pick)
        dsp = dispersion(p, tr).loc[start:]
        rew = at_cost(*run(p, w_ewall(p, tr), start), PROTO_COST)
        rcd = at_cost(*run(p, w_candg(p, tr, 10), start), PROTO_COST)
        dx.append(dsp.disp_std.mean())
        dy.append(m(rcd)[1] - m(rew)[1])
        dew.append(m(rew)[1])
        dcand.append(m(rcd)[1])
        if (i + 1) % 50 == 0:
            print(f"    ... {i + 1}/{N_DRAWS} draws")
    b, t, r2 = ols(dx, dy)
    rho, rt = spearman(dx, dy)
    print(f"  dispersion across draws: min {min(dx):.4f}  median {np.median(dx):.4f}  "
          f"max {max(dx):.4f}   (ETF36 sits at {df[df.panel == 'ETF36'].iloc[0].disp_std:.4f}, "
          f"B136 at {df[df.panel == 'B136'].iloc[0].disp_std:.4f})")
    print(f"  ranking premium (CANDg-n10 minus EWall Sharpe): mean {np.mean(dy):+.3f}  "
          f"sd {np.std(dy):.3f}  positive in {sum(1 for v in dy if v > 0)} of {N_DRAWS} draws")
    print(f"  REGRESSION premium ~ dispersion:  slope {b:+.3f} Sharpe per unit  t {t:+.2f}  "
          f"R2 {r2:.3f}   Spearman {rho:+.3f} (t {rt:+.2f})")
    lo = [dy[i] for i in np.argsort(dx)[:N_DRAWS // 3]]
    hi = [dy[i] for i in np.argsort(dx)[-N_DRAWS // 3:]]
    se = np.sqrt(np.var(hi, ddof=1) / len(hi) + np.var(lo, ddof=1) / len(lo))
    print(f"  top vs bottom dispersion TERCILE of draws: premium {np.mean(hi):+.3f} vs "
          f"{np.mean(lo):+.3f}, difference {np.mean(hi) - np.mean(lo):+.3f} (t {(np.mean(hi) - np.mean(lo)) / se:+.2f})")
    b2, t2, r22 = ols(dx, dcand)
    b3, t3, r23 = ols(dx, dew)
    print(f"  control — the same regression on the LEVELS: CANDg-n10 Sharpe slope {b2:+.3f} "
          f"(t {t2:+.2f}, R2 {r22:.3f}); EWall Sharpe slope {b3:+.3f} (t {t3:+.2f}, R2 {r23:.3f})")
    print(f"  ... so dispersion moves BOTH books, and only {b / b2:.0%} of its effect on the ranked "
          f"book's Sharpe is differential.  Most of it is 'this panel went up', not 'ranking worked'.")

    # The draw regression implies a break-even dispersion.  It is fitted ONLY on B136 sub-panels,
    # so the seven panels are an out-of-sample check on it — a real prediction, not a restatement.
    Xd = np.column_stack([np.ones(len(dx)), dx])
    a0, a1 = np.linalg.lstsq(Xd, np.asarray(dy), rcond=None)[0]
    be = -a0 / a1
    print(f"\n  BREAK-EVEN DISPERSION implied by the draws: premium = {a0:+.3f} {a1:+.3f}*disp "
          f"-> zero at disp_std = {be:.3f}")
    print(f"  (the draws only span {min(dx):.3f}-{max(dx):.3f}, so this is an EXTRAPOLATION; the "
          f"seven panels are the out-of-sample check)")
    print(f"  {'panel':<10}{'disp_std':>10}{'predicted':>11}{'actual n10 prem':>17}   sign agrees?")
    agree = 0
    for nm in panels:
        e = df[(df.panel == nm) & (df.arm == "EWall")].iloc[0]
        act = df[(df.panel == nm) & (df.kind == "CANDg") & (df.n == 10)].iloc[0].prem
        pred = a0 + a1 * e.disp_std
        ok = (pred > 0) == (act > 0)
        agree += ok
        print(f"  {nm:<10}{e.disp_std:10.4f}{pred:+11.3f}{act:+17.3f}   {'yes' if ok else 'NO':>12}")
    print(f"  sign agreement: {agree} of {len(panels)} panels")

    # -------- rule 8
    print(f"\n{'=' * 150}\nRule 8 walk-forward — (panel, n) chosen on IS 2009-2016 only, "
          f"evaluated untouched on {OOS_START}-2026, at {PROTO_COST} bps.\n" + "=" * 150)
    spy56 = px56["SPY"].pct_change().fillna(0).loc[st:]
    isc, iss, isdd = m(spy56.loc[:IS_END])
    oc_s, osh_s, odd_s = m(spy56.loc[OOS_START:])
    print(f"  Reference SPY: IS {isc:.1%}/{iss:.3f}/{isdd:.1%}  OOS {oc_s:.1%}/{osh_s:.3f}/{odd_s:.1%}"
          f"   4b-aware IS bars: MaxDD>={0.60 * isdd:.1%}, CAGR>={0.70 * isc:.1%}")
    print(f"  {'panel':<10}{'arm':<10}{'IS CAGR':>9}{'IS Sh':>8}{'IS DD':>8}   "
          f"{'OOS CAGR':>9}{'OOS Sh':>8}{'OOS DD':>8}{'IS prem':>9}{'OOS prem':>10}")
    cand = []
    for nm in panels:
        ew = RET[(nm, "EWall", PROTO_COST)]
        for n in NS:
            r = RET[(nm, f"CANDg-n{n}", PROTO_COST)]
            ic, ish, idd = m(r.loc[:IS_END])
            oc, osh, odd = m(r.loc[OOS_START:])
            ip = ish - m(ew.loc[:IS_END])[1]
            op = osh - m(ew.loc[OOS_START:])[1]
            cand.append((nm, n, ic, ish, idd, oc, osh, odd, ip, op))
            print(f"  {nm:<10}{'CANDg-n' + str(n):<10}{ic:9.1%}{ish:8.3f}{idd:8.1%}   "
                  f"{oc:9.1%}{osh:8.3f}{odd:8.1%}{ip:+9.3f}{op:+10.3f}")

    def clears(c):
        return c[6] > osh_s and c[7] >= 0.60 * odd_s and c[5] >= 0.70 * oc_s

    r1 = max(cand, key=lambda x: x[3])
    ok = [c for c in cand if c[4] >= 0.60 * isdd and c[2] >= 0.70 * isc]
    r2 = max(ok, key=lambda x: x[3]) if ok else None
    print(f"  RULE A (max IS Sharpe)      -> {r1[0]}/CANDg-n{r1[1]}: OOS {r1[5]:.1%}/{r1[6]:.3f}/"
          f"{r1[7]:.1%} [{'clears' if clears(r1) else 'FAILS'} OOS 4b bars]")
    if r2:
        print(f"  RULE B (4b-aware IS filter) -> {r2[0]}/CANDg-n{r2[1]}: OOS {r2[5]:.1%}/{r2[6]:.3f}/"
              f"{r2[7]:.1%} [{'clears' if clears(r2) else 'FAILS'} OOS 4b bars]")
    else:
        print("  RULE B (4b-aware IS filter) -> NOTHING selected")
    ip = spearman([c[8] for c in cand], [c[9] for c in cand])
    print(f"  Does the IS ranking premium predict the OOS ranking premium? "
          f"Spearman {ip[0]:+.3f} (t {ip[1]:+.2f}) over {len(cand)} (panel, n) points.")

    # -------- summary
    print(f"\n{'=' * 150}\nSUMMARY\n" + "=" * 150)
    print(f"  4b passes: {[f'{r.panel}/{r.arm}' for _, r in df[df.pass4b].iterrows()]}")
    print(f"  4a passes: {[f'{r.panel}/{r.arm}' for _, r in df[df.pass4a].iterrows()]}")
    pr = df[(df.n > 0) & (df.kind == "CANDg")]
    print(f"  gross-matched ranking premium positive in {int((pr.prem > 0).sum())} of {len(pr)} "
          f"(panel, n) cells at 10 bps; |t|>2 in {int((pr.t.abs() > 2).sum())}")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
