#!/usr/bin/env python3
"""Idea 276 - "is-breadth-a-small-cap-dummy-everywhere-in-the-record".

The question
------------
Idea 271 regressed a panel-level reversal indicator on four pre-backtest panel
characteristics and found `breadth` (the share of a panel that RULES v1's eligibility
gate admits, averaged over rebalance days) is PERFECTLY BIMODAL over its 53 panels:
every SMALL439-derived panel lands in 0.307-0.329, every large-cap panel in 0.619-0.745,
with no overlap.  A regression on breadth across mixed-capitalisation panels is therefore
a two-cluster split, not a slope, and `breadth < 0.5` is arithmetically identical to
`source == SMALL439` on that corpus.

This run asks the two questions that follow:

  Q1 (MECHANISM) Is breadth intrinsically bimodal, or is the bimodality an artefact of
     the record only ever sampling PURE panels?  Directly constructed: mix small-cap and
     large-cap names in one panel at share q = 0.0 .. 1.0 and measure breadth.  A smooth
     monotone curve means breadth is a continuous readout of capitalisation mix, so on a
     corpus of pure panels it is EXACTLY a cap dummy - collinear by sampling, not by
     nature.  A step function or a gap in the middle would mean breadth carries something
     of its own.

  Q2 (CENSUS) How much of the published record is exposed?  Count every published claim
     that names panels on both sides of the capitalisation line, and report how many of
     those additionally attribute their result to a panel PROPERTY (breadth, dispersion,
     correlation, eligible-set vol) - those are the claims that are, on idea 271's
     finding, reporting the same one indicator.

Design
------
Panels
    5 NAMED, idea 271's own set:
        U56      research/universe.json tradables (ETFs + mega caps), SPY excluded
        B136     research/universe_broad.json (large caps + the same ETFs)
        BSTK100  B136 minus every ETF -> pure large-cap stocks
        ETF36    the ETFs alone
        SMALL439 data/prices_small.csv minus the 44 tickers with max_1d_move >= 1.0
                 in data/small_meta.csv (split artefacts), per the sprint's standing rule
    MIX sweep: k = 40 names, share q of them drawn from SMALL439 and (1-q) from BSTK100,
        q in {0.0, 0.1, ..., 1.0}, 6 independent draws per q (seeded) = 66 panels.
        Stock-vs-stock on both sides, so the axis is capitalisation, not asset class.

Measurement
    gate     RULES v1's eligibility clause, unchanged: px > 200d MA AND vol20 < 0.60
    breadth  mean over weekly rebalance days of n_elig,t / k   (idea 271's definition)
    windows  IS 2010-2016, OOS 2017-2026, and full - all panels share the SMALL439 index
             (2010-01-04 on) so the mix sweep is measured on one common calendar.

Books (so the census sits on real returns, not only on a statistic)
    CAND-n   idea 2's KEEP-candidate construction: RULES v1 gate, composite score, top n
             equal-weighted at 75% gross, weekly, 10 bps, next-day execution.
    Baselines RULES v2 (live) on the same panel, RULES v1 on the same panel, SPY.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q  (11 values)      2. n in {10, 20}
k = 40, 6 draws, the gate, 75% gross, weekly cadence, 10 bps and next-day execution are
all fixed at the record's published conventions and are NOT tuned here.
Grid = 66 mix panels x 2 n = 132 book cells + 5 named panels x 2 n = 10, ALL reported.

Rule 8 walk-forward
    Choose q on 2010-2016 (argmax IS Sharpe of CAND-n, averaged over the 6 draws),
    evaluate that q untouched on 2017-2026 against (a) the do-nothing anchor = mean OOS
    Sharpe over all q, (b) SPY, (c) RULES v2.  Reported per n.  Breadth itself is also
    re-measured OOS to test whether the bimodality is stable out of sample.

SURVIVORSHIP CAVEAT: SMALL439 and B136/BSTK100 are CURRENT constituents of their screens.
Every small-cap number here is biased upward by an unknown amount and no cross-panel
comparison in this file should be read as a tradable edge; the object under test is the
COLLINEARITY of a panel statistic with capitalisation, which survivorship affects only
through the level of the eligible share, not through its ordering.

Outputs: .panels.csv, .books.csv, .walkforward.csv, .census.csv, .console.txt, .result.md
"""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_MIX, N_DRAWS, QS = 40, 6, [round(0.1 * i, 1) for i in range(11)]
NS = [10, 20]

# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c != "SPY" and c not in bad]
    P(f"SMALL439: {len(px.columns)-1} screened names, dropped {len(bad)} with max_1d_move>=1.0 -> {len(keep)}")
    return px, keep

def build_sources():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    px56, pxb = load_universe(), load_universe(broad=True)
    pxs, s_stk = small_panel()
    b_all = [c for c in pxb.columns if c != "SPY"]
    b_stk = [c for c in b_all if c not in etfs]
    b_etf = [c for c in b_all if c in etfs]
    u_all = [c for c in px56.columns if c != "SPY"]
    P(f"B136 {len(b_all)} = BSTK{len(b_stk)} stocks + ETF{len(b_etf)} ETFs;  U56 {len(u_all)}")
    return dict(px56=px56, pxb=pxb, pxs=pxs, s_stk=s_stk, b_stk=b_stk, b_etf=b_etf, u_all=u_all)

def gate(px):
    """RULES v1 eligibility, unchanged."""
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return above & (vol20 < 0.60)

def breadth_of(px, cols, lo=None, hi=None):
    """mean over weekly rebalance days of n_elig/k, on the window [lo, hi]."""
    sub = px[cols]
    e = gate(sub)
    mask = rebalance_mask(sub.index, FREQ)
    w = e.loc[mask.values]
    if lo is not None: w = w.loc[lo:]
    if hi is not None: w = w.loc[:hi]
    w = w.iloc[40:] if lo is None else w                      # skip 200d warm-up on full window
    if len(w) == 0: return np.nan
    return float((w.sum(axis=1) / len(cols)).mean())

# ---------------------------------------------------------------- books
def cand_weights(n):
    def f(px):
        tradables = [c for c in px.columns if c != "SPY"]
        s, above, vol20 = score(px[tradables], vol_scale=False)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f

def run(px, wfn):
    return backtest(px, wfn(px), cost_bps=COST, freq=FREQ)["returns"]

def stats(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(x); return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])

def full_row(tag, r, spy):
    h = len(r) // 2
    d = stats(r)
    return dict(tag=tag, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=stats(r, OOS_START)["CAGR"], OOS_Sharpe=stats(r, OOS_START)["Sharpe"],
                OOS_MaxDD=stats(r, OOS_START)["MaxDD"], IS_Sharpe=stats(r, None, IS_END)["Sharpe"])

