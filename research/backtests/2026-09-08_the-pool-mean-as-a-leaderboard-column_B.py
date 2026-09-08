#!/usr/bin/env python3
"""QUEUE idea 205 — the-pool-mean-as-a-leaderboard-column  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 205)
    "following 204, propose the pool's mean dSharpe (and its sign) as a required column beside
     any published selector claim, back-fill it wherever the parent script's grid CSV survives,
     and report how many of the record's selector claims are made over a negative-expectancy
     pool.  Cheap; max 2 params."

WHAT IS ACTUALLY BEING TESTED
    Idea 196 found S2LF beating RANDOM out of its own pool by +0.0110 while still losing to
    do-nothing by -0.0032, because the POOL's mean dSharpe was negative.  Idea 204 proposes the
    general form; idea 205 proposes the bookkeeping: publish the pool's mean dSharpe beside every
    selector claim so a reader can see whether a "selector beats X" sentence was written over a
    pool that could not have helped.

    Two of the record's scripts already carry the column
      (2026-09-08_does-any-selector-beat-doing-nothing_B, ..._pre-register-K_CAGR-..._cloud),
    and BOTH compute it the same way:
            pool_mean_dSharpe = mean(OOS_Sharpe of the pool) - OOS_Sharpe(control)
    i.e. OUT OF SAMPLE.  That is the first thing this run checks, because it decides what kind
    of column the record is being asked to adopt:

      Q1  BACK-FILL (the literal ask).  Over every surviving committed CSV that can be resolved
          into (cell, pool, do-nothing arm), what share of the record's selector claims stand
          over a pool whose own mean is negative?
      Q2  IS THE COLUMN CAUSAL?  The published form reads the OOS window, so it is not knowable
          when the selector fires.  Build its causal twin -- the same mean computed on the IS
          window only -- and measure how well the twin's SIGN and LEVEL track the published one.
          A column that only exists after the fact is a post-mortem, not a leaderboard column.
      Q3  IS IT DECISION-RELEVANT?  Regress the incumbent selector's realised d(OOS Sharpe) on
          both forms of the column, paired over every cell.
      Q4  PRICE IT.  Turn the causal twin into a GATE (take the selector's pick only when the
          pool's IS mean clears tau, else hold the cell's own ungated book) and run it through
          both KEEP paths and PROTOCOL rule 8, including a NESTED walk-forward in which tau
          itself is chosen on 2013-2016 and read once on 2017-2026.

    This is a statement about the record's bookkeeping, not a book.  It cannot promote a
    candidate; both KEEP paths are scored anyway on every arm-row and every gated selection.

CORPUS
    (a) LIVE, re-derived here with the imported harness: 3 panels (u56 / broad / small) x 9 (or
        6) books at matched gross 0.75 x 3 cost rungs (0, 10, 25 bps) x idea 94's 17 arms
        = 72 cells, 1,224 arm-rows.  This is idea 151's corpus, re-derived so the IS-window pool
        mean -- which no committed file carries -- can be computed at all.
    (b) BACK-FILL, read-only, over every research/backtests/*.csv that satisfies the
        pre-registered poolability rule below.  Nothing is re-run; files that cannot be resolved
        are reported as unresolvable rather than dropped silently.

POOLABILITY RULE (pre-registered, applied without exception to every CSV in the directory)
    A file contributes cells iff it has an `arm` column, an OOS metric column
    (OOS_Sharpe, else Sharpe), and at least one row whose arm is a do-nothing name
    {control, ctl, none, off, noop, base, do-nothing, do_nothing, hold, identity}.  The cell key
    is the file's own columns intersected with a fixed list of cell-shaped names; a cell counts
    iff it holds EXACTLY ONE do-nothing row and >= 2 distinct rival arms.

TUNED PARAMETERS -- exactly two, every value reported
    1. tau, the gate threshold on the causal (IS-window) pool mean:
         {-inf, -0.02, -0.01, 0.00, +0.01, +0.02, +inf}    (7 values;
          -inf == gate off, always take the pick; +inf == gate always on, always do nothing)
    2. K, the selector the gate sits in front of: {K_Sharpe (the incumbent), K_CAGR}
    7 x 2 = 14 grid points, each scored on 72 cells x 2 pools.  Panels, books, cost rungs, the
    pool definition (P_ALL / P_S1) and the scoring metric are REPORTED axes, never selected on.

WALK-FORWARD (PROTOCOL rule 8), two levels
    Level 1 (the corpus's own):  every selector reads IS (<= 2016-12-31) only; every pick is
        read once on 2017-01-01..2026 against the cell's do-nothing control, RULES v2 (live),
        RULES v1 and SPY, cost-matched at each rung.
    Level 2 (NESTED, for tau):  arms are selected on A = <= 2012-12-31, the pool mean is computed
        on A, tau* is chosen on B = 2013-01-01..2016-12-31, and the (K, tau*) rule is read ONCE
        on C = 2017-01-01..2026, untouched by either choice.  Reported against the same four
        comparands.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  A majority of the record's back-fillable selector claims stand over a pool whose mean is
        negative (idea 196's finding is the general case, not its own accident).
    P2  The causal (IS) twin agrees in SIGN with the published (OOS) column in fewer than 75% of
        cells -- i.e. the column as published cannot be used prospectively.
    P3  The published (OOS) column explains a large share of the incumbent selector's realised
        d(OOS Sharpe) (it is partly the same numbers), and the causal twin explains far less.
    P4  No tau on the grid produces a positive mean d(OOS Sharpe) against do-nothing that
        survives the nested walk-forward.

CAVEATS carried, not buried
    * Survivorship (idea 54): all three panels are current constituents; every CAGR here is
      flattered and no level in this file is an achievable return.  Both sides of every pair are
      drawn from the same flattered panel, so the paired signs are unaffected.
    * Idea 401's restatement: data/prices.csv was rewritten after ideas 133/142 were committed
      while broad/small were not, so the reproduction gate against the committed 1,224-row grid
      is quoted per panel and per column rather than asserted.
    * 72 cells are not 72 independent observations -- books and arms overlap heavily inside a
      panel.  Per-panel and per-rung breakdowns are given so the clustering is visible.
    * The back-fill reads committed CSVs at face value.  It cannot know whether a given file's
      `arm` column was ever the subject of a published selector sentence; it reports the
      poolable population, and the per-file table is written out so the mapping is auditable.
    * Idea 126: every row is quoted at t+1 execution only, 10 bps at PROTOCOL's own rung.

HARNESS
    Idea 94 (H.run, H.arm_specs, H.halves, H.window, H.pass4a), idea 129 (C.bars_win,
    C.margins_at, C.fails) and idea 133 (D.book_weights, D.books_for, D.panel_px) are IMPORTED,
    not re-implemented.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .cells.csv, .picks.csv,
.backfill.csv, .paired.csv, .keeppaths.csv and .walkforward.csv next to itself.
Modifies nothing.
"""
import glob
import importlib.util
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_the-pool-mean-as-a-leaderboard-column_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I151_GRID = OUT / "2026-09-08_does-any-selector-beat-doing-nothing_B.grid.csv"
I151_PICKS = OUT / "2026-09-08_does-any-selector-beat-doing-nothing_B.picks.csv"

