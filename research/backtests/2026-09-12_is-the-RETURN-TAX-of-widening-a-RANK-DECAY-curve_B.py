#!/usr/bin/env python3
"""Idea 589 - is the RETURN TAX of widening a RANK DECAY curve?  (lane B, 2026-09-12)

Idea 320 measured the width dial (how many ranked names a book holds) and found an
ASYMMETRY: widening's VOL benefit is bunched (+0.190..+0.443 over 6 cells) while its
RETURN cost is 1.5x more dispersed (-0.546..-0.149).  It called the dispersed leg the
panel-specific part - the TAX - but never measured the tax itself.  This run measures it
directly and asks what predicts it.

THE OBJECT.  For a panel, a date t and the record's v1 eligibility (above the 200d MA,
vol20 < 0.60, priced), rank every eligible name by the v1 composite score and let

    mu(k) = mean forward return of the k-th RANKED eligible name,

the forward leg running close t+1 -> close t'+1 where t' is the next weekly rebalance
(exactly the engine's next-day execution).  mu(k) as a function of k is the RANK DECAY
CURVE.  Its partial means M(n) = (1/n) sum_{k<=n} mu(k) are, by construction, the
arithmetic mean return of an equal-weight top-n basket held one rebalance period, so the
decay curve makes an ARITHMETIC prediction about the width dial:

    d(AnnRet)/dn from n -> n'  ==  g * 52 * (M(n') - M(n)) / (n' - n)          [H_DECAY]

That prediction is NOT trivially true of a traded book: the engine drifts weights between
rebalances, de-grosses to cash when fewer than n names are eligible, pays 10 bps of
turnover, and compounds.  H_DECAY is the hypothesis that none of that matters - that the
tax IS the decay curve.

THE RIVAL the queue names is the panel's NAME COUNT:

    the width slope is a function of N (how many names the panel has)           [H_N]

Both are tested on the same cells, and the decay curve is re-measured in each era so the
relationship itself can be walked forward (rule 8) rather than only the book.

BOOKS.  book(n, g) = baseline.rules_v1_weights(px, n=n, w=g/n): rank eligible names by the
v1 score, hold the top n at g/n of NAV each, the rest CASH, weekly cadence.  Gross is g
when >= n names are eligible and less otherwise (de-gross, never re-spread) - the record's
convention.  TWO TUNED PARAMETERS, as PROTOCOL 4 allows: the width n (10 levels) and the
gross g (2 levels).  All 10 x 2 x 3 panels = 60 books are reported, every one of them, at
cost rungs 0 / 10 / 25 bps (10 bps is the headline everywhere, PROTOCOL rule 2).  Nothing
else is fitted; panel, era and cost are reported axes, not dials.

PANELS.  U56 (research/universe.json), B136 (research/universe_broad.json), SMALL716
(data/prices_small.csv.gz).  SURVIVORSHIP: all three are current-constituent lists, so
every LEVEL below is optimistic.  The object of this run is a WITHIN-PANEL slope in n and
a prediction of that slope from a curve measured on the same panel and window, which
survivorship moves far less than it moves levels.

CONVENTION NOTE (stated, not hidden): SPY is excluded from the TRADEABLE set on all three
panels - it is the benchmark, and holding the benchmark inside a ranked book contaminates
a rank-decay measurement.  baseline.rules_v2_weights (the live book, used for the 4a
comparand) is called unmodified and therefore DOES hold SPY on U56/B136; that difference
is a level effect on the comparand, not on any slope measured here.

KEEP.  Both paths are evaluated at 10 bps on every one of the 60 books, full sample and
both halves (4a vs the live RULES v2 baseline on the same panel; 4b vs SPY).  Rule 8: n
and g are chosen on 2009-2016 IS Sharpe alone, per panel, and 2017-2026 is read exactly
once, reported against the baseline and SPY on the same window.

Outputs (all committed, all under research/):
  .txt          full console log
  .decay.csv    mu(k) and its coverage, per (panel, era)
  .cells.csv    one row per (panel, n, g, cost): metrics, both KEEP verdicts, binding bar
  .slopes.csv   per (panel, era, g): decay slope, PREDICTED and REALIZED width slope, vol slope
  .steps.csv    every adjacent-width step: predicted vs realized, the many-point H_DECAY test
  .wf.csv       rule-8 grid, IS pick, OOS read
  .result.md    the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask                            # noqa: E402

DATE = "2026-09-12"
SLUG = "is-the-RETURN-TAX-of-widening-a-RANK-DECAY-curve"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ---- pre-registered grid and conventions -----------------------------------------------
WIDTHS = [1, 2, 3, 5, 8, 10, 15, 20, 30, 40]      # tuned dial 1
GROSSES = [0.75, 1.00]                            # tuned dial 2
COSTS = [0, 10, 25]
HEADLINE_COST = 10
FREQ = "W"
KMAX = 40
COVER_MIN = 0.80          # a rung k enters a slope fit only if >=80% of dates have >=k eligible
CONTRAST = (5, 20)        # the pre-declared width contrast for the headline scalar
FIT_K = (5, 20)           # decay-slope OLS window, matched to CONTRAST
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MAXVOL = 0.60             # v1 eligibility, unchanged

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def ann(r: pd.Series) -> float:
    """Annualized ARITHMETIC mean return - the statistic the decay curve predicts."""
    return float(r.mean() * 252)


def bars(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], AnnRet=ann(r), Sharpe=m["Sharpe"], Vol=m["Vol"], MaxDD=m["MaxDD"])


# ---- panel machinery --------------------------------------------------------------------
def panel(name: str):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
    px = px.dropna(how="all").ffill()
    trade = [c for c in px.columns if c != "SPY"]
    return px, trade


def elig_rank(px: pd.DataFrame, trade: list[str]):
    """v1 eligibility + v1 score ranks over the TRADEABLE columns only."""
    q = px[trade]
    s, above, vol20 = score(q)
    elig = s.where(above & (vol20 < MAXVOL))
    rk_avg = elig.rank(axis=1, ascending=False)                      # rules_v1's own convention
    rk_int = elig.rank(axis=1, ascending=False, method="first")      # integer ranks for mu(k)
    return elig, rk_avg, rk_int


def book(px: pd.DataFrame, trade: list[str], rk_avg: pd.DataFrame, n: int, g: float) -> pd.DataFrame:
    w = (rk_avg <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def decay(px: pd.DataFrame, trade: list[str], rk_int: pd.DataFrame, lo, hi):
    """mu(k) over rebalance dates inside [lo, hi].  Forward leg t+1 -> t'+1 (engine timing)."""
    idx = px.index
    mask = rebalance_mask(idx, FREQ)
    pos = np.flatnonzero(mask.values)
    pos = pos[(pos + 1) < len(idx)]
    q = px[trade]
    mu, cnt = {}, {}
    rows_r, rows_k = [], []
    for a, b in zip(pos[:-1], pos[1:]):
        d = idx[a]
        if not (lo <= d <= hi):
            continue
        p0, p1 = q.iloc[a + 1], q.iloc[b + 1]
        fwd = (p1 / p0 - 1.0)
        kk = rk_int.iloc[a]
        ok = kk.notna() & fwd.notna()
        rows_k.append(kk[ok].values)
        rows_r.append(fwd[ok].values)
    if not rows_k:
        return pd.DataFrame(columns=["k", "mu", "n_obs", "cover"]), 0
    ndates = len(rows_k)
    K = np.concatenate(rows_k).astype(int)
    R = np.concatenate(rows_r).astype(float)
    out = []
    for k in range(1, KMAX + 1):
        sel = K == k
        out.append(dict(k=k, mu=float(R[sel].mean()) if sel.any() else np.nan,
                        n_obs=int(sel.sum()), cover=sel.sum() / ndates))
    return pd.DataFrame(out), ndates


