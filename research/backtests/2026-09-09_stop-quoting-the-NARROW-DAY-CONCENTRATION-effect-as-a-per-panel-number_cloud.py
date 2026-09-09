#!/usr/bin/env python3
"""Idea 583 - stop quoting a CONDITIONAL-SUBSET statistic as a per-panel number.

Premise (idea 319): idea 316's `ann_eff_on_narrow_pp` was published as three per-panel
numbers (+5.9 / +0.3 / -4.2 pp/yr).  Idea 319 gave it a COMPOSITION standard error for the
first time (4.8-7.7 pp/yr, |t| 1.24 / 0.06 / 0.55).  This run asks the cheaper and more
universal question: every statistic of the form

    ann_eff = 252 * mean( r_A(t) - r_B(t) | day t is in subset C )

also has a TIME-SERIES standard error that costs nothing to compute and that the record
never prints.  If that SE alone swamps the published effects, then every narrow-day
effect, gate-on/gate-off premium, drawdown-year edge and regime split in the record is a
point estimate wearing a fact's clothes, and LEADERBOARD needs an SE column.

Two tuned parameters only: (condition family, threshold q).  Everything else is pinned.

Structure
  GATES        three pre-registered checks, printed before any hypothesis is read.
  CENSUS       mechanical scan of every committed CSV under research/ for columns that
               ARE conditional-subset statistics, and whether the same file carries any
               se/t/ci sibling column.
  POPULATION   3 panels x 4 condition families x 3 thresholds = 36 cells.  Each cell gets
               the point estimate, a Newey-West SE (lag 5), a stationary-block-bootstrap
               SE (block 21d, 500 reps), t, and the conditioned-day count.  ALL reported.
  RULE 8       WF-A picks (family, q) per panel on IS <= 2016-12-31 by conditional effect
               and reads the tradable conditional book OOS 2017+ once.  WF-B picks over
               all 36 books by IS Sharpe.  Both KEEP paths (4a and 4b) evaluated on the
               full sample and on OOS.

Costs 10 bps per unit turnover, weekly cadence, weights decided at close t applied t+1.
SMALL panel: tickers with max_1d_move >= 1.0 dropped; SURVIVORSHIP - current constituents
of the sub-$2B screen only (data/SMALL_PANEL_README.md).
"""
import sys, json, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, metrics, rebalance_mask  # noqa

RNG = np.random.default_rng(583)
COST_BPS = 10.0
FREQ = "W"
IS_END = pd.Timestamp("2016-12-31")
pd.set_option("display.width", 220, "display.max_columns", 60, "display.max_rows", 300)


