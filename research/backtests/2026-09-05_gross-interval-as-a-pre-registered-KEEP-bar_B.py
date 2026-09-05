#!/usr/bin/env python3
"""QUEUE idea 90 — gross-interval-as-a-pre-registered-KEEP-bar  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 90)
    Idea 84 showed 4b's drawdown CAP and its CAGR FLOOR both live on the gross axis: the cap
    pushes exposure down, the floor pushes it up.  Idea 144 then proved that along a book's own
    static-gross family CAGR and |MaxDD| are both monotone in the multiplier m, so the set of m
    at which a book passes 4b ought to be an INTERVAL [m_lo, m_hi], and a "4b KEEP" is really
    the statement that the interval is non-empty.  Idea 90 asks the follow-on question:

        Should PROTOCOL quote the WIDTH of that interval as a robustness statistic
        instead of a single pass/fail?

    Pre-registered sub-questions, answered in order, with a NO on Q3 being a KILL of the idea:

      Q1  Is the passing set actually an interval?  For all 306 books, is the set of passing m
          a single contiguous run?  (If it is not, "the interval" is the wrong object and the
          proposal has to be restated as a run-count, which is reported instead.)
      Q2  CENSUS.  Derive [m_lo, m_hi] and its width for EVERY corpus book — not just the four
          standing candidates — per (panel, cost) cell, under both gross ceilings.  Report the
          queue's own operational KEEP: a non-empty interval on BOTH large-cap universes at
          BOTH 10 and 25 bps, and the width of the INTERSECTION (one m that works in all four).
      Q3  IS THE WIDTH INFORMATIVE?  Two tests, both pre-registered:
            (a) cross-cell portability — does a book's width in one cell predict a non-empty
                interval in the other three?
            (b) out-of-sample — does the width measured on the IS window (2009-2016) predict
                an OOS 4b pass or OOS Sharpe on 2017-2026?
          If width carries no information beyond the pass/fail it refines, it is a description,
          not a robustness statistic, and idea 90 is a KILL.
      Q4  AS A BAR.  Sweep the two coefficients a width bar would need — the width threshold w*
          and the number of cells k it must hold in — and report every grid point: how many
          books are admitted, and the admitted set's OOS quality, against the incumbent
          POINT-4b bar and idea 144's FAMILY-4b.
      Q5  RULE 8 (required).  As a prospective selector read on 2009-2016 alone, does picking
          the arm with the WIDEST IS interval beat the incumbent IS-Sharpe argmax, the IS-4b
          screen, and idea 144's family screen, out of sample?  Report OOS CAGR/Sharpe/MaxDD
          against RULES v1 and SPY.

HARNESS (nothing new is invented; the corpus is the one the question was asked about)
    Idea 94's simulator (`2026-09-04_drawdown-insurance-price-list_B.py`) is imported, and the
    gross family is rebuilt with idea 144's exact construction, then checked against idea 144's
    committed `family.csv.gz` cell by cell (max|diff| over all 24 shared numeric columns must
    be 0).  That check is run BEFORE any new number is read.

CORPUS
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 books, each swept over m in {0.10, 0.15, ..., 1.30} = 25 points -> 7,650 backtests.
    Weekly, t+1, 75% target gross at m=1.00, 10 and 25 bps, IS <= 2016-12-31, OOS >= 2017-01-01.
    NO LEVERAGE: m = 1.30 is 97.5% target gross; run() caps realised gross at 1.00.
    Gross ceiling m_max in {1.00, 1.30} is reported as an ARM everywhere, not tuned.

BARS (published coefficients, held fixed — they are NOT this run's tuned parameters)
    phi = 0.70 (CAGR floor), delta = 0.60 (MaxDD cap).  Full-sample 4b = {H1, H2, OOS, DD, CAGR}.
    Window 4b (used for the IS screen and the OOS test, identical shape on each window) =
    {H1, H2, DD, CAGR} computed inside that window against SPY inside the same window.

TUNED PARAMETERS — exactly two, both swept exhaustively and all points printed
    w*  minimum interval width in {0.00, 0.05, ..., 0.60}      (13 points)
    k   number of large-cap cells the interval must be non-empty in, in {1, 2, 3, 4}
    Neither is chosen; the grid is the output.

BOTH KEEP PATHS are evaluated on every book: 4a via H.pass4a against RULES v1 on the same panel
and cost rung, 4b as POINT-4b (m = 1.00) and as FAMILY-4b (some m in the family).

CAVEATS carried, not buried
    - Survivorship (idea 54): all three panels are current-constituent lists.
    - Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so every IS
      drawdown cap admits too much; this biases every Q5 selector in the same direction.
    - Idea 38 (u56/broad calendar-day index) and idea 126 (t+1-only execution) carry over.
    - Idea 144: the two `ebud` and two `ddctl` arms are not scale-free, so their families are
      not pure exposure rescales and their "interval" is not a pure gross interval.  Every
      Q1-Q4 statistic is therefore reported split by PURE (ctl/gate/stop) vs SCALE-DEP.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_gross-interval-as-a-pre-registered-KEEP-bar_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I144_FAMILY = OUT / "2026-09-05_is-the-ladder-even-a-candidate_C.family.csv.gz"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
PANELS = ["u56", "broad", "small"]
LARGE_CELLS = [("u56", 10.0), ("u56", 25.0), ("broad", 10.0), ("broad", 25.0)]

STEP = 0.05
MGRID = [round(x, 2) for x in np.arange(0.10, 1.3001, STEP)]     # 25 construction points
MCEIL = [1.00, 1.30]                                             # arm, not a tuned parameter
PHI0, DELTA0 = 0.70, 0.60                                        # published bar coefficients

BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARSW = ("H1", "H2", "DD", "CAGR")                               # window (IS / OOS) bar shape
PURE_KINDS = ("ctl", "gate", "stop")

WSTARS = [round(x, 2) for x in np.arange(0.00, 0.6001, STEP)]    # tuned param 1
KREQ = [1, 2, 3, 4]                                              # tuned param 2

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values)[0, 1])


# ------------------------------------------------------------------ panels (idea 144 verbatim)
_PCACHE = {}


def panel(name):
    if name not in _PCACHE:
        _PCACHE[name] = _panel(name)
    return _PCACHE[name]


def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def bars_win(spy, which):
    """SPY's reference numbers on the full sample or inside one window."""
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def stats_of(r, which):
    w = H.window(r, which) if which != "full" else r
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=oos)


