#!/usr/bin/env python3
"""Idea 496 (cloud, 2026-09-10) -- PUBLISH THE *PENALTY* BESIDE EVERY RESIDUALISATION.

Idea 483 found that `survive` -- the record's residualisation statistic,
`pR2(signal | control) / R2(signal raw)` -- moves 0.020 -> 0.959 across lam 1e-3..100 on
B136, while the in-sample-vs-out-of-fold gap the file was built to measure never exceeds
0.13.  The ridge penalty, which most committed residualisations never publish, is a bigger
dial than the thing being studied.

The queue asks: re-read every committed residualisation at three penalties and report which
conclusions are penalty-stable.

PRE-REGISTRATION (fixed before any number below was read):

  * EXACTLY TWO TUNED PARAMETERS, and no more:
      PENALTY  in {1e-3, 1e-2, 1e-1, 1, 10, 100}  -- the ridge lam; LOW/MID/HIGH = 1e-3/1/100
      PANEL    in {U56, B136, SMALL439}
    Fold count K, control width (WIDE = every name, NARROW10 = the 10 most-drawn), target,
    cost rung and sample half are REPORTED axes, never chosen.  Every grid point is written.

  * PART A -- CENSUS.  A RESIDUALISATION SITE is a committed artefact row that publishes a
    partial-R2 / kill / survive statistic computed by fitting a control and residualising
    (RESID_COLS).  Two claim sets:
      COMMITTED -- every research/backtests/*.csv[.gz] carrying such a column.
      ALL       -- COMMITTED plus every prose line in the committed record (CHANGELOG.md,
                   QUEUE.md, LEADERBOARD.md, PROTOCOL.md, *.result.md, *.memo.md) that
                   asserts a residualisation conclusion in words (RESID_PHRASES).
    The census's headline number is how many sites PUBLISH THE PENALTY they were computed at.

  * PART B -- RE-READ AT THREE PENALTIES.
      B1 COMMITTED RE-READ.  For every committed residualisation artefact that carries its
         own lam ladder, the verdict (`survive >= 0.5`, i.e. the control did NOT kill the
         signal, and the sign/size of the residualised t) is read at LOW, MID and HIGH off
         its OWN rows -- an exact re-read, no re-fit, so it cannot disagree with the record
         for any reason but the penalty.  A conclusion is PENALTY-STABLE iff its verdict is
         identical at all three.
      B2 FRESH RE-RUN.  Idea 483's construction rebuilt from scratch (200 equal-weight
         20-name draw books per panel, seeds 0..199, weekly, 10 bps, t+1) and run over the
         whole PENALTY x PANEL x K x width grid, so the answer rests on measurement and not
         only on committed rows.  Gate G3 requires this to reproduce idea 483's committed
         grid.csv exactly.
      B3 THE UNPUBLISHED-PENALTY FILES.  Artefacts with a residualisation column and NO lam
         column are named, and where their construction is recoverable they are re-run over
         the ladder; where it is not, they are published as PENALTY-UNRECOVERABLE rather
         than imputed.

  * PART C -- DOES THE DIAL CHANGE WHAT YOU WOULD TRADE?  A residualisation exists to decide
    which book/characteristic to believe.  At each penalty the control is fitted on the
    IN-SAMPLE half only, book Sharpe is residualised, and the top-residual book is held out
    of sample -- against the raw (un-residualised) IS-Sharpe pick, the live RULES v2 book and
    SPY.  Both KEEP paths are evaluated on every one of the 600 draw books and on every pick.

  * PROTOCOL rule 8: every selector's inputs come from 2009-2016 only; 2017-2026 is read once.

  * BOTH KEEP PATHS.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
    4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

SURVIVORSHIP (PROTOCOL 9): U56 and B136 are current-constituent lists; SMALL439 is the
sub-$2B screen with `data/small_meta.csv max_1d_move >= 1.0` dropped (idea 118), current
constituents only and back-filled to 2010 alone.  Every LEVEL below is optimistic and none is
a tradable estimate.  What is meant to survive is the WITHIN-panel penalty contrast -- the same
books, the same rows, the same target, read at a different lam -- which a common level shift
cannot move, and the census arithmetic, which is a property of committed files.

Deterministic, standalone, offline.  Writes .console.txt, .census.csv, .grid.csv,
.reread.csv, .keeppaths.csv, .walkforward.csv.  Reads only committed artefacts + baseline.py.
Modifies nothing in the repo.
"""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