# ----------------------------------------------------------------------------- machinery
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, cost_bps=COST_BPS, freq=FREQ):
    """engine.backtest semantics (decide t, apply t+1, drift between rebalances) with the
    per-name work vectorised.  Gate G1 asserts equality with engine.backtest."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    held = np.empty_like(wt)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def mets(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def cand_weights(px, n=20, gross=1.0):
    """The 2026-09-04 KEEP 4b candidate family: top-n by the composite score with NO vol
    scaler, equal weight, gross fixed."""
    s, above, vol20 = score(px, vol_scale=False)
    s = s.drop(columns=["SPY"], errors="ignore").reindex(columns=px.columns).where(px.notna())
    rank = s.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return (sel.div(cnt, axis=0) * gross).fillna(0.0)


def ewall_weights(px, gross=1.0):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return (gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0)).fillna(0.0)


# ------------------------------------------------------------------ standard errors
def nw_se(x: np.ndarray, lag=5):
    """Newey-West SE of the MEAN of x (already restricted to the conditioned days, kept in
    calendar order so the autocovariances are the ones an overlapping subset actually has)."""
    x = np.asarray(x, float)
    T = len(x)
    if T < 10:
        return np.nan
    e = x - x.mean()
    g0 = (e @ e) / T
    s = g0
    for L in range(1, min(lag, T - 1) + 1):
        gl = (e[L:] @ e[:-L]) / T
        s += 2.0 * (1.0 - L / (lag + 1.0)) * gl
    if s <= 0.0:            # degenerate (constant series, or NW truncation drove it non-positive)
        return 0.0
    return np.sqrt(s / T)


def block_boot_se(diff: pd.Series, cond: pd.Series, block=21, reps=500, rng=RNG):
    """Stationary-block bootstrap of the conditional mean.  Blocks are drawn from the FULL
    calendar (so the conditioning itself is resampled, not held fixed) - this is the SE of
    'run the same experiment on another 16-year path of this panel'."""
    d = diff.values
    c = cond.values.astype(bool)
    T = len(d)
    if T < 3 * block or c.sum() < 10:
        return np.nan
    nb = int(np.ceil(T / block))
    starts = rng.integers(0, T - block, size=(reps, nb))
    out = np.empty(reps)
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(reps, -1)[:, :T]
    for k in range(reps):
        ii = idx[k]
        cc = c[ii]
        out[k] = d[ii][cc].mean() if cc.sum() >= 10 else np.nan
    return float(np.nanstd(out, ddof=1))


# ------------------------------------------------------------------ condition families
def conditions(px, panel_rets):
    """Four recurring conditioning forms in the record, each at three thresholds.
    Every condition is knowable at close t (no look-ahead); the effect series it selects is
    the SAME day's realised r_A - r_B, exactly as the record quotes it."""
    spy = px["SPY"] if "SPY" in px.columns else px.mean(axis=1)
    out = {}
    # 1. NARROW: cross-sectional dispersion of daily returns below quantile q (idea 316's form)
    disp = panel_rets.std(axis=1)
    for q in (0.20, 0.35, 0.50):
        thr = disp.expanding(252).quantile(q)
        out[("NARROW", q)] = (disp <= thr).fillna(False)
    # 2. GATEON: breadth (share of names above their 200d MA) above quantile q
    ma = px.drop(columns=["SPY"], errors="ignore").rolling(200).mean()
    br = (px.drop(columns=["SPY"], errors="ignore") > ma).sum(axis=1) / ma.notna().sum(axis=1).replace(0, np.nan)
    for q in (0.50, 0.65, 0.80):
        thr = br.expanding(252).quantile(q)
        out[("GATEON", q)] = (br >= thr).fillna(False)
    # 3. DDYEAR: SPY drawdown from its running max deeper than x (the 'drawdown-year edge')
    dd = spy / spy.cummax() - 1.0
    for x in (0.05, 0.10, 0.20):
        out[("DDYEAR", x)] = (dd <= -x).fillna(False)
    # 4. HIVOL: SPY 20d realised vol above quantile q (the 'regime split')
    rv = spy.pct_change().rolling(20).std() * np.sqrt(252)
    for q in (0.50, 0.70, 0.85):
        thr = rv.expanding(252).quantile(q)
        out[("HIVOL", q)] = (rv >= thr).fillna(False)
    return out


# ----------------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {len(px.columns) - len(keep)} names with max_1d_move >= 1.0")
    return px[keep]


