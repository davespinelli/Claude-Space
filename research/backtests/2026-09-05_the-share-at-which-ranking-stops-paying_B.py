#!/usr/bin/env python3
"""QUEUE idea 159 — the-share-at-which-ranking-stops-paying  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 159)
    "idea 153's regression gives a slope but PROTOCOL wants a NUMBER: the book share above
     which any cross-sectional key is arithmetic noise.  Fit the |dCAGR|-vs-share curve per
     panel and report the share at which the tilt's realised magnitude falls below the 10 bps
     cost of running it, with a bootstrap interval.  Bears on ideas 124 (book-size floor) and
     82 (ranking subtracts value).  Max 2 params."

WHAT IS AT STAKE.  Idea 153 established that book share m (the fraction of the eligible panel
    the book holds) governs the realised MAGNITUDE of a cross-sectional tilt with R^2 0.43-0.60,
    15-50x more than the key's own Fama-MacBeth t.  A slope is not a rule.  What RULES can quote
    is a share m* above which the tilt's realised gross magnitude no longer covers the cost of
    running it -- i.e. above which ranking is arithmetic noise you pay 10 bps for.  Ideas 72,
    82, 141 and 160 have now four times independently concluded "drop the ranking"; if m* comes
    back BELOW the incumbent book's own share of 0.53 that is a fifth derivation with a number
    attached, and if it comes back ABOVE it the incumbent is defended for the first time.

THE MEASUREMENT, fixed before any number was read
    For each (panel, share m, tilt) the tilt book and its own NONE control at matched (panel, m)
    are run ONCE at 0 bps; every cost rung is derived exactly from the same path as
        r_c = r_0 - turnover * c / 1e4                      (engine.backtest is linear in cost)
    so the gross and net legs of the comparison are the same book, not two runs.

    GROSS VALUE of the tilt      g(m) = |CAGR(tilt @ 0 bps) - CAGR(NONE @ 0 bps)|   pp/yr
    COST of running the tilt, three bars, ALL reported, the first pre-registered as primary:
      BAR-INC  c_inc(m) = [CAGR(tilt@0)-CAGR(tilt@10)] - [CAGR(NONE@0)-CAGR(NONE@10)]
               the EXACT incremental cost of choosing the tilted book over its control.  This
               is the economically correct number and it may be <= 0 (a tilt can be cheaper).
      BAR-OVL  c_ovl(m) = 10bps x annualised sum over rebalances of |w_tilt - w_NONE|
               the cost of EXPRESSING the tilt -- trading from the control's book into the
               tilt's book each rebalance.  Always >= 0; an upper bound on BAR-INC.
      BAR-FLAT c = 0.10 pp/yr, one 10 bps round trip a year.  A floor: "worth doing at all".

    m* = the smallest share at which g(m) <= c(m) and stays there.  Reported two ways:
      (i) EMPIRICAL: linear interpolation of the grid points of g(m) - c(m) at its last sign
          change (no fit, no free parameter);
      (ii) FITTED: OLS of log g(m) on m (idea 153's curve is a decay), crossed with the fitted
          log c(m); this is the "fit the curve" the idea asks for.
    Neither adds a tuned parameter -- both read the same 2-parameter grid.

BOOTSTRAP (the interval the idea asks for)
    Circular block bootstrap, block = 21 trading days, 2000 replicates, seed 159.  The SAME
    block index sequence is applied to the tilt path and its control path jointly, so the
    resample preserves the daily pairing that dCAGR is a function of.  Each replicate yields a
    whole g_b(m) curve; m*_b is solved on it against the point-estimate cost curve; the interval
    is the 5th/95th percentile of {m*_b}.  Replicates with no crossing inside [m_min, 1.00] are
    reported as a censoring rate, not dropped silently.

TUNED PARAMETERS -- exactly two, both swept exhaustively, ALL grid points reported:
    1. target BOOK SHARE m in {0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.53, 0.70, 0.85, 1.00},
       realised as n = max(2, round(m x mean weekly eligible count)) -- idea 153's own map, so
       m = 0.53 lands on u56 n=20, the incumbent.
    2. the TILT, 3 values (idea 81/153 verbatim):
           INV  = composite / sqrt(vol20)   (RULES v1's live tilt)
           NONE = composite                 (the control, not a treatment)
           POS  = composite * sqrt(vol20)
    Panels (u56/broad/small), cost rungs (0/10/25 bps), the three cost bars, the two crossing
    estimators, the OOS window and every diagnostic are REPORTED axes, never selected on.  The
    200d gate, vol20 < 0.60 and GROSS = 0.75 stay at RULES v1's values.

CONFOUNDS, declared before the result
    (i) At m -> 1.00 all three tilts hold the same eligible set, so g -> 0 MECHANICALLY.  That
        endpoint is not evidence of a crossing; a crossing located AT m = 1.00 is reported as
        "no crossing inside the grid", and the fitted estimator is also run on m <= 0.70.
    (ii) idea 73/81/153's de-grossing: the literal GROSS/n book invests less than 0.75 when
        fewer than n names are eligible, which bites hardest at large m.  The whole grid is
        re-run gross-normalised ("norm") as a reported control on the crossing itself.
    (iii) m is a sample-average share; realised n_held/n_elig is a printed column.

REPRODUCTION, asserted before any new number is read
    [a] idea 153's INV-vs-NONE daily name overlap at n = 20: u56 69.4%, broad 42.5%.
    [b] idea 153's matched-share dCAGR(POS-NONE) at m = 0.20, 10 bps, literal: u56 +2.83%/yr,
        broad +2.75%/yr; and at matched n = 20: u56 +0.49%/yr, broad +2.89%/yr.
    [c] idea 153's mean weekly eligible counts: u56 37.5, broad 91.5, small 141.2.
    [d] the cost-derivation identity: r_0 - turnover*10/1e4 must equal a fresh 10 bps
        engine.backtest run to 1e-12 on one book, or the whole gross/net split is invalid.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction [a]-[d] holds.
    P2  g(m) is monotone decreasing in m within both large-cap panels: Spearman(m, g) <= -0.6
        for both tilts on u56 and on broad.
    P3  A crossing exists against BAR-OVL on both large-cap panels at 10 bps and lies strictly
        inside the grid, i.e. in [0.15, 0.85] -- not at an endpoint.
    P4  The bootstrap 5-95 interval for m* is at least 0.25 wide on at least one panel: the
        number is real but not sharply identified, and PROTOCOL should quote the interval.
    P5  The incumbent's own share 0.53 sits BELOW m* on u56 (the tilt still has gross magnitude
        to express there) while its SIGNED dCAGR for INV is negative -- magnitude is available,
        the live tilt just spends it in the wrong direction.
    P6  Rule 8: an m*-gated selector (drop the tilt above m*, keep the best IS tilt below it)
        does NOT beat plain IS-Sharpe or do-nothing on mean OOS Sharpe.  Ideas 160 and 162 both
        killed their selectors; the prior is that this one dies too.

WALK-FORWARD (PROTOCOL rule 8), selection rules fixed BEFORE any OOS number is read
    m* is re-estimated on 2009-2016 ONLY (2011-2016 on the small panel) from the IS window's own
    g and cost curves.  Four selectors, each reads its pick ONCE on 2017-01-01..2026:
      S_MSTAR   best IS Sharpe among books with m <= m*_IS, tilt free below m*, forced NONE above
      S_IS      best IS Sharpe over the whole (m, tilt) grid                    (the usual bar)
      S_NONE    NONE at the incumbent share m = 0.53                            (do-nothing)
      S_LIVE    RULES v1 on that panel                                          (the book)
    Reported as OOS CAGR/Sharpe/MaxDD against RULES v1 (same panel, same cost) and SPY.
    Both KEEP paths (4a and 4b) are evaluated at EVERY book, full sample and OOS window alone.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).
    * Idea 49/39: the eligibility gate is INVERTED on the small panel, so its numbers are about
      a gate that does not work there; reported, not traded.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's.
    * A block bootstrap on one realised path cannot manufacture independent histories; the
      interval is sampling error around THIS path, not parameter uncertainty across worlds.

HARNESS
    `baseline` (the live rules), idea 129's panel/4b-bar machinery and idea 94's window/halves
    machinery are IMPORTED, so the panels, the control arm and the bars are the committed ones.

POST-HOC, declared as post-hoc
    The ratio diagnostic (section "THE RATIO g/c") and its bootstrap of the log-slope
    difference d = slope(log g) - slope(log c) were added AFTER P3 failed, to explain WHY the
    crossing is not locatable.  It is a diagnosis of a failed prediction, not a pre-registered
    test, and it is labelled as such everywhere it is quoted.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .curve.csv, .crossing.csv,
.ratio.csv, .dslope.csv, .bootstrap.csv, .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-share-at-which-ranking-stops-paying_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
OOS_START = H.OOS_START
IS_END = H.IS_END
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60

SHARES = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.53, 0.70, 0.85, 1.00]  # tuned parameter 1
TILTS = ["INV", "NONE", "POS"]                                          # tuned parameter 2
TREAT = ["INV", "POS"]                                                  # NONE is the control
CONSTR = ["lit", "norm"]                                                # reported axis
BARS = ["INC", "OVL", "FLAT"]
FLAT_BAR = 0.0010                                # 0.10 pp/yr, one 10 bps round trip
BLOCK, NBOOT, SEED = 21, 2000, 159

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book (idea 81/153 verbatim)
def parts(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    return comp * (0.5 + 0.5 * above.astype(float)), above, v


_SC = {}


def score_of(px, tilt, pk):
    key = (pk, tilt)
    if key not in _SC:
        s, above, v = parts(px)
        vv = v.clip(lower=0.08) ** 0.5
        _SC[key] = ({"INV": s / vv, "NONE": s, "POS": s * vv}[tilt], above, v)
    return _SC[key]


def held_mask(px, tilt, n, pk):
    s, above, v = score_of(px, tilt, pk)
    rank = s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False)
    return rank <= n


def weights(px, tilt, n, pk, constr="lit"):
    m = held_mask(px, tilt, n, pk).astype(float)
    if constr == "lit":
        return m * (GROSS / n)
    k = m.sum(axis=1).replace(0, np.nan)
    return m.div(k, axis=0).fillna(0.0) * GROSS


def eligible_mask(px, pk):
    _, above, v = score_of(px, "NONE", pk)
    return above & (v < MAX_VOL)


def overlap(A, B):
    inter = (A & B).sum(axis=1)
    un = (A | B).sum(axis=1).replace(0, np.nan)
    return float((inter / un).mean())


def net(r0, to, c):
    """Engine is linear in cost: derive any rung from the 0 bps path and its turnover."""
    return r0 - to * c / 1e4


def cagr(r):
    if len(r) < 60:
        return np.nan
    return metrics(r)["CAGR"]


# ------------------------------------------------------------------ crossing estimators
def cross_empirical(ms, g, c):
    """Smallest share at which g - c <= 0 and never turns positive again; linear interp."""
    d = np.asarray(g, float) - np.asarray(c, float)
    ms = np.asarray(ms, float)
    ok = np.isfinite(d)
    if ok.sum() < 2:
        return np.nan
    d, ms = d[ok], ms[ok]
    if d[0] <= 0:
        return ms[0]              # already noise at the smallest share tested
    # last index where d > 0; the crossing is between it and the next point
    pos = np.where(d > 0)[0]
    i = pos[-1]
    if i == len(d) - 1:
        return np.nan             # still paying at m = 1.00: no crossing inside the grid
    x0, x1, y0, y1 = ms[i], ms[i + 1], d[i], d[i + 1]
    return float(x0 + (x1 - x0) * y0 / (y0 - y1))


def cross_fitted(ms, g, c, mmax=1.01):
    """OLS of log g on m and of log c on m (idea 153's curve is a decay); solve the crossing."""
    ms = np.asarray(ms, float)
    g, c = np.asarray(g, float), np.asarray(c, float)
    k = np.isfinite(g) & np.isfinite(c) & (g > 0) & (c > 0) & (ms <= mmax)
    if k.sum() < 3:
        return np.nan, np.nan, np.nan
    X = np.column_stack([np.ones(k.sum()), ms[k]])
    bg = np.linalg.lstsq(X, np.log(g[k]), rcond=None)[0]
    bc = np.linalg.lstsq(X, np.log(c[k]), rcond=None)[0]
    den = bg[1] - bc[1]
    if abs(den) < 1e-12:
        return np.nan, bg[1], bc[1]
    return float((bc[0] - bg[0]) / den), float(bg[1]), float(bc[1])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    k = np.isfinite(a) & np.isfinite(b)
    if k.sum() < 3:
        return np.nan
    ra = pd.Series(a[k]).rank().values
    rb = pd.Series(b[k]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def block_idx(nobs, rng):
    """Circular block bootstrap index of length nobs, block = BLOCK."""
    nb = int(np.ceil(nobs / BLOCK))
    starts = rng.integers(0, nobs, size=nb)
    idx = (starts[:, None] + np.arange(BLOCK)[None, :]).ravel() % nobs
    return idx[:nobs]


def main():
    say("=" * 190)
    say(f"IDEA 159 — the-share-at-which-ranking-stops-paying   ({STEM})")
    say("At what book share does a cross-sectional tilt's realised gross magnitude stop covering "
        "the 10 bps cost of running it?")
    say("=" * 190)

    ok, ref = {}, {}
    grid_rows, curve_rows, cross_rows, boot_rows, wf_rows = [], [], [], [], []
    RET = {}          # (pk, constr, m, tilt) -> (r0 series, turnover series)

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms_, mso_ = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {}
        v1res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        v1r0, v1to = v1res["returns"].loc[start:], v1res["turnover"].loc[start:]
        for c in COSTS:
            v1[c] = net(v1r0, v1to, c)
        el = eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        ref[pk] = dict(px=px, start=start, spy=ms_, spy_oos=mso_, bfull=bfull, bIS=bIS,
                       bOOS=bOOS, v1=v1, n_elig=n_elig, desc=desc, nmap=nmap, spyr=spy)

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, "
            f"mean weekly eligible names {n_elig:.1f}")
        say("    share -> n:  " + ", ".join(f"m={m:.2f}->n={nmap[m]}" for m in SHARES))
        say(f"    SPY full {ms_['CAGR']:.2%}/{ms_['Sharpe']:.3f}/{ms_['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso_['CAGR']:.2%}/{mso_['Sharpe']:.3f}"
            f"/{mso_['MaxDD']:.2%}")
        for c in COSTS:
            a_, b_ = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {a_['CAGR']:.2%}/{a_['Sharpe']:.3f}/{a_['MaxDD']:.2%}"
                f" | OOS {b_['CAGR']:.2%}/{b_['Sharpe']:.3f}/{b_['MaxDD']:.2%}")

        # ---------- reproduction [a] and [c]
        pub_e = {"u56": 37.5, "broad": 91.5, "small": 141.2}[pk]
        ok[f"c:{pk}"] = abs(n_elig - pub_e) < 0.15
        say(f"[c] mean weekly eligible: idea 153 published {pub_e}, this run {n_elig:.1f} -> "
            f"{'MATCH' if ok[f'c:{pk}'] else 'MISMATCH'}")
        if pk in ("u56", "broad"):
            Msk = {t: held_mask(px, t, 20, pk).loc[start:] for t in TILTS}
            o = overlap(Msk["INV"], Msk["NONE"])
            pub = 0.694 if pk == "u56" else 0.425
            ok[f"a:{pk}"] = abs(o - pub) < 0.006
            say(f"[a] {pk} n=20 INV-vs-NONE overlap: idea 153/81 published {pub:.1%}, this run "
                f"{o:.1%} -> {'MATCH' if ok[f'a:{pk}'] else 'MISMATCH'}")

        # ---------- the grid: one 0 bps run per book, every rung derived
        for cn in CONSTR:
            for m in SHARES:
                n = nmap[m]
                for t in TILTS:
                    W = weights(px, t, n, pk, constr=cn)
                    res = backtest(px, W, cost_bps=0.0, freq=FREQ)
                    r0, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    RET[(pk, cn, m, t)] = (r0, to, W)
                    yrs = len(r0) / 252
                    row = dict(panel=pk, constr=cn, m=m, n=n, tilt=t,
                               n_held=float(res["weights"].loc[start:].gt(0).sum(axis=1).mean()),
                               gross=float(res["weights"].loc[start:].sum(axis=1).mean()),
                               to_yr=float(to.sum() / yrs))
                    row["CAGR_0"] = cagr(r0)
                    for c in COSTS:
                        rc = net(r0, to, c)
                        mm = metrics(rc)
                        h1, h2 = H.halves(rc)
                        mo = metrics(rc.loc[OOS_START:])
                        row[f"CAGR_{int(c)}"] = mm["CAGR"]
                        row[f"Sharpe_{int(c)}"] = mm["Sharpe"]
                        row[f"MaxDD_{int(c)}"] = mm["MaxDD"]
                        row[f"H1_{int(c)}"] = h1
                        row[f"H2_{int(c)}"] = h2
                        row[f"OOSSharpe_{int(c)}"] = mo["Sharpe"]
                        row[f"OOSCAGR_{int(c)}"] = mo["CAGR"]
                        row[f"OOSMaxDD_{int(c)}"] = mo["MaxDD"]
                        # 4a vs the live book, 4b vs SPY (full sample and OOS window)
                        bs = metrics(v1[c])
                        bh1, bh2 = H.halves(v1[c])
                        row[f"pass4a_{int(c)}"] = bool(h1 > bh1 and h2 > bh2
                                                       and mm["MaxDD"] >= bs["MaxDD"])
                        mg = C.margins_at(rc, bfull, PHI0, DELTA0, "full")
                        row[f"pass4b_{int(c)}"] = len(C.fails(mg)) == 0
                        row[f"fail4b_{int(c)}"] = "|".join(C.fails(mg)) or "-"
                        mgo = C.margins_at(rc, bOOS, PHI0, DELTA0, "OOS")
                        row[f"pass4bOOS_{int(c)}"] = len(C.fails(mgo)) == 0
                    grid_rows.append(row)

        # ---------- reproduction [b] and [d], read off the grid just built
        if pk in ("u56", "broad"):
            gd = pd.DataFrame(grid_rows)
            q = gd[(gd.panel == pk) & (gd.constr == "lit") & (gd.m == 0.20)]
            dc = float(q[q.tilt == "POS"].CAGR_10.iloc[0] - q[q.tilt == "NONE"].CAGR_10.iloc[0])
            pubb = 0.0283 if pk == "u56" else 0.0275
            ok[f"b:{pk}"] = abs(dc - pubb) < 0.0012
            say(f"[b] {pk} dCAGR(POS-NONE) at m=0.20 @10bps: idea 153 published {pubb:+.2%}, "
                f"this run {dc:+.2%} -> {'MATCH' if ok[f'b:{pk}'] else 'MISMATCH'}")
        if pk == "u56":
            r0, to, W = RET[(pk, "lit", 0.53, "NONE")]
            fresh = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            err = float((net(r0, to, 10.0) - fresh).abs().max())
            ok["d"] = err < 1e-12
            say(f"[d] cost-derivation identity (u56 NONE m=0.53): max |derived - fresh 10bps| "
                f"= {err:.2e} -> {'MATCH' if ok['d'] else 'MISMATCH'}")

    G = pd.DataFrame(grid_rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    say("\n" + "=" * 190)
    say("REPRODUCTION GATE: " + ("ALL PASS" if all(ok.values()) else "FAILURES -> " +
        ", ".join(k for k, v in ok.items() if not v)))
    say(f"  {sum(ok.values())} of {len(ok)} checks match.  Grid: {len(G)} books "
        f"({len(PANELS)} panels x {len(SHARES)} shares x {len(TILTS)} tilts x "
        f"{len(CONSTR)} constructions), every cost rung derived from the same 0 bps path.")
    say("=" * 190)

    # ================================================================ the curve g(m) and c(m)
    say("\n### THE CURVE: gross value of the tilt g(m) vs the cost of running it, 10 bps, "
        "literal book")
    say("    g   = |CAGR(tilt@0bps) - CAGR(NONE@0bps)|, pp/yr")
    say("    INC = exact incremental cost of the tilt over its control (may be <= 0)")
    say("    OVL = 10bps x annualised sum |w_tilt - w_NONE| over rebalances (upper bound)")
    for pk in PANELS:
        for cn in CONSTR:
            for t in TREAT:
                for m in SHARES:
                    r0t, tot, Wt = RET[(pk, cn, m, t)]
                    r0n, ton, Wn = RET[(pk, cn, m, "NONE")]
                    yrs = len(r0t) / 252
                    g = abs(cagr(r0t) - cagr(r0n))
                    sg = cagr(r0t) - cagr(r0n)
                    c10t, c10n = net(r0t, tot, 10.0), net(r0n, ton, 10.0)
                    c_inc = (cagr(r0t) - cagr(c10t)) - (cagr(r0n) - cagr(c10n))
                    # overlay: trade from the control book into the tilt book each rebalance
                    reb = tot[tot > 0].index
                    dist = float((Wt.reindex(reb).fillna(0.0)
                                  - Wn.reindex(reb).fillna(0.0)).abs().sum(axis=1).sum())
                    c_ovl = dist / yrs * 10.0 / 1e4
                    curve_rows.append(dict(panel=pk, constr=cn, tilt=t, m=m,
                                           n=ref[pk]["nmap"][m], g=g, signed_dCAGR=sg,
                                           dSharpe=metrics(c10t)["Sharpe"] - metrics(c10n)["Sharpe"],
                                           c_INC=c_inc, c_OVL=c_ovl, c_FLAT=FLAT_BAR,
                                           overlap=overlap(held_mask(ref[pk]["px"], t,
                                                                     ref[pk]["nmap"][m], pk)
                                                           .loc[ref[pk]["start"]:],
                                                           held_mask(ref[pk]["px"], "NONE",
                                                                     ref[pk]["nmap"][m], pk)
                                                           .loc[ref[pk]["start"]:])))
    CV = pd.DataFrame(curve_rows)
    CV.to_csv(OUT / f"{STEM}.curve.csv", index=False)

    for pk in PANELS:
        sub = CV[(CV.panel == pk) & (CV.constr == "lit")]
        say(f"\n[{pk}] literal book, 10 bps")
        disp = sub.pivot_table(index="m", columns="tilt",
                               values=["g", "signed_dCAGR", "c_INC", "c_OVL"])
        say(disp.to_string(float_format=lambda x: f"{x*100:+.3f}"))
        for t in TREAT:
            s = sub[sub.tilt == t].sort_values("m")
            say(f"    Spearman(m, g) for {t}: {spearman(s.m, s.g):+.3f}   "
                f"Spearman(overlap, g): {spearman(s.overlap, s.g):+.3f}")

    # ================================================================ the crossing m*
    say("\n" + "=" * 190)
    say("### THE NUMBER: m* = the share at which the tilt's gross magnitude stops covering its "
        "cost.  Both estimators, all three bars, both constructions.")
    say("=" * 190)
    for pk in PANELS:
        for cn in CONSTR:
            for t in TREAT:
                s = CV[(CV.panel == pk) & (CV.constr == cn) & (CV.tilt == t)].sort_values("m")
                for bar in BARS:
                    cc = s[f"c_{bar}"].values
                    me = cross_empirical(s.m.values, s.g.values, cc)
                    mf, bg, bc = cross_fitted(s.m.values, s.g.values, cc)
                    mf70, _, _ = cross_fitted(s.m.values, s.g.values, cc, mmax=0.70)
                    cross_rows.append(dict(panel=pk, constr=cn, tilt=t, bar=bar,
                                           m_star_emp=me, m_star_fit=mf, m_star_fit_le70=mf70,
                                           slope_log_g=bg, slope_log_c=bc,
                                           g_at_053=float(s[s.m == 0.53].g.iloc[0]),
                                           c_at_053=float(s[s.m == 0.53][f"c_{bar}"].iloc[0])))
    CR = pd.DataFrame(cross_rows)
    CR.to_csv(OUT / f"{STEM}.crossing.csv", index=False)
    say(CR.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ================================================================ why the crossing may not exist
    say("\n" + "=" * 190)
    say("### THE RATIO g/c — the decisive diagnostic.  A crossing EXISTS only if the ratio falls "
        "through 1 in m, i.e. only if g decays FASTER in m than c does.")
    say("    If value and cost are the same function of share, the ratio is flat and no "
        "threshold exists at any share.  d = slope(log g) - slope(log c); d < 0 is required.")
    say("=" * 190)
    ratio_rows = []
    for pk in PANELS:
        for cn in CONSTR:
            for t in TREAT:
                s = CV[(CV.panel == pk) & (CV.constr == cn) & (CV.tilt == t)].sort_values("m")
                for bar in BARS:
                    rr = (s.g / s[f"c_{bar}"]).values
                    _, bg, bc = cross_fitted(s.m.values, s.g.values, s[f"c_{bar}"].values)
                    ratio_rows.append(dict(panel=pk, constr=cn, tilt=t, bar=bar,
                                           ratio_min=float(np.nanmin(rr)),
                                           ratio_med=float(np.nanmedian(rr)),
                                           ratio_max=float(np.nanmax(rr)),
                                           ratio_at_005=float(rr[0]), ratio_at_053=float(rr[6]),
                                           ratio_at_100=float(rr[-1]),
                                           spearman_m_ratio=spearman(s.m.values, rr),
                                           d_logslope=bg - bc if np.isfinite(bg) and
                                           np.isfinite(bc) else np.nan))
    RA = pd.DataFrame(ratio_rows)
    RA.to_csv(OUT / f"{STEM}.ratio.csv", index=False)
    say(RA.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    lit = RA[RA.constr == "lit"]
    say(f"\n  cells (all 36) whose empirical crossing is locatable inside the grid: "
        f"{int(CR.m_star_emp.notna().sum())} of {len(CR)}")
    say(f"  BAR-OVL, literal, ratio g/c never falls below 1 in: "
        f"{int((lit[lit.bar=='OVL'].ratio_min > 1).sum())} of "
        f"{len(lit[lit.bar=='OVL'])} (panel, tilt) cells")
    say(f"  BAR-INC, literal, ratio g/c never falls below 1 in: "
        f"{int((lit[lit.bar=='INC'].ratio_min > 1).sum())} of "
        f"{len(lit[lit.bar=='INC'])} (panel, tilt) cells")
    say("  |d_logslope| by bar (literal): " + ", ".join(
        f"{b} median {float(lit[lit.bar==b].d_logslope.abs().median()):.3f}" for b in BARS))

    # bootstrap the log-slope difference d for BAR-OVL: is d < 0 distinguishable from 0?
    say("\n  bootstrap of d = slope(log g) - slope(log c), BAR-OVL, literal "
        f"({NBOOT} replicates, same block scheme):")
    dboot_rows = []
    for pk in PANELS:
        for t in TREAT:
            s = CV[(CV.panel == pk) & (CV.constr == "lit") & (CV.tilt == t)].sort_values("m")
            cc = s["c_OVL"].values
            paths = [(RET[(pk, "lit", m, t)][0].values,
                      RET[(pk, "lit", m, "NONE")][0].values) for m in SHARES]
            nobs = len(paths[0][0]); yrs = nobs / 252
            rng3 = np.random.default_rng(SEED + 7000 + hash((pk, t)) % 10_000)
            ds = []
            for _ in range(NBOOT):
                idx = block_idx(nobs, rng3)
                gb = []
                for (a, b) in paths:
                    ca = (1 + a[idx]).prod() ** (1 / yrs) - 1
                    cb = (1 + b[idx]).prod() ** (1 / yrs) - 1
                    gb.append(abs(ca - cb))
                _, bg, bc = cross_fitted(np.array(SHARES), np.array(gb), cc)
                if np.isfinite(bg) and np.isfinite(bc):
                    ds.append(bg - bc)
            ds = np.array(ds)
            lo, hi = float(np.percentile(ds, 5)), float(np.percentile(ds, 95))
            dboot_rows.append(dict(panel=pk, tilt=t, d_point=float(
                RA[(RA.panel == pk) & (RA.constr == "lit") & (RA.tilt == t)
                   & (RA.bar == "OVL")].d_logslope.iloc[0]),
                d_boot_median=float(np.median(ds)), lo5=lo, hi95=hi,
                frac_d_lt_0=float((ds < 0).mean())))
            say(f"    {pk:6s} {t:4s}  d = {dboot_rows[-1]['d_point']:+.3f}  boot 5-95 "
                f"[{lo:+.3f}, {hi:+.3f}]  P(d<0) = {dboot_rows[-1]['frac_d_lt_0']:.1%}  "
                f"{'crossing possible' if hi < 0 else 'NO crossing distinguishable from parallel'}")
    pd.DataFrame(dboot_rows).to_csv(OUT / f"{STEM}.dslope.csv", index=False)

    # ================================================================ bootstrap interval
    say("\n" + "=" * 190)
    say(f"### BOOTSTRAP: circular block bootstrap, block = {BLOCK}d, {NBOOT} replicates, "
        f"seed {SEED}; tilt and control resampled with the SAME block index.")
    say("    Interval is the 5-95 percentile of m*_b (empirical estimator).  'censored' = "
        "replicates with no crossing inside the grid.")
    say("=" * 190)
    rng = np.random.default_rng(SEED)
    for pk in PANELS:
        for t in TREAT:
            s = CV[(CV.panel == pk) & (CV.constr == "lit") & (CV.tilt == t)].sort_values("m")
            paths = []
            for m in SHARES:
                r0t = RET[(pk, "lit", m, t)][0].values
                r0n = RET[(pk, "lit", m, "NONE")][0].values
                paths.append((r0t, r0n))
            nobs = len(paths[0][0])
            yrs = nobs / 252
            for bar in BARS:
                cc = s[f"c_{bar}"].values
                draws, cens = [], 0
                rng2 = np.random.default_rng(SEED + hash((pk, t, bar)) % 10_000)
                for _ in range(NBOOT):
                    idx = block_idx(nobs, rng2)
                    gb = []
                    for (a, b) in paths:
                        ca = (1 + a[idx]).prod() ** (1 / yrs) - 1
                        cb = (1 + b[idx]).prod() ** (1 / yrs) - 1
                        gb.append(abs(ca - cb))
                    mb = cross_empirical(np.array(SHARES), np.array(gb), cc)
                    if np.isfinite(mb):
                        draws.append(mb)
                    else:
                        cens += 1
                d = np.array(draws)
                lo = float(np.percentile(d, 5)) if len(d) else np.nan
                hi = float(np.percentile(d, 95)) if len(d) else np.nan
                md = float(np.median(d)) if len(d) else np.nan
                pt = cross_empirical(s.m.values, s.g.values, cc)
                boot_rows.append(dict(panel=pk, tilt=t, bar=bar, m_star_point=pt,
                                      boot_median=md, lo5=lo, hi95=hi,
                                      width=hi - lo if len(d) else np.nan,
                                      censored=cens / NBOOT))
                say(f"  {pk:6s} {t:4s} BAR-{bar:4s}  point m* = "
                    f"{'n/a  ' if not np.isfinite(pt) else f'{pt:.3f}'}   boot median "
                    f"{'n/a' if not np.isfinite(md) else f'{md:.3f}'}   "
                    f"5-95 [{lo:.3f}, {hi:.3f}] width {hi-lo:.3f}   censored "
                    f"{cens/NBOOT:.1%}")
    BT = pd.DataFrame(boot_rows)
    BT.to_csv(OUT / f"{STEM}.bootstrap.csv", index=False)

    # ================================================================ both KEEP paths
    say("\n" + "=" * 190)
    say("### BOTH KEEP PATHS, all books")
    say("=" * 190)
    for c in COSTS:
        for cn in CONSTR:
            sub = G[G.constr == cn]
            say(f"  @{int(c)}bps {cn:4s}:  4a {int(sub[f'pass4a_{int(c)}'].sum())}/{len(sub)}"
                f"   4b {int(sub[f'pass4b_{int(c)}'].sum())}/{len(sub)}"
                f"   4b-on-OOS-window {int(sub[f'pass4bOOS_{int(c)}'].sum())}/{len(sub)}")
    p4b = G[(G.pass4b_10) | (G.pass4b_25)]
    if len(p4b):
        say("\n  the 4b passes (full sample):")
        say(p4b[["panel", "constr", "m", "n", "tilt", "CAGR_10", "Sharpe_10", "MaxDD_10",
                 "H1_10", "H2_10", "OOSSharpe_10", "pass4b_10", "pass4b_25", "pass4a_10"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        # cross-universe: same (m, tilt, constr) passing on BOTH large-cap panels
        key = ["constr", "m", "tilt"]
        a = set(map(tuple, p4b[(p4b.panel == "u56") & p4b.pass4b_10][key].values))
        b = set(map(tuple, p4b[(p4b.panel == "broad") & p4b.pass4b_10][key].values))
        say(f"\n  cross-universe 4b @10bps (same (constr, m, tilt) on u56 AND broad): "
            f"{len(a & b)} arms -> {sorted(a & b)}")
    else:
        say("  no 4b passes anywhere.")

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 190)
    say("### PROTOCOL RULE 8 WALK-FORWARD — m* re-estimated on the IS window only, pick read "
        "ONCE on 2017-01-01 ->")
    say("=" * 190)
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        bIS, bOOS = ref[pk]["bIS"], ref[pk]["bOOS"]
        for cn in CONSTR:
            for c in COSTS:
                # --- IS curves
                gIS, cIS = {}, {}
                for t in TREAT:
                    gg, ci, co = [], [], []
                    for m in SHARES:
                        r0t, tot, Wt = RET[(pk, cn, m, t)]
                        r0n, ton, Wn = RET[(pk, cn, m, "NONE")]
                        a0, b0 = r0t.loc[:IS_END], r0n.loc[:IS_END]
                        at, bt = tot.loc[:IS_END], ton.loc[:IS_END]
                        yrs = len(a0) / 252
                        gg.append(abs(cagr(a0) - cagr(b0)))
                        ci.append((cagr(a0) - cagr(net(a0, at, c)))
                                  - (cagr(b0) - cagr(net(b0, bt, c))))
                        reb = at[at > 0].index
                        co.append(float((Wt.reindex(reb).fillna(0.0)
                                         - Wn.reindex(reb).fillna(0.0))
                                        .abs().sum(axis=1).sum()) / yrs * c / 1e4)
                    gIS[t] = np.array(gg)
                    cIS[t] = dict(INC=np.array(ci), OVL=np.array(co),
                                  FLAT=np.full(len(SHARES), FLAT_BAR * c / 10.0))
                mstar_IS = {}
                for t in TREAT:
                    mstar_IS[t] = cross_empirical(np.array(SHARES), gIS[t], cIS[t]["OVL"])
                # the gate: the tighter of the two treatments' IS crossings
                cand = [v for v in mstar_IS.values() if np.isfinite(v)]
                gate = min(cand) if cand else 1.01

                # --- IS Sharpe of every book
                isS, allbooks = {}, []
                for m in SHARES:
                    for t in TILTS:
                        r0, to, _ = RET[(pk, cn, m, t)]
                        rc = net(r0, to, c)
                        isS[(m, t)] = metrics(rc.loc[:IS_END])["Sharpe"]
                        allbooks.append((m, t))

                def oos_of(m, t):
                    r0, to, _ = RET[(pk, cn, m, t)]
                    rc = net(r0, to, c).loc[OOS_START:]
                    mm = metrics(rc)
                    return mm["CAGR"], mm["Sharpe"], mm["MaxDD"]

                picks = {}
                # S_MSTAR: tilt free at m <= gate, forced NONE above it
                pool = [(m, t) for (m, t) in allbooks if (m <= gate or t == "NONE")]
                picks["S_MSTAR"] = max(pool, key=lambda k: isS[k])
                picks["S_IS"] = max(allbooks, key=lambda k: isS[k])
                picks["S_NONE"] = (0.53, "NONE")
                for sel, (m, t) in picks.items():
                    oc, os_, od = oos_of(m, t)
                    wf_rows.append(dict(panel=pk, constr=cn, cost=c, selector=sel,
                                        gate=gate, pick_m=m, pick_tilt=t,
                                        pick_n=ref[pk]["nmap"][m],
                                        IS_Sharpe=isS[(m, t)], OOS_CAGR=oc,
                                        OOS_Sharpe=os_, OOS_MaxDD=od))
                v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
                wf_rows.append(dict(panel=pk, constr=cn, cost=c, selector="S_LIVE",
                                    gate=gate, pick_m=np.nan, pick_tilt="INV(n=5,w=.15)",
                                    pick_n=5, IS_Sharpe=metrics(
                                        ref[pk]["v1"][c].loc[:IS_END])["Sharpe"],
                                    OOS_CAGR=v1o["CAGR"], OOS_Sharpe=v1o["Sharpe"],
                                    OOS_MaxDD=v1o["MaxDD"]))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  mean OOS Sharpe by selector over the 12 (panel x constr x cost) cells:")
    piv = WF.groupby("selector")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean()
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    base = WF[WF.selector == "S_IS"].set_index(["panel", "constr", "cost"]).OOS_Sharpe
    ms = WF[WF.selector == "S_MSTAR"].set_index(["panel", "constr", "cost"]).OOS_Sharpe
    nn = WF[WF.selector == "S_NONE"].set_index(["panel", "constr", "cost"]).OOS_Sharpe
    say(f"  S_MSTAR - S_IS   : mean {float((ms-base).mean()):+.4f}, wins "
        f"{int((ms>base).sum())} of {len(base)}")
    say(f"  S_MSTAR - S_NONE : mean {float((ms-nn).mean()):+.4f}, wins "
        f"{int((ms>nn).sum())} of {len(base)}")
    spy_oos = ref['u56']['spy_oos']
    say(f"  SPY OOS: {spy_oos['CAGR']:.2%}/{spy_oos['Sharpe']:.3f}/{spy_oos['MaxDD']:.2%}")

    # ================================================================ prediction scorecard
    say("\n" + "=" * 190)
    say("### PREDICTION SCORECARD")
    say("=" * 190)
    P = {}
    P["P1 reproduction [a]-[d]"] = all(ok.values())
    sp = []
    for pk in ("u56", "broad"):
        for t in TREAT:
            s = CV[(CV.panel == pk) & (CV.constr == "lit") & (CV.tilt == t)].sort_values("m")
            sp.append(spearman(s.m, s.g))
    P["P2 Spearman(m,g) <= -0.6 on both large-cap panels, both tilts"] = all(x <= -0.6 for x in sp)
    inside = []
    for pk in ("u56", "broad"):
        for t in TREAT:
            r = CR[(CR.panel == pk) & (CR.constr == "lit") & (CR.tilt == t)
                   & (CR.bar == "OVL")].m_star_emp
            v = float(r.iloc[0]) if len(r) else np.nan
            inside.append(np.isfinite(v) and 0.15 <= v <= 0.85)
    P["P3 crossing vs BAR-OVL strictly inside [0.15,0.85] on both large-cap panels"] = all(inside)
    P["P4 bootstrap 5-95 width >= 0.25 somewhere"] = bool(
        (BT.width.dropna() >= 0.25).any())
    u = CV[(CV.panel == "u56") & (CV.constr == "lit") & (CV.tilt == "INV") & (CV.m == 0.53)]
    mst_u = CR[(CR.panel == "u56") & (CR.constr == "lit") & (CR.tilt == "INV")
               & (CR.bar == "OVL")].m_star_emp
    mstv = float(mst_u.iloc[0]) if len(mst_u) else np.nan
    P["P5 0.53 below m* on u56 AND signed dCAGR(INV) < 0 there"] = bool(
        (not np.isfinite(mstv) or 0.53 < mstv) and float(u.signed_dCAGR.iloc[0]) < 0)
    P["P6 S_MSTAR beats neither S_IS nor S_NONE on mean OOS Sharpe"] = bool(
        float(ms.mean()) <= float(base.mean()) and float(ms.mean()) <= float(nn.mean()))
    for k, v in P.items():
        say(f"  {'HELD  ' if v else 'FAILED'}  {k}")
    say(f"  {sum(P.values())} of {len(P)} predictions held.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.{{console.txt,grid.csv,curve.csv,crossing.csv,ratio.csv,dslope.csv,"
        f"bootstrap.csv,walkforward.csv}}")


if __name__ == "__main__":
    main()