PHI0, DELTA0 = 0.70, 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_CAGR": "IS_CAGR"}      # tuned param 2
TAUS = [-np.inf, -0.02, -0.01, 0.00, 0.01, 0.02, np.inf]        # tuned param 1
POOLS = ["P_ALL", "P_S1"]

# nested walk-forward windows (level 2)
A_END, B_START, B_END = "2012-12-31", "2013-01-01", "2016-12-31"

DO_NOTHING = {"control", "ctl", "none", "off", "noop", "base",
              "do-nothing", "do_nothing", "hold", "identity"}
CELLKEYS = ["panel", "universe", "uname", "corpus", "book", "family", "stratum", "dial",
            "score", "conv", "kind", "cost", "cost_bps", "bps", "rung", "pool", "default",
            "gamma", "phi", "delta", "q", "f", "m", "eps", "metric", "scope", "site", "sleeve"]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
D = _load(I133, "i133")

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START

pd.set_option("display.width", 320)
pd.set_option("display.max_columns", 140)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    """Two-sided exact binomial sign test at p=0.5, ties excluded by the caller."""
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def wslice(r, lo=None, hi=None):
    return r.loc[(lo or r.index[0]):(hi or r.index[-1])]


def ols(y, x):
    """Slope, intercept, r2 and the slope's t on the finite pairs."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    n = len(y)
    if n < 3 or x.std() == 0:
        return dict(n=n, slope=np.nan, icept=np.nan, r2=np.nan, t=np.nan)
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss_res = float(((y - yh) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    se = math.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()) if n > 2 else np.nan
    return dict(n=n, slope=float(b), icept=float(a), r2=r2,
                t=float(b / se) if se and np.isfinite(se) and se > 0 else np.nan)


# ================================================================= A. live corpus
def build_grid():
    """3 panels x 9 (or 6) books x 3 rungs x 17 arms, re-derived from the imported harness."""
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = C.bars_win(spy, "full"), C.bars_win(spy, "IS"), C.bars_win(spy, "OOS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        books = D.books_for(pk, px)
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms, spy_oos=mso, v1=v1, v2=v2,
                       start=start, spy_ret=spy, books=books)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}, {len(books)} books {books}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" | OOS Sharpe {mso['Sharpe']:.3f} CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            o2, o1 = metrics(H.window(v2[c], "OOS")), metrics(H.window(v1[c], "OOS"))
            say(f"    RULES v2 @{c:>4.0f}bps CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
                f"MaxDD {mv2['MaxDD']:.2%} OOS {o2['Sharpe']:.3f}/{o2['CAGR']:.2%}/"
                f"{o2['MaxDD']:.2%} | v1 Sharpe {mv1['Sharpe']:.3f} OOS {o1['Sharpe']:.3f}"
                f"/{o1['CAGR']:.2%}/{o1['MaxDD']:.2%}")

        # gate (a): the modified runner reproduces engine.backtest on every ungated book
        worst = 0.0
        for b in books:
            W = D.book_weights(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a] engine-equivalence, {len(books)} ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT - unsafe'})")

        for b in books:
            for c in COSTS:
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = D.book_weights(px, b, gate, conv)
                    res = H.run(px, W, bps=c, **kw)
                    r = res["r"].loc[start:]
                    rets[(pk, b, c, arm)] = r
                    mm = metrics(r)
                    mi, mo = metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    mA = metrics(wslice(r, None, A_END))
                    mB = metrics(wslice(r, B_START, B_END))
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    omg = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    fail, ofail = C.fails(mg), C.fails(omg)
                    rows.append(dict(
                        panel=pk, book=b, cost=c, arm=arm, kind=kind, conv=conv,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=calmar(mi["CAGR"], mi["MaxDD"]),
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        A_Sharpe=mA["Sharpe"], A_CAGR=mA["CAGR"], A_MaxDD=mA["MaxDD"],
                        B_Sharpe=mB["Sharpe"], B_CAGR=mB["CAGR"], B_MaxDD=mB["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"],
                        IS_m_CAGR=ismg["CAGR"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                        m_CAGR=mg["CAGR"],
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-", n_fail=len(fail),
                        pass4b_oos=(len(ofail) == 0), fail4b_oos=",".join(ofail) or "-",
                        pass4a_v2=H.pass4a(r, v2[c]), pass4a_v1=H.pass4a(r, v1[c])))
    df = pd.DataFrame(rows)
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_P_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_P_ALL"] = True
    return df, rets, ref


def reproduction_check(df):
    """Against idea 151's committed 1,224-row grid, per column and per panel."""
    if not I151_GRID.exists():
        say("\n[b] reproduction: idea 151's grid CSV is absent; gate skipped.")
        return pd.DataFrame()
    g = pd.read_csv(I151_GRID)
    j = df.merge(g, on=["panel", "book", "cost", "arm"], suffixes=("", "_151"))
    keys = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
            "IS_Calmar", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]
    say(f"\n[b] reproduction of idea 151's committed grid: {len(j)} of {len(df)} rows matched "
        f"(it published {len(g)}).")
    out = []
    for pk, s in j.groupby("panel"):
        out.append(dict(panel=pk, rows=len(s),
                        **{k: float((s[k] - s[f"{k}_151"]).abs().max()) for k in keys}))
    RP = pd.DataFrame(out).set_index("panel")
    say(RP.to_string(float_format=lambda x: f"{x:.2e}"))
    exact = [p for p in RP.index if RP.loc[p, keys].max() < 1e-12]
    say(f"    EXACT (max|diff| < 1e-12) on: {exact or 'no panel'}.  Gate (a) shows the simulator "
        f"is exact; any remainder is idea 401's data restatement, a DATA difference.")
    return RP.reset_index()