def partial_means(dc: pd.DataFrame) -> dict:
    m = dc.set_index("k")["mu"]
    cum, out = 0.0, {}
    for k in range(1, KMAX + 1):
        v = m.get(k, np.nan)
        if not np.isfinite(v):
            break
        cum += v
        out[k] = cum / k
    return out


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan, np.nan
    x, y = x[ok], y[ok]
    b = np.polyfit(x, y, 1)
    yhat = np.polyval(b, x)
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ((y - yhat) ** 2).sum() / ss if ss > 0 else np.nan
    return float(b[0]), float(r2)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(x[ok], y[ok])[0, 1])


# ---- KEEP paths (PROTOCOL rule 4) --------------------------------------------------------
def keep_paths(r, b, spy):
    """r=idea, b=live RULES v2 baseline, spy=SPY, all on the same window.  Returns
    (keep4a, keep4b, binding-bar string for 4b)."""
    h = len(r) // 2
    mr, mb, ms = metrics(r), metrics(b), metrics(spy)
    r1, r2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    b1, b2 = metrics(b.iloc[:h]), metrics(b.iloc[h:])
    s1, s2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    k4a = (r1["Sharpe"] > b1["Sharpe"]) and (r2["Sharpe"] > b2["Sharpe"]) and (mr["MaxDD"] >= mb["MaxDD"])
    fails = []
    if not r1["Sharpe"] > s1["Sharpe"]:
        fails.append("H1")
    if not r2["Sharpe"] > s2["Sharpe"]:
        fails.append("H2")
    if not mr["MaxDD"] >= 0.60 * ms["MaxDD"]:      # MaxDD are negative: >= means shallower
        fails.append("DD")
    if not mr["CAGR"] >= 0.70 * ms["CAGR"]:
        fails.append("CAGR")
    return bool(k4a), len(fails) == 0, ("-" if not fails else "+".join(fails))