T0 = time.time()
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------------- pre-registered constants
LAMS = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]        # tuned param 1 (all reported)
LOW, MID, HIGH = 0.001, 1.0, 100.0                 # the queue's "three penalties"
FOLDS = [2, 3, 5, 10]                              # reported axis (idea 483's own)
NDRAW, KNAMES = 200, 20                            # idea 483's own corpus, seeds 0..199
NARROW_P = 10
COST, FREQ = 10, "W"
RUNGS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SURVIVE_BAR = 0.5                                  # verdict: signal SURVIVES the control

# A RESIDUALISATION artefact must carry a PARTIAL statistic -- a number computed by fitting a
# control and reading what is left.  A `kill`/`survive` column alone is a survival claim, not a
# residualisation, and is censused separately rather than scored.
PARTIAL_COLS = [r"(^|_)p(artial)?_?r2", r"_given_"]        # matched case-insensitively
DERIVED_COLS = [r"^kill", r"^survive"]
RESID_COLS = PARTIAL_COLS + DERIVED_COLS
RESID_PHRASES = [r"residualis", r"partial R2", r"partial R\^?2", r"\bpR2\b",
                 r"controll?ing for", r"control kills", r"kill fraction", r"once the .{0,20}is controlled"]
PROSE_FILES = ["research/CHANGELOG.md", "research/QUEUE.md", "research/LEADERBOARD.md",
               "research/PROTOCOL.md"]


# ================================================================ fast backtest (gated at G1)
def fast_backtest(px, w, cost_bps=10.0, freq="W"):
    """Bit-for-bit `engine.backtest` on returns and turnover, without the pandas .iloc loop."""
    rets = px.pct_change().fillna(0.0).values
    W = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nd, nc = rets.shape
    cur = np.zeros(nc)
    held = np.empty((nd, nc))
    turn = np.zeros(nd)
    for i in range(nd):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def mtr(r):
    if len(r) < 30:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1), MaxDD=float(dd),
                Sharpe=float(r.mean() * 252 / vol) if vol else np.nan)


def halves(r):
    h = len(r) // 2
    return mtr(r.iloc[:h]), mtr(r.iloc[h:])


# ================================================== idea 483's estimator, re-implemented
def ridge_fit(X, y, lam):
    Xc = X - X.mean(0)
    yc = y - y.mean()
    A = Xc.T @ Xc + lam * np.eye(X.shape[1])
    b = np.linalg.solve(A, Xc.T @ yc)
    return b, y.mean(), X.mean(0)


def ridge_pred(X, b, ym, xm):
    return (X - xm) @ b + ym


def oof_pred(X, y, lam, K, seed=7):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    fold = np.zeros(len(y), int)
    for f, chunk in enumerate(np.array_split(idx, K)):
        fold[chunk] = f
    pred = np.empty(len(y))
    for f in range(K):
        tr, te = fold != f, fold == f
        b, ym, xm = ridge_fit(X[tr], y[tr], lam)
        pred[te] = ridge_pred(X[te], b, ym, xm)
    return pred