def margins(stat, b, phi, delta):
    return dict(H1=stat["H1"] - b["s1"], H2=stat["H2"] - b["s2"],
                OOS=stat["OOS_Sharpe"] - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(stat["MaxDD"]),
                CAGR=stat["CAGR"] - phi * b["scagr"])


# ------------------------------------------------------------------ one (panel, book, cost) cell
def do_cell(pname, px, spy, book, cost, bfull, bIS, v1_net):
    """Idea 144's do_cell, plus the OOS-window statistics idea 90 needs for Q3(b)."""
    rows = []
    start = spy.index[0]
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = H.targets(px, book, gate, conv)
        for m_ in MGRID:
            res = H.run(px, W, m=m_, bps=cost, **kw)
            r = res["r"].loc[start:]
            g = res["gross"].loc[start:]
            sf, si, so = stats_of(r, "full"), stats_of(r, "IS"), stats_of(r, "OOS")
            mgf, mgi = margins(sf, bfull, PHI0, DELTA0), margins(si, bIS, PHI0, DELTA0)
            rows.append(dict(
                panel=pname, book=book, cost=cost, arm=arm, kind=kind, m=m_,
                CAGR=sf["CAGR"], Sharpe=sf["Sharpe"], MaxDD=sf["MaxDD"], H1=sf["H1"], H2=sf["H2"],
                OOS_Sharpe_full=sf["OOS_Sharpe"],
                IS_CAGR=si["CAGR"], IS_Sharpe=si["Sharpe"], IS_MaxDD=si["MaxDD"],
                IS_H1=si["H1"], IS_H2=si["H2"],
                OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                OOS_H1=so["H1"], OOS_H2=so["H2"],
                m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"], m_DD=mgf["DD"], m_CAGR=mgf["CAGR"],
                IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
                gross=float(g.mean()), gross_cv=float(g.std() / g.mean()) if g.mean() > 0 else np.nan,
                pass4a=H.pass4a(r, v1_net),
                TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
            ))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ bars -> boolean columns
def attach_bars(F, BARS):
    for key, idx in (("b_s1", "s1"), ("b_s2", "s2"), ("b_soos", "soos"),
                     ("b_sdd", "sdd"), ("b_scagr", "scagr")):
        F[key] = F.panel.map({p: BARS[p]["full"][idx] for p in BARS})
    for key, idx in (("bi_s1", "s1"), ("bi_s2", "s2"), ("bi_sdd", "sdd"), ("bi_scagr", "scagr")):
        F[key] = F.panel.map({p: BARS[p]["IS"][idx] for p in BARS})
    for key, idx in (("bo_s1", "s1"), ("bo_s2", "s2"), ("bo_sdd", "sdd"), ("bo_scagr", "scagr")):
        F[key] = F.panel.map({p: BARS[p]["OOS"][idx] for p in BARS})
    F["book_id"] = F.panel + "|" + F.book + "|" + F.cost.astype(str) + "|" + F.arm
    F["cell"] = F.panel + "@" + F.cost.astype(int).astype(str)
    return F


