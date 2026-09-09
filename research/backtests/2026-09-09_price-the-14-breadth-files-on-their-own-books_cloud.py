#!/usr/bin/env python3
"""Idea 286 — price the 14 `breadth` files on their own books.

Idea 276's census left 14 files naming `breadth` explicitly as the TIGHT LOWER BOUND on the
set exposed to a collinearity: over 53 panels `breadth` (the share of a panel the RULES v1
gate admits) is perfectly bimodal — every SMALL439-derived panel 0.307-0.329, every large-cap
panel 0.619-0.745, no overlap — so a claim that reads "X happens because the panel's breadth
is low" is, on named panels, indistinguishable from "X happens on small caps".  The queue asks
to re-run each of those files' HEADLINE comparison with the cap mix q reported beside the
breadth reading, and to count how many headlines survive the restatement.

Three stages.

  A. AUDIT the 14.  Extract each file's headline block and ask two questions of it: does the
     HEADLINE assert a comparison across the capitalisation line, and does it attribute that
     comparison to a panel property?  Both are hand-read against the quoted sentence and the
     reading is committed to .audit.csv, so the classification can be checked rather than
     believed.  (Idea 276 said its own census was keyword-level and named 14 as a lower bound;
     this stage is the semantic pass it asked for.)

  B. RESTATE on the cap-mix ladder.  Rebuild idea 276's MIX construction — k = 40 names, a
     share q drawn from the sub-$2B panel and 1-q from the large-cap stock panel, q on a
     5-rung ladder, 8 draws per rung — measure breadth on every panel, and re-run the headline
     statistic of every restatable family with q AND breadth reported side by side.  Each
     family's verdict is then read off the ladder rather than off two named panels.  Because
     breadth is a deterministic-ish function of q, the only honest question left is whether
     breadth carries anything ONCE q IS CONTROLLED: that is a within-q regression, reported
     with its degrees of freedom (N, p, dof) per idea 512.

  C. PROTOCOL.  Rule-8 walk-forward (arm chosen on the first half, second half read once) and
     BOTH KEEP paths (4a vs the live RULES v2, 4b vs SPY) for every arm on every panel.

Two tuned parameters, and only two: book size n and gross g.  The cap-mix q, the draw index
and the per-family dials (fixed at the values the SOURCE files published, never searched here)
are treatment axes; every grid point is reported.

Costs 10 bps, weekly, weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: the sub-$2B panel and B136 are CURRENT constituents of their screens, and every
mixed panel inherits that bias on its small-cap side; the small-cap half of every q rung is
biased upward by an unknown amount, so no LEVEL comparison across q is a tradable statement.
The object under test is the ORDERING of a dial's effect along q, which survivorship moves
only through the level of the eligible share.
"""
from __future__ import annotations
import json, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, score  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-09_price-the-14-breadth-files-on-their-own-books_cloud"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
K_MIX, N_DRAWS = 40, 8
QS = [0.0, 0.25, 0.5, 0.75, 1.0]
NS = [10, 20, 30]                 # tuned param 1
GROSS = [0.75, 1.00]              # tuned param 2
SEL = [0.25, 0.50, 0.75, 0.90, 1.00]   # idea 155's selectivity grid, taken as published
M_SHARE = 0.50                    # idea 157's book share m, taken as published

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ------------------------------------------------------------------ A. the 14 files
# idea 276's census: research/backtests/2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-
# the-record_cloud.census.csv, rows with breadth & cross.  Read back rather than retyped.
CENSUS = OUT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv"