def load_panels():
    p = {}
    p["U56"] = load_universe()
    p["B136"] = load_universe(broad=True)
    p["SMALL"] = small_panel()
    for k, v in p.items():
        print(f"  {k}: {v.shape[0]} rows x {v.shape[1]} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    return p


# ----------------------------------------------------------------------------- GATES
def gates(panels):
    print("\n" + "=" * 100)
    print("GATES (pre-registered, printed before any hypothesis is read)")
    print("=" * 100)
    px = panels["U56"]

    # G1 - fast_backtest must equal engine.backtest on a real book
    w = cand_weights(px, 20)
    r_fast, t_fast = fast_backtest(px, w)
    eng = engine_backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    d_r = float(np.abs(r_fast - eng["returns"]).max())
    d_t = float(np.abs(t_fast - eng["turnover"]).max())
    g1 = d_r < 1e-12 and d_t < 1e-12
    print(f"G1 fast_backtest vs engine.backtest on U56/CAND-20: max|dret| {d_r:.3e}  max|dturn| {d_t:.3e}  -> {'PASS' if g1 else 'FAIL'}")

    # G2 - reproduce a committed published anchor (idea 486's U56/RULES v1 numbers)
    rv1, _ = fast_backtest(px, rules_v1_weights(px))
    rv1 = rv1.loc[px.index[260]:]
    c, s, m = mets(rv1)
    tgt = (0.064194, 0.66110, -0.138278)
    g2 = abs(c - tgt[0]) < 5e-4 and abs(s - tgt[1]) < 5e-3 and abs(m - tgt[2]) < 5e-3
    print(f"G2 U56/RULES v1 rebuild {c:.4%} / {s:.5f} / {m:.4%} vs published 6.4194% / 0.66110 / -13.8278%  -> {'PASS' if g2 else 'FAIL'}")

    # G3 - the SE machinery must return exactly 0 on a book differenced against itself
    zero = pd.Series(0.0, index=px.index)
    cond = pd.Series(True, index=px.index)
    se_nw = nw_se(zero.values)
    se_bb = block_boot_se(zero, cond, reps=100)
    g3 = (se_nw is not np.nan and se_nw < 1e-12) and (se_bb < 1e-12)
    print(f"G3 SE of a book minus itself: NW {se_nw:.3e}  block-bootstrap {se_bb:.3e}  -> {'PASS' if g3 else 'FAIL'}")
    print(f"GATES: {'ALL PASS' if (g1 and g2 and g3) else 'FAILURE - read nothing below'}")
    return g1 and g2 and g3


# ----------------------------------------------------------------------------- CENSUS
CONDWORDS = ("narrow", "gate_on", "gateon", "_on_", "regime", "hivol", "ddyear", "drawdown_year",
             "eff_on", "premium", "prem_", "_prem", "conditional", "when_", "cond_", "state_on",
             "armed", "on_days", "offdays", "off_days", "bear", "bull", "crisis")
SEWORDS = ("_se", "se_", "stderr", "std_err", "tstat", "t_stat", "_t", "t_", "ci_", "_ci",
           "pval", "p_val", "_p", "boot", "sd_", "_sd")


def census():
    print("\n" + "=" * 100)
    print("CENSUS - committed CSVs under research/: which conditional-subset statistic columns carry an SE sibling?")
    print("=" * 100)
    files = sorted((ROOT / "research").rglob("*.csv"))
    n_files = n_read = n_hit_files = n_cond_cols = n_with_se = n_strict = 0
    hits = []
    for f in files:
        n_files += 1
        try:
            head = pd.read_csv(f, nrows=1)
        except Exception:
            continue
        n_read += 1
        cols = [str(c) for c in head.columns]
        low = [c.lower() for c in cols]
        cond = [c for c, l in zip(cols, low) if any(w in l for w in CONDWORDS)]
        if not cond:
            continue
        has_se = any(any(w in l for w in SEWORDS) for l in low)
        # STRICT leg: does the conditional column have its OWN se/t sibling, by name?
        cset = set(low)
        strict = sum(1 for c in cond if any(
            (c.lower() + suf) in cset or (pre + c.lower()) in cset
            for suf in ("_se", "_sd", "_t", "_tstat", "_stderr", "_ci", "_p", "_pval", "_boot")
            for pre in ("se_", "sd_", "t_", "tstat_", "stderr_", "ci_", "p_")))
        n_hit_files += 1
        n_cond_cols += len(cond)
        n_strict += strict
        if has_se:
            n_with_se += len(cond)
        hits.append((str(f.relative_to(ROOT)), len(cond), has_se, strict))
    print(f"CSV files under research/: {n_files} ({n_read} readable)")
    print(f"Files carrying >=1 conditional-subset statistic column: {n_hit_files}")
    print(f"Conditional-subset statistic COLUMNS: {n_cond_cols}")
    print(f"  ... of which sit in a file that carries ANY se/t/ci/bootstrap sibling column: "
          f"{n_with_se} ({n_with_se / max(n_cond_cols, 1):.1%})")
    print("  (that test is deliberately GENEROUS: a file scores if ANY column looks like an SE,")
    print("   whether or not it belongs to the conditional statistic itself.)")
    print(f"  ... of which carry their OWN name-matched se/t/sd/ci sibling (STRICT): "
          f"{n_strict} ({n_strict / max(n_cond_cols, 1):.1%})")
    top = sorted(hits, key=lambda h: -h[1])[:12]
    print("\n  Largest carriers:")
    for f, k, sflag, st in top:
        print(f"    {k:4d} cond cols  any-se-in-file={'Y' if sflag else 'N'}  own-se={st:4d}  {f}")
    return dict(files=n_files, hit_files=n_hit_files, cols=n_cond_cols, with_se=n_with_se, strict=n_strict)


# ------------------------------------------------------------------------- POPULATION
def population(panels):
    print("\n" + "=" * 100)
    print("POPULATION - 3 panels x 4 condition families x 3 thresholds = 36 cells, ALL reported")
    print("A = CAND-20 (the 2026-09-04 KEEP 4b family, equal weight, no vol scaler); B = EW-all.")
    print("stat = 252 * mean(r_A - r_B | condition) in pp/yr.  Costs 10 bps, weekly, next-day fill.")
    print("=" * 100)
    rows, books = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        prets = px.drop(columns=["SPY"], errors="ignore").pct_change()
        rA, _ = fast_backtest(px, cand_weights(px, 20))
        rB, _ = fast_backtest(px, ewall_weights(px))
        diff = (rA - rB).loc[start:]
        conds = conditions(px, prets)
        for (fam, q), c in conds.items():
            c = c.reindex(diff.index).fillna(False)
            n_on = int(c.sum())
            if n_on < 30:
                rows.append(dict(panel=pname, family=fam, thr=q, n_on=n_on, share=np.nan,
                                 stat_pp=np.nan, se_nw_pp=np.nan, se_bb_pp=np.nan, t_nw=np.nan, t_bb=np.nan))
                continue
            x = diff[c].values
            est = 252 * x.mean() * 100
            se_nw_pp = 252 * nw_se(x) * 100
            se_bb_pp = 252 * block_boot_se(diff, c) * 100
            rows.append(dict(panel=pname, family=fam, thr=q, n_on=n_on, share=n_on / len(diff),
                             stat_pp=est, se_nw_pp=se_nw_pp, se_bb_pp=se_bb_pp,
                             t_nw=est / se_nw_pp if se_nw_pp else np.nan,
                             t_bb=est / se_bb_pp if se_bb_pp else np.nan))
        books[pname] = dict(px=px, rA=rA, rB=rB, conds=conds, start=start)
    df = pd.DataFrame(rows)
    print(df.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    ok = df.dropna(subset=["t_bb"])
    print(f"\n  cells with a finite t: {len(ok)}/{len(df)}")
    print(f"  |t_bb| >= 2 (composition-and-path SE): {(ok['t_bb'].abs() >= 2).sum()} / {len(ok)} "
          f"({(ok['t_bb'].abs() >= 2).mean():.1%})")
    print(f"  |t_nw| >= 2 (time-series SE only):     {(ok['t_nw'].abs() >= 2).sum()} / {len(ok)} "
          f"({(ok['t_nw'].abs() >= 2).mean():.1%})")
    print(f"  median |stat| {ok['stat_pp'].abs().median():.2f} pp/yr vs median SE_bb {ok['se_bb_pp'].median():.2f} pp/yr "
          f"(ratio {ok['stat_pp'].abs().median() / ok['se_bb_pp'].median():.2f}x)")
    print(f"  sign disagreement across panels at the SAME (family, thr): ", end="")
    piv = ok.pivot_table(index=["family", "thr"], columns="panel", values="stat_pp")
    dis = ((piv > 0).sum(axis=1).between(1, 2)).sum()
    print(f"{dis} of {len(piv)} (family, thr) rungs have panels of BOTH signs")
    return df, books


# ------------------------------------------------------------------- tradable books
def conditional_book(px, cond, n=20):
    """The tradable form of the conditional claim: hold A (CAND-20) on days the condition is
    ON, hold B (EW-all) otherwise.  Condition read at close t, weights applied t+1 by the
    engine, weekly cadence."""
    wA = cand_weights(px, n)
    wB = ewall_weights(px)
    c = cond.reindex(px.index).fillna(False)
    return wA.where(c, wB)


def keep_paths(r, base, spy, label):
    """4a vs the live book, 4b vs SPY.  Returns a dict of the legs, all printed."""
    cr, sr, mr = mets(r); h1r, h2r = halves(r)
    cb, sb, mb = mets(base); h1b, h2b = halves(base)
    cs, ss, ms = mets(spy); h1s, h2s = halves(spy)
    a = (h1r > h1b) and (h2r > h2b) and (mr >= mb)
    b = (h1r > h1s) and (h2r > h2s) and (mr >= 0.60 * ms) and (cr >= 0.70 * cs)
    print(f"    {label:38s} CAGR {cr:7.2%}  Sharpe {sr:6.3f} (H1 {h1r:.3f} / H2 {h2r:.3f})  MaxDD {mr:7.2%}"
          f"   4a {'PASS' if a else 'fail'}  4b {'PASS' if b else 'fail'}")
    return dict(label=label, CAGR=cr, Sharpe=sr, MaxDD=mr, H1=h1r, H2=h2r, p4a=a, p4b=b)


def rule8(panels, books, df):
    print("\n" + "=" * 100)
    print("RULE 8 WALK-FORWARD - IS <= 2016-12-31 chooses, OOS 2017-01-01.. read ONCE")
    print("=" * 100)
    out = []
    for pname, B in books.items():
        px, start = B["px"], B["start"]
        spy = px["SPY"].pct_change().fillna(0.0)
        base, _ = fast_backtest(px, rules_v2_weights(px))
        diff = (B["rA"] - B["rB"]).loc[start:]
        # WF-A: pick (family, thr) by the LARGEST IS conditional effect - the record's own claim shape
        best, best_v = None, -np.inf
        is_tbl = []
        for (fam, q), c in B["conds"].items():
            c = c.reindex(diff.index).fillna(False)
            m = c & (diff.index <= IS_END)
            if m.sum() < 30:
                continue
            v = 252 * diff[m].mean() * 100
            is_tbl.append((fam, q, m.sum(), v))
            if v > best_v:
                best_v, best = v, (fam, q)
        print(f"\n{pname}: IS conditional effects (pp/yr), all grid points:")
        print("   " + "  ".join(f"{f}@{q}={v:+.2f}" for f, q, n, v in is_tbl))
        print(f"  WF-A pick = {best[0]}@{best[1]} (IS {best_v:+.2f} pp/yr)")
        wbook = conditional_book(px, B["conds"][best])
        r, _ = fast_backtest(px, wbook)
        segs = [("FULL", slice(start, None)), ("OOS 2017+", slice(pd.Timestamp("2017-01-01"), None))]
        for tag, sl in segs:
            print(f"  [{pname} {tag}]")
            rr = keep_paths(r.loc[sl], base.loc[sl], spy.loc[sl], f"WF-A {best[0]}@{best[1]}")
            keep_paths(B["rA"].loc[sl], base.loc[sl], spy.loc[sl], "parent A = CAND-20")
            keep_paths(B["rB"].loc[sl], base.loc[sl], spy.loc[sl], "parent B = EW-all")
            keep_paths(base.loc[sl], base.loc[sl], spy.loc[sl], "RULES v2 (live baseline)")
            keep_paths(spy.loc[sl], base.loc[sl], spy.loc[sl], "SPY")
            rr.update(panel=pname, seg=tag, pick=f"{best[0]}@{best[1]}", path="WF-A")
            out.append(rr)
        # WF-B: pick the conditional BOOK with the best IS Sharpe on this panel, read OOS once
        cand = []
        for (fam, q), c in B["conds"].items():
            rb, _ = fast_backtest(px, conditional_book(px, c))
            cand.append((fam, q, metrics(rb.loc[start:IS_END])["Sharpe"], rb))
        cand.sort(key=lambda z: -z[2])
        fam, q, s_is, rb = cand[0]
        print(f"  WF-B pick by IS Sharpe = {fam}@{q} (IS Sharpe {s_is:.3f}); all IS Sharpes: "
              + "  ".join(f"{f}@{qq}={ss:.3f}" for f, qq, ss, _ in cand))
        for tag, sl in segs:
            rr = keep_paths(rb.loc[sl], base.loc[sl], spy.loc[sl], f"WF-B {fam}@{q} [{tag}]")
            rr.update(panel=pname, seg=tag, pick=f"{fam}@{q}", path="WF-B")
            out.append(rr)
    return pd.DataFrame(out)


def main():
    print("Idea 583 - conditional-subset statistics without a standard error")
    print("Panels:")
    panels = load_panels()
    g = gates(panels)
    if not g:
        print("GATE FAILURE - stopping."); return
    cen = census()
    df, books = population(panels)
    wf = rule8(panels, books, df)
    outdir = ROOT / "research" / "backtests"
    stem = "2026-09-09_stop-quoting-the-NARROW-DAY-CONCENTRATION-effect-as-a-per-panel-number_cloud"
    df.to_csv(outdir / f"{stem}.cells.csv", index=False)
    wf.to_csv(outdir / f"{stem}.wf.csv", index=False)
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    ok = df.dropna(subset=["t_bb"])
    print(f"census: {cen['cols']} conditional-subset statistic columns in {cen['hit_files']} committed files; "
          f"{cen['with_se']} ({cen['with_se']/max(cen['cols'],1):.1%}) sit in a file with ANY se/t sibling, but only "
          f"{cen['strict']} ({cen['strict']/max(cen['cols'],1):.1%}) carry their OWN name-matched SE")
    print(f"population: {(ok['t_bb'].abs() >= 2).sum()}/{len(ok)} cells reach |t_bb| >= 2; "
          f"median |stat| {ok['stat_pp'].abs().median():.2f} pp/yr vs median SE {ok['se_bb_pp'].median():.2f} pp/yr")
    print(f"4a passes across all walk-forward rows: {int(wf['p4a'].sum())}/{len(wf)}; "
          f"4b passes: {int(wf['p4b'].sum())}/{len(wf)}")
    print(f"wrote {stem}.cells.csv and {stem}.wf.csv")


if __name__ == "__main__":
    main()