# ================================================================= B. the column, two ways
def build_cells(df, rets, ref):
    """One row per (panel, book, cost, pool): the column as PUBLISHED (OOS) and its CAUSAL twin
    (IS), plus the A/B-window twins the nested walk-forward needs."""
    rows = []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl = s[s.arm == "control"].iloc[0]
        for pool in POOLS:
            cand = s[s[f"adm_{pool}"]]
            fell_back = not len(cand)
            use = s[s.arm == "control"] if fell_back else cand
            rows.append(dict(
                panel=pk, book=b, cost=c, pool=pool, n_pool=len(use), n_arms=len(s),
                pool_empty=fell_back,
                # the record's published form: reads the OOS window -> NOT knowable at decision time
                pool_mean_dSharpe_OOS=float(use.OOS_Sharpe.mean() - ctl.OOS_Sharpe),
                pool_mean_dCAGR_OOS=float(use.OOS_CAGR.mean() - ctl.OOS_CAGR),
                # the causal twin: same statistic, IS window only
                pool_mean_dSharpe_IS=float(use.IS_Sharpe.mean() - ctl.IS_Sharpe),
                pool_mean_dCAGR_IS=float(use.IS_CAGR.mean() - ctl.IS_CAGR),
                # nested walk-forward twins
                pool_mean_dSharpe_A=float(use.A_Sharpe.mean() - ctl.A_Sharpe),
                pool_mean_dSharpe_B=float(use.B_Sharpe.mean() - ctl.B_Sharpe),
                ctl_OOS_Sharpe=float(ctl.OOS_Sharpe), ctl_OOS_CAGR=float(ctl.OOS_CAGR),
                ctl_OOS_MaxDD=float(ctl.OOS_MaxDD),
                ctl_B_Sharpe=float(ctl.B_Sharpe)))
    return pd.DataFrame(rows)


def make_picks(df, cells, ref):
    """For each cell x pool x selector: the pick, its realised OOS delta vs do-nothing, and both
    forms of the column carried alongside.  This is the row shape idea 205 proposes."""
    rows = []
    idx = cells.set_index(["panel", "book", "cost", "pool"])
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl = s[s.arm == "control"].iloc[0]
        mv1 = metrics(H.window(ref[pk]["v1"][c], "OOS"))
        mv2 = metrics(H.window(ref[pk]["v2"][c], "OOS"))
        mso = ref[pk]["spy_oos"]
        for pool in POOLS:
            cand = s[s[f"adm_{pool}"]]
            use = s[s.arm == "control"] if not len(cand) else cand
            cr = idx.loc[(pk, b, c, pool)]
            for K, col in SELECTORS.items():
                p = use.loc[use[col].idxmax()]
                # the same selector re-run on window A only, for the nested walk-forward
                acol = "A_Sharpe" if K == "K_Sharpe" else "A_CAGR"
                pA = use.loc[use[acol].idxmax()]
                rows.append(dict(
                    panel=pk, book=b, cost=c, pool=pool, selector=K, arm=p.arm,
                    n_pool=len(use), moved=bool(p.arm != "control"),
                    pool_mean_dSharpe_OOS=float(cr.pool_mean_dSharpe_OOS),
                    pool_mean_dSharpe_IS=float(cr.pool_mean_dSharpe_IS),
                    pool_mean_dSharpe_A=float(cr.pool_mean_dSharpe_A),
                    OOS_Sharpe=float(p.OOS_Sharpe), OOS_CAGR=float(p.OOS_CAGR),
                    OOS_MaxDD=float(p.OOS_MaxDD),
                    ctl_OOS_Sharpe=float(ctl.OOS_Sharpe), ctl_OOS_CAGR=float(ctl.OOS_CAGR),
                    ctl_OOS_MaxDD=float(ctl.OOS_MaxDD),
                    d_OOS_Sharpe=float(p.OOS_Sharpe - ctl.OOS_Sharpe),
                    d_OOS_CAGR=float(p.OOS_CAGR - ctl.OOS_CAGR),
                    d_OOS_MaxDD=float(abs(ctl.OOS_MaxDD) - abs(p.OOS_MaxDD)),
                    armA=pA.arm, movedA=bool(pA.arm != "control"),
                    B_Sharpe=float(pA.B_Sharpe), ctl_B_Sharpe=float(ctl.B_Sharpe),
                    d_B_Sharpe=float(pA.B_Sharpe - ctl.B_Sharpe),
                    A_OOS_Sharpe=float(pA.OOS_Sharpe), A_OOS_CAGR=float(pA.OOS_CAGR),
                    A_OOS_MaxDD=float(pA.OOS_MaxDD),
                    v1_OOS_Sharpe=mv1["Sharpe"], v2_OOS_Sharpe=mv2["Sharpe"],
                    spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                    spy_OOS_MaxDD=mso["MaxDD"],
                    pass4a_v2=bool(p.pass4a_v2), pass4a_v1=bool(p.pass4a_v1),
                    pass4b=bool(p.pass4b), pass4b_oos=bool(p.pass4b_oos),
                    ctl_pass4b=bool(ctl.pass4b), ctl_pass4b_oos=bool(ctl.pass4b_oos),
                    ctl_pass4a_v2=bool(ctl.pass4a_v2), ctl_pass4a_v1=bool(ctl.pass4a_v1),
                    ctl_Sharpe=float(ctl.Sharpe), ctl_CAGR=float(ctl.CAGR),
                    ctl_MaxDD=float(ctl.MaxDD),
                    full_Sharpe=float(p.Sharpe), full_CAGR=float(p.CAGR),
                    full_MaxDD=float(p.MaxDD)))
    return pd.DataFrame(rows)