def main():
    say(f"# Idea 589 - {SLUG} (lane B, {DATE})")
    say(f"grid: widths {WIDTHS} x gross {GROSSES} x 3 panels = {len(WIDTHS)*len(GROSSES)*3} books; "
        f"costs {COSTS} bps; freq {FREQ}; headline {HEADLINE_COST} bps")

    cells, decays, slopes, steps, wfrows = [], [], [], [], []
    gate_lines = []

    for pname in ["U56", "B136", "SMALL716"]:
        px, trade = panel(pname)
        N = len(trade)
        elig, rk_avg, rk_int = elig_rank(px, trade)
        start = px.index[260]                                   # warm-up, as baseline.compare
        full = px.loc[start:]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
        base0, baset = base_r["returns"].loc[start:], base_r["turnover"].loc[start:]
        base_h = base0 - baset * HEADLINE_COST / 1e4

        med_elig = float(elig.loc[start:].notna().sum(axis=1).median())
        say(f"\n## panel {pname}: {N} tradeable names (SPY excluded from books), "
            f"{len(full)} days {full.index[0].date()}..{full.index[-1].date()}, "
            f"median eligible {med_elig:.0f}")

        # ---- gates --------------------------------------------------------------------
        w_chk = book(px, trade, rk_avg, 5, 0.75)
        w_ref = rules_v1_weights(px[trade], n=5, w=0.75 / 5).reindex(columns=px.columns).fillna(0.0)
        g2 = float(np.abs(w_chk.values - w_ref.values).max())
        res_chk = backtest(px, w_chk, cost_bps=0, freq=FREQ)
        res_c10 = backtest(px, w_chk, cost_bps=HEADLINE_COST, freq=FREQ)
        g1 = float(np.abs((res_chk["returns"] - res_chk["turnover"] * HEADLINE_COST / 1e4)
                          - res_c10["returns"]).max())
        # G3: rank objects agree on the top-n SET for every width in the grid
        g3 = max(int(((rk_avg <= n) != (rk_int <= n)).values.sum()) for n in WIDTHS)
        gate_lines.append(dict(panel=pname, G1_cost_identity=g1, G2_book_is_rules_v1=g2,
                               G3_rank_tie_disagreements=g3))
        say(f"   GATES  G1 cost identity max|d| {g1:.3e} | G2 book==rules_v1 max|d| {g2:.3e} "
            f"| G3 rank-tie disagreements {g3}")

        # ---- decay curves per era -------------------------------------------------------
        eras = {"FULL": (start, px.index[-1]),
                "IS": (start, pd.Timestamp(IS_END)),
                "OOS": (pd.Timestamp(OOS_START), px.index[-1])}
        dcs, pms = {}, {}
        for ename, (lo, hi) in eras.items():
            dc, nd = decay(px, trade, rk_int, lo, hi)
            dc.insert(0, "era", ename)
            dc.insert(0, "panel", pname)
            dc["n_dates"] = nd
            dcs[ename] = dc
            pms[ename] = partial_means(dc)
            decays.append(dc)
            good = dc[(dc["cover"] >= COVER_MIN) & dc["mu"].notna()]
            kfit = good[(good["k"] >= FIT_K[0]) & (good["k"] <= FIT_K[1])]
            b, r2 = ols_slope(kfit["k"], kfit["mu"] * 52)
            say(f"   decay {ename:4s} n_dates {nd:4d} | mu(1) {dc.mu.iloc[0]*52:+.2%}/yr "
                f"mu(5) {dc.mu.iloc[4]*52:+.2%} mu(20) {dc.mu.iloc[19]*52:+.2%} "
                f"| kmax@cover>={COVER_MIN:.0%}: {int(good.k.max()) if len(good) else 0} "
                f"| OLS slope k{FIT_K[0]}..{FIT_K[1]} {b*1e4:+.1f} bp/yr per rank (R2 {r2:.2f})")

        # ---- the 60-book grid ------------------------------------------------------------
        grid = {}
        for g in GROSSES:
            for n in WIDTHS:
                w = book(px, trade, rk_avg, n, g)
                res = backtest(px, w, cost_bps=0, freq=FREQ)
                r0, tn = res["returns"].loc[start:], res["turnover"].loc[start:]
                grid[(n, g)] = (r0, tn)
                for c in COSTS:
                    r = r0 - tn * c / 1e4
                    m = bars(r)
                    h = len(r) // 2
                    k4a, k4b, bind = keep_paths(r, base0 - baset * c / 1e4, spy_r)
                    cells.append(dict(panel=pname, N=N, n=n, gross=g, cost_bps=c, **m,
                                      H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                                      turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                      keep4a=k4a, keep4b=k4b, bind4b=bind))

        mspy, mbase = metrics(spy_r), metrics(base_h)
        say(f"   comparands FULL @10bps: SPY CAGR {mspy['CAGR']:.2%} Sharpe {mspy['Sharpe']:.2f} "
            f"MaxDD {mspy['MaxDD']:.1%} | RULES v2 CAGR {mbase['CAGR']:.2%} "
            f"Sharpe {mbase['Sharpe']:.2f} MaxDD {mbase['MaxDD']:.1%}")
        say(f"   {'n':>3} {'g':>5} | {'CAGR':>7} {'AnnRet':>7} {'Shrp':>5} {'Vol':>6} {'MaxDD':>7} "
            f"{'trn/yr':>6} | 4a 4b bind   (10 bps)")
        for g in GROSSES:
            for n in WIDTHS:
                row = [c for c in cells if c["panel"] == pname and c["n"] == n
                       and c["gross"] == g and c["cost_bps"] == HEADLINE_COST][0]
                say(f"   {n:>3} {g:>5.2f} | {row['CAGR']:>7.2%} {row['AnnRet']:>7.2%} "
                    f"{row['Sharpe']:>5.2f} {row['Vol']:>6.2%} {row['MaxDD']:>7.1%} "
                    f"{row['turnover_yr']:>6.2f} | {int(row['keep4a'])}  {int(row['keep4b'])}  "
                    f"{row['bind4b']}")

        # ---- H_DECAY: predicted vs realized, per era, per gross ---------------------------
        for ename, (lo, hi) in eras.items():
            M = pms[ename]
            dc = dcs[ename]
            good = dc[(dc["cover"] >= COVER_MIN) & dc["mu"].notna()]
            kmax_cov = int(good.k.max()) if len(good) else 0
            kfit = good[(good["k"] >= FIT_K[0]) & (good["k"] <= FIT_K[1])]
            bslope, br2 = ols_slope(kfit["k"], kfit["mu"] * 52)
            for g in GROSSES:
                def rr(n, cost):
                    r0, tn = grid[(n, g)]
                    r = (r0 - tn * cost / 1e4).loc[lo:hi]
                    return r
                lo_n, hi_n = CONTRAST
                pred = np.nan
                if lo_n in M and hi_n in M:
                    pred = g * 52 * (M[hi_n] - M[lo_n]) / (hi_n - lo_n)
                real0 = (ann(rr(hi_n, 0)) - ann(rr(lo_n, 0))) / (hi_n - lo_n)
                real10 = (ann(rr(hi_n, HEADLINE_COST)) - ann(rr(lo_n, HEADLINE_COST))) / (hi_n - lo_n)
                volsl = (metrics(rr(hi_n, HEADLINE_COST))["Vol"] - metrics(rr(lo_n, HEADLINE_COST))["Vol"]) / (hi_n - lo_n)
                shsl = (metrics(rr(hi_n, HEADLINE_COST))["Sharpe"] - metrics(rr(lo_n, HEADLINE_COST))["Sharpe"]) / (hi_n - lo_n)
                slopes.append(dict(panel=pname, N=N, med_elig=med_elig, era=ename, gross=g,
                                   kmax_cover=kmax_cov, decay_slope_bp_per_rank=bslope * 1e4,
                                   decay_r2=br2, pred_width_slope=pred,
                                   real_width_slope_0bps=real0, real_width_slope_10bps=real10,
                                   vol_slope_10bps=volsl, sharpe_slope_10bps=shsl,
                                   err_0bps=real0 - pred, err_10bps=real10 - pred))
                # every adjacent step (the many-point test)
                for a, b_ in zip(WIDTHS[:-1], WIDTHS[1:]):
                    p = g * 52 * (M[b_] - M[a]) / (b_ - a) if (a in M and b_ in M) else np.nan
                    r0_ = (ann(rr(b_, 0)) - ann(rr(a, 0))) / (b_ - a)
                    r10_ = (ann(rr(b_, HEADLINE_COST)) - ann(rr(a, HEADLINE_COST))) / (b_ - a)
                    steps.append(dict(panel=pname, era=ename, gross=g, n_from=a, n_to=b_,
                                      pred=p, real_0bps=r0_, real_10bps=r10_,
                                      err_0bps=r0_ - p, err_10bps=r10_ - p))

        # ---- rule 8 walk-forward ----------------------------------------------------------
        isl, ish = start, pd.Timestamp(IS_END)
        ool, ooh = pd.Timestamp(OOS_START), px.index[-1]
        best, bsh = None, -np.inf
        for g in GROSSES:
            for n in WIDTHS:
                r0, tn = grid[(n, g)]
                r = (r0 - tn * HEADLINE_COST / 1e4).loc[isl:ish]
                m = metrics(r)
                ro = (r0 - tn * HEADLINE_COST / 1e4).loc[ool:ooh]
                mo = metrics(ro)
                oa, ob, obind = keep_paths(ro, (base0 - baset * HEADLINE_COST / 1e4).loc[ool:ooh],
                                           spy_r.loc[ool:ooh])
                wfrows.append(dict(panel=pname, n=n, gross=g, IS_CAGR=m["CAGR"], IS_Sharpe=m["Sharpe"],
                                   IS_MaxDD=m["MaxDD"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"], OOS_keep4a=oa, OOS_keep4b=ob,
                                   OOS_bind4b=obind, endpoint=(n in (WIDTHS[0], WIDTHS[-1])
                                                               or g in (GROSSES[0], GROSSES[-1])),
                                   picked=False))
                if m["Sharpe"] > bsh:
                    bsh, best = m["Sharpe"], (n, g)
        n_s, g_s = best
        for row in wfrows:
            if row["panel"] == pname and row["n"] == n_s and row["gross"] == g_s:
                row["picked"] = True
        r0, tn = grid[best]
        oos = (r0 - tn * HEADLINE_COST / 1e4).loc[ool:ooh]
        oos_b = (base0 - baset * HEADLINE_COST / 1e4).loc[ool:ooh]
        oos_s = spy_r.loc[ool:ooh]
        mo, mb2, ms2 = metrics(oos), metrics(oos_b), metrics(oos_s)
        k4a_o, k4b_o, bind_o = keep_paths(oos, oos_b, oos_s)
        interior = (n_s not in (WIDTHS[0], WIDTHS[-1])) and (g_s not in (GROSSES[0], GROSSES[-1]))
        say(f"   RULE 8  IS pick n={n_s} g={g_s:.2f} (IS Sharpe {bsh:.2f}) | grid-interior: {interior}")
        say(f"     OOS {ool.date()}..{ooh.date()}: idea CAGR {mo['CAGR']:.2%} Sharpe {mo['Sharpe']:.2f} "
            f"MaxDD {mo['MaxDD']:.1%} | RULES v2 {mb2['CAGR']:.2%}/{mb2['Sharpe']:.2f}/{mb2['MaxDD']:.1%} "
            f"| SPY {ms2['CAGR']:.2%}/{ms2['Sharpe']:.2f}/{ms2['MaxDD']:.1%} | OOS 4a {int(k4a_o)} "
            f"4b {int(k4b_o)} bind {bind_o}")
        # IS->OOS rank stability of the width dial
        gi = [w for w in wfrows if w["panel"] == pname]
        say(f"     IS->OOS Sharpe ordering over the {len(gi)} grid points: Spearman "
            f"{spearman([w['IS_Sharpe'] for w in gi], [w['OOS_Sharpe'] for w in gi]):+.3f}")

    # ---------------- cross-cell analysis ----------------------------------------------
    S = pd.DataFrame(slopes)
    T = pd.DataFrame(steps)
    C = pd.DataFrame(cells)
    D = pd.concat(decays, ignore_index=True)
    W = pd.DataFrame(wfrows)
    G = pd.DataFrame(gate_lines)

    say("\n## H_DECAY - does the rank-decay curve predict the width slope?")
    for cost, col in [(0, "real_0bps"), (HEADLINE_COST, "real_10bps")]:
        sub = T[T["pred"].notna() & T[col].notna()]
        r_p, r_s = pearson(sub["pred"], sub[col]), spearman(sub["pred"], sub[col])
        sl, r2 = ols_slope(sub["pred"], sub[col])
        say(f"   adjacent steps, n={len(sub)} (3 panels x 3 eras x 2 gross x 9 steps): "
            f"@{cost:>2} bps Pearson {r_p:+.3f} Spearman {r_s:+.3f} | OLS real = {sl:+.3f}*pred "
            f"(R2 {r2:.3f}) | median |err| {np.median(np.abs(sub['pred']-sub[col])):.2%}/yr")
    hl = S[S["era"] == "FULL"]
    say(f"   headline {CONTRAST[0]}->{CONTRAST[1]} contrast, {len(hl)} cells (3 panels x 2 gross), FULL:")
    for _, r in hl.iterrows():
        say(f"     {r.panel:8s} g{r.gross:.2f}  pred {r.pred_width_slope:+.3%}/yr/name  "
            f"real@10 {r.real_width_slope_10bps:+.3%}  err {r.err_10bps:+.3%}  "
            f"| vol slope {r.vol_slope_10bps:+.3%}  Sharpe slope {r.sharpe_slope_10bps:+.4f}")
    say(f"   FULL cells: Pearson(pred, real@10) {pearson(hl['pred_width_slope'], hl['real_width_slope_10bps']):+.3f} "
        f"Spearman {spearman(hl['pred_width_slope'], hl['real_width_slope_10bps']):+.3f}")

    say("\n## H_N - is the width slope a function of the panel's NAME COUNT instead?")
    for era in ["FULL", "IS", "OOS"]:
        sub = S[S["era"] == era]
        say(f"   {era:4s} n={len(sub)} cells | Spearman(real@10, DECAY slope) "
            f"{spearman(sub['decay_slope_bp_per_rank'], sub['real_width_slope_10bps']):+.3f} "
            f"| Spearman(real@10, N) {spearman(sub['N'], sub['real_width_slope_10bps']):+.3f} "
            f"| Spearman(real@10, median eligible) "
            f"{spearman(sub['med_elig'], sub['real_width_slope_10bps']):+.3f}")
    say("   (6 cells per era: 3 panels x 2 gross.  Rank correlations on 6 points are weak evidence "
        "and are reported as such; the many-point step test above is the load-bearing one.)")

    say("\n## idea 320's asymmetry, re-measured on this grid (FULL, 10 bps, 6 cells)")
    vb = hl["vol_slope_10bps"].values
    rb = hl["real_width_slope_10bps"].values
    say(f"   vol benefit  range [{vb.min():+.4%}, {vb.max():+.4%}] spread {vb.max()-vb.min():.4%}"
        f"  (sd {vb.std(ddof=1):.4%})")
    say(f"   return cost  range [{rb.min():+.4%}, {rb.max():+.4%}] spread {rb.max()-rb.min():.4%}"
        f"  (sd {rb.std(ddof=1):.4%})")
    ratio = (rb.max() - rb.min()) / (vb.max() - vb.min()) if (vb.max() - vb.min()) else np.nan
    say(f"   dispersion ratio return/vol = {ratio:.2f}x  (idea 320 reported 1.5x)  "
        f"-> premise {'REPRODUCED' if ratio > 1 else 'NOT reproduced'} in direction")
    ex = hl[hl["panel"] != "SMALL716"]
    vb2, rb2 = ex["vol_slope_10bps"].values, ex["real_width_slope_10bps"].values
    r2r = (rb2.max() - rb2.min()) / (vb2.max() - vb2.min()) if (vb2.max() - vb2.min()) else np.nan
    say(f"   CONFOUND, stated: both spreads are dominated by SMALL716, whose 5->20 width slope is "
        f"{hl[hl.panel=='SMALL716'].iloc[0].real_width_slope_10bps:+.2%}/yr/name against U56's "
        f"{hl[(hl.panel=='U56')&(hl.gross==0.75)].iloc[0].real_width_slope_10bps:+.2%}; on the two "
        f"LARGE-CAP panels alone the ratio is {r2r:.1f}x, i.e. idea 320's direction holds where its "
        f"cells lived and reverses only when a 40%-vol panel enters.  Either way the comparison is a "
        f"SCALE comparison, not a normalised one, in idea 320's form and in this one.")

    say("\n## rule 8 on the RELATIONSHIP (not just the book): fit H_DECAY on IS, read OOS")
    is_sub = T[(T["era"] == "IS") & T["pred"].notna()]
    oos_sub = T[(T["era"] == "OOS") & T["pred"].notna()]
    sl_is, r2_is = ols_slope(is_sub["pred"], is_sub["real_10bps"])
    key = ["panel", "gross", "n_from", "n_to"]
    j = is_sub.set_index(key)["pred"].rename("pred_IS").to_frame().join(
        oos_sub.set_index(key)["real_10bps"].rename("real_OOS"), how="inner")
    say(f"   IS fit: real = {sl_is:+.3f}*pred (R2 {r2_is:.3f}, n={len(is_sub)})")
    say(f"   OOS-predicted-by-IS-curve: Pearson(pred_IS, real_OOS) {pearson(j['pred_IS'], j['real_OOS']):+.3f} "
        f"Spearman {spearman(j['pred_IS'], j['real_OOS']):+.3f} (n={len(j)}) "
        f"| median |err| {np.median(np.abs(j['pred_IS']-j['real_OOS'])):.2%}/yr")
    ood = pearson(oos_sub["pred"], oos_sub["real_10bps"])
    say(f"   for reference, the OOS curve on OOS books: Pearson {ood:+.3f} "
        f"-> the curve must be measured IN the window it predicts.")

    say("\n## KEEP census (10 bps, full sample, all 60 books)")
    h = C[C["cost_bps"] == HEADLINE_COST]
    say(f"   4a passes {int(h['keep4a'].sum())} / {len(h)}   4b passes {int(h['keep4b'].sum())} / {len(h)}"
        f"   BOTH {int((h['keep4a'] & h['keep4b']).sum())}")
    if h["keep4b"].any():
        say("   4b passers:")
        for _, r in h[h["keep4b"]].sort_values("Sharpe", ascending=False).iterrows():
            say(f"     {r.panel:8s} n={int(r.n):<3d} g={r.gross:.2f}  CAGR {r.CAGR:.2%} "
                f"Sharpe {r.Sharpe:.2f} MaxDD {r.MaxDD:.1%}")
    say("   binding 4b bar by frequency: " +
        ", ".join(f"{k}:{v}" for k, v in h["bind4b"].value_counts().items()))
    say(f"   cost ladder sensitivity of the 4b count: " +
        ", ".join(f"{c} bps:{int(C[C.cost_bps==c]['keep4b'].sum())}" for c in COSTS))
    say(f"   OOS (2017-2026) keep census over the same 60 books @10 bps: "
        f"4a {int(W['OOS_keep4a'].sum())} / {len(W)}   4b {int(W['OOS_keep4b'].sum())} / {len(W)}")
    both = W.merge(h[["panel", "n", "gross", "keep4b"]], on=["panel", "n", "gross"], how="left")
    surv = both[both["keep4b"] & both["OOS_keep4b"]]
    say(f"   books passing 4b on BOTH the full sample and OOS: {len(surv)} / {len(h)}")
    for _, r in surv.iterrows():
        say(f"     {r.panel:8s} n={int(r.n):<3d} g={r.gross:.2f}  OOS CAGR {r.OOS_CAGR:.2%} "
            f"Sharpe {r.OOS_Sharpe:.2f} MaxDD {r.OOS_MaxDD:.1%}  | grid ENDPOINT: {bool(r.endpoint)} "
            f"| was the rule-8 IS pick: {bool(r.picked)}")
    say("   NOTE: a book that passes 4b but is NOT the rule-8 IS pick was chosen by reading the "
        "whole grid, i.e. post hoc.  PROTOCOL 8 pre-registers the PICK, not the passer, so such a "
        "book is PARK, never KEEP.")

    # ---------------- write everything ------------------------------------------------
    D.to_csv(f"{OUT}.decay.csv", index=False)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    S.to_csv(f"{OUT}.slopes.csv", index=False)
    T.to_csv(f"{OUT}.steps.csv", index=False)
    W.to_csv(f"{OUT}.wf.csv", index=False)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {OUT.name}.[txt|decay|cells|slopes|steps|wf|gates].csv")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