def keep_paths(row, spy_row, v2_row):
    """4a: Sharpe > live rules in BOTH halves and MaxDD no worse.  4b: Sharpe > SPY in
    both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    a = (row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"] and row["MaxDD"] >= v2_row["MaxDD"])
    b = (row["H1"] > spy_row["H1"] and row["H2"] > spy_row["H2"] and row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]
         and row["MaxDD"] >= 0.60 * spy_row["MaxDD"] and row["CAGR"] >= 0.70 * spy_row["CAGR"])
    return bool(a), bool(b)

# ---------------------------------------------------------------- census
SMALL_TOK = re.compile(r"SMALL\s?\d{2,3}|small[- ]cap panel|small panel|prices_small|small=True|sub-\$2B|SMALL_PANEL", re.I)
LARGE_TOK = re.compile(r"\bU56\b|\bB136\b|BSTK\s?\d{2,3}|\bETF\s?36\b|universe\.json|universe_broad|broad=True|mega[- ]cap|large[- ]cap", re.I)
PROP_TOK  = re.compile(r"\bbreadth\b|\bdispersion\b|\bdisp\b|pairwise correlation|\bcorr\b|eligible[- ]set vol|\bn_elig\b|\bevol\b", re.I)
CMP_TOK   = re.compile(r"\bvs\.?\b|\bversus\b|compare|cross-universe|cross-panel|both universes|on both panels|does not hold on|holds on|second panel|other panel|pool", re.I)

def census():
    files = sorted(list((ROOT / "research" / "backtests").glob("*.md"))) + \
            [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    rows = []
    for f in files:
        try: t = f.read_text(errors="ignore")
        except Exception: continue
        s, l = bool(SMALL_TOK.search(t)), bool(LARGE_TOK.search(t))
        rows.append(dict(file=f.name, chars=len(t), small=s, large=l, cross=s and l,
                         prop=bool(PROP_TOK.search(t)), cmp=bool(CMP_TOK.search(t)),
                         breadth=bool(re.search(r"\bbreadth\b", t, re.I))))
    return pd.DataFrame(rows)

def census_leaderboard():
    """Row-level census of LEADERBOARD.md: one claim per table row."""
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    rows = [ln for ln in txt.splitlines() if ln.startswith("|") and ln.count("|") >= 6
            and not re.match(r"^\|\s*-+", ln) and "Date" not in ln[:20]]
    out = []
    for ln in rows:
        s, l = bool(SMALL_TOK.search(ln)), bool(LARGE_TOK.search(ln))
        out.append(dict(row=ln[:160], small=s, large=l, cross=s and l,
                        prop=bool(PROP_TOK.search(ln)), cmp=bool(CMP_TOK.search(ln))))
    return pd.DataFrame(out)

# ---------------------------------------------------------------- main
def main():
    src = build_sources()
    pxs, pxb, px56 = src["pxs"], src["pxb"], src["px56"]

    # one common calendar for everything that gets mixed
    idx = pxs.index.intersection(pxb.index)
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]

    # ---- Q1a: named panels, breadth on full / IS / OOS
    named = {"U56": (px56, src["u_all"]), "B136": (pxb, [c for c in pxb.columns if c != "SPY"]),
             "BSTK100": (pxb, src["b_stk"]), "ETF36": (pxb, src["b_etf"]),
             "SMALL439": (pxs, src["s_stk"])}
    prows = []
    for tag, (px, cols) in named.items():
        prows.append(dict(panel=tag, kind="named", q=np.nan, draw=np.nan, k=len(cols),
                          breadth=breadth_of(px, cols),
                          breadth_IS=breadth_of(px, cols, "2010-01-01", IS_END),
                          breadth_OOS=breadth_of(px, cols, OOS_START, None)))
    P("\n=== NAMED PANELS: breadth (idea 271's definition) ===")
    P(pd.DataFrame(prows).set_index("panel")[["k", "breadth", "breadth_IS", "breadth_OOS"]]
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- Q1b: the MIX sweep - does breadth interpolate?
    rng = np.random.default_rng(2026)
    mix_cols = {}
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
            mix_cols[(q, d)] = (sc, lc)
            px = pd.concat([pxs_c[sc], pxb_c[lc]], axis=1) if sc and lc else (pxs_c[sc] if sc else pxb_c[lc])
            cols = sc + lc
            prows.append(dict(panel=f"MIX q={q:.1f} d{d}", kind="mix", q=q, draw=d, k=K_MIX,
                              breadth=breadth_of(px, cols, "2010-08-01", None),
                              breadth_IS=breadth_of(px, cols, "2010-08-01", IS_END),
                              breadth_OOS=breadth_of(px, cols, OOS_START, None)))
    panels = pd.DataFrame(prows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)

    mix = panels[panels.kind == "mix"]
    agg = mix.groupby("q")[["breadth", "breadth_IS", "breadth_OOS"]].agg(["mean", "min", "max"])
    P("\n=== Q1: MIX SWEEP - breadth vs small-cap share q (k=40, 6 draws each, ALL 66 reported) ===")
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    rho = mix[["q", "breadth"]].corr(method="spearman").iloc[0, 1]
    pear = mix[["q", "breadth"]].corr().iloc[0, 1]
    P(f"\nSpearman(q, breadth) = {rho:+.4f}   Pearson = {pear:+.4f}   R2(linear in q) = {pear**2:.4f}")
    # is the middle empty (bimodal) or populated (continuous)?
    lo_c, hi_c = 0.329, 0.619                                  # idea 271's published gap
    ingap = mix[(mix.breadth > lo_c) & (mix.breadth < hi_c)]
    P(f"mix panels landing INSIDE idea 271's empty gap ({lo_c}, {hi_c}): {len(ingap)} of {len(mix)}"
      f"   -> {'gap is FILLED: breadth is continuous in cap mix' if len(ingap) else 'gap survives'}")
    P(f"breadth range over the sweep: {mix.breadth.min():.4f} .. {mix.breadth.max():.4f}")
    # monotone?
    mm = mix.groupby("q").breadth.mean()
    P(f"monotone decreasing in q: {bool((mm.diff().dropna() < 0).all())}"
      f"   (per-step deltas {', '.join(f'{d:+.3f}' for d in mm.diff().dropna())})")
    # where does the 0.5 threshold cut?
    cross = [q for q in QS if mm[q] < 0.5]
    P(f"idea 271's `breadth<0.5` line is crossed at q >= {min(cross):.1f}" if cross else "0.5 never crossed")
    # OOS stability of the separation
    P(f"IS/OOS breadth rank agreement over the 66 mix panels: Spearman "
      f"{mix[['breadth_IS','breadth_OOS']].corr(method='spearman').iloc[0,1]:+.4f}")

    # ---- books on every mix panel (+ named), both KEEP paths
    P("\n=== BOOKS: CAND-n on every panel (132 mix cells + 10 named), ALL reported ===")
    brows = []
    for (q, d), (sc, lc) in mix_cols.items():
        cols = sc + lc
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[[c for c in cols] + ["SPY"]]
        spy_r = full_row("SPY", spy.pct_change().fillna(0).loc[px.index[260]:], None)
        v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                                 .reindex(columns=p.columns).fillna(0.0)).loc[px.index[260]:], None)
        for n in NS:
            r = run(px, cand_weights(n)).loc[px.index[260]:]
            row = full_row(f"CAND{n}", r, spy)
            a, b = keep_paths(row, spy_r, v2_r)
            brows.append(dict(panel=f"MIX q={q:.1f} d{d}", kind="mix", q=q, draw=d, n=n,
                              **{k: v for k, v in row.items() if k != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_OOS_S=spy_r["OOS_Sharpe"], v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"],
                              v2_H2=v2_r["H2"], v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              pass4a=a, pass4b=b))
    for tag, (pxn, cols) in named.items():
        px = pxn[[c for c in cols] + (["SPY"] if "SPY" in pxn.columns else [])].copy()
        if "SPY" not in px.columns:
            px["SPY"] = pxb["SPY"].reindex(px.index).ffill()
        px = px.dropna(how="all").ffill()
        st = px.index[260]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:], None)
        v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                                 .reindex(columns=p.columns).fillna(0.0)).loc[st:], None)
        for n in NS:
            r = run(px, cand_weights(n)).loc[st:]
            row = full_row(f"CAND{n}", r, None)
            a, b = keep_paths(row, spy_r, v2_r)
            brows.append(dict(panel=tag, kind="named", q=np.nan, draw=np.nan, n=n,
                              **{k: v for k, v in row.items() if k != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_OOS_S=spy_r["OOS_Sharpe"], v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"],
                              v2_H2=v2_r["H2"], v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              pass4a=a, pass4b=b))
    books = pd.DataFrame(brows)
    books.to_csv(f"{OUT}.books.csv", index=False)

    for n in NS:
        sub = books[(books.kind == "mix") & (books.n == n)]
        g = sub.groupby("q")[["CAGR", "Sharpe", "MaxDD", "IS_Sharpe", "OOS_Sharpe", "spy_S", "v2_S"]].mean()
        P(f"\n-- CAND{n} on the mix sweep (mean of 6 draws per q) --")
        P(g.to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"   4a passes {int(sub.pass4a.sum())}/{len(sub)}   4b passes {int(sub.pass4b.sum())}/{len(sub)}")
    nm = books[books.kind == "named"]
    P("\n-- named panels --")
    P(nm.set_index(["panel", "n"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                                    "spy_S", "v2_S", "pass4a", "pass4b"]]
      .to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- correlation of the BOOK outcome with breadth vs with q (is breadth adding anything?)
    m = books[books.kind == "mix"].merge(panels[panels.kind == "mix"][["panel", "breadth"]], on="panel")
    P("\n=== does breadth carry anything beyond q? (mix cells only) ===")
    for n in NS:
        s = m[m.n == n]
        r_q = s[["q", "OOS_Sharpe"]].corr(method="spearman").iloc[0, 1]
        r_b = s[["breadth", "OOS_Sharpe"]].corr(method="spearman").iloc[0, 1]
        r_qb = s[["q", "breadth"]].corr(method="spearman").iloc[0, 1]
        P(f"  n={n}: Spearman(q,OOS_S) {r_q:+.4f}   Spearman(breadth,OOS_S) {r_b:+.4f}"
          f"   Spearman(q,breadth) {r_qb:+.4f}")

    # ---- rule 8 walk-forward: choose q on 2010-2016, evaluate 2017-2026
    P("\n=== RULE 8 WALK-FORWARD (choose q on 2010-2016, evaluate 2017-2026) ===")
    wrows = []
    for n in NS:
        s = m[m.n == n]
        gi = s.groupby("q").IS_Sharpe.mean(); go = s.groupby("q").OOS_Sharpe.mean()
        qhat = gi.idxmax()
        anchor = go.mean()                                    # do-nothing = average over all q
        best_oos = go.max()
        wrows.append(dict(n=n, q_hat=qhat, IS_Sharpe=gi[qhat], OOS_Sharpe=go[qhat],
                          OOS_anchor_meanq=anchor, OOS_best_q=go.idxmax(), OOS_best=best_oos,
                          regret=go[qhat] - best_oos, edge_vs_anchor=go[qhat] - anchor,
                          spy_OOS=s.spy_OOS_S.mean(), v2_OOS=s.v2_OOS_S.mean()))
        P(f"  n={n}: IS argmax q={qhat:.1f} (IS Sharpe {gi[qhat]:.3f}) -> OOS {go[qhat]:.3f}"
          f" | do-nothing anchor {anchor:.3f} (edge {go[qhat]-anchor:+.3f})"
          f" | best possible OOS q={go.idxmax():.1f} {best_oos:.3f} (regret {go[qhat]-best_oos:+.3f})"
          f" | SPY OOS {s.spy_OOS_S.mean():.3f}  v2 OOS {s.v2_OOS_S.mean():.3f}")
    pd.DataFrame(wrows).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- Q2: the census
    P("\n=== Q2: CENSUS OF THE PUBLISHED RECORD ===")
    cf = census(); cf.to_csv(f"{OUT}.census.csv", index=False)
    tot = len(cf); cross = int(cf.cross.sum())
    P(f"corpus: {tot} markdown files (backtest results/memos + LEADERBOARD + CHANGELOG)")
    P(f"  name a SMALL-cap panel:                 {int(cf.small.sum())}")
    P(f"  name a LARGE-cap panel/universe:        {int(cf.large.sum())}")
    P(f"  CROSS-CAP (both sides named):           {cross}  ({cross/tot:.1%} of the corpus)")
    x = cf[cf.cross]
    P(f"  of those, also use comparison language: {int(x.cmp.sum())}")
    P(f"  of those, attribute to a panel PROPERTY:{int(x.prop.sum())}"
      f"  <- exposed to idea 271's collinearity")
    P(f"  of those, name `breadth` explicitly:    {int(x.breadth.sum())}")
    lb = census_leaderboard()
    P(f"\nLEADERBOARD rows: {len(lb)};  cross-cap rows {int(lb.cross.sum())}"
      f" ({lb.cross.mean():.1%});  of those with a panel-property word {int(lb[lb.cross].prop.sum())}")
    P("\nmost recent cross-cap + property files (up to 15):")
    for f in list(x[x.prop].file)[-15:]: P("   ", f)
    P("\nCAVEAT: this is a KEYWORD census, not a semantic one. It counts files that name "
      "panels on both sides of the capitalisation line AND use a panel-property word; it "
      "does not verify that each such file's headline claim is the collinear one. Read the "
      "counts as an upper bound on exposure and the `breadth` column as the tight lower bound.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
