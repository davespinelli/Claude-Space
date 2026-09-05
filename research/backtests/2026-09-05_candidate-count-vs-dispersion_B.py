#!/usr/bin/env python3
"""Idea 78 - "candidate-count-vs-dispersion": inside ONE panel, is the gross selection
spread governed by how MANY names are eligible, or by how far APART their momenta are?

The question
------------
Idea 73 killed dispersion as a universe clause but left a live confound in its own
diagnostics.  Across its seven panels the gross selection spread (mean forward 1-week
return of the top-n eligible minus the equal-weighted eligible set) ranked with the
number of eligible candidates far better than with their dispersion:

    Spearman(n_elig, spread)  +0.571 / +0.857 / +0.964   at n = 5 / 10 / 20
    Spearman(sd,     spread)  +0.429 / +0.679 / +0.357

but across panels the two move together - a bigger panel is also a wider one - and
seven points cannot separate them.  This run separates them INSIDE one panel, where the
names, the survivorship exposure, the gate, the costs and the days are all held fixed.

Design
------
The instrument is a random subsample of the candidate set.

    Test A (primary, gross, no costs).  On B136, each rebalance week, draw k names at
        random FROM THE ELIGIBLE SET and pretend that draw is the whole candidate set.
        The candidate count is then EXACTLY k in every week of every cell, while
        dispersion is left free to vary from draw to draw (a random k-subset is an
        unbiased sample of the panel's cross-section, so E[sd] does not depend on k).
        Two readings therefore separate cleanly:
            A1  spread ACROSS k at fixed n  -> the COUNT effect at matched dispersion
            A2  Spearman(draw dispersion, draw spread) WITHIN a (k, n) cell over 100
                draws -> the DISPERSION effect at exactly matched count
        Primary week set = weeks with n_elig >= 80 (= max k), identical for every cell,
        so that no cell is evaluated on a different sample than another.  The
        each-cell-own-weeks reading is reported beside it.

    Test B (book level, 10 bps, next-day execution).  A weekly re-draw is not a
        tradable universe, so the book test uses a FIXED random k-name sub-panel of
        B136 per draw, held for the whole sample: mean n_elig then scales with k while
        E[sd] again does not.  50 draws per k, CAND-20 and EWall on each, net Sharpe
        premium and both KEEP paths on every one of the 300 books.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. k in {20, 40, 80}      candidate count (the instrument)
    2. n in {5, 10, 20}       book size, gross test only; the book test fixes n = 20,
                              which is the cell idea 73 published the +0.964 for
Everything else - the 200d / vol20 < 0.60 gate, 75% gross, weekly rebalancing, 10 bps,
t+1 execution, the composite without /sqrt(vol20) - is RULES v1's own and is held fixed.
Grid A = 3 k x 3 n x 100 draws = 900 points, all reported (cell summaries + full CSV).
Grid B = 3 k x 50 draws x 2 books = 300 points, all reported.

Pre-checks run BEFORE any new number is read
    [a] harness: idea 2's U56/CAND20 row and the live v1 row on universe.json's window.
    [b] premise: idea 73's two cross-panel Spearman triples, recomputed from scratch on
        all seven panels.  If they do not reproduce, idea 78 has no premise.

Walk-forward (PROTOCOL rule 8) - selectors fixed before any OOS number was read
    S0  do-nothing control: full B136 CAND-20, no subsample.
    S1  IS-Sharpe argmax over the 150 (k, draw) CAND-20 books.
    S2  DISPERSION rule: the sub-panel with the highest in-sample mean eligible-set
        dispersion (idea 73's hypothesis).
    S3  COUNT rule: the sub-panel with the highest in-sample mean n_elig (this idea's
        rival hypothesis).  S2 and S3 are the pre-registered pair.
    S4  random sub-panel (seed fixed in advance), the size-matched null.
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: universe_broad.json is current constituents, one-directional.  A random
sub-panel inherits it in full; nothing here corrects it, and the count effect this run
measures is measured on names already known to have survived.

Deterministic (all draws from numpy Generator(PCG64) with fixed seeds), standalone.
Reads baseline.py and engine.py; modifies nothing.
"""
import sys, json, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
NS = [5, 10, 20]
N_DRAWS_A = 100
N_DRAWS_B = 50
N_BOOKS = [5, 20]           # book sizes for the tradable test; 20 is idea 73's published cell
N_BOOK = 20                 # the pre-registered walk-forward cell
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MIN_ELIG = 5
SEED_A = 78_000
SEED_B = 78_500
SEED_S4 = 78_999
SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- panels (idea 73's)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    b_stk = [t for t in px136.columns if t not in set(etf36)]
    s_stk = [c for c in pxs.columns if c != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":      sub(px56, list(px56.columns)),
        "ETF36":    sub(px56, etf36),
        "ETF24":    sub(px56, etf24),
        "STK20":    sub(px56, stk_g, tradable=stk_g),
        "B136":     sub(px136, list(px136.columns)),
        "BSTK100":  sub(px136, b_stk, tradable=b_stk),
        "SMALL484": sub(pxs, s_stk, tradable=s_stk),
    }


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights_cand(px, tradable, n, gross=GROSS):
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def weights_ewall(px, tradable, gross=GROSS):
    elig = eligible_mask(px, tradable)
    cnt = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, dtype=float)), pd.Series(np.asarray(b, dtype=float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0:
        return 0.0
    return float(x.mean() / (x.std() / np.sqrt(len(x))))


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- cross-panel premise
def panel_weekly(px, tradable, ns):
    """Weekly n_elig, dispersion and gross selection spread for each n on one panel."""
    mom = px.shift(21) / px.shift(252) - 1
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0].where(elig)
    rank = s.rank(axis=1, ascending=False)
    mask = rebalance_mask(px.index, FREQ)
    dates = px.index[mask.values]
    fwd = px.loc[dates].pct_change().shift(-1)
    el = elig.loc[dates]
    ok = el.sum(axis=1) >= MIN_ELIG
    m = mom.where(elig).loc[dates]
    out = pd.DataFrame({"n_elig": el.sum(axis=1).where(ok),
                        "sd": m.std(axis=1).where(ok)})
    b = fwd.where(el).mean(axis=1)
    for n in ns:
        top = rank.loc[dates] <= n
        out[f"spread{n}"] = (fwd.where(top).mean(axis=1) - b).where(ok)
    return out


# ---------------------------------------------------------------- Test A machinery
def testA_arrays(px, tradable):
    """Matrices restricted to rebalance dates: eligibility, composite rank key, momentum,
    forward 1-week returns."""
    mask = rebalance_mask(px.index, FREQ)
    dates = px.index[mask.values]
    elig = eligible_mask(px, tradable).loc[dates]
    s = score(px, vol_scale=False)[0].loc[dates]
    mom = (px.shift(21) / px.shift(252) - 1).loc[dates]
    fwd = px.loc[dates].pct_change().shift(-1)
    return dates, elig.values, s.values, mom.values, fwd.values


def main():
    t0 = time.time()
    P("=" * 200)
    P(f"Idea 78 candidate-count-vs-dispersion (lane B) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    P("=" * 200)

    panels = build_panels()
    px56 = panels["U56"][0]
    px136, tr136 = panels["B136"]

    yrs = px56.index.to_series().groupby(px56.index.year).count()
    P(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [a]: harness
    P("\n--- pre-check [a] harness on universe.json's own window (must match published rows) ---")
    start56 = px56.index[260]
    for lbl, w, want in [("U56/CAND20", weights_cand(px56, panels["U56"][1], 20),
                          "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                         ("U56/v1", rules_v1_weights(px56), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = backtest(px56, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        P(f"  {lbl:<11} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    # ------------------------------------------------ pre-check [b]: idea 73's premise
    P("\n--- pre-check [b] idea 73's cross-panel confound, recomputed from scratch ---")
    start_c = max(p.index[260] for p, _ in panels.values())
    end_c = min(p.index[-1] for p, _ in panels.values())
    prem = {}
    for pk, (p, tr) in panels.items():
        wk = panel_weekly(p, tr, NS).loc[start_c:end_c]
        prem[pk] = dict(n_elig=wk["n_elig"].mean(), sd=wk["sd"].mean(),
                        **{f"spread{n}": wk[f"spread{n}"].mean() * 52 for n in NS})
    premdf = pd.DataFrame(prem).T
    P(fmt(premdf))
    P(f"  common window {start_c.date()} -> {end_c.date()}")
    rows = []
    for n in NS:
        rows.append(dict(n=n,
                         sp_n_elig=spearman(premdf["n_elig"], premdf[f"spread{n}"]),
                         sp_sd=spearman(premdf["sd"], premdf[f"spread{n}"])))
    prem_sp = pd.DataFrame(rows).set_index("n")
    P("\n  Spearman across the 7 panels (idea 73 published n_elig +0.571/+0.857/+0.964, sd +0.429/+0.679/+0.357):")
    P(fmt(prem_sp))
    P(f"  Spearman(n_elig, sd) across panels = {spearman(premdf['n_elig'], premdf['sd']):+.3f}  <- the confound itself")

    # ------------------------------------------------ Test A: matched count, gross
    P("\n" + "=" * 200)
    P("TEST A - gross selection spread inside B136 at EXACTLY matched candidate count k")
    P("=" * 200)
    dates, E, S, M, F = testA_arrays(px136, tr136)
    keep_t = (dates >= px136.index[260])
    n_elig_w = E.sum(axis=1)
    common = keep_t & (n_elig_w >= max(KS)) & np.isfinite(F).any(axis=1)
    P(f"  rebalance weeks after warm-up: {int(keep_t.sum())};  with n_elig >= {max(KS)}: {int(common.sum())} "
      f"({common.sum() / keep_t.sum():.1%})  -> primary common week set")
    P(f"  B136 eligible count on those weeks: mean {n_elig_w[common].mean():.1f}, min {n_elig_w[common].min()}, max {n_elig_w[common].max()}")

    Fz = np.where(np.isfinite(F), F, np.nan)

    def cell_spread(sel, weeks, n):
        """sel: (W x C) bool drawn candidate set; returns weekly spread on `weeks`."""
        sc = np.where(sel, S, -np.inf)
        # rank descending within the drawn set
        order = np.argsort(-sc, axis=1, kind="stable")
        topmask = np.zeros_like(sel)
        rows = np.arange(sel.shape[0])[:, None]
        topmask[rows, order[:, :n]] = True
        topmask &= sel
        a = np.nanmean(np.where(topmask, Fz, np.nan), axis=1)
        b = np.nanmean(np.where(sel, Fz, np.nan), axis=1)
        return (a - b)[weeks]

    def draw_sets(rng, k, weeks):
        """Per-week random k of the eligible names, on the rows flagged in `weeks`."""
        u = rng.random(E.shape)
        u = np.where(E, u, -1.0)
        order = np.argsort(-u, axis=1, kind="stable")
        sel = np.zeros_like(E)
        rows = np.arange(E.shape[0])[:, None]
        sel[rows, order[:, :k]] = True
        sel &= E
        return sel

    recA = []
    for k in KS:
        rng = np.random.default_rng(SEED_A + k)
        own = keep_t & (n_elig_w >= k) & np.isfinite(F).any(axis=1)
        for d in range(N_DRAWS_A):
            sel = draw_sets(rng, k, common)
            sd_c = np.nanstd(np.where(sel, M, np.nan), axis=1, ddof=1)
            row = dict(k=k, draw=d,
                       sd_common=float(np.nanmean(sd_c[common])),
                       n_common=int(common.sum()), n_own=int(own.sum()))
            for n in NS:
                if n > k:
                    continue
                sp_c = cell_spread(sel, common, n)
                sp_o = cell_spread(sel, own, n)
                row[f"spread{n}"] = float(np.nanmean(sp_c) * 52)
                row[f"t{n}"] = tstat(sp_c)
                row[f"spread{n}_own"] = float(np.nanmean(sp_o) * 52)
            recA.append(row)
    A = pd.DataFrame(recA)
    A.to_csv(OUT / f"{STEM}.gridA.csv", index=False)

    P(f"\n  A1 COUNT EFFECT - mean over {N_DRAWS_A} draws, common week set ({int(common.sum())} weeks), annualised spread")
    a1 = A.groupby("k").agg(sd=("sd_common", "mean"),
                            **{f"spread{n}": (f"spread{n}", "mean") for n in NS},
                            **{f"t{n}": (f"t{n}", "mean") for n in NS})
    P(fmt(a1))
    P("  (dispersion `sd` is flat across k by construction - a random k-subset is an unbiased sample of the same")
    P("   cross-section - so any movement of `spread` across k is a COUNT effect with dispersion matched.)")
    a1own = A.groupby("k").agg(**{f"spread{n}_own": (f"spread{n}_own", "mean") for n in NS},
                               weeks=("n_own", "max"))
    P("\n  same, each k on its OWN week set (n_elig >= k; different samples - reported, not compared):")
    P(fmt(a1own))

    P(f"\n  full-sample panel control (no subsample, all {int(keep_t.sum())} weeks, n_elig free):")
    ctrl = {}
    for n in NS:
        sp = cell_spread(E, keep_t, n)
        ctrl[n] = dict(spread=float(np.nanmean(sp) * 52), t=tstat(sp))
    P(fmt(pd.DataFrame(ctrl).T))

    P(f"\n  A2 DISPERSION EFFECT at exactly matched count - Spearman(draw sd, draw spread) over {N_DRAWS_A} draws:")
    rows = []
    for k in KS:
        sub = A[A.k == k]
        r = dict(k=k)
        for n in NS:
            if n > k:
                r[f"rho_n{n}"] = np.nan
            else:
                r[f"rho_n{n}"] = spearman(sub["sd_common"], sub[f"spread{n}"])
        r["sd_spread_across_draws"] = float(sub["sd_common"].std())
        rows.append(r)
    a2 = pd.DataFrame(rows).set_index("k")
    P(fmt(a2))
    P("  (a positive rho here would be dispersion paying with the candidate count held exactly fixed.)")

    # pooled standardised OLS of spread on (log k, sd) over all 900 draws
    P("\n  pooled OLS on all draws, spread(n) ~ z(log k) + z(sd)  (standardised betas, in bp/yr):")
    rows = []
    for n in NS:
        sub = A[A[f"spread{n}"].notna()]
        X = np.column_stack([np.ones(len(sub)),
                             (np.log(sub["k"]) - np.log(sub["k"]).mean()) / np.log(sub["k"]).std(),
                             (sub["sd_common"] - sub["sd_common"].mean()) / sub["sd_common"].std()])
        y = sub[f"spread{n}"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X) * (resid @ resid) / (len(y) - 3)))
        rows.append(dict(n=n, b_logk=beta[1] * 1e4, t_logk=beta[1] / se[1],
                         b_sd=beta[2] * 1e4, t_sd=beta[2] / se[2], npts=len(y)))
    P(fmt(pd.DataFrame(rows).set_index("n"), 2))

    P("\n  A3 SELECTIVITY - the same 9 cells arranged by q = n/k, the quantile depth the book selects.")
    P("     A book of n names out of k candidates takes the top q of the cross-section; raising k at fixed n")
    P("     therefore makes the book MORE selective as well as giving it more names to choose between.")
    rows = []
    for k in KS:
        sub = A[A.k == k]
        for n in NS:
            rows.append(dict(q=n / k, k=k, n=n, sd=sub["sd_common"].mean(),
                             spread=sub[f"spread{n}"].mean(), t=sub[f"t{n}"].mean(),
                             spread_sd_draws=sub[f"spread{n}"].std(),
                             se_weekly=abs(sub[f"spread{n}"].mean() / sub[f"t{n}"].mean())
                             if sub[f"t{n}"].mean() else np.nan))
    A3 = pd.DataFrame(rows).sort_values(["q", "k"])
    P(fmt(A3.set_index(["q", "k", "n"])))
    P("\n     constant-q diagonals (count varies 4x, selectivity held fixed):")
    for q in sorted({n / k for k in KS for n in NS}):
        cells = A3[np.isclose(A3["q"], q)]
        if len(cells) > 1:
            body = "   ".join(f"k={int(r.k)},n={int(r.n)}: {r.spread:+.4f}" for r in cells.itertuples())
            P(f"       q={q:.3f}  {body}    range {cells.spread.max() - cells.spread.min():+.4f}")
    P(f"\n     Spearman(q, spread) over the 9 cells = {spearman(A3['q'], A3['spread']):+.3f};  "
      f"Spearman(k, spread) over the same 9 = {spearman(A3['k'], A3['spread']):+.3f}")
    for q in sorted({n / k for k in KS for n in NS}):
        cells = A3[np.isclose(A3["q"], q)]
        if len(cells) > 2:
            P(f"     Spearman(k, spread) along the q={q:.2f} diagonal = {spearman(cells['k'], cells['spread']):+.3f} "
              f"({len(cells)} points)")

    # ------------------------------------------------ Test B: book level with costs
    P("\n" + "=" * 200)
    P(f"TEST B - tradable sub-panels: {N_DRAWS_B} fixed random k-name sub-panels of B136 per k, "
      f"CAND-{N_BOOK} and EWall, {COST_BPS} bps")
    P("=" * 200)
    startb = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    ms, mb = metrics(spy), metrics(base)
    P(f"  SPY               {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves "
      f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    P(f"  RULES v1 on B136  {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  halves "
      f"{half_sharpes(base)[0]:.3f}/{half_sharpes(base)[1]:.3f}  OOS Sharpe {metrics(base.loc[OOS_START:])['Sharpe']:.3f}")
    P(f"  4b bars: MaxDD <= {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}, "
      f"H1 > {half_sharpes(spy)[0]:.3f}, H2 > {half_sharpes(spy)[1]:.3f}, OOS Sharpe > {metrics(spy_oos)['Sharpe']:.3f}")

    names136 = [c for c in px136.columns if c in tr136]
    recB = []
    series = {}
    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(N_DRAWS_B):
            cols = list(rng.choice(names136, size=k, replace=False))
            keep = list(dict.fromkeys(cols + ["SPY"]))
            p = px136[keep].dropna(how="all").ffill()
            tr = set(cols)
            el = eligible_mask(p, tr)
            wmask = rebalance_mask(p.index, FREQ).values
            ne = el[wmask].sum(axis=1).loc[startb:]
            mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(el[cols])
            sdw = mom_p[wmask].loc[startb:].std(axis=1)
            r_e = backtest(p, weights_ewall(p, tr), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
            me = metrics(r_e)
            for nb in N_BOOKS:
                r_c = backtest(p, weights_cand(p, tr, nb), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
                series[(k, d, nb)] = r_c
                mc = metrics(r_c)
                h1, h2 = half_sharpes(r_c)
                recB.append(dict(
                    k=k, n=nb, draw=d, n_elig=float(ne.mean()), sd=float(sdw.mean()),
                    n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()),
                    CAGR=mc["CAGR"], Sharpe=mc["Sharpe"], MaxDD=mc["MaxDD"], H1=h1, H2=h2,
                    Sharpe_IS=metrics(r_c.loc[:IS_END])["Sharpe"],
                    Sharpe_OOS=metrics(r_c.loc[OOS_START:])["Sharpe"],
                    CAGR_OOS=metrics(r_c.loc[OOS_START:])["CAGR"],
                    MaxDD_OOS=metrics(r_c.loc[OOS_START:])["MaxDD"],
                    ew_Sharpe=me["Sharpe"], ew_CAGR=me["CAGR"], ew_MaxDD=me["MaxDD"],
                    premium=mc["Sharpe"] - me["Sharpe"],
                    f4a=fail_4a(r_c, base),
                    f4b=fail_4b(r_c, spy, r_c.loc[OOS_START:], spy_oos)))
        P(f"  k={k:<3} done  ({time.time() - t0:.0f}s)")
    B = pd.DataFrame(recB)
    B.to_csv(OUT / f"{STEM}.gridB.csv", index=False)

    P("\n  B1 by (k, n) - means over draws; premium = Sharpe(CAND-n) - Sharpe(EWall) on the SAME sub-panel:")
    b1 = B.groupby(["k", "n"]).agg(n_elig=("n_elig", "mean"), sd=("sd", "mean"),
                                   CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
                                   ew_Sharpe=("ew_Sharpe", "mean"), premium=("premium", "mean"),
                                   prem_sd=("premium", "std"),
                                   pass4a=("f4a", lambda s: (s == "-").sum()),
                                   pass4b=("f4b", lambda s: (s == "-").sum()),
                                   npts=("draw", "count"))
    P(fmt(b1))
    P("  (at k=20, n=20 the book holds every eligible name, so its premium is a weighting artefact, not a")
    P("   selection payoff - that cell is reported and excluded from the premium-vs-k reading.)")
    P(f"\n  B2 within-cell Spearman over {N_DRAWS_B} draws (candidate pool held at k by construction):")
    rows = []
    for k in KS:
        for nb in N_BOOKS:
            s = B[(B.k == k) & (B.n == nb)]
            rows.append(dict(k=k, n=nb,
                             rho_sd_premium=spearman(s["sd"], s["premium"]),
                             rho_sd_Sharpe=spearman(s["sd"], s["Sharpe"]),
                             rho_nelig_premium=spearman(s["n_elig"], s["premium"]),
                             rho_nelig_Sharpe=spearman(s["n_elig"], s["Sharpe"])))
    P(fmt(pd.DataFrame(rows).set_index(["k", "n"])))
    for nb in N_BOOKS:
        s = B[B.n == nb]
        P(f"\n  pooled over {len(s)} sub-panels at n={nb}: rho(k, premium) = {spearman(s['k'], s['premium']):+.3f}, "
          f"rho(sd, premium) = {spearman(s['sd'], s['premium']):+.3f}, "
          f"rho(n_elig, premium) = {spearman(s['n_elig'], s['premium']):+.3f}")
    P(f"  4a passes {(B.f4a == '-').sum()} of {len(B)};  4b passes {(B.f4b == '-').sum()} of {len(B)}")
    P("\n  4b failing-bar census over all sub-panel books:")
    P(B.f4b.str.split(",").explode().value_counts().to_string())
    P("\n  B3 per-cell 4b base rates and OOS distribution - what a random pick from each cell is worth:")
    b3 = B.groupby(["k", "n"]).agg(pass4b=("f4b", lambda s: (s == "-").mean()),
                                   pass4a=("f4a", lambda s: (s == "-").mean()),
                                   OOS_Sharpe=("Sharpe_OOS", "mean"),
                                   OOS_Sharpe_sd=("Sharpe_OOS", "std"),
                                   OOS_Sharpe_max=("Sharpe_OOS", "max"),
                                   OOS_CAGR=("CAGR_OOS", "mean"))
    for bar in ["H1", "H2", "OOS", "DD", "CAGR"]:
        b3[f"fail_{bar}"] = B.assign(x=B.f4b.str.split(",").apply(lambda v: bar in v)).groupby(["k", "n"])["x"].mean()
    P(fmt(b3))

    # full-panel controls at the book level
    P("\n  controls on the FULL B136 panel (no subsample):")
    ctl = {}
    full_cand = {}
    for lbl, w in ([(f"CAND{nb}", weights_cand(px136, tr136, nb)) for nb in N_BOOKS]
                   + [("EWall", weights_ewall(px136, tr136))]):
        r = backtest(px136, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        ctl[lbl] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        Sharpe_OOS=metrics(r.loc[OOS_START:])["Sharpe"],
                        CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                        f4a_ok=float(fail_4a(r, base) == "-"),
                        f4b_ok=float(fail_4b(r, spy, r.loc[OOS_START:], spy_oos) == "-"))
        if lbl.startswith("CAND"):
            full_cand[int(lbl[4:])] = r
    ctldf = pd.DataFrame(ctl).T
    P(fmt(ctldf))
    for nb in N_BOOKS:
        P(f"  full-panel premium n={nb}: {ctldf.loc[f'CAND{nb}', 'Sharpe'] - ctldf.loc['EWall', 'Sharpe']:+.3f} Sharpe "
          f"(mean sub-panel premium at n={nb}: {B[B.n == nb].premium.mean():+.3f})")
        P(f"  full-panel CAND{nb}: 4a {fail_4a(full_cand[nb], base)}   4b "
          f"{fail_4b(full_cand[nb], spy, full_cand[nb].loc[OOS_START:], spy_oos)}")

    # ------------------------------------------------ Test C: rule 8 walk-forward
    P("\n" + "=" * 200)
    P(f"TEST C - PROTOCOL rule 8 walk-forward: parameters chosen on <= {IS_END}, {OOS_START}-> read once")
    P("=" * 200)
    wf = []
    for nb in N_BOOKS:
        IS = B[B.n == nb]
        tag = "PRE-REGISTERED" if nb == N_BOOK else "secondary"
        picks = {
            f"n={nb} S0 do-nothing (full B136)": None,
            f"n={nb} S1 IS-Sharpe argmax": IS.sort_values(["Sharpe_IS", "k"], ascending=[False, True]).iloc[0],
            f"n={nb} S2 DISPERSION (max IS sd)": IS.sort_values(["sd_IS", "k"], ascending=[False, True]).iloc[0],
            f"n={nb} S3 COUNT (max IS n_elig)": IS.sort_values(["n_elig_IS", "k"], ascending=[False, True]).iloc[0],
            f"n={nb} S4 random sub-panel": IS.iloc[np.random.default_rng(SEED_S4).integers(len(IS))],
        }
        for lbl, row in picks.items():
            if row is None:
                r, kk, dd = full_cand[nb], "-", "-"
            else:
                kk, dd = int(row.k), int(row.draw)
                r = series[(kk, dd, nb)]
            r_oos = r.loc[OOS_START:]
            m, mo = metrics(r), metrics(r_oos)
            if row is None:
                cell_rate, cell_oos = np.nan, np.nan
            else:
                cell = B[(B.k == kk) & (B.n == nb)]
                cell_rate, cell_oos = float((cell.f4b == "-").mean()), float(cell.Sharpe_OOS.mean())
            wf.append(dict(selector=lbl + ("" if nb == N_BOOK else "  [secondary]"), k=kk, draw=dd,
                           IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           cell_OOS_Sharpe=cell_oos, cell_4b_rate=cell_rate,
                           full_Sharpe=m["Sharpe"], full_MaxDD=m["MaxDD"],
                           f4a=fail_4a(r, base), f4b=fail_4b(r, spy, r_oos, spy_oos)))
        P(f"  ({tag} block for n={nb})")
    for lbl, r in [("SPY", spy), ("RULES v1 (B136)", base)]:
        mo = metrics(r.loc[OOS_START:])
        wf.append(dict(selector=lbl, k="-", draw="-", IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       full_Sharpe=metrics(r)["Sharpe"], full_MaxDD=metrics(r)["MaxDD"], f4a="-", f4b="-"))
    W = pd.DataFrame(wf).set_index("selector")
    W.to_csv(OUT / f"{STEM}.walkforward.csv")
    P(fmt(W))
    P("  cell_OOS_Sharpe / cell_4b_rate = what the pick's OWN (k, n) cell delivers on average and how often a")
    P("  RANDOM member of it passes 4b - a selector that only matches its cell's base rate has found nothing.")
    for nb in N_BOOKS:
        s = B[B.n == nb]
        P(f"\n  n={nb}: Spearman(IS Sharpe, OOS Sharpe) over {len(s)} sub-panels = {spearman(s.Sharpe_IS, s.Sharpe_OOS):+.3f}")
        P(f"        Spearman(IS sd, OOS Sharpe)      = {spearman(s.sd_IS, s.Sharpe_OOS):+.3f}   <- dispersion as a selector")
        P(f"        Spearman(IS n_elig, OOS Sharpe)  = {spearman(s.n_elig_IS, s.Sharpe_OOS):+.3f}   <- count as a selector")
        P(f"        OOS Sharpe of the sub-panels: mean {s.Sharpe_OOS.mean():.3f}, sd {s.Sharpe_OOS.std():.3f}, "
          f"min {s.Sharpe_OOS.min():.3f}, max {s.Sharpe_OOS.max():.3f}; "
          f"full-panel control {metrics(full_cand[nb].loc[OOS_START:])['Sharpe']:.3f}")

    P(f"\nDone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