# Hand-read of each headline block, with the family whose statistic restates it.
#   family SIZE   sign of Sharpe(bigger book) - Sharpe(smaller book)
#   family SHARE  a share-of-eligible book against a fixed-n book
#   family SEL    the selectivity that maximises the Sharpe premium over EWall
#   family REV    the Sharpe-vs-CAGR ordering reversal share
#   family NONE   the headline makes no cross-cap panel-property comparison
AUDIT = {
 "2026-09-04_insider-cluster-smallcap.result.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=False,
    headline="KILL - all 8 arms, both KEEP paths ... the book-size problem is fixed and the result got worse",
    why="cross-cap (mega-cap idea 32 vs the 439-name panel) but the headline attributes the "
        "result to insider-signal quality and book size, not to a panel property; and its "
        "instrument is a Form 4 cache, not a price-only panel dial, so the q ladder cannot carry it"),
 "2026-09-05_does-book-share-price-a-tilt_C.result.md": dict(
    family="SHARE", cross_cap=True, breadth_in_headline=True,
    headline="book share prices a cross-sectional tilt; the key's own t-statistic does not",
    why="the headline statistic is a book expressed as a SHARE of the eligible set, i.e. of breadth"),
 "2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.result.md": dict(
    family="SIZE", cross_cap=True, breadth_in_headline=True,
    headline="the size floor is a UNIVERSE clause ... the sign reverses at exactly one boundary - the sub-$2B panel",
    why="an explicit sign reversal across the capitalisation line - the collinearity idea 276 names"),
 "2026-09-05_required-gross-as-a-leaderboard-column_cloud.result.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=False,
    headline="KILL of the proposed column as a re-labelling device",
    why="the headline is about a column's rehabilitation rate over 378 books, not a cross-cap comparison"),
 "2026-09-05_the-on-share-column_cloud.result.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=True,
    headline="on-share ALONE does not predict which published overlay claims are inside their band",
    why="on-share is a book property (share of days armed), not a panel's eligible share; the "
        "headline compares CLAIMS, not panels"),
 "2026-09-05_the-screen-is-a-book-size-rule_cloud.result.md": dict(
    family="SIZE", cross_cap=True, breadth_in_headline=False,
    headline="n >= 25 ... fires in 11 of 11 cells including ... the two small-panel cells where the screen is structurally empty",
    why="the headline asserts the size floor fires on BOTH sides of the cap line"),
 "2026-09-06_do-the-18-majority-reversing-files-have-reversing-HEADLINES_cloud.result.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=False,
    headline="0 of 48 HEADLINE sentences change once the CAGR column is beside them",
    why="a claim about the record's sentences, not about panels"),
 "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.result.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=True,
    headline="conditional arms lose more per armed day than unconditional ones ... BETTER in 82/136 for breadth20",
    why="`breadth20` here NAMES AN INSTRUMENT (a breadth gate), not a panel property - a false "
        "positive of idea 276's keyword census"),
 "2026-09-06_is-the-reversal-share-a-function-of-n-over-n_elig_C.result.md": dict(
    family="REV", cross_cap=True, breadth_in_headline=True,
    headline="reversal share is NOT a monotone function of n / n_elig ... at MATCHED ratio the five panels disagree 0.00 vs 1.00 in 6 of 7 rows",
    why="n_elig is breadth x k; the headline is a cross-panel disagreement at matched breadth ratio"),
 "2026-09-06_is-the-sharpe-cagr-reversal-a-PANEL-property_C.result.md": dict(
    family="REV", cross_cap=True, breadth_in_headline=True,
    headline="small-cap panels never reverse, large-cap panels usually do",
    why="the binary cross-cap fact idea 276 was written to test"),
 "2026-09-06_time-varying-share-vs-fixed-n_B.result.md": dict(
    family="SHARE", cross_cap=True, breadth_in_headline=True,
    headline="KILL of the time-varying count n_t = round(m x E_t)",
    why="E_t is the eligible count, i.e. breadth x k, measured on 3 panels across the cap line"),
 "2026-09-06_where-selectivity-and-cost-cross_B.result.md": dict(
    family="SEL", cross_cap=True, breadth_in_headline=True,
    headline="the q that maximises the net Sharpe premium over EWall is 0.90 on U56 and 0.95 on B136 ... on the small panel there is one crossing",
    why="an explicit large-vs-small statement about where selectivity pays"),
 "LEADERBOARD.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=True,
    headline="(not a headline: a 2,543-row table)",
    why="idea 276 counted the corpus files LEADERBOARD.md and CHANGELOG.md, which carry no headline "
        "sentence to restate; 6 of its own leaderboard ROWS are cross-cap with a panel-property word"),
 "CHANGELOG.md": dict(
    family="NONE", cross_cap=True, breadth_in_headline=True,
    headline="(not a headline: the rules log)", why="same as LEADERBOARD.md"),
}

# ------------------------------------------------------------------ panels (idea 276's construction)
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c != "SPY" and c not in bad]
    return px, keep, len(bad)