def bar_ok(D, which, phi=PHI0, delta=DELTA0):
    if which == "full":
        return pd.DataFrame(dict(
            H1=D.H1 - D.b_s1 > 0, H2=D.H2 - D.b_s2 > 0,
            OOS=D.OOS_Sharpe_full - D.b_soos > 0,
            DD=delta * D.b_sdd.abs() - D.MaxDD.abs() > 0,
            CAGR=D.CAGR - phi * D.b_scagr > 0), index=D.index)
    if which == "IS":
        return pd.DataFrame(dict(
            H1=D.IS_H1 - D.bi_s1 > 0, H2=D.IS_H2 - D.bi_s2 > 0,
            DD=delta * D.bi_sdd.abs() - D.IS_MaxDD.abs() > 0,
            CAGR=D.IS_CAGR - phi * D.bi_scagr > 0), index=D.index)
    return pd.DataFrame(dict(
        H1=D.OOS_H1 - D.bo_s1 > 0, H2=D.OOS_H2 - D.bo_s2 > 0,
        DD=delta * D.bo_sdd.abs() - D.OOS_MaxDD.abs() > 0,
        CAGR=D.OOS_CAGR - phi * D.bo_scagr > 0), index=D.index)


# ------------------------------------------------------------------ the interval itself
def intervals(F, which, mmax):
    """Per book: the set of m (<= mmax) at which every bar of `which` clears, as an interval."""
    keys = list(BARS5 if which == "full" else BARSW)
    sub = F[F.m <= mmax + 1e-9]
    ok = bar_ok(sub, which)[keys].all(axis=1)
    d = pd.DataFrame(dict(book_id=sub.book_id.values, panel=sub.panel.values,
                          book=sub.book.values, cost=sub.cost.values, arm=sub.arm.values,
                          kind=sub.kind.values, cell=sub.cell.values,
                          m=sub.m.values, ok=ok.values)).sort_values(["book_id", "m"])
    out = []
    for bid, g in d.groupby("book_id", sort=False):
        okv = g.ok.values
        mv = g.m.values
        n = int(okv.sum())
        if n:
            idx = np.flatnonzero(okv)
            runs = 1 + int((np.diff(idx) > 1).sum())
            lo, hi = float(mv[idx[0]]), float(mv[idx[-1]])
            # widest contiguous run (the interval a bar would actually quote)
            runs_list, s = [], None
            for i in range(len(okv)):
                if okv[i] and s is None:
                    s = i
                if (not okv[i] or i == len(okv) - 1) and s is not None:
                    e = i if okv[i] else i - 1
                    runs_list.append((s, e))
                    s = None
            best = max(runs_list, key=lambda t: t[1] - t[0])
            blo, bhi = float(mv[best[0]]), float(mv[best[1]])
            wid_run = (best[1] - best[0] + 1) * STEP
        else:
            runs, lo, hi, blo, bhi, wid_run = 0, np.nan, np.nan, np.nan, np.nan, 0.0
        r0 = g.iloc[0]
        out.append(dict(book_id=bid, panel=r0.panel, book=r0.book, cost=r0.cost, arm=r0.arm,
                        kind=r0.kind, cell=r0.cell, which=which, mmax=mmax,
                        n_m=n, n_runs=runs, m_lo=lo, m_hi=hi, span=(hi - lo) if n else 0.0,
                        width=n * STEP, run_lo=blo, run_hi=bhi, run_width=wid_run,
                        contiguous=bool(runs <= 1), passed=bool(n > 0)))
    return pd.DataFrame(out)


def fmt(df, cols=None, f=3):
    d = df[cols] if cols else df
    return d.to_string(float_format=lambda x: f"{x:.{f}f}")