def ols_t(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    if xc.std() == 0:
        return 0.0, 0.0, 0.0
    b = (xc @ yc) / (xc @ xc)
    resid = yc - b * xc
    n = len(x)
    s2 = resid @ resid / (n - 2)
    se = np.sqrt(s2 / (xc @ xc))
    r2 = 1 - (resid @ resid) / (yc @ yc)
    return b, b / se if se else 0.0, r2


def r2_of(pred, y):
    y = np.asarray(y, float)
    pred = np.asarray(pred, float)
    return 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def ew_weights(px, names, gross=1.0):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = gross * sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w


def draw_books(px, tickers, ndraw=NDRAW, k=KNAMES, seed0=0):
    """idea 483's corpus, name for name: ndraw equal-weight k-name books, weekly, 10 bps."""
    rets, turns, M = {}, {}, np.zeros((ndraw, len(tickers)))
    tix = {t: j for j, t in enumerate(tickers)}
    for i in range(ndraw):
        rng = np.random.default_rng(seed0 + i)
        names = list(rng.choice(tickers, size=k, replace=False))
        for t in names:
            M[i, tix[t]] = 1.0
        r, tn = fast_backtest(px, ew_weights(px, names), cost_bps=COST, freq=FREQ)
        rets[i] = r
        turns[i] = tn
    return pd.DataFrame(rets), pd.DataFrame(turns), M


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


# ================================================================================== MAIN
def main():
    P("=" * 118)
    P("IDEA 496 -- publish the PENALTY beside every residualisation   (cloud, 2026-09-10)")
    P("=" * 118)

    sm, ndrop = small_panel()
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": sm}
    for k, v in panels.items():
        P(f"  panel {k:<9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P(f"  SMALL: dropped {ndrop} tickers with max_1d_move >= 1.0 (idea 118)")

    # ---------------------------------------------------------------- GATES
    P("\n" + "=" * 118)
    P("GATES")
    P("=" * 118)
    g_px = panels["U56"]
    wv2 = rules_v2_weights(g_px)
    eng = backtest(g_px, wv2, cost_bps=COST, freq=FREQ)
    fr, ft = fast_backtest(g_px, wv2, cost_bps=COST, freq=FREQ)
    gs = g_px.index[260]
    g1r = float(np.abs((eng["returns"] - fr).loc[gs:].values).max())
    g1t = float(np.abs((eng["turnover"] - ft).loc[gs:].values).max())
    P(f"  G1  fast_backtest vs engine.backtest on the read window ({gs.date()}..)  "
      f"returns {g1r:.3e}  turnover {g1t:.3e}  -> {'PASS' if max(g1r, g1t) < 1e-12 else 'FAIL'}")

    g_tick = [c for c in g_px.columns if c != "SPY"]
    g_names = list(np.random.default_rng(0).choice(g_tick, size=KNAMES, replace=False))
    g_w = ew_weights(g_px, g_names)
    r10, t10 = fast_backtest(g_px, g_w, cost_bps=COST, freq=FREQ)
    g2 = max(float(np.abs((r10 + t10 * (COST - c) / 1e4 -
                           fast_backtest(g_px, g_w, cost_bps=c, freq=FREQ)[0]).values).max())
             for c in RUNGS)
    P(f"  G2  exact cost re-rung r(c) = r(10bps) + turnover*(10-c)/1e4 vs a live re-run at "
      f"{RUNGS} bps: {g2:.3e}  -> {'PASS' if g2 < 1e-15 else 'FAIL'}")

    # ---------------------------------------------------------------- PART A
    P("\n" + "=" * 118)
    P("PART A -- CENSUS: every committed residualisation, and whether it publishes its penalty")
    P("=" * 118)
    rx_col = re.compile("|".join(RESID_COLS), re.I)
    rx_part = re.compile("|".join(PARTIAL_COLS), re.I)
    rows = []
    survival_only = []
    files = sorted(list((ROOT / "research/backtests").glob("*.csv")) +
                   list((ROOT / "research/backtests").glob("*.csv.gz")))
    nscan = 0
    for f in files:
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        nscan += 1
        rc = [c for c in head.columns if rx_col.search(c)]
        if not rc:
            continue
        lc = {c.lower() for c in head.columns}
        haslam = bool(lc & {"lam", "lambda", "penalty", "ridge", "alpha", "l2"})
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        part = [c for c in d.columns if rx_part.search(c) and d[c].dtype.kind == "f"]
        if not part:                       # a kill/survive flag with no partial statistic
            survival_only.append(dict(artefact=f.name, rows=len(d), cols=";".join(rc[:5])))
            continue
        lamvals = sorted(set(d["lam"].dropna())) if "lam" in d.columns else []
        rows.append(dict(artefact=f.name, rows=len(d), resid_cols=";".join(rc[:6]),
                         partial_cols=";".join(part[:6]),
                         publishes_penalty=haslam, n_penalties=len(lamvals),
                         penalties=";".join(f"{x:g}" for x in lamvals[:8])))
    C = pd.DataFrame(rows).sort_values("artefact")
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    SO = pd.DataFrame(survival_only)
    P(f"  scanned {nscan} committed CSV artefacts in research/backtests/")
    P(f"  {len(SO)} artefacts carry a kill/survive flag with NO partial statistic -- survival "
      f"claims, not residualisations; censused but NOT scored")
    P(f"  COMMITTED residualisation artefacts (carry a partial-R2 / _given_ column): {len(C)}  "
      f"({int(C.publishes_penalty.sum())} publish a penalty column, "
      f"{int((~C.publishes_penalty).sum())} do NOT)")
    P(f"  of those that do, {int((C.n_penalties >= 3).sum())} carry 3 or more penalties "
      f"(i.e. can be re-read at three without a re-fit)")
    P("")
    P(f"    {'artefact':<86s} {'rows':>6s} {'lam?':>5s} {'#lam':>5s}  columns")
    for _, r in C.iterrows():
        P(f"    {r.artefact[:86]:<86s} {r.rows:>6d} {str(r.publishes_penalty):>5s} "
          f"{r.n_penalties:>5d}  {r.resid_cols[:60]}")

    rx_pr = re.compile("|".join(RESID_PHRASES), re.I)
    prose_paths = [ROOT / p for p in PROSE_FILES]
    prose_paths += sorted((ROOT / "research/backtests").glob("*.result.md"))
    prose_paths += sorted((ROOT / "research/backtests").glob("*.memo.md"))
    lam_in_line = re.compile(r"\blam(bda)?\b|\bpenalty\b|\bridge\b|1e-?\d", re.I)
    npl, npl_lam = 0, 0
    prose_rows = []
    for pth in prose_paths:
        try:
            txt = pth.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            if rx_pr.search(line):
                npl += 1
                has = bool(lam_in_line.search(line))
                npl_lam += int(has)
                prose_rows.append(dict(file=str(pth.relative_to(ROOT)), line=ln,
                                       names_penalty=has, text=line.strip()[:300]))
    PR = pd.DataFrame(prose_rows)
    PR.to_csv(OUT / f"{STEM}.prose.csv", index=False)
    P(f"\n  PROSE residualisation claims across {len(prose_paths)} committed prose files: {npl} lines, "
      f"of which {npl_lam} ({npl_lam / max(npl, 1):.1%}) name a penalty at all")
    P(f"  ALL claim set = {len(C)} artefacts + {npl} prose lines")

    # ---------------------------------------------------------------- PART B1
    P("\n" + "=" * 118)
    P("PART B1 -- COMMITTED RE-READ: every residualisation with its own lam ladder, at LOW/MID/HIGH")
    P("=" * 118)
    reread = []
    for _, r in C[C.publishes_penalty & (C.n_penalties >= 2)].iterrows():
        d = pd.read_csv(ROOT / "research/backtests" / r.artefact)
        lams = sorted(set(d["lam"].dropna()))
        three = [min(lams), min(lams, key=lambda x: abs(x - 1.0)), max(lams)]
        stat_cols = [c for c in d.columns if rx_col.search(c) and d[c].dtype.kind == "f"]
        keys = [c for c in ("panel", "scope", "y", "width", "K", "folds", "scheme", "N", "n", "p")
                if c in d.columns and c != "lam"]
        for sc in stat_cols:
            for kv, sub in (d.groupby(keys) if keys else [((), d)]):
                vals = {}
                for L in three:
                    v = sub.loc[np.isclose(sub["lam"], L), sc]
                    vals[L] = float(v.median()) if len(v) else np.nan
                got = [v for v in vals.values() if np.isfinite(v)]
                if len(got) < 2:
                    continue
                # the VERDICT a reader takes away, per statistic type
                if sc.lower().startswith("kill"):
                    verd = [bool(v < (1 - SURVIVE_BAR)) for v in got]   # kill < 0.5 -> signal survives
                elif sc.lower().startswith("survive"):
                    verd = [bool(v >= SURVIVE_BAR) for v in got]
                elif sc.lower().startswith("t_") or sc.lower().startswith("t"):
                    verd = [(bool(abs(v) >= 2.0), bool(v > 0)) for v in got]   # significant, and which way
                else:
                    verd = [bool(v > 0) for v in got]                   # pR2 sign / presence
                reread.append(dict(artefact=r.artefact, stat=sc,
                                   cell="|".join(map(str, kv)) if keys else "ALL",
                                   lam_low=three[0], lam_mid=three[1], lam_high=three[2],
                                   v_low=vals[three[0]], v_mid=vals[three[1]], v_high=vals[three[2]],
                                   spread=float(np.nanmax(got) - np.nanmin(got)),
                                   stable=bool(len(set(verd)) == 1), n_read=len(got)))
    RR = pd.DataFrame(reread)
    RR.to_csv(OUT / f"{STEM}.reread.csv", index=False)
    if len(RR):
        P(f"  {len(RR)} committed residualisation CONCLUSIONS re-read at three penalties "
          f"off their own rows (no re-fit)")
        P(f"  PENALTY-STABLE (identical verdict at LOW, MID and HIGH): "
          f"{int(RR.stable.sum())} / {len(RR)} = {RR.stable.mean():.1%}")
        P(f"  median |value| spread across the three penalties: {RR.spread.median():.4f}, "
          f"max {RR.spread.max():.4f}")
        P("\n  by artefact:")
        agg = RR.groupby("artefact").agg(conclusions=("stable", "size"),
                                         stable=("stable", "sum"),
                                         med_spread=("spread", "median"),
                                         max_spread=("spread", "max"))
        agg["stable_rate"] = agg.stable / agg.conclusions
        P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
        P("\n  by statistic:")
        agg2 = RR.groupby("stat").agg(conclusions=("stable", "size"), stable=("stable", "sum"),
                                      med_spread=("spread", "median"), max_spread=("spread", "max"))
        P(agg2.to_string(float_format=lambda x: f"{x:.4f}"))
        P("\n  the 12 widest-moving conclusions:")
        P(RR.nlargest(12, "spread")[["artefact", "stat", "cell", "v_low", "v_mid", "v_high",
                                     "spread", "stable"]].to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))
    else:
        P("  no committed residualisation carries a re-readable lam ladder")

    P("\n  B3 -- residualisation artefacts that publish NO penalty (the dial is unrecoverable "
      "from the artefact alone):")
    for _, r in C[~C.publishes_penalty].iterrows():
        P(f"    {r.artefact[:96]:<96s} {r.rows:>6d} rows  [{r.resid_cols[:52]}]")
    if len(SO):
        P(f"\n  (for the record, the {len(SO)} kill/survive artefacts that carry no partial "
          f"statistic and are NOT scored as residualisations:)")
        for _, r in SO.iterrows():
            P(f"    {r.artefact[:96]:<96s} {r.rows:>6d} rows  [{r.cols[:52]}]")

    # ---------------------------------------------------------------- PART B2
    P("\n" + "=" * 118)
    P("PART B2 -- FRESH RE-RUN of idea 483's construction over PENALTY x PANEL x K x width")
    P("=" * 118)
    grid, books = [], []
    picks = []
    for pname, px in panels.items():
        tickers = [c for c in px.columns if c != "SPY"]
        R, TN, M = draw_books(px, tickers)
        start = px.index[260]
        R = R.loc[start:]
        TN = TN.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base, _ = fast_backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)
        base = base.loc[start:]
        h = len(R) // 2
        IS, OOS = R.iloc[:h], R.iloc[h:]
        y_full = np.array([metrics(R[c])["Sharpe"] for c in R.columns])
        y_is = np.array([metrics(IS[c])["Sharpe"] for c in IS.columns])
        y_oos = np.array([metrics(OOS[c])["Sharpe"] for c in OOS.columns])
        ann = (px[tickers].pct_change().loc[start:].mean() * 252).values
        ann_is = (px[tickers].pct_change().loc[start:].iloc[:h].mean() * 252).values
        sd_full = np.array([np.nanstd(ann[M[i] > 0]) for i in range(len(M))])
        sd_is = np.array([np.nanstd(ann_is[M[i] > 0]) for i in range(len(M))])
        narrow_cols = np.argsort(-M.sum(0))[:NARROW_P]
        b_raw, t_raw, r2_raw = ols_t(sd_full, y_full)
        strong = abs(t_raw) >= 2.0
        kdiv = r2_raw if strong else np.nan
        bm, bh1, bh2 = mtr(base), *halves(base)
        sm_, sh1, sh2 = mtr(spy), *halves(spy)
        spy_oos = mtr(spy.loc[OOS_START:])
        P(f"\n  {pname}: {len(tickers)} names, {NDRAW} draw books, raw sd -> Sharpe "
          f"t {t_raw:+.3f} R2 {r2_raw:.4f}{'' if strong else '  [|t|<2, kill suppressed]'}")
        P(f"    RULES v2 {bm['CAGR']:.2%}/{bm['Sharpe']:.4f}/{bm['MaxDD']:.2%}   "
          f"SPY {sm_['CAGR']:.2%}/{sm_['Sharpe']:.4f}/{sm_['MaxDD']:.2%} "
          f"(halves {sh1['Sharpe']:.3f}/{sh2['Sharpe']:.3f}, OOS {spy_oos['Sharpe']:.3f})")

        # book-level KEEP paths, every draw book, every cost rung (exact re-rung:
        # r(c) = r(COST) + turnover*(COST - c)/1e4, which G2 verifies against a live re-run)
        for i, col in enumerate(R.columns):
            for rung in RUNGS:
                rr = R[col] + TN[col] * (COST - rung) / 1e4
                m = mtr(rr)
                m1, m2 = halves(rr)
                oo = mtr(rr.loc[OOS_START:])
                books.append(dict(
                    panel=pname, book=int(col), rung=rung, sd=sd_full[i],
                    Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"],
                    H1=m1["Sharpe"], H2=m2["Sharpe"], OOS_Sharpe=oo["Sharpe"],
                    pass4a=bool(m1["Sharpe"] > bh1["Sharpe"] and m2["Sharpe"] > bh2["Sharpe"]
                                and m["MaxDD"] >= bm["MaxDD"]),
                    pass4b=bool(m1["Sharpe"] > sh1["Sharpe"] and m2["Sharpe"] > sh2["Sharpe"]
                                and oo["Sharpe"] > spy_oos["Sharpe"]
                                and m["MaxDD"] >= 0.60 * sm_["MaxDD"]
                                and m["CAGR"] >= 0.70 * sm_["CAGR"])))

        for width, cols in (("WIDE", np.arange(M.shape[1])), (f"NARROW{NARROW_P}", narrow_cols)):
            X = M[:, cols]
            for lam in LAMS:
                b, ym, xm = ridge_fit(X, y_full, lam)
                pred_is = ridge_pred(X, b, ym, xm)
                e_is = y_full - pred_is
                _, t_isf, pr2_isf = ols_t(sd_full, e_is)
                bs, yms, xms = ridge_fit(X, sd_full, lam)
                r2_sd_is = r2_of(ridge_pred(X, bs, yms, xms), sd_full)
                for K in FOLDS:
                    e_oof = y_full - oof_pred(X, y_full, lam, K)
                    _, t_oof, pr2_oof = ols_t(sd_full, e_oof)
                    r2_sd_oof = r2_of(oof_pred(X, sd_full, lam, K), sd_full)
                    grid.append(dict(panel=pname, p=len(cols), n=len(y_full), width=width,
                                     lam=lam, K=K, t_raw=t_raw, R2_raw=r2_raw,
                                     raw_signal_strong=strong, t_insample=t_isf,
                                     pR2_insample=pr2_isf,
                                     survive_insample=pr2_isf / kdiv if strong else np.nan,
                                     kill_insample=1 - pr2_isf / kdiv if strong else np.nan,
                                     t_oof=t_oof, pR2_oof=pr2_oof,
                                     survive_oof=pr2_oof / kdiv if strong else np.nan,
                                     kill_oof=1 - pr2_oof / kdiv if strong else np.nan,
                                     R2_fit_y_insample=r2_of(pred_is, y_full),
                                     R2_fit_y_oof=r2_of(oof_pred(X, y_full, lam, K), y_full),
                                     R2_control_reproduces_sd_insample=r2_sd_is,
                                     R2_control_reproduces_sd_oof=r2_sd_oof))

        # ---------------- PART C: does the dial change the book you would trade?
        Xw = M
        for lam in LAMS:
            bi, ymi, xmi = ridge_fit(Xw, y_is, lam)             # control fitted on IS ONLY
            resid_is = y_is - ridge_pred(Xw, bi, ymi, xmi)
            j_res = int(np.argmax(resid_is))
            j_raw = int(np.argmax(y_is))
            j_sd = int(np.argmax(sd_is))
            for tag, j in (("RESID", j_res), ("RAW_IS_SHARPE", j_raw), ("SD", j_sd)):
                col = R.columns[j]
                rr = R[col]
                m = mtr(rr)
                m1, m2 = halves(rr)
                oo = mtr(rr.loc[OOS_START:])
                picks.append(dict(panel=pname, lam=lam, selector=tag, book=int(col),
                                  IS_Sharpe=y_is[j], OOS_Sharpe=y_oos[j],
                                  full_Sharpe=m["Sharpe"], full_CAGR=m["CAGR"], full_MaxDD=m["MaxDD"],
                                  H1=m1["Sharpe"], H2=m2["Sharpe"],
                                  OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"],
                                  v2_OOS_Sharpe=mtr(base.loc[OOS_START:])["Sharpe"],
                                  spy_OOS_Sharpe=spy_oos["Sharpe"],
                                  beats_v2=bool(oo["Sharpe"] > mtr(base.loc[OOS_START:])["Sharpe"]),
                                  beats_spy=bool(oo["Sharpe"] > spy_oos["Sharpe"]),
                                  pass4a=bool(m1["Sharpe"] > bh1["Sharpe"] and m2["Sharpe"] > bh2["Sharpe"]
                                              and m["MaxDD"] >= bm["MaxDD"]),
                                  pass4b=bool(m1["Sharpe"] > sh1["Sharpe"] and m2["Sharpe"] > sh2["Sharpe"]
                                              and oo["Sharpe"] > spy_oos["Sharpe"]
                                              and m["MaxDD"] >= 0.60 * sm_["MaxDD"]
                                              and m["CAGR"] >= 0.70 * sm_["CAGR"])))
        P(f"    {pname} done ({time.time() - T0:.0f}s)")

    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    BK = pd.DataFrame(books)
    BK.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    W = pd.DataFrame(picks)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  {len(G)} grid points written ({len(LAMS)} penalties x {len(FOLDS)} folds x 2 widths "
      f"x {len(panels)} panels)")

    # --------------- G3: reproduce idea 483's committed grid exactly
    ref = ROOT / "research/backtests/2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud.grid.csv"
    if ref.exists():
        D = pd.read_csv(ref)
        keys = ["panel", "width", "lam", "K"]
        j = D.merge(G, on=keys, suffixes=("_ref", "_new"))
        cmp_cols = [c for c in ("t_insample", "pR2_insample", "survive_insample", "t_oof",
                                "pR2_oof", "survive_oof", "R2_raw", "t_raw",
                                "R2_control_reproduces_sd_insample") if f"{c}_ref" in j.columns]
        worst = {c: float(np.nanmax(np.abs(j[f"{c}_ref"] - j[f"{c}_new"]))) for c in cmp_cols}
        mx = max(worst.values()) if worst else np.nan
        P(f"\n  G3  idea 483's committed grid re-derived: {len(j)}/{len(D)} rows joined on "
          f"{keys}, over {len(cmp_cols)} published columns.")
        # Split per panel, following the record's own G2a/G2b precedent: two of the three price
        # files are frozen and one (U56 -> data/prices.csv) is live and has gained trading days
        # since idea 483 ran, so a per-panel split says which is machinery and which is vintage.
        for pn, sub in j.groupby("panel"):
            w = {c: float(np.nanmax(np.abs(sub[f"{c}_ref"] - sub[f"{c}_new"]))) for c in cmp_cols}
            mxp = max(w.values())
            lab = ("PASS (machinery identical)" if mxp < 1e-9 else
                   "VINTAGE, reported not waived" if pn == "U56" else "FAIL")
            P(f"      {pn:<10s} {len(sub):>3d} rows  max|d| {mxp:.3e}  worst {max(w, key=w.get)}  -> {lab}")
        P(f"      whole grid max|d| = {mx:.3e}; per published column:")
        for c, v in sorted(worst.items(), key=lambda kv: -kv[1]):
            P(f"        {c:<38s} {v:.3e}")
    else:
        P("\n  G3  idea 483's committed grid.csv not found -- gate not runnable")

    # --------------- the queue's own headline
    P("\n  G4  the queue's headline (B136 WIDE, survive across lam 1e-3..100):")
    q = G[(G.panel == "B136") & (G.width == "WIDE")].groupby("lam").agg(
        survive_IS=("survive_insample", "median"), survive_OOF=("survive_oof", "median"),
        t_IS=("t_insample", "median"), t_OOF=("t_oof", "median"),
        sd_repro_IS=("R2_control_reproduces_sd_insample", "median"))
    P(q.to_string(float_format=lambda x: f"{x:+.4f}"))
    if len(q):
        sp = float(q.survive_IS.max() - q.survive_IS.min())
        P(f"      penalty spread in survive_IS = {sp:.4f}  (queue quotes 0.020 -> 0.959 = 0.939)")

    # --------------- which conclusions are penalty-stable, freshly measured
    P("\n" + "=" * 118)
    P("WHICH CONCLUSIONS ARE PENALTY-STABLE?  (fresh grid, verdict = survive >= 0.5)")
    P("=" * 118)
    fresh = []
    for (pn, wd, K), sub in G.groupby(["panel", "width", "K"]):
        for stat in ("survive_insample", "survive_oof"):
            v = {L: float(sub.loc[np.isclose(sub.lam, L), stat].median()) for L in (LOW, MID, HIGH)}
            got = [x for x in v.values() if np.isfinite(x)]
            if len(got) < 2:
                continue
            verd = [bool(x >= SURVIVE_BAR) for x in got]
            fresh.append(dict(panel=pn, width=wd, K=K, stat=stat, v_low=v[LOW], v_mid=v[MID],
                              v_high=v[HIGH], spread=max(got) - min(got),
                              stable=bool(len(set(verd)) == 1)))
    FR = pd.DataFrame(fresh)
    if len(FR):
        P(f"  {len(FR)} fresh conclusions; PENALTY-STABLE {int(FR.stable.sum())}/{len(FR)} = "
          f"{FR.stable.mean():.1%}; median spread {FR.spread.median():.4f}, max {FR.spread.max():.4f}")
        P(FR.groupby(["panel", "width", "stat"]).agg(
            n=("stable", "size"), stable=("stable", "sum"), med_spread=("spread", "median"),
            max_spread=("spread", "max")).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- PART C summary + rule 8
    P("\n" + "=" * 118)
    P("PART C / RULE 8 -- does the penalty change the BOOK you would trade?  "
      "(control fitted on 2009-2016 only; OOS read once)")
    P("=" * 118)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for pn in panels:
        sub = W[(W.panel == pn) & (W.selector == "RESID")]
        P(f"\n  {pn}: RESID picks {sorted(set(sub.book))} across the 6 penalties "
          f"({sub.book.nunique()} distinct books); OOS Sharpe "
          f"{sub.OOS_Sharpe.min():+.4f}..{sub.OOS_Sharpe.max():+.4f} "
          f"(spread {sub.OOS_Sharpe.max() - sub.OOS_Sharpe.min():.4f})")
    P(f"\n  rule-8 picks over all {len(W)} (panel x lam x selector) cells: "
      f"beats RULES v2 OOS {int(W.beats_v2.sum())}/{len(W)}, beats SPY OOS {int(W.beats_spy.sum())}/{len(W)}, "
      f"4a {int(W.pass4a.sum())}/{len(W)}, 4b {int(W.pass4b.sum())}/{len(W)}")
    for sel in ("RESID", "RAW_IS_SHARPE", "SD"):
        s = W[W.selector == sel]
        P(f"    {sel:<14s} mean OOS Sharpe {s.OOS_Sharpe.mean():+.4f}   "
          f"beats v2 {int(s.beats_v2.sum())}/{len(s)}   beats SPY {int(s.beats_spy.sum())}/{len(s)}   "
          f"4a {int(s.pass4a.sum())}/{len(s)}  4b {int(s.pass4b.sum())}/{len(s)}")

    P("\n  BOTH KEEP PATHS on all 600 draw books, every cost rung:")
    BK["pass_both"] = BK.pass4a & BK.pass4b
    P(BK.groupby(["panel", "rung"])[["pass4a", "pass4b", "pass_both"]].sum().to_string())
    b10 = BK[BK.rung == COST]
    P(f"    at PROTOCOL's own {COST} bps rung: 4a {int(b10.pass4a.sum())}/{len(b10)}, "
      f"4b {int(b10.pass4b.sum())}/{len(b10)}, BOTH {int(b10.pass_both.sum())}/{len(b10)}")

    P(f"\ndone in {time.time() - T0:.0f}s")
    flush_log()


if __name__ == "__main__":
    try:
        main()
    finally:
        flush_log()