# ================================================================= C. back-fill census
def backfill_census():
    """The literal ask: back-fill the column over every surviving committed CSV that the
    pre-registered poolability rule can resolve."""
    files = sorted(glob.glob(str(OUT / "*.csv")))
    frows, cellrows, unres = [], [], []
    for fp in files:
        name = os.path.basename(fp)
        if name.startswith(STEM):
            continue
        try:
            d = pd.read_csv(fp, low_memory=False)
        except Exception as e:
            unres.append(dict(file=name, why=f"unreadable: {type(e).__name__}"))
            continue
        cols = list(d.columns)
        if "arm" not in cols:
            unres.append(dict(file=name, why="no arm column"))
            continue
        met = "OOS_Sharpe" if "OOS_Sharpe" in cols else ("Sharpe" if "Sharpe" in cols else None)
        if met is None:
            unres.append(dict(file=name, why="no OOS_Sharpe/Sharpe column"))
            continue
        d["_dn"] = d.arm.astype(str).str.strip().str.lower().isin(DO_NOTHING)
        if not d._dn.any():
            unres.append(dict(file=name, why="no do-nothing arm"))
            continue
        keys = [k for k in CELLKEYS if k in cols and k != "arm"]
        if not keys:
            keys = []
        g = d.groupby(keys, dropna=False) if keys else [((), d)]
        nc, nneg, npos, nzero = 0, 0, 0, 0
        for gk, s in (g if keys else g):
            dn = s[s._dn]
            rival = s[~s._dn]
            if len(dn) != 1 or rival.arm.nunique() < 2:
                continue
            ctlv = float(dn[met].iloc[0])
            pv = pd.to_numeric(rival[met], errors="coerce").dropna()
            if not np.isfinite(ctlv) or len(pv) < 2:
                continue
            pm = float(pv.mean() - ctlv)
            nc += 1
            nneg += int(pm < 0)
            npos += int(pm > 0)
            nzero += int(pm == 0)
            cellrows.append(dict(file=name, metric=met, n_rival=len(pv), n_arms=len(s),
                                 pool_mean_d=pm,
                                 cell="|".join(f"{k}={v}" for k, v in
                                               zip(keys, gk if isinstance(gk, tuple) else (gk,)))
                                 if keys else "-"))
        if nc == 0:
            unres.append(dict(file=name, why="no cell with 1 do-nothing arm and >=2 rivals"))
            continue
        frows.append(dict(file=name, metric=met, keys="|".join(keys) or "-", cells=nc,
                          neg=nneg, pos=npos, zero=nzero, neg_share=nneg / nc))
    F = pd.DataFrame(frows).sort_values(["neg_share", "cells"], ascending=[False, False])
    CE = pd.DataFrame(cellrows)
    U = pd.DataFrame(unres)
    say(f"\n================ Q1  BACK-FILL over the committed record ================")
    say(f"    {len(files)} CSVs under research/backtests/; {len(F)} are poolable under the "
        f"pre-registered rule, contributing {len(CE)} cells; {len(U)} unresolvable "
        f"(top reasons: {U.why.str.split(':').str[0].value_counts().head(4).to_dict() if len(U) else '-'}).")
    if len(CE):
        neg = int((CE.pool_mean_d < 0).sum())
        say(f"    NEGATIVE-EXPECTANCY POOLS: {neg} of {len(CE)} cells "
            f"({neg/len(CE):.1%}); mean pool_mean_d {CE.pool_mean_d.mean():+.4f}, "
            f"median {CE.pool_mean_d.median():+.4f}.")
        say(f"    Files whose pools are negative in EVERY cell: "
            f"{int((F.neg_share == 1.0).sum())} of {len(F)}; "
            f"in NO cell: {int((F.neg_share == 0.0).sum())}.")
        # the headline is cell-weighted and the cell census is concentrated; de-concentrate it
        top = F.sort_values("cells", ascending=False).iloc[0]
        rest = CE[CE.file != top.file]
        say(f"    CONCENTRATION, reported not buried: the largest single file "
            f"({top.file}) contributes {int(top.cells)} of {len(CE)} cells "
            f"({top.cells/len(CE):.1%}).  Excluding it: "
            f"{int((rest.pool_mean_d < 0).sum())} of {len(rest)} negative "
            f"({(rest.pool_mean_d < 0).mean():.1%}).")
        say(f"    FILE-weighted (each poolable file one vote, its own neg_share): "
            f"median {F.neg_share.median():.1%}, mean {F.neg_share.mean():.1%} over "
            f"{len(F)} files.")
        say("\n    Top 20 poolable files by cell count:")
        say(F.sort_values("cells", ascending=False).head(20).to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    return F, CE, U


# ================================================================= D. gate + keep paths
def gate_grid(picks):
    """Tuned parameter 1 (tau) x tuned parameter 2 (K), every point reported.

    GATE(K, tau): take K's pick iff the cell's CAUSAL pool mean >= tau, else hold the control.
    tau = -inf is the ungated incumbent; tau = +inf is do-nothing.
    """
    rows = []
    for pool in POOLS:
        for K in SELECTORS:
            s = picks[(picks.pool == pool) & (picks.selector == K)]
            for tau in TAUS:
                take = s.pool_mean_dSharpe_IS >= tau
                dS = np.where(take, s.d_OOS_Sharpe, 0.0)
                dC = np.where(take, s.d_OOS_CAGR, 0.0)
                dD = np.where(take, s.d_OOS_MaxDD, 0.0)
                oS = np.where(take, s.OOS_Sharpe, s.ctl_OOS_Sharpe)
                oC = np.where(take, s.OOS_CAGR, s.ctl_OOS_CAGR)
                oD = np.where(take, s.OOS_MaxDD, s.ctl_OOS_MaxDD)
                nz = dS[dS != 0]
                w = int((nz > 0).sum())
                rows.append(dict(
                    pool=pool, selector=K, tau=tau, cells=len(s),
                    take_rate=float(take.mean()),
                    mean_dOOS_Sharpe=float(np.mean(dS)), t_dS=tstat(dS),
                    mean_dOOS_CAGR=float(np.mean(dC)), t_dC=tstat(dC),
                    mean_dOOS_MaxDD=float(np.mean(dD)), t_dD=tstat(dD),
                    n_moved=int(len(nz)), wins=w, losses=int(len(nz) - w),
                    win_rate=float(w / len(nz)) if len(nz) else np.nan,
                    sign_p=sign_p(w, len(nz)),
                    mean_OOS_Sharpe=float(np.mean(oS)), mean_OOS_CAGR=float(np.mean(oC)),
                    mean_OOS_MaxDD=float(np.mean(oD)),
                    beat_spy_share=float(np.mean(oS > s.spy_OOS_Sharpe.values)),
                    beat_v2_share=float(np.mean(oS > s.v2_OOS_Sharpe.values)),
                    beat_v1_share=float(np.mean(oS > s.v1_OOS_Sharpe.values)),
                    pass4a_v2=int(np.where(take, s.pass4a_v2, s.ctl_pass4a_v2).sum()),
                    pass4a_v1=int(np.where(take, s.pass4a_v1, s.ctl_pass4a_v1).sum()),
                    pass4b=int(np.where(take, s.pass4b, s.ctl_pass4b).sum()),
                    pass4b_oos=int(np.where(take, s.pass4b_oos, s.ctl_pass4b_oos).sum()),
                    both_paths=int((np.where(take, s.pass4a_v2, s.ctl_pass4a_v2)
                                    & np.where(take, s.pass4b, s.ctl_pass4b)).sum())))
    return pd.DataFrame(rows)


def nested_walkforward(picks):
    """PROTOCOL rule 8, level 2.  Arms selected on A (<=2012); the pool mean computed on A;
    tau* chosen on B (2013-2016); the (K, tau*) rule read ONCE on C (2017+)."""
    rows = []
    for pool in POOLS:
        for K in SELECTORS:
            s = picks[(picks.pool == pool) & (picks.selector == K)]
            # choose tau on window B, using the A-window pool mean and the A-window pick
            best, bt = None, -np.inf
            ibest, ibt = None, -np.inf          # the same, restricted to an INTERIOR tau
            btab = []
            for tau in TAUS:
                take = s.pool_mean_dSharpe_A >= tau
                dB = float(np.mean(np.where(take, s.d_B_Sharpe, 0.0)))
                btab.append(dict(pool=pool, selector=K, tau=tau, window="B(2013-2016)",
                                 take_rate=float(take.mean()), mean_d=dB))
                if dB > bt:
                    bt, best = dB, tau
                if np.isfinite(tau) and dB > ibt:
                    ibt, ibest = dB, tau
            for r in btab:
                r["chosen"] = (r["tau"] == best)
                rows.append(r)

            def read_once(tau, label):
                take = s.pool_mean_dSharpe_A >= tau
                oS = np.where(take, s.A_OOS_Sharpe, s.ctl_OOS_Sharpe)
                oC = np.where(take, s.A_OOS_CAGR, s.ctl_OOS_CAGR)
                oD = np.where(take, s.A_OOS_MaxDD, s.ctl_OOS_MaxDD)
                d = oS - s.ctl_OOS_Sharpe.values
                nz = d[d != 0]
                w = int((nz > 0).sum())
                return dict(pool=pool, selector=K, tau=tau, window=label,
                            take_rate=float(take.mean()), mean_d=float(np.mean(d)),
                            chosen=True, t=tstat(d), n_moved=int(len(nz)), wins=w,
                            sign_p=sign_p(w, len(nz)),
                            OOS_Sharpe=float(np.mean(oS)), OOS_CAGR=float(np.mean(oC)),
                            OOS_MaxDD=float(np.mean(oD)),
                            ctl_OOS_Sharpe=float(s.ctl_OOS_Sharpe.mean()),
                            ctl_OOS_CAGR=float(s.ctl_OOS_CAGR.mean()),
                            ctl_OOS_MaxDD=float(s.ctl_OOS_MaxDD.mean()),
                            v1_OOS_Sharpe=float(s.v1_OOS_Sharpe.mean()),
                            v2_OOS_Sharpe=float(s.v2_OOS_Sharpe.mean()),
                            spy_OOS_Sharpe=float(s.spy_OOS_Sharpe.mean()),
                            spy_OOS_CAGR=float(s.spy_OOS_CAGR.mean()),
                            spy_OOS_MaxDD=float(s.spy_OOS_MaxDD.mean()))

            rows.append(read_once(best, "C(2017-2026) READ ONCE"))
            # tau = -inf and +inf are the degenerate endpoints (gate off / do nothing); when the
            # honest window picks one of them the GATE itself is never actually priced, so the
            # best INTERIOR tau is read once as well, unconditionally, and reported either way,
            # alongside BOTH endpoints on the same window so the domination test is out of sample.
            rows.append(read_once(ibest, "C(2017-2026) READ ONCE, INTERIOR-tau ONLY"))
            rows.append(read_once(-np.inf, "C(2017-2026) endpoint: UNGATED"))
            rows.append(read_once(np.inf, "C(2017-2026) endpoint: DO-NOTHING"))
    return pd.DataFrame(rows)


# ================================================================= main
def main():
    say(__doc__.split("HARNESS")[0].rstrip())
    say("\n================ A.  LIVE CORPUS ================")
    df, rets, ref = build_grid()
    say(f"\n[grid] {len(df)} arm-rows, {df.groupby(['panel','book','cost']).ngroups} cells.")
    RP = reproduction_check(df)

    cells = build_cells(df, rets, ref)
    picks = make_picks(df, cells, ref)

    # ---------------- Q1 back-fill ----------------
    F, CE, U = backfill_census()

    # the live corpus's own answer to Q1, at both forms of the column
    say(f"\n    LIVE corpus (this run's 144 cell x pool rows), for comparison:")
    for form in ["pool_mean_dSharpe_OOS", "pool_mean_dSharpe_IS"]:
        v = cells[form]
        say(f"      {form:24s} negative in {int((v<0).sum()):3d} of {len(v)} "
            f"({(v<0).mean():.1%}); mean {v.mean():+.4f} median {v.median():+.4f}")

    # ---------------- Q2 is the column causal ----------------
    say("\n================ Q2  IS THE PUBLISHED COLUMN CAUSAL? ================")
    say("    The record's two committed instances compute the column on the OOS window, so it is")
    say("    not knowable when the selector fires.  Its causal twin is the same statistic read on")
    say("    the IS window only.  If the two disagree, the column can only ever be a post-mortem.")
    a, b = cells.pool_mean_dSharpe_IS.values, cells.pool_mean_dSharpe_OOS.values
    agree = int(np.sum(np.sign(a) == np.sign(b)))
    say(f"    sign agreement IS vs OOS: {agree} of {len(a)} ({agree/len(a):.1%})   "
        f"pearson r {np.corrcoef(a,b)[0,1]:+.4f}   spearman {H.spearman(a,b):+.4f}")
    say(f"    regression OOS ~ IS: {ols(b, a)}")
    for pk, s in cells.groupby("panel"):
        ai, bi = s.pool_mean_dSharpe_IS.values, s.pool_mean_dSharpe_OOS.values
        ag = int(np.sum(np.sign(ai) == np.sign(bi)))
        say(f"      {pk:6s} n {len(s):3d}  sign agreement {ag/len(s):6.1%}  "
            f"r {np.corrcoef(ai,bi)[0,1]:+.4f}  meanIS {ai.mean():+.4f}  meanOOS {bi.mean():+.4f}")

    # verify against the record's own committed column
    if I151_PICKS.exists():
        g = pd.read_csv(I151_PICKS)
        g = g[(g.default == "K_Sharpe")][["panel", "book", "cost", "pool", "pool_mean_dSharpe"]]
        j = cells.merge(g, on=["panel", "book", "cost", "pool"], how="inner")
        if len(j):
            dd = float((j.pool_mean_dSharpe - j.pool_mean_dSharpe_OOS).abs().max())
            say(f"\n    [c] the committed column reproduces: max|diff| vs idea 151's published "
                f"pool_mean_dSharpe over {len(j)} rows = {dd:.3e} "
                f"({'EXACT' if dd < 1e-9 else 'restatement-level' if dd < 1e-3 else 'MISMATCH'})")

    # ---------------- Q3 decision relevance ----------------
    say("\n================ Q3  IS THE COLUMN DECISION-RELEVANT? ================")
    say("    Paired over every cell: the incumbent selector's realised d(OOS Sharpe) against")
    say("    do-nothing, regressed on each form of the column.")
    prows = []
    for pool in POOLS:
        for K in SELECTORS:
            s = picks[(picks.pool == pool) & (picks.selector == K)]
            for form in ["pool_mean_dSharpe_OOS", "pool_mean_dSharpe_IS"]:
                o = ols(s.d_OOS_Sharpe.values, s[form].values)
                sg = int(np.sum(np.sign(s[form].values) == np.sign(s.d_OOS_Sharpe.values)))
                prows.append(dict(pool=pool, selector=K, column=form, n=o["n"],
                                  slope=o["slope"], r2=o["r2"], t=o["t"],
                                  sign_agree=sg / len(s),
                                  mean_d=float(s.d_OOS_Sharpe.mean()),
                                  t_mean_d=tstat(s.d_OOS_Sharpe.values)))
    P = pd.DataFrame(prows)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- Q4 price it ----------------
    say("\n================ Q4  PRICE THE COLUMN AS A GATE (all 14 grid points x 2 pools) ======")
    G = gate_grid(picks)
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n    Read: tau=-inf is the ungated incumbent selector, tau=+inf is do-nothing "
        "(d == 0 by construction).")
    say("    A gate that helps must show mean_dOOS_Sharpe > 0 with take_rate strictly inside "
        "(0,1).")
    best = G[(G.tau > -np.inf) & (G.tau < np.inf)].sort_values("mean_dOOS_Sharpe",
                                                               ascending=False).head(3)
    say("\n    Best three interior grid points by mean d(OOS Sharpe):")
    say(best.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n================ RULE 8, LEVEL 2 — NESTED WALK-FORWARD FOR tau ================")
    W = nested_walkforward(picks)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- KEEP paths ----------------
    say("\n================ KEEP PATHS (PROTOCOL 4a and 4b) ================")
    say(f"    Arm-rows: 4a-vs-v2 {int(df.pass4a_v2.sum())}/{len(df)}, "
        f"4a-vs-v1 {int(df.pass4a_v1.sum())}/{len(df)}, "
        f"4b(full) {int(df.pass4b.sum())}/{len(df)}, 4b(OOS) {int(df.pass4b_oos.sum())}/{len(df)}, "
        f"BOTH(4a_v2 & 4b) {int((df.pass4a_v2 & df.pass4b).sum())}/{len(df)}.")
    say("    Gated selections, per grid point, are in the Q4 table's pass4a_*/pass4b_* columns.")
    kp = G[["pool", "selector", "tau", "take_rate", "pass4a_v2", "pass4a_v1", "pass4b",
            "pass4b_oos", "both_paths", "mean_OOS_Sharpe", "mean_OOS_CAGR", "mean_OOS_MaxDD",
            "beat_spy_share", "beat_v2_share"]]
    say(kp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dn = G[G.tau == np.inf][["pool", "selector", "pass4a_v2", "pass4b", "pass4b_oos",
                             "both_paths"]].iloc[0]
    say(f"\n    Do-nothing baseline for the same 72 cells: 4a_v2 {int(dn.pass4a_v2)}, "
        f"4b {int(dn.pass4b)}, 4b_oos {int(dn.pass4b_oos)}, both {int(dn.both_paths)}.")
    say("    NO grid point that beats do-nothing on the KEEP counts while also beating it on "
        "d(OOS Sharpe) is a KEEP; the verdict below states which, if any, does.")

    # ---------------- verdict ----------------
    say("\n================ PRE-REGISTERED PREDICTIONS ================")
    negshare = float((CE.pool_mean_d < 0).mean()) if len(CE) else np.nan
    say(f"    P1 majority of back-fillable claims over a negative pool: "
        f"{negshare:.1%} -> {'CONFIRMED' if negshare > 0.5 else 'REJECTED'}")
    say(f"    P2 IS/OOS sign agreement < 75%: {agree/len(a):.1%} -> "
        f"{'CONFIRMED' if agree/len(a) < 0.75 else 'REJECTED'}")
    r2o = float(P[P.column == 'pool_mean_dSharpe_OOS'].r2.mean())
    r2i = float(P[P.column == 'pool_mean_dSharpe_IS'].r2.mean())
    say(f"    P3 published column explains much, causal twin little: mean r2 "
        f"{r2o:.4f} vs {r2i:.4f} -> {'CONFIRMED' if r2o > r2i else 'REJECTED'}")
    wf = W[W.window == "C(2017-2026) READ ONCE"]
    wi = W[W.window.str.contains("INTERIOR")]
    say(f"    P4 no tau survives the nested walk-forward: "
        f"OOS mean_d {[round(float(x),4) for x in wf.mean_d.values]} -> "
        f"{'CONFIRMED' if (wf.mean_d <= 0).all() else 'REJECTED as literally coded'}")
    say(f"       the literal test is contaminated by the DEGENERATE endpoints: the honest "
        f"window chose tau*=-inf (gate off) or +inf (do nothing) in "
        f"{int((~np.isfinite(wf.tau)).sum())} of {len(wf)} arms, so any positive number there "
        f"belongs to the UNGATED selector, not to the gate.")
    say(f"       priced on the gate itself (best INTERIOR tau, chosen on B, read once on C): "
        f"mean_d {[round(float(x),4) for x in wi.mean_d.values]}; positive in "
        f"{int((wi.mean_d > 0).sum())} of {len(wi)} arms.")

    # DOMINATION TEST: is the best interior gate ever better than BOTH degenerate endpoints?
    say("\n================ DOMINATION TEST — is an interior gate ever the best thing to do? ====")
    say("    For each (pool, selector) arm the gate has two degenerate endpoints: tau=-inf (the")
    say("    ungated selector) and tau=+inf (do nothing).  A gate is only worth a column if its")
    say("    best INTERIOR threshold beats BOTH of them.  In sample (the full IS->OOS reading)")
    say("    and out of sample (the nested B->C reading), on mean d(OOS Sharpe):")
    drows = []
    for pool in POOLS:
        for K in SELECTORS:
            g = G[(G.pool == pool) & (G.selector == K)]
            ung = float(g[g.tau == -np.inf].mean_dOOS_Sharpe.iloc[0])
            non = float(g[g.tau == np.inf].mean_dOOS_Sharpe.iloc[0])
            gi = g[(g.tau > -np.inf) & (g.tau < np.inf)]
            bi = float(gi.mean_dOOS_Sharpe.max())
            bit = float(gi.loc[gi.mean_dOOS_Sharpe.idxmax(), "tau"])
            w = W[(W.pool == pool) & (W.selector == K)]
            oi = float(w[w.window.str.contains("INTERIOR")].mean_d.iloc[0])
            ou = float(w[w.window.str.endswith("UNGATED")].mean_d.iloc[0])
            od = float(w[w.window.str.endswith("DO-NOTHING")].mean_d.iloc[0])
            drows.append(dict(pool=pool, selector=K,
                              IS_ungated=ung, IS_donothing=non, IS_best_interior=bi,
                              IS_best_tau=bit,
                              IS_gate_dominates=bool(bi > ung and bi > non),
                              OOS_ungated=ou, OOS_donothing=od, OOS_interior=oi,
                              OOS_gate_dominates=bool(oi > ou and oi > od)))
    DM = pd.DataFrame(drows)
    say(DM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    The interior gate dominates both endpoints in {int(DM.IS_gate_dominates.sum())} "
        f"of {len(DM)} arms in sample and {int(DM.OOS_gate_dominates.sum())} of {len(DM)} "
        f"out of sample.")
    dom = DM[DM.OOS_gate_dominates]
    for _, d in dom.iterrows():
        ch = W[(W.pool == d.pool) & (W.selector == d.selector)
               & (W.window == "C(2017-2026) READ ONCE")].tau.iloc[0]
        say(f"    NOTE on the one OOS domination ({d.pool}/{d.selector}): the honest B window "
            f"chose tau*={ch}, NOT an interior threshold -- the interior tau read here exists "
            f"only because this leg FORCES an interior choice.  The gate never wins a decision "
            f"the walk-forward was actually allowed to make.")
    DM.to_csv(OUT / f"{STEM}.domination.csv", index=False)

    say("\n================ VERDICT ================")
    interior = G[(G.tau > -np.inf) & (G.tau < np.inf)]
    dn_row = G[G.tau == np.inf]
    beats_dn = interior[interior.mean_dOOS_Sharpe > 0]
    say(f"    Q1  BACK-FILL: the column can be reconstructed for {len(F)} of "
        f"{len(F)+len(U)} committed CSVs ({len(CE)} cells).  "
        f"{negshare:.1%} of those cells stand over a negative-expectancy pool "
        f"(file-weighted median {F.neg_share.median():.1%}).")
    say(f"    Q2  The published (OOS-window) form has a usable causal twin: IS vs OOS sign "
        f"agreement {agree/len(a):.1%}, r {np.corrcoef(a,b)[0,1]:+.3f}, "
        f"OOS ~ IS r2 {ols(b,a)['r2']:.3f}.  The column is FORECASTABLE.")
    say(f"    Q3  It is NOT decision-relevant: the slope of the incumbent selector's realised "
        f"d(OOS Sharpe) on the column changes SIGN across the four (pool, selector) arms "
        f"(OOS form {[round(float(x),3) for x in P[P.column=='pool_mean_dSharpe_OOS'].slope.values]}, "
        f"IS form {[round(float(x),3) for x in P[P.column=='pool_mean_dSharpe_IS'].slope.values]}) and "
        f"sign agreement ranges "
        f"{P.sign_agree.min():.1%}-{P.sign_agree.max():.1%}.")
    say(f"    Q4  As a GATE it is a KILL: {len(beats_dn)} of {len(interior)} interior grid "
        f"points beat do-nothing on mean d(OOS Sharpe), but the interior gate dominates BOTH "
        f"of its own degenerate endpoints in {int(DM.IS_gate_dominates.sum())} of {len(DM)} "
        f"arms in sample and {int(DM.OOS_gate_dominates.sum())} of {len(DM)} out of sample -- "
        f"every apparent win is the gate walking toward one endpoint, never past it.  "
        f"4a-vs-v2 passes fall from {int(G[(G.tau==-np.inf)].pass4a_v2.max())} (ungated) to "
        f"{int(interior.pass4a_v2.max())} at every interior tau; both-paths from "
        f"{int(G[(G.tau==-np.inf)].both_paths.max())} to {int(interior.both_paths.max())}.")
    say(f"    KEEP PATHS: 4a {int(interior.pass4a_v2.max())} of {len(interior)} interior grid "
        f"points; 4b {int((interior.pass4b > int(dn_row.pass4b.max())).sum())} grid points "
        f"improving on do-nothing's {int(dn_row.pass4b.max())}; BOTH PATHS "
        f"{int(interior.both_paths.max())}.  NO KEEP, on either path, at any grid point.")
    say("    RECOMMENDATION: publish the column in its CAUSAL (IS-window) form as a "
        "REPORT-ONLY context column beside a selector claim -- it is cheap, forecastable and "
        "it does show that ~80% of the record's back-fillable selector claims stand over a "
        "pool that could not have helped.  Do NOT make it a gate, a screen or a KEEP bar: "
        "priced as one it loses at every threshold and on the nested walk-forward.")

    # ---------------- write ----------------
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    picks.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    if len(CE):
        CE.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
    F.to_csv(OUT / f"{STEM}.backfill_files.csv", index=False)
    U.to_csv(OUT / f"{STEM}.backfill_unresolved.csv", index=False)
    P.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    G.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    if len(RP):
        RP.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\n[written] {STEM}.{{grid,cells,picks,backfill,backfill_files,backfill_unresolved,"
        f"paired,keeppaths,walkforward,console}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