# ------------------------------------------------------------------ main
def main():
    say("=" * 200)
    say("IDEA 90 — gross-interval-as-a-pre-registered-KEEP-bar.  Is the WIDTH of a book's "
        "4b-passing gross interval a robustness statistic, or only a description?")
    say(f"corpus = 3 panels x 3 books x 17 arms x 2 costs = 306 BOOKS x {len(MGRID)} gross points "
        f"m in [{MGRID[0]}, {MGRID[-1]}] = {306*len(MGRID)} backtests")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, {GROSS:.0%} target gross at m=1.00, "
        f"costs {COSTS} bps.  Bars held at the published phi={PHI0}, delta={DELTA0}.")
    say(f"TUNED (2): w* in {WSTARS}   k in {KREQ}.  Gross ceiling m_max in {MCEIL} is an ARM.")
    say("=" * 200)

    FR, BARS, V1OOS, SPYOOS = [], {}, {}, {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        BARS[pname] = {w: bars_win(spy, w) for w in ("full", "IS", "OOS")}
        so = metrics(H.window(spy, "OOS"))
        SPYOOS[pname] = so
        v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
                  for c in COSTS}
        V1OOS[pname] = {c: metrics(H.window(v1_net[c], "OOS")) for c in COSTS}
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} "
            f"| eval from {start.date()}")
        say(f"    SPY full  CAGR {BARS[pname]['full']['scagr']:.2%}  halves "
            f"{BARS[pname]['full']['s1']:.3f}/{BARS[pname]['full']['s2']:.3f}  "
            f"MaxDD {BARS[pname]['full']['sdd']:.2%}  OOS Sharpe {BARS[pname]['full']['soos']:.3f}")
        say(f"    SPY OOS   CAGR {so['CAGR']:.2%}  Sharpe {so['Sharpe']:.3f}  "
            f"MaxDD {so['MaxDD']:.2%}   |   RULES v1 OOS @10bps "
            f"{V1OOS[pname][10.0]['CAGR']:.2%}/{V1OOS[pname][10.0]['Sharpe']:.3f}/"
            f"{V1OOS[pname][10.0]['MaxDD']:.2%}")
        for book in BOOKS:
            for cost in COSTS:
                FR.append(do_cell(pname, px, spy, book, cost,
                                  BARS[pname]["full"], BARS[pname]["IS"], v1_net[cost]))
                say(f"    ... {pname}/{book}@{cost:.0f}bps done ({len(FR[-1])} rows)")
    F = attach_bars(pd.concat(FR, ignore_index=True), BARS)
    say(f"\nfamily frame: {F.shape[0]} rows x {F.shape[1]} cols, "
        f"{F.book_id.nunique()} books, {F.m.nunique()} gross points")

    # ---------------------------------------------------------- HARNESS CHECK vs idea 144
    say("\n" + "=" * 200)
    say("HARNESS CHECK — rebuild vs idea 144's committed family.csv.gz (run before any new number)")
    say("=" * 200)
    G = pd.read_csv(I144_FAMILY)
    key = ["panel", "book", "cost", "arm", "m"]
    shared = [c for c in G.columns if c in F.columns and c not in key
              and pd.api.types.is_numeric_dtype(G[c])
              and not pd.api.types.is_bool_dtype(G[c])]
    A = F.set_index(key).sort_index()
    B = G.set_index(key).sort_index()
    say(f"rows: idea144 {len(B)}  this run {len(A)}  index identical: {A.index.equals(B.index)}")
    common_idx = A.index.intersection(B.index)
    worst, worst_col = 0.0, None
    for c in shared:
        d = float((A.loc[common_idx, c] - B.loc[common_idx, c]).abs().max())
        if d > worst:
            worst, worst_col = d, c
    say(f"shared numeric columns compared: {len(shared)} over {len(common_idx)} common rows  ->  "
        f"max|diff| = {worst:.3e} (on {worst_col})")
    say("    idea 144's CSV is written rounded to 6 decimals, so 5e-7 is the file's own "
        "quantisation, not a harness difference; the bar is 1e-6.")
    p4a = int((A.loc[common_idx, "pass4a"].astype(bool).values
               != B.loc[common_idx, "pass4a"].astype(bool).values).sum())
    say(f"pass4a disagreements: {p4a} of {len(common_idx)}")
    assert worst < 1e-6 and p4a == 0, "harness does not reproduce idea 144"
    v144 = intervals(F, "full", 1.30)
    say(f"idea 144 census reproduced: FAMILY-4b passes at m<=1.30 = {int(v144.passed.sum())} "
        f"(idea 144 published 72);  at m<=1.00 = "
        f"{int(intervals(F, 'full', 1.00).passed.sum())} (published 58);  "
        f"POINT-4b at m=1.00 = "
        f"{int(bar_ok(F[F.m == 1.00], 'full')[list(BARS5)].all(axis=1).sum())} (published 29)")
    say(f"4a passes at m=1.00: {int(F[F.m == 1.00].pass4a.sum())};  "
        f"anywhere in the family: {int(F.groupby('book_id').pass4a.any().sum())}")

    # ---------------------------------------------------------- Q1 contiguity
    say("\n" + "=" * 200)
    say("Q1 — IS THE PASSING SET AN INTERVAL?  (if not, 'width' is the wrong object)")
    say("=" * 200)
    IV = {}
    for which in ("full", "IS", "OOS"):
        for mm in MCEIL:
            IV[(which, mm)] = intervals(F, which, mm)
    for which in ("full", "IS", "OOS"):
        for mm in MCEIL:
            v = IV[(which, mm)]
            p = v[v.passed]
            say(f"{which:>4} bars, m<=<{mm:.2f}>: {len(p):3d} of {len(v)} books have a non-empty "
                f"passing set; contiguous in {int(p.contiguous.sum())} of {len(p)} "
                f"({(p.contiguous.mean() if len(p) else float('nan')):.1%}); "
                f"n_runs max {int(p.n_runs.max()) if len(p) else 0}")
    v = IV[("full", 1.30)]
    p = v[v.passed]
    say("\nnon-contiguous books (full bars, m<=1.30) — the exceptions, listed in full:")
    nc = p[~p.contiguous]
    say(fmt(nc[["book_id", "kind", "n_m", "n_runs", "m_lo", "m_hi", "width", "run_width"]])
        if len(nc) else "    (none)")
    say("\ncontiguity by arm kind (full bars, m<=1.30, non-empty books only):")
    say(fmt(p.assign(pure=p.kind.isin(PURE_KINDS)).groupby(["pure", "kind"])
            .agg(books=("contiguous", "size"), contiguous=("contiguous", "sum"),
                 mean_runs=("n_runs", "mean"))))

    # ---------------------------------------------------------- Q2 census
    say("\n" + "=" * 200)
    say("Q2 — CENSUS.  [m_lo, m_hi] and its width for every corpus book, per cell.")
    say("=" * 200)
    for mm in MCEIL:
        v = IV[("full", mm)]
        say(f"\n--- gross ceiling m_max = {mm:.2f}")
        t = v.groupby("cell").agg(books=("passed", "size"), nonempty=("passed", "sum"),
                                  mean_width=("width", "mean"), max_width=("width", "max"))
        t["mean_width_pass"] = v[v.passed].groupby("cell").width.mean()
        t["median_width_pass"] = v[v.passed].groupby("cell").width.median()
        say(fmt(t))
        pv = v[v.passed]
        if len(pv):
            say("width distribution over non-empty books: " + ", ".join(
                f"{q}={pv.width.quantile(q/100):.2f}" for q in (0, 25, 50, 75, 100)))
            say("\ntop 15 books by interval width:")
            say(fmt(pv.nlargest(15, "width")[["book_id", "kind", "m_lo", "m_hi", "width", "n_runs"]]))
    v = IV[("full", 1.30)]
    say("\nby arm kind (full bars, m<=1.30):")
    say(fmt(v.assign(pure=v.kind.isin(PURE_KINDS)).groupby(["pure", "kind"])
            .agg(books=("passed", "size"), nonempty=("passed", "sum"),
                 mean_width=("width", "mean"))))

    # the queue's own operational KEEP: non-empty in all four large-cap cells
    say("\n--- the queue's operational KEEP: non-empty on BOTH large-cap universes at BOTH costs")
    for mm in MCEIL:
        v = IV[("full", mm)]
        L = v[v.cell.isin([f"{p}@{int(c)}" for p, c in LARGE_CELLS])].copy()
        L["ba"] = L.book + "|" + L.arm
        piv = L.pivot_table(index="ba", columns="cell", values="width", aggfunc="first")
        pivp = L.pivot_table(index="ba", columns="cell", values="passed", aggfunc="first")
        piv["cells"] = pivp.sum(axis=1)
        piv["min_width"] = piv[[c for c in piv.columns if "@" in str(c)]].min(axis=1)
        # intersection: an m that clears every large-cap cell simultaneously
        keys = list(BARS5)
        sub = F[(F.m <= mm + 1e-9) & F.cell.isin([f"{p}@{int(c)}" for p, c in LARGE_CELLS])].copy()
        sub["ok"] = bar_ok(sub, "full")[keys].all(axis=1)
        sub["ba"] = sub.book + "|" + sub.arm
        inter = sub.groupby(["ba", "m"]).ok.all().reset_index()
        iw = inter[inter.ok].groupby("ba").agg(i_lo=("m", "min"), i_hi=("m", "max"),
                                               i_n=("m", "size"))
        piv = piv.join(iw)
        piv["i_width"] = piv.i_n.fillna(0) * STEP
        say(f"\nm_max = {mm:.2f}   (cells = how many of the 4 large-cap cells are non-empty; "
            f"i_width = width of the INTERSECTION)")
        say(fmt(piv.sort_values(["cells", "i_width", "min_width"], ascending=False)
                [[c for c in piv.columns if "@" in str(c)] +
                 ["cells", "min_width", "i_lo", "i_hi", "i_width"]], f=2))
        say(f"books with all 4 cells non-empty: {int((piv.cells == 4).sum())} of {len(piv)}; "
            f"with a non-empty INTERSECTION: {int((piv.i_width > 0).sum())}")

    # ---------------------------------------------------------- Q3 is width informative?
    say("\n" + "=" * 200)
    say("Q3 — IS THE WIDTH INFORMATIVE?  (a) cross-cell portability   (b) IS -> OOS")
    say("=" * 200)
    v = IV[("full", 1.30)]
    L = v[v.cell.isin([f"{p}@{int(c)}" for p, c in LARGE_CELLS])].copy()
    L["ba"] = L.book + "|" + L.arm
    W = L.pivot_table(index="ba", columns="cell", values="width", aggfunc="first")
    P = L.pivot_table(index="ba", columns="cell", values="passed", aggfunc="first")
    say("\n(a) pairwise Spearman of interval WIDTH across the four large-cap cells:")
    cc = [c for c in W.columns]
    M = pd.DataFrame(index=cc, columns=cc, dtype=float)
    for i in cc:
        for j in cc:
            M.loc[i, j] = spearman(W[i].values, W[j].values)
    say(fmt(M))
    say("\n(a) does width in one cell predict a non-empty interval in the other three?")
    rows = []
    for c in cc:
        others = [x for x in cc if x != c]
        oth = P[others].all(axis=1)
        base = float(oth.mean())
        for thr in (0.05, 0.15, 0.30, 0.50):
            sel = W[c] >= thr
            rows.append(dict(cell=c, thr=thr, n_sel=int(sel.sum()),
                             P_others_given=float(oth[sel].mean()) if sel.any() else np.nan,
                             P_others_base=base,
                             lift=(float(oth[sel].mean()) - base) if sel.any() else np.nan))
        rows.append(dict(cell=c, thr=np.nan, n_sel=int((W[c] > 0).sum()),
                         P_others_given=float(oth[W[c] > 0].mean()) if (W[c] > 0).any() else np.nan,
                         P_others_base=base,
                         lift=(float(oth[W[c] > 0].mean()) - base) if (W[c] > 0).any() else np.nan))
    say(fmt(pd.DataFrame(rows)))
    say("    (thr = NaN row is the plain pass/fail: non-empty at all.  The question idea 90 asks "
        "is whether the graded rows beat that one.)")
    say("\n(a) Spearman(width in cell, number of OTHER cells non-empty), per cell:")
    for c in cc:
        say(f"    {c:>10}: rho = {spearman(W[c].values, P[[x for x in cc if x != c]].sum(axis=1).values):+.3f}"
            f"   |   binary pass/fail rho = "
            f"{spearman(P[c].astype(float).values, P[[x for x in cc if x != c]].sum(axis=1).values):+.3f}")

    say("\n(b) IS width (2009-2016 bars) vs OOS outcome (2017-2026), all 306 books, m<=1.30:")
    vis, voos = IV[("IS", 1.30)], IV[("OOS", 1.30)]
    J = vis[["book_id", "panel", "book", "cost", "arm", "kind", "cell", "width", "passed",
             "m_lo", "m_hi"]].rename(columns={"width": "IS_width", "passed": "IS_pass",
                                              "m_lo": "IS_lo", "m_hi": "IS_hi"})
    J = J.merge(voos[["book_id", "width", "passed"]].rename(
        columns={"width": "OOS_width", "passed": "OOS_pass"}), on="book_id")
    pub = F[F.m == 1.00].set_index("book_id")
    J["OOS_Sharpe_m1"] = J.book_id.map(pub.OOS_Sharpe)
    J["OOS_CAGR_m1"] = J.book_id.map(pub.OOS_CAGR)
    J["OOS_MaxDD_m1"] = J.book_id.map(pub.OOS_MaxDD)
    J["IS_Sharpe_m1"] = J.book_id.map(pub.IS_Sharpe)
    say(f"    IS non-empty: {int(J.IS_pass.sum())} of {len(J)};  "
        f"OOS non-empty: {int(J.OOS_pass.sum())} of {len(J)}")
    say(f"    Spearman(IS_width, OOS_width)       = {spearman(J.IS_width, J.OOS_width):+.3f}")
    say(f"    Spearman(IS_width, OOS_Sharpe@m=1)  = {spearman(J.IS_width, J.OOS_Sharpe_m1):+.3f}")
    say(f"    Spearman(IS_pass , OOS_width)       = "
        f"{spearman(J.IS_pass.astype(float), J.OOS_width):+.3f}   <- the pass/fail it must beat")
    say(f"    Spearman(IS_pass , OOS_Sharpe@m=1)  = "
        f"{spearman(J.IS_pass.astype(float), J.OOS_Sharpe_m1):+.3f}")
    say(f"    Spearman(IS_Sharpe@m=1, OOS_Sharpe@m=1) = "
        f"{spearman(J.IS_Sharpe_m1, J.OOS_Sharpe_m1):+.3f}   <- the incumbent selector's signal")
    say("\n    within IS-passing books only (does the GRADE add anything to the pass?):")
    Jp = J[J.IS_pass]
    say(f"      n = {len(Jp)};  Spearman(IS_width, OOS_width) = {spearman(Jp.IS_width, Jp.OOS_width):+.3f}"
        f";  Spearman(IS_width, OOS_Sharpe@m=1) = {spearman(Jp.IS_width, Jp.OOS_Sharpe_m1):+.3f}")
    say("\n    P(OOS non-empty | IS width >= w), against the base rate and against IS_pass:")
    rows = []
    for w in WSTARS:
        sel = J.IS_width >= w
        if w == 0:
            sel = J.IS_width > -1
        rows.append(dict(w=w, n=int(sel.sum()),
                         P_OOS_pass=float(J.OOS_pass[sel].mean()) if sel.any() else np.nan,
                         mean_OOS_Sharpe=float(J.OOS_Sharpe_m1[sel].mean()) if sel.any() else np.nan,
                         mean_OOS_CAGR=float(J.OOS_CAGR_m1[sel].mean()) if sel.any() else np.nan))
    say(fmt(pd.DataFrame(rows)))
    say(f"    base rate P(OOS non-empty) = {J.OOS_pass.mean():.3f};  "
        f"P(OOS non-empty | IS_pass) = {J.OOS_pass[J.IS_pass].mean():.3f};  "
        f"P(OOS non-empty | not IS_pass) = {J.OOS_pass[~J.IS_pass].mean():.3f}")
    say("\n    by panel (the IS->OOS relation is not pooled-safe):")
    say(fmt(J.groupby("cell").apply(lambda g: pd.Series(dict(
        n=len(g), IS_pass=g.IS_pass.sum(), OOS_pass=g.OOS_pass.sum(),
        rho_width=spearman(g.IS_width, g.OOS_width),
        rho_pass=spearman(g.IS_pass.astype(float), g.OOS_width),
        rho_width_sharpe=spearman(g.IS_width, g.OOS_Sharpe_m1))), include_groups=False)))

    # ---------------------------------------------------------- Q4 as a bar
    say("\n" + "=" * 200)
    say("Q4 — WIDTH AS A BAR.  Grid: w* x k, all points reported.  Admitted-set OOS quality is "
        "the test; a bar that admits fewer books but no better ones is not a bar.")
    say("=" * 200)
    Wl = L.pivot_table(index="ba", columns="cell", values="width", aggfunc="first")
    Pl = L.pivot_table(index="ba", columns="cell", values="passed", aggfunc="first")
    oos_by_ba = (F[(F.m == 1.00) & F.cell.isin([f"{p}@{int(c)}" for p, c in LARGE_CELLS])]
                 .assign(ba=lambda d: d.book + "|" + d.arm)
                 .groupby("ba")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean())
    rows = []
    for w in WSTARS:
        for k in KREQ:
            sel = (Wl >= w).sum(axis=1) >= k
            adm = Wl.index[sel]
            o = oos_by_ba.reindex(adm)
            rows.append(dict(w_star=w, k=k, admitted=int(sel.sum()),
                             mean_OOS_Sharpe=float(o.OOS_Sharpe.mean()) if len(o) else np.nan,
                             mean_OOS_CAGR=float(o.OOS_CAGR.mean()) if len(o) else np.nan,
                             mean_OOS_MaxDD=float(o.OOS_MaxDD.mean()) if len(o) else np.nan))
    Q4 = pd.DataFrame(rows)
    say(fmt(Q4))
    inc = Pl.sum(axis=1) >= 4
    o = oos_by_ba.reindex(Pl.index[inc])
    say(f"\nreference — the incumbent 'non-empty in all 4 cells' bar (w*=0.05, k=4): "
        f"admits {int(inc.sum())}, mean OOS Sharpe {o.OOS_Sharpe.mean():.3f}, "
        f"CAGR {o.OOS_CAGR.mean():.2%}, MaxDD {o.OOS_MaxDD.mean():.2%}")
    pnt = F[(F.m == 1.00) & F.cell.isin([f"{p}@{int(c)}" for p, c in LARGE_CELLS])].copy()
    pnt["ok"] = bar_ok(pnt, "full")[list(BARS5)].all(axis=1)
    pnt["ba"] = pnt.book + "|" + pnt.arm
    p4 = pnt.groupby("ba").ok.sum()
    for k in KREQ:
        adm = p4.index[p4 >= k]
        o = oos_by_ba.reindex(adm)
        say(f"reference — POINT-4b in >= {k} of 4 cells: admits {len(adm)}, "
            f"mean OOS Sharpe {o.OOS_Sharpe.mean():.3f}, CAGR {o.OOS_CAGR.mean():.2%}, "
            f"MaxDD {o.OOS_MaxDD.mean():.2%}" if len(adm) else
            f"reference — POINT-4b in >= {k} of 4 cells: admits 0")
    say(f"reference — the whole large-cap corpus (no bar): {len(oos_by_ba)} books, "
        f"mean OOS Sharpe {oos_by_ba.OOS_Sharpe.mean():.3f}, "
        f"CAGR {oos_by_ba.OOS_CAGR.mean():.2%}, MaxDD {oos_by_ba.OOS_MaxDD.mean():.2%}")

    # ---------------------------------------------------------- Q5 rule 8
    say("\n" + "=" * 200)
    say("Q5 — RULE 8 WALK-FORWARD.  Screens read 2009-2016 ONLY; picks read once on 2017-2026.")
    say("    S0  no screen        : IS-Sharpe argmax at the published m = 1.00")
    say("    S1  IS-POINT-4b      : screen at m=1.00, then IS-Sharpe argmax   (the incumbent)")
    say("    S2  IS-FAMILY-4b     : any m clears the IS bars, then IS-Sharpe argmax at its m*")
    say("    S3  IS-WIDTH (new)   : widest IS interval, traded at its MIDPOINT m")
    say("    S4  IS-WIDTH @ m=1   : widest IS interval, traded at the published m (isolates the "
        "selection from the gross choice)")
    say("=" * 200)
    picks = []
    for (pname, book, cost), g in F.groupby(["panel", "book", "cost"], sort=False):
        cellname = f"{pname}|{book}|{cost:.0f}"
        gi = g[g.m <= 1.30 + 1e-9].copy()
        gi["is_ok"] = bar_ok(gi, "IS")[list(BARSW)].all(axis=1)
        at1 = gi[gi.m == 1.00].set_index("arm")
        iv = IV[("IS", 1.30)]
        iv = iv[(iv.panel == pname) & (iv.book == book) & (iv.cost == cost)].set_index("arm")

        def emit(sel, arm, m_):
            if arm is None:
                picks.append(dict(cell=cellname, panel=pname, book=book, cost=cost, sel=sel,
                                  arm=None, m=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                                  OOS_MaxDD=np.nan))
                return
            r = gi[(gi.arm == arm) & (np.isclose(gi.m, m_))].iloc[0]
            picks.append(dict(cell=cellname, panel=pname, book=book, cost=cost, sel=sel,
                              arm=arm, m=float(m_), OOS_CAGR=r.OOS_CAGR,
                              OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD))

        emit("S0", at1.IS_Sharpe.idxmax(), 1.00)
        ok1 = at1[at1.index.isin(gi[(gi.m == 1.00) & gi.is_ok].arm)]
        emit("S1", ok1.IS_Sharpe.idxmax() if len(ok1) else None, 1.00)
        fam = gi[gi.is_ok]
        if len(fam):
            mstar = fam.groupby("arm").m.max()
            best = fam[fam.set_index(["arm", "m"]).index.isin(list(mstar.items()))]
            b = best.loc[best.IS_Sharpe.idxmax()]
            emit("S2", b.arm, b.m)
        else:
            emit("S2", None, np.nan)
        ivp = iv[iv.passed]
        if len(ivp):
            wmax = ivp.width.max()
            cand = ivp[np.isclose(ivp.width, wmax)]
            if len(cand) > 1:                      # tie-break on IS Sharpe at m=1.00
                cand = cand.loc[[at1.IS_Sharpe.reindex(cand.index).idxmax()]]
            arm = cand.index[0]
            lo, hi = float(cand.run_lo.iloc[0]), float(cand.run_hi.iloc[0])
            mid = MGRID[int(np.argmin([abs(x - (lo + hi) / 2) for x in MGRID]))]
            mid = min(max(mid, lo), hi)
            emit("S3", arm, mid)
            emit("S4", arm, 1.00)
        else:
            emit("S3", None, np.nan)
            emit("S4", None, np.nan)
    PK = pd.DataFrame(picks)
    say("\nper-cell picks and their untouched OOS numbers:")
    say(fmt(PK.pivot_table(index="cell", columns="sel", values="OOS_Sharpe", aggfunc="first")))
    say("\nfull pick table:")
    say(fmt(PK))
    ent = PK.pivot_table(index="cell", columns="sel", values="arm", aggfunc="first")
    say(f"\ncells entered, of {PK.cell.nunique()}: " +
        ", ".join(f"{s}={int(ent[s].notna().sum())}" for s in sorted(PK.sel.unique())))
    moved = {s: int((ent[s].notna() & ent["S0"].notna() & (ent[s] != ent["S0"])).sum())
             for s in sorted(PK.sel.unique()) if s != "S0"}
    say(f"picks that MOVE vs the no-screen S0: {moved}")
    common = ent.dropna().index
    say(f"\nPAIRED on the {len(common)} cells every selector enters "
        f"(mean of per-cell OOS statistics):")
    P5 = PK[PK.cell.isin(common)].groupby("sel")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
    say(fmt(P5, f=4))
    say("\nreference on the same paired cells:")
    ref = []
    for c in common:
        pn, bk, cs = c.split("|")
        ref.append(dict(cell=c, SPY_CAGR=SPYOOS[pn]["CAGR"], SPY_Sharpe=SPYOOS[pn]["Sharpe"],
                        SPY_MaxDD=SPYOOS[pn]["MaxDD"],
                        V1_CAGR=V1OOS[pn][float(cs)]["CAGR"],
                        V1_Sharpe=V1OOS[pn][float(cs)]["Sharpe"],
                        V1_MaxDD=V1OOS[pn][float(cs)]["MaxDD"]))
    RF = pd.DataFrame(ref)
    say(fmt(RF.drop(columns=["cell"]).mean().to_frame("mean").T, f=4))
    say("\nunpaired (each selector over every cell it enters):")
    say(fmt(PK.groupby("sel")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean(), f=4))
    say("\nper-cell OOS Sharpe of each selector vs SPY and RULES v1 on that cell:")
    T = PK.pivot_table(index="cell", columns="sel", values="OOS_Sharpe", aggfunc="first")
    T["SPY"] = [SPYOOS[c.split("|")[0]]["Sharpe"] for c in T.index]
    T["V1"] = [V1OOS[c.split("|")[0]][float(c.split("|")[2])]["Sharpe"] for c in T.index]
    say(fmt(T, f=3))
    for s in sorted(PK.sel.unique()):
        d = T[T[s].notna()]
        say(f"    {s}: beats SPY OOS Sharpe in {int((d[s] > d.SPY).sum())} of {len(d)} cells; "
            f"beats RULES v1 in {int((d[s] > d.V1).sum())} of {len(d)}")

    # ---------------------------------------------------------- outputs
    F.to_csv(OUT / f"{STEM}.family.csv.gz", index=False)
    pd.concat([IV[k].assign(which_key=str(k)) for k in IV], ignore_index=True).to_csv(
        OUT / f"{STEM}.intervals.csv", index=False)
    J.to_csv(OUT / f"{STEM}.is_oos.csv", index=False)
    Q4.to_csv(OUT / f"{STEM}.bargrid.csv", index=False)
    PK.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say("\nwrote: family.csv.gz, intervals.csv, is_oos.csv, bargrid.csv, walkforward.csv, console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
