#!/usr/bin/env python3
"""Idea 324 - "does-the-IS-CHOOSER-ever-beat-a-coin-across-BOOKS" (lane C, 2026-09-07).

The question
------------
PROTOCOL rule 8 (walk-forward) is applied everywhere in this record as if in-sample
selection were informative: choose the parameter on 2009-2016, evaluate 2017-2026
untouched.  Idea 47 found that on ITS four books the rule-8 chooser picked the OOS-best
in 27/90 cells (chance 22.5), 0/30 on the small panel, and was ANTI-correlated on B136
(it picked F085 in 0/30 cells while F085 won OOS in 30/30).  The queue asks for a
census: across the record's multi-arm families, does the IS pick beat a coin?

"A coin" is made precise here as **the arm-average**: the expected result of choosing an
arm at random from the same grid.  Two null-comparands are reported for every cell -
the mean OOS Sharpe over the family's arms (what a random pick earns in expectation) and
the pick's percentile rank inside the family's OOS ordering (coin expectation 0.5).
The OOS-best is reported as the ceiling (chance 1/k).

Why this is run as live grids and not as a text scrape of LEADERBOARD.md
------------------------------------------------------------------------
The leaderboard rows record verdicts, not each study's IS pick and its arm-by-arm OOS
ordering, so a scrape cannot answer the question.  Instead the record's own dials are
rebuilt as six families and re-run end to end, so every arm's IS and OOS metrics are
computed here and every cell is reported.

The six families (the record's own dials, taken as GIVEN - none of them is searched)
-----------------------------------------------------------------------------------
    N   top-n at GROSS/n, de-grossing when E_t < n        n in {5,10,15,20,25,30,40}   (idea 2)
    F   top ceil(f*E_t) at GROSS/k                        f in {0.25,.4,.55,.7,.85,1.0} (idea 46)
    B   RULES v2 band book, band b                        b in {0,.02,.04,.06,.08,.10,.12}
    V   top-20 with eligibility vol20 < c                 c in {.25,.35,.45,.60,.80,9.9} (idea 314)
    G   top-20 gated to cash below breadth quintile q     q in {0,1,2,3,4}              (idea 48)
    R   top-20 at rebalance frequency                     freq in {D,W,M,Q}
35 arms per panel.  Panels: U56 (universe.json), B136 (universe_broad.json), SMALL439
(sub-$2B screen, max_1d_move >= 1.0 dropped).  105 backtests, all at 10 bps, t+1 fill.

The two tuned parameters (PROTOCOL rule 4 - and they are the OBJECT of study, not dials
on a book)
----------------------------------------------------------------------------------------
    chooser statistic  in {IS_Sharpe, IS_CAGR, IS_4b}   (IS_4b = best IS Sharpe among arms
                                                         clearing the IS 4b bars; falls back
                                                         to IS_Sharpe when none clears, and
                                                         the fallback is flagged in the CSV)
    IS/OOS split year  in {2014, 2016, 2018}            (2016 is PROTOCOL rule 8's own)
6 families x 3 panels x 3 stats x 3 splits = 162 census cells, ALL reported.

Composite books (the part that gets a LEADERBOARD row)
------------------------------------------------------
At PROTOCOL's own setting (IS_Sharpe, split 2016) two books are formed on U56 and B136:
    CHOOSER = equal-weight blend of the 6 families' IS-picked arms
    COIN    = equal-weight blend of ALL 35 arms
Both are run through baseline.compare (full sample + halves vs RULES v2 and SPY) and both
KEEP paths are evaluated on the full sample and on the OOS window alone.  CHOOSER's picks
are made on IS data only, so its OOS window is clean; its full-sample numbers are IS-
contaminated by construction and are labelled as such.

SURVIVORSHIP: all three panels are current-constituent lists, so absolute CAGRs are
optimistic.  The census statistic is a WITHIN-panel, within-family comparison of a pick
against its own arm-average, which is far less exposed to that bias than the levels are.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys, json, math
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, score, rules_v2_weights, compare, backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
GROSS, COST, WARM = 0.75, 10.0, 260
SPLITS = [2014, 2016, 2018]
STATS = ["IS_Sharpe", "IS_CAGR", "IS_4b"]


# ---------------------------------------------------------------- books (the arms) -----
def _elig(px, max_vol=0.60):
    s, above, vol20 = score(px, vol_scale=True)
    return s.where(above & (vol20 < max_vol))


def w_topn(px, n=20, max_vol=0.60):
    e = _elig(px, max_vol)
    return (e.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)


def w_frac(px, f=0.85):
    e = _elig(px)
    E = e.notna().sum(axis=1)
    k = np.ceil(f * E).clip(lower=1)
    sel = e.rank(axis=1, ascending=False).le(k, axis=0) & e.notna()
    return sel.astype(float).div(k.replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def breadth_pct(px, win=756, minp=252):
    """Causal percentile of today's breadth (share of priced names above their 200d MA)
    within the trailing `win` trading days.  Uses only data available at close t."""
    ma = px.rolling(200).mean()
    above = (px > ma) & px.notna()
    brd = above.sum(axis=1) / px.notna().sum(axis=1).replace(0, np.nan)
    return brd.rolling(win, min_periods=minp).apply(lambda x: float((x <= x[-1]).mean()), raw=True)


def w_gate(px, q=0, pct=None):
    w = w_topn(px, 20)
    if q == 0:
        return w
    off = (pct <= q / 5.0).fillna(False)          # NaN warm-up -> ungated
    return w.where(~off, 0.0)


def family_arms(px):
    """{family: [(arm_label, weights DataFrame, freq), ...]} - fixed, nothing searched."""
    pct = breadth_pct(px)
    fam = {}
    fam["N"] = [(f"N{n}", w_topn(px, n), "W") for n in (5, 10, 15, 20, 25, 30, 40)]
    fam["F"] = [(f"F{f:.2f}", w_frac(px, f), "W") for f in (0.25, 0.40, 0.55, 0.70, 0.85, 1.00)]
    fam["B"] = [(f"B{b:.2f}", rules_v2_weights(px, band=b, gross=GROSS), "W")
                for b in (0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12)]
    fam["V"] = [(f"V{c:.2f}", w_topn(px, 20, max_vol=c), "W")
                for c in (0.25, 0.35, 0.45, 0.60, 0.80, 9.90)]
    fam["G"] = [(f"G{q}", w_gate(px, q, pct), "W") for q in (0, 1, 2, 3, 4)]
    fam["R"] = [(f"R{f}", w_topn(px, 20), f) for f in ("D", "W", "M", "Q")]
    return fam


# ---------------------------------------------------------------- metric helpers -------
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass_4b(r, spy):
    """PROTOCOL 4b on one window: Sharpe > SPY in BOTH halves, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  (The OOS leg of 4b is checked separately by the caller.)"""
    c, s, d = m3(r); cs, ss, ds = m3(spy)
    h1, h2 = halves(r); s1, s2 = halves(spy)
    return bool(h1 > s1 and h2 > s2 and d >= 0.6 * ds and c >= 0.7 * cs)


def pctrank(vals, i):
    """Percentile rank of arm i among `vals` (0 = worst, 1 = best), ties shared.
    A coin drawn uniformly from the arms has expectation 0.5."""
    v = np.asarray(vals, float); k = len(v)
    if k < 2: return np.nan
    lt = float((v < v[i]).sum()); eq = float((v == v[i]).sum()) - 1.0
    return (lt + 0.5 * eq) / (k - 1)


def spearman(a, b):
    ra = pd.Series(a).rank(); rb = pd.Series(b).rank()
    return float(ra.corr(rb))


# ---------------------------------------------------------------- panels ---------------
def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c not in bad]
    out["SMALL439"] = pxs[keep].dropna(how="all").ffill()
    return out


# ---------------------------------------------------------------- main -----------------
def main():
    con = []
    def say(*a):
        line = " ".join(str(x) for x in a); print(line); con.append(line)

    P = panels()
    say("# Idea 324 - does the rule-8 IS chooser beat a coin?  (lane C, 10 bps, t+1)")
    for k, v in P.items():
        say(f"  panel {k}: {v.shape[1]} cols x {len(v)} rows, {v.index[0].date()} .. {v.index[-1].date()}")

    grid_rows, cells, wmats = [], [], {}
    for pname, px in P.items():
        spy_all = px["SPY"].pct_change().fillna(0.0)
        start = px.index[WARM]
        fam = family_arms(px)
        rets, W = {}, {}
        for f, arms in fam.items():
            for label, w, freq in arms:
                res = backtest(px, w, cost_bps=COST, freq=freq)
                r = res["returns"].loc[start:]
                rets[(f, label)] = r
                W[(f, label)] = w
                c, s, d = m3(r)
                grid_rows.append(dict(panel=pname, family=f, arm=label, freq=freq,
                                      CAGR=c, Sharpe=s, MaxDD=d,
                                      turnover_yr=res["turnover"].loc[start:].sum() / (len(r) / 252)))
        wmats[pname] = W
        say(f"  {pname}: {len(rets)} arms backtested")

        # ---- census: for every (family, split, stat), who does the IS chooser pick? ----
        for split in SPLITS:
            is_end, oos_start = f"{split}-12-31", f"{split+1}-01-01"
            for f, arms in fam.items():
                labels = [a[0] for a in arms]
                R = [rets[(f, l)] for l in labels]
                Ris = [r.loc[:is_end] for r in R]
                Roos = [r.loc[oos_start:] for r in R]
                spy_is, spy_oos = spy_all.loc[start:is_end], spy_all.loc[oos_start:]
                is_sh = [metrics(x)["Sharpe"] for x in Ris]
                is_cg = [metrics(x)["CAGR"] for x in Ris]
                is_4b = [pass_4b(x, spy_is) for x in Ris]
                oos_sh = [metrics(x)["Sharpe"] for x in Roos]
                oos_cg = [metrics(x)["CAGR"] for x in Roos]
                oos_4b = [pass_4b(x, spy_oos) for x in Roos]
                rho = spearman(is_sh, oos_sh)
                for stat in STATS:
                    fell_back = False
                    if stat == "IS_Sharpe":
                        i = int(np.argmax(is_sh))
                    elif stat == "IS_CAGR":
                        i = int(np.argmax(is_cg))
                    else:
                        ok = [j for j, p in enumerate(is_4b) if p]
                        if ok:
                            i = max(ok, key=lambda j: is_sh[j])
                        else:
                            i = int(np.argmax(is_sh)); fell_back = True
                    best = int(np.argmax(oos_sh))
                    cells.append(dict(
                        panel=pname, family=f, k=len(labels), split=split, stat=stat,
                        pick=labels[i], oos_best=labels[best], fell_back=fell_back,
                        pick_oos_Sharpe=oos_sh[i], arm_mean_oos_Sharpe=float(np.mean(oos_sh)),
                        arm_med_oos_Sharpe=float(np.median(oos_sh)),
                        best_oos_Sharpe=oos_sh[best], worst_oos_Sharpe=float(np.min(oos_sh)),
                        arm_sd_oos_Sharpe=float(np.std(oos_sh, ddof=1)),
                        d_vs_mean=oos_sh[i] - float(np.mean(oos_sh)),
                        z_vs_mean=(oos_sh[i] - float(np.mean(oos_sh))) /
                                  float(np.std(oos_sh, ddof=1)) if np.std(oos_sh, ddof=1) > 1e-12 else np.nan,
                        pctrank_Sharpe=pctrank(oos_sh, i),
                        pctrank_CAGR=pctrank(oos_cg, i),
                        is_oos_best=int(i == best),
                        pick_oos_4b=int(oos_4b[i]), n_arms_oos_4b=int(sum(oos_4b)),
                        spearman_is_oos=rho,
                        pick_is_Sharpe=is_sh[i], pick_oos_CAGR=oos_cg[i],
                        arm_mean_oos_CAGR=float(np.mean(oos_cg)),
                        spy_oos_Sharpe=metrics(spy_oos)["Sharpe"],
                        spy_oos_CAGR=metrics(spy_oos)["CAGR"]))

    grid = pd.DataFrame(grid_rows); grid.to_csv(f"{OUT}.grid.csv", index=False)
    cen = pd.DataFrame(cells); cen.to_csv(f"{OUT}.census.csv", index=False)

    # ------------------------------------------------------------ census verdict -------
    say("")
    say("## CENSUS - 162 cells (6 families x 3 panels x 3 chooser stats x 3 splits), all in .census.csv")
    say(f"  cells                                 : {len(cen)}")
    say(f"  IS pick beats the ARM-MEAN OOS Sharpe : {int(cen.d_vs_mean.gt(0).sum())}/{len(cen)} "
        f"({cen.d_vs_mean.gt(0).mean():.1%}; coin = 50.0%)")
    say(f"  mean pctrank of the pick (coin = 0.500): {cen.pctrank_Sharpe.mean():.3f}  "
        f"median {cen.pctrank_Sharpe.median():.3f}")
    exp_best = float((1.0 / cen.k).sum())
    say(f"  IS pick IS the OOS-best               : {int(cen.is_oos_best.sum())}/{len(cen)} "
        f"(chance {exp_best:.1f})")
    say(f"  mean OOS Sharpe of pick - arm-mean    : {cen.d_vs_mean.mean():+.4f} "
        f"(median {cen.d_vs_mean.median():+.4f})")
    say(f"  mean Spearman(IS Sharpe, OOS Sharpe)  : {cen.spearman_is_oos.mean():+.3f} "
        f"over {cen.groupby(['panel','family','split']).ngroups} independent orderings")
    say(f"  pick passes OOS 4b                    : {int(cen.pick_oos_4b.sum())}/{len(cen)}; "
        f"arms passing OOS 4b overall {int(cen.n_arms_oos_4b.sum())}/{int(cen.k.sum())}")
    say(f"  IS_4b chooser fell back to IS_Sharpe  : {int(cen.fell_back.sum())}/{int((cen.stat=='IS_4b').sum())} of its cells")
    say(f"  mean effect size (pick - mean)/sd_arms: {cen.z_vs_mean.mean():+.3f} "
        f"(median {cen.z_vs_mean.median():+.3f}); the OOS-best arm sits at "
        f"{cen.groupby(['panel','family','split']).apply(lambda g: (g.best_oos_Sharpe.iloc[0]-g.arm_mean_oos_Sharpe.iloc[0])/g.arm_sd_oos_Sharpe.iloc[0]).mean():+.3f}")

    def sign_p(x, n):
        return min(1.0, 2 * min(sum(math.comb(n, j) for j in range(x, n + 1)),
                                sum(math.comb(n, j) for j in range(0, x + 1))) / 2 ** n)

    n, x = len(cen), int(cen.d_vs_mean.gt(0).sum())
    say(f"  two-sided sign test, all 162 cells    : p = {sign_p(x, n):.4f}  "
        f"(OVERSTATED - the 162 cells share only 54 arm orderings and the 3 stats mostly agree)")
    ind = cen[cen.stat == "IS_Sharpe"]                     # PROTOCOL rule 8's own statistic
    ni, xi = len(ind), int(ind.d_vs_mean.gt(0).sum())
    say(f"  HEADLINE - rule 8's own stat (IS_Sharpe), {ni} orderings:")
    say(f"    beats arm-mean {xi}/{ni} ({xi/ni:.1%}), sign-test p = {sign_p(xi, ni):.4f}, "
        f"mean pctrank {ind.pctrank_Sharpe.mean():.3f}, mean dSharpe {ind.d_vs_mean.mean():+.4f}, "
        f"mean z {ind.z_vs_mean.mean():+.3f}")
    one = ind[ind.split == 2016]                           # fully non-overlapping windows
    n1, x1 = len(one), int(one.d_vs_mean.gt(0).sum())
    say(f"    at the single PROTOCOL split (2016), {n1} orderings: beats arm-mean {x1}/{n1}, "
        f"p = {sign_p(x1, n1):.4f}, mean z {one.z_vs_mean.mean():+.3f}")
    say("    (splits 2014/2016/2018 reuse overlapping data, so only the 2016 row is clean of that.)")

    for by in ("panel", "family", "stat", "split"):
        say("")
        say(f"### by {by}")
        g = cen.groupby(by).agg(cells=("pctrank_Sharpe", "size"),
                                beats_mean=("d_vs_mean", lambda s: float((s > 0).mean())),
                                mean_pctrank=("pctrank_Sharpe", "mean"),
                                mean_dSharpe=("d_vs_mean", "mean"),
                                is_best=("is_oos_best", "sum"),
                                mean_z=("z_vs_mean", "mean"),
                                mean_rho=("spearman_is_oos", "mean"))
        say(g.to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ composites ----------
    say("")
    say("## COMPOSITE BOOKS at PROTOCOL's own setting (stat=IS_Sharpe, split 2016)")
    comp_rows, lb_lines = [], []
    for pname in ("U56", "B136"):
        px = P[pname]; W = wmats[pname]
        sub = cen[(cen.panel == pname) & (cen.stat == "IS_Sharpe") & (cen.split == 2016)]
        picks = {r.family: r.pick for r in sub.itertuples()}
        say(f"  {pname} picks: " + ", ".join(f"{f}={picks[f]}" for f in ("N", "F", "B", "V", "G", "R")))
        chooser_w = sum(W[(f, l)] for f, l in picks.items()) / len(picks)
        coin_w = sum(W[k] for k in W) / len(W)
        for bname, wm in (("CHOOSER", chooser_w), ("COIN", coin_w)):
            say("")
            say(f"--- {bname} composite on {pname} (full sample; CHOOSER's IS window is contaminated by construction) ---")
            out = compare(f"idea324-{bname}-{pname}", lambda _px, _w=wm: _w, px)
            con.append(out["table"].to_string(float_format=lambda x: f"{x:.3f}"))
            con.append("Verdict: " + out["verdict"])
            lb_lines.append(out["row"])
            # OOS-only evaluation (rule 8): 2017-01-01 onward
            r = backtest(px, wm, cost_bps=COST, freq="W")["returns"].loc[px.index[WARM]:]
            b = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[px.index[WARM]:]
            spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARM]:]
            ro, bo, so = r.loc["2017-01-01":], b.loc["2017-01-01":], spy.loc["2017-01-01":]
            c, s, d = m3(ro); bc, bs, bd = m3(bo); sc, ss, sd = m3(so)
            h1, h2 = halves(r); s1, s2 = halves(spy); b1, b2 = halves(b)
            p4a = bool(h1 > b1 and h2 > b2 and m3(r)[2] >= m3(b)[2])
            p4b = bool(h1 > s1 and h2 > s2 and s > ss and m3(r)[2] >= 0.6 * m3(spy)[2] and m3(r)[0] >= 0.7 * m3(spy)[0])
            say(f"  OOS 2017+ : {bname:8s} CAGR {c:6.2%}  Sharpe {s:5.3f}  MaxDD {d:7.2%}")
            say(f"              RULES v2 CAGR {bc:6.2%}  Sharpe {bs:5.3f}  MaxDD {bd:7.2%}")
            say(f"              SPY      CAGR {sc:6.2%}  Sharpe {ss:5.3f}  MaxDD {sd:7.2%}")
            say(f"  4a {'PASS' if p4a else 'FAIL'} / 4b {'PASS' if p4b else 'FAIL'}  "
                f"(full-sample halves {h1:.3f}/{h2:.3f} vs SPY {s1:.3f}/{s2:.3f}, v2 {b1:.3f}/{b2:.3f})")
            comp_rows.append(dict(panel=pname, book=bname, full_CAGR=m3(r)[0], full_Sharpe=m3(r)[1],
                                  full_MaxDD=m3(r)[2], H1=h1, H2=h2, oos_CAGR=c, oos_Sharpe=s, oos_MaxDD=d,
                                  oos_v2_CAGR=bc, oos_v2_Sharpe=bs, oos_v2_MaxDD=bd,
                                  oos_spy_CAGR=sc, oos_spy_Sharpe=ss, oos_spy_MaxDD=sd,
                                  pass_4a=p4a, pass_4b=p4b))
    cp = pd.DataFrame(comp_rows); cp.to_csv(f"{OUT}.composites.csv", index=False)

    say("")
    say("## DOES THE ARM-BY-ARM EDGE SURVIVE INTO A BOOK?  CHOOSER minus COIN, OOS 2017+")
    for pn in ("U56", "B136"):
        ch = cp[(cp.panel == pn) & (cp.book == "CHOOSER")].iloc[0]
        co = cp[(cp.panel == pn) & (cp.book == "COIN")].iloc[0]
        say(f"  {pn:5s} dSharpe {ch.oos_Sharpe - co.oos_Sharpe:+.3f}   "
            f"dCAGR {ch.oos_CAGR - co.oos_CAGR:+.2%}   dMaxDD {ch.oos_MaxDD - co.oos_MaxDD:+.2%}   "
            f"(CHOOSER {ch.oos_Sharpe:.3f} vs COIN {co.oos_Sharpe:.3f}); 4a/4b: "
            f"CHOOSER {'P' if ch.pass_4a else 'F'}/{'P' if ch.pass_4b else 'F'}, "
            f"COIN {'P' if co.pass_4a else 'F'}/{'P' if co.pass_4b else 'F'}")

    say("")
    say("## LEADERBOARD rows")
    for l in lb_lines: say(l)
    Path(f"{OUT}.console.txt").write_text("\n".join(con) + "\n")


if __name__ == "__main__":
    main()