def build_sources():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    px56, pxb = load_universe(), load_universe(broad=True)
    pxs, s_stk, ndrop = small_panel()
    b_all = [c for c in pxb.columns if c != "SPY"]
    b_stk = [c for c in b_all if c not in etfs]
    return dict(px56=px56, pxb=pxb, pxs=pxs, s_stk=s_stk, b_stk=b_stk,
                u_all=[c for c in px56.columns if c != "SPY"], ndrop=ndrop)

def gate(px):
    """RULES v1 eligibility, unchanged from idea 276."""
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return above & (vol20 < 0.60)

def breadth_of(px, cols):
    e = gate(px[cols])
    w = e.loc[rebalance_mask(px.index, FREQ).values].iloc[40:]
    return float((w.sum(axis=1) / len(cols)).mean()) if len(w) else np.nan

# ------------------------------------------------------------------ books
def _elig(px, tradables):
    s, above, vol20 = score(px[tradables], vol_scale=False)
    return s.where(above & (vol20 < 0.60))

def w_topn(n, gross):
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        rank = _elig(px, tr).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (gross / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f

def w_ewall(gross):
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        e = _elig(px, tr).notna().astype(float)
        cnt = e.sum(axis=1).replace(0, np.nan)
        return (gross * e.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0)
    return f

def w_share(m, gross):
    """idea 157's time-varying count n_t = round(m * E_t), E_t the eligible count."""
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        el = _elig(px, tr)
        E = el.notna().sum(axis=1)
        nt = (m * E).round().clip(lower=1)
        rank = el.rank(axis=1, ascending=False)
        sel = rank.le(nt, axis=0).astype(float)
        cnt = sel.sum(axis=1).replace(0, np.nan)
        return (gross * sel.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0)
    return f

def w_sel(s, gross):
    """idea 155's selectivity: hold the top s-share of the eligible set (s=1.0 == EWall)."""
    return w_share(s, gross)

# ------------------------------------------------------------------ dof-aware within fit (idea 512)
def ncdf(x): return 0.5 * (1.0 + __import__("math").erf(x / __import__("math").sqrt(2.0)))

def within_fit(d, xcol, ycol, cellcol, min_cell=2):
    """Cell-demeaned OLS with BOTH dof conventions reported (idea 512's required columns)."""
    import math
    d = d[[cellcol, xcol, ycol]].dropna()
    d = d[d.groupby(cellcol)[cellcol].transform("size") >= min_cell]
    N = len(d); P = int(d[cellcol].nunique()) if N else 0
    out = dict(N=N, p=P, dof_naive=N - 2, dof_correct=N - P - 1)
    if N < 10 or P < 2 or N - P - 1 <= 1:
        return {**out, "slope": np.nan, "R2": np.nan, "t_naive": np.nan, "t_correct": np.nan,
                "inflation": np.nan}
    x = (d[xcol] - d.groupby(cellcol)[xcol].transform("mean")).values.astype(float)
    y = (d[ycol] - d.groupby(cellcol)[ycol].transform("mean")).values.astype(float)
    sxx = float(x @ x)
    if sxx <= 0:
        return {**out, "slope": np.nan, "R2": np.nan, "t_naive": np.nan, "t_correct": np.nan,
                "inflation": np.nan}
    b = float(x @ y) / sxx; e = y - b * x
    rss = float(e @ e); sst = float(y @ y)
    tn = b / math.sqrt(rss / (N - 2) / sxx)
    tc = b / math.sqrt(rss / (N - P - 1) / sxx)
    return dict(out, slope=b, R2=1 - rss / sst if sst > 0 else np.nan, t_naive=tn, t_correct=tc,
                inflation=math.sqrt((N - 2) / (N - P - 1)))

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {STAMP}\n")

    # ---------------- A. audit -------------------------------------------
    cen = pd.read_csv(CENSUS)
    fourteen = sorted(cen[cen.breadth & cen.cross].file.tolist())
    say("## A. AUDIT of idea 276's 14 `breadth` files")
    say(f"idea 276's census reproduces at {len(fourteen)} files (breadth & cross) — "
        f"{'MATCH' if len(fourteen) == 14 else 'MISMATCH'} against its published 14")
    missing = [f for f in fourteen if f not in AUDIT]
    if missing:
        say(f"!! files not covered by this run's hand-read: {missing}")
    rows = []
    for f in fourteen:
        a = AUDIT.get(f, dict(family="UNREAD", cross_cap=None, breadth_in_headline=None,
                              headline="", why=""))
        rows.append(dict(file=f, **a))
    AU = pd.DataFrame(rows)
    AU.to_csv(OUT / f"{STAMP}.audit.csv", index=False)
    say("\nhand-read of each headline block (the quoted sentence is in .audit.csv):")
    say(AU.groupby("family").agg(files=("file", "size"),
                                 breadth_word_in_headline=("breadth_in_headline", "sum")).to_string())
    rest = AU[AU.family != "NONE"]
    say(f"\nheadlines that actually assert a cross-cap comparison carried by a PANEL PROPERTY, "
        f"and are therefore restatable on a cap-mix ladder: {len(rest)} of {len(AU)}")
    for _, r in rest.iterrows():
        say(f"  [{r.family}] {r.file}\n        \"{r.headline}\"")
    say(f"\nthe other {len(AU)-len(rest)}: {', '.join(AU[AU.family=='NONE'].file)}")
    for _, r in AU[AU.family == "NONE"].iterrows():
        say(f"  - {r.file}: {r.why}")
    say("")

    # ---------------- B. the ladder --------------------------------------
    src = build_sources()
    say(f"## B. RESTATEMENT on the cap-mix ladder (idea 276's MIX construction)")
    say(f"small panel: dropped {src['ndrop']} tickers with max_1d_move >= 1.0; "
        f"{len(src['s_stk'])} names available; large-cap stock pool {len(src['b_stk'])}")
    spy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]

    # every mixed panel is run on ONE common window - the small panel's trading days - so the
    # q rungs are comparable to each other; the named anchors keep their own windows, as the
    # files being restated used them.
    COMMON = src["pxs"].index

    def mk(cols_s, cols_l, label=""):
        parts = []
        if cols_s: parts.append(src["pxs"][cols_s])
        if cols_l: parts.append(src["pxb"][cols_l].reindex(COMMON, method="ffill"))
        px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
        return px.join(spy.reindex(px.index, method="ffill").rename("SPY"))

    panels = []
    rng = np.random.default_rng(20260909)
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
            panels.append((f"MIX q={q:.2f} d{d}", "mix", q, mk(sc, lc, "")))
    # named anchors, for continuity with the files being restated
    panels.append(("U56", "named", 0.0, src["px56"]))
    panels.append(("B136", "named", 0.0, src["pxb"]))
    sm = src["pxs"][src["s_stk"]].join(src["pxs"]["SPY"])
    panels.append((f"SMALL{len(src['s_stk'])}", "named", 1.0, sm))
    say(f"panels: {len(QS)}x{N_DRAWS} mixed (k={K_MIX}) + 3 named = {len(panels)}")

    arms, prow = [], []
    for label, kind, q, px in panels:
        tr = [c for c in px.columns if c != "SPY"]
        start = px.index[260]
        spr = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spr) // 2
        bw = rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)
        base = backtest(px, bw, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        ms, ms1, ms2 = metrics(spr), metrics(spr.iloc[:h]), metrics(spr.iloc[h:])
        mb, mb1, mb2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
        br = breadth_of(px, tr)
        prow.append(dict(panel=label, kind=kind, q=q, k=len(tr), breadth=br,
                         SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
                         base_Sharpe=mb["Sharpe"], base_CAGR=mb["CAGR"], base_MaxDD=mb["MaxDD"]))
        specs = [(f"top{n}", n, g, w_topn(n, g)) for n in NS for g in GROSS]
        specs += [("ewall", np.nan, g, w_ewall(g)) for g in GROSS]
        specs += [(f"share_m{M_SHARE:.2f}", np.nan, g, w_share(M_SHARE, g)) for g in GROSS]
        specs += [(f"sel{s:.2f}", np.nan, 0.75, w_sel(s, 0.75)) for s in SEL if s < 1.0]
        for name, n, g, fn in specs:
            r = backtest(px, fn(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
            arms.append(dict(panel=label, kind=kind, q=q, breadth=br, arm=name, n=n, gross=g,
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=m1["Sharpe"], H2=m2["Sharpe"], OOS_CAGR=m2["CAGR"],
                             OOS_MaxDD=m2["MaxDD"],
                             pass4a=(m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                                     and m["MaxDD"] >= mb["MaxDD"]),
                             pass4b=(m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                                     and m["MaxDD"] >= 0.6 * ms["MaxDD"]
                                     and m["CAGR"] >= 0.7 * ms["CAGR"]),
                             base_Sharpe=mb["Sharpe"], base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"],
                             base_OOS_CAGR=mb2["CAGR"], base_OOS_MaxDD=mb2["MaxDD"],
                             SPY_Sharpe=ms["Sharpe"], SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"],
                             SPY_OOS_CAGR=ms2["CAGR"], SPY_OOS_MaxDD=ms2["MaxDD"],
                             SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"]))
    A = pd.DataFrame(arms); P_ = pd.DataFrame(prow)
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    P_.to_csv(OUT / f"{STAMP}.panels.csv", index=False)

    say("\nbreadth beside q — the reading idea 286 asks the record to publish:")
    say(P_[P_.kind == "mix"].groupby("q").breadth.agg(["mean", "min", "max", "size"])
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say(P_[P_.kind == "named"][["panel", "k", "breadth", "SPY_Sharpe", "base_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    rho = P_[P_.kind == "mix"][["q", "breadth"]].corr(method="spearman").iloc[0, 1]
    say(f"Spearman(q, breadth) over the {int((P_.kind=='mix').sum())} mixed panels: {rho:+.4f}"
        "  — the collinearity idea 276 named, reproduced on this run's own draws")

    # ---- the family statistics, per panel ------------------------------
    fam = []
    for label, g in [(l, g) for l in A.panel.unique() for g in GROSS]:
        s = A[(A.panel == label) & (A.gross == g)].set_index("arm")
        if not len(s): continue
        q = float(s.q.iloc[0]); br = float(s.breadth.iloc[0]); kind = s.kind.iloc[0]
        def S(a): return float(s.loc[a, "Sharpe"]) if a in s.index else np.nan
        def C(a): return float(s.loc[a, "CAGR"]) if a in s.index else np.nan
        d_size = S("top30") - S("top10")
        d_share = S(f"share_m{M_SHARE:.2f}") - S("top20")
        # reversal: within this gross, over the 4 arms {top10,top20,top30,ewall}, the share of
        # pairs whose Sharpe ordering disagrees with their CAGR ordering
        names = ["top10", "top20", "top30", "ewall"]
        pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
        rev = [np.sign(S(a) - S(b)) != np.sign(C(a) - C(b)) for a, b in pairs
               if np.isfinite(S(a)) and np.isfinite(S(b))]
        fam.append(dict(panel=label, kind=kind, q=q, breadth=br, gross=g,
                        D_size=d_size, D_share=d_share,
                        reversal=float(np.mean(rev)) if rev else np.nan,
                        n_pairs=len(rev)))
    # selectivity argmax is computed at gross 0.75 only (idea 155's own rung)
    for label in A.panel.unique():
        s = A[(A.panel == label) & (A.gross == 0.75)].set_index("arm")
        prem = {}
        for sel in SEL:
            a = "ewall" if sel >= 1.0 else f"sel{sel:.2f}"
            if a in s.index and "ewall" in s.index:
                prem[sel] = float(s.loc[a, "Sharpe"]) - float(s.loc["ewall", "Sharpe"])
        if prem:
            best = max(prem, key=prem.get)
            for f_ in fam:
                if f_["panel"] == label and f_["gross"] == 0.75:
                    f_["sel_argmax"] = best
                    f_["sel_premium"] = prem[best]
    F = pd.DataFrame(fam)
    F.to_csv(OUT / f"{STAMP}.families.csv", index=False)

    say("\n### family statistics on the ladder (mixed panels, mean over the 8 draws per rung)")
    mixF = F[F.kind == "mix"]
    say(mixF.groupby(["q", "gross"]).agg(breadth=("breadth", "mean"), D_size=("D_size", "mean"),
                                         D_size_pos=("D_size", lambda s: float((s > 0).mean())),
                                         D_share=("D_share", "mean"),
                                         D_share_neg=("D_share", lambda s: float((s < 0).mean())),
                                         reversal=("reversal", "mean")).to_string(
        float_format=lambda x: f"{x:+.4f}"))
    say("\nnamed anchors:")
    say(F[F.kind == "named"][["panel", "q", "breadth", "gross", "D_size", "D_share", "reversal",
                              "sel_argmax", "sel_premium"]].to_string(
        index=False, float_format=lambda x: f"{x:+.4f}"))
    if "sel_argmax" in F.columns:
        say("\nselectivity argmax by rung (gross 0.75):")
        say(mixF[mixF.gross == 0.75].groupby("q").sel_argmax.agg(
            ["mean", "median", "min", "max"]).to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- does breadth carry anything ONCE q is controlled? ---------------
    say("\n### within-q regressions — breadth against each family statistic, cell = q rung")
    say("(N, p, dof reported per idea 512; p = cells absorbed, dof_correct = N-p-1)")
    wrows = []
    for stat in ["D_size", "D_share", "reversal"]:
        d = mixF.dropna(subset=[stat]).copy(); d["cell"] = d.q.astype(str)
        r = within_fit(d, "breadth", stat, "cell")
        pooled = (np.corrcoef(d.breadth, d[stat])[0, 1]
                  if len(d) > 2 and d[stat].std() > 0 and d.breadth.std() > 0 else np.nan)
        wrows.append(dict(stat=stat, pooled_corr_with_breadth=pooled, **r))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.withinq.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- headline survival ----------------------------------------------
    def rung(qv, col, g=None):
        d = mixF[(mixF.q == qv)] if g is None else mixF[(mixF.q == qv) & (mixF.gross == g)]
        return float(d[col].mean())
    verdicts = []
    d_size_q0, d_size_q1 = rung(0.0, "D_size"), rung(1.0, "D_size")
    d_share_all = [rung(q, "D_share") for q in QS]
    rev_q0, rev_q1 = rung(0.0, "reversal"), rung(1.0, "reversal")
    sel_q0 = rung(0.0, "sel_argmax", 0.75) if "sel_argmax" in mixF.columns else np.nan
    sel_q1 = rung(1.0, "sel_argmax", 0.75) if "sel_argmax" in mixF.columns else np.nan
    rev_by_q = [rung(q, "reversal") for q in QS]
    verdicts.append(dict(file="2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.result.md",
        family="SIZE", claim="size effect POSITIVE on large caps and NON-POSITIVE on small caps",
        evidence=f"D_size q=0 {d_size_q0:+.4f}, q=1 {d_size_q1:+.4f}",
        survives=bool(d_size_q0 > 0 and d_size_q1 <= 0)))
    verdicts.append(dict(file="2026-09-05_the-screen-is-a-book-size-rule_cloud.result.md",
        family="SIZE", claim="the size floor fires on BOTH sides of the cap line",
        evidence=f"D_size q=0 {d_size_q0:+.4f}, q=1 {d_size_q1:+.4f}",
        survives=bool(d_size_q0 > 0 and d_size_q1 > 0)))
    verdicts.append(dict(file="2026-09-06_time-varying-share-vs-fixed-n_B.result.md",
        family="SHARE", claim="fixed n beats the time-varying share count at every rung",
        evidence="D_share by q " + ", ".join(f"{v:+.4f}" for v in d_share_all),
        survives=bool(all(v < 0 for v in d_share_all))))
    verdicts.append(dict(file="2026-09-05_does-book-share-price-a-tilt_C.result.md",
        family="SHARE", claim="a share book is a faithful restatement of a fixed-n book (|dSharpe| < 0.10)",
        evidence="|D_share| max " + f"{max(abs(v) for v in d_share_all):.4f}",
        survives=bool(max(abs(v) for v in d_share_all) < 0.10)))
    verdicts.append(dict(file="2026-09-05_where-selectivity-and-cost-cross_B.result.md",
        family="SEL", claim="the Sharpe-premium argmax sits at 0.90-1.00 on large caps and lower on small",
        evidence=f"sel argmax q=0 {sel_q0:.3f}, q=1 {sel_q1:.3f}",
        survives=bool(np.isfinite(sel_q0) and sel_q0 >= 0.85 and sel_q1 < 0.85)))
    verdicts.append(dict(file="2026-09-06_is-the-sharpe-cagr-reversal-a-PANEL-property_C.result.md",
        family="REV", claim="small-cap panels never reverse, large-cap panels usually do",
        evidence=f"reversal q=0 {rev_q0:.3f}, q=1 {rev_q1:.3f}",
        survives=bool(rev_q1 == 0.0 and rev_q0 > 0.5)))
    mono = all(rev_by_q[i] <= rev_by_q[i + 1] for i in range(len(rev_by_q) - 1)) or \
           all(rev_by_q[i] >= rev_by_q[i + 1] for i in range(len(rev_by_q) - 1))
    verdicts.append(dict(file="2026-09-06_is-the-reversal-share-a-function-of-n-over-n_elig_C.result.md",
        family="REV", claim="reversal share is NOT a monotone function of the eligible-share ratio",
        evidence="reversal by q " + ", ".join(f"{v:.3f}" for v in rev_by_q),
        survives=bool(not mono)))
    V = pd.DataFrame(verdicts)
    V.to_csv(OUT / f"{STAMP}.verdicts.csv", index=False)
    say("\n### headline survival on the restatement")
    say(V.to_string(index=False))
    say(f"\nSURVIVE {int(V.survives.sum())} of {len(V)} restatable headlines "
        f"({len(AU)} files audited, {len(AU)-len(rest)} carry no cross-cap panel-property headline)")

    # ---------------- C. protocol ----------------------------------------
    say("\n## C. Rule 8 walk-forward (arm chosen on the first half, second half read once)")
    wf = []
    for label in A.panel.unique():
        s = A[A.panel == label]
        pick = s.iloc[int(s.H1.values.argmax())]
        wf.append(dict(panel=label, kind=pick.kind, q=pick.q, arm=pick.arm, gross=pick.gross,
                       IS_Sharpe=pick.H1, OOS_Sharpe=pick.H2, OOS_CAGR=pick.OOS_CAGR,
                       OOS_MaxDD=pick.OOS_MaxDD, OOS_Sharpe_base=pick.base_H2,
                       OOS_CAGR_base=pick.base_OOS_CAGR, OOS_MaxDD_base=pick.base_OOS_MaxDD,
                       OOS_Sharpe_SPY=pick.SPY_H2, OOS_CAGR_SPY=pick.SPY_OOS_CAGR,
                       OOS_MaxDD_SPY=pick.SPY_OOS_MaxDD,
                       OOS_Sharpe_mean_arm=float(s.H2.mean())))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(WF.groupby("kind").agg(panels=("panel", "size"), OOS_Sharpe=("OOS_Sharpe", "median"),
                               OOS_CAGR=("OOS_CAGR", "median"), OOS_MaxDD=("OOS_MaxDD", "median"),
                               mean_arm=("OOS_Sharpe_mean_arm", "median"),
                               base=("OOS_Sharpe_base", "median"),
                               SPY=("OOS_Sharpe_SPY", "median")).to_string(
        float_format=lambda x: f"{x:.4f}"))
    say(f"the IS-chosen arm beats the panel's own mean arm OOS in "
        f"{int((WF.OOS_Sharpe > WF.OOS_Sharpe_mean_arm).sum())}/{len(WF)} panels; "
        f"beats RULES v2 OOS in {int((WF.OOS_Sharpe > WF.OOS_Sharpe_base).sum())}/{len(WF)}; "
        f"beats SPY OOS in {int((WF.OOS_Sharpe > WF.OOS_Sharpe_SPY).sum())}/{len(WF)}")
    say(WF[WF.kind == "named"].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n## Both KEEP paths, every arm on every panel")
    say(A.groupby("kind")[["pass4a", "pass4b"]].agg(["sum", "size"]).to_string())
    say(f"TOTAL 4a {int(A.pass4a.sum())}/{len(A)}   4b {int(A.pass4b.sum())}/{len(A)}")
    if A.pass4b.any():
        say("4b passers by q rung:")
        say(A[A.pass4b].groupby(["q", "arm"]).size().to_string())
        top = A[A.pass4b].sort_values("Sharpe", ascending=False).head(10)
        say(top[["panel", "arm", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "SPY_CAGR", "SPY_Sharpe", "SPY_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    if A.pass4a.any():
        say("4a passers:")
        say(A[A.pass4a][["panel", "arm", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()
