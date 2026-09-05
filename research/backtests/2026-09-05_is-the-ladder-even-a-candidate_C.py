#!/usr/bin/env python3
"""QUEUE idea 144 — is-the-ladder-even-a-candidate  (research sprint lane C, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 144)
    Idea 131 showed that every candidate version of 4b's *adequacy* bar (the CAGR floor, and
    its proposed replacement, a mean-gross floor) exists for exactly one reason: to stop the
    static-gross LADDER — a pure de-risking lever with no Sharpe content — from being recorded
    as a 4b pass.  It also showed no return- or exposure-LEVEL threshold can do that without
    discarding real defensive books (families overlap; 0 of 34 gamma grid points do both jobs).

    Idea 144 tests the CONSTRUCTION fix instead of another metric:

        A static rescaling of an existing book is the SAME BOOK, not a new corpus row.

    Under that convention the ladder is not a candidate to be excluded — it is the interior of
    each book's own gross family.  The pre-registered questions:

      Q1  Is the convention even coherent?  Is Sharpe invariant, CAGR monotone-increasing and
          |MaxDD| monotone-increasing along a book's own gross family?  (If not, "the same
          book" is not a well-defined equivalence and the idea dies here.)
      Q2  Status quo: with the ladder present as 342 separate corpus rows, which of 4b's five
          bars is LOAD-BEARING — i.e. deleting it changes at least one verdict?
      Q3  The fix: drop the ladder from the corpus and evaluate all 306 books under FAMILY-4b
          (a book passes iff SOME point of its own gross family clears every bar).  Re-derive
          which bars are load-bearing.  If the answer is "none", 4b LOSES a bar.
      Q4  If the CAGR floor and the MaxDD cap stop being individually load-bearing but remain
          jointly so, they have collapsed into ONE bar.  Derive it, state it in closed form,
          and measure how exactly the closed form reproduces the exhaustive family verdict.
      Q5  Rule 8: as a PROSPECTIVE screen read on 2009-2016 alone, does FAMILY-4b select better
          out-of-sample than POINT-4b, than no screen, and than the same screen with the CAGR
          floor / the DD cap deleted?  (The family convention lets the screen choose m as well
          as the arm, which is exactly the new overfitting risk it introduces; the walk-forward
          is the test of it.)

    An answer of "the floor is still load-bearing after the fix" is a KILL of idea 144 and is
    reported as such.  Rule 7: nothing is tuned until it works; every grid point is printed.

HARNESS
    Idea 94's script (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED and idea
    131's corpus is reproduced EXACTLY before any new number is read, so this run adjudicates
    the same 306 rows the question was asked about.  Four checks:
      (a) H.run vs engine.backtest, ungated EWall u56 — must be exact;
      (b) idea 94's published EWall+vol60-dg u56@10bps row (11.6% / 1.133 / -16.9%);
      (c) idea 131/129's census: 306 rows, 82 Pareto, 29 pass 4b, 27 floor-only,
          342 ladder rows of which 97 floor-only and all at m <= 0.80;
      (d) idea 131's IS-screen groups A=45 / B=9 / C=252.

CORPUS (nothing new is invented)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 books.  Weekly, t+1, 75% target gross at m=1.00, 10 and 25 bps,
    IS <= 2016-12-31, OOS >= 2017-01-01.
    GROSS FAMILY of each book: static multiplier m on the target weights,
    m in {0.10, 0.15, ..., 1.30} = 25 points (idea 131's 19-point ladder 0.10-1.00 is a strict
    subset, so its numbers are reproduced inside this run).  m = 1.00 is the published point.
    NO LEVERAGE: m = 1.30 is 97.5% target gross, and run() caps any row's gross at 1.00.

TUNED PARAMETERS — exactly two, the two bar coefficients under adjudication
    phi   CAGR floor    in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta MaxDD cap     in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}         (0.60 published)
    All 42 grid points reported, under BOTH conventions.
    m is NOT a tuned parameter: it is the construction dial, swept exhaustively, and the
    m_max ceiling is run as an ARM (1.00 = idea 131's ladder, 1.30 = the no-leverage ceiling)
    with both values reported everywhere.

BOTH KEEP PATHS are evaluated on every book, under both conventions (4a via H.pass4a against
RULES v1 on the same panel and cost rung; 4b as POINT-4b and as FAMILY-4b).

CAVEATS carried, not buried
    - Survivorship (idea 54): all three panels are current-constituent lists.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so every IS
      drawdown cap admits too much.  This biases all selectors in Q5 the same way.
    - Idea 38 (u56/broad calendar-day index) and idea 126 (t+1 only) carry over.
    - The rescale is defined as scaling the TARGET weights.  For the two `ebud` arms the
      turnover budget is an absolute quantity, so scaling m changes how hard it bites; those
      arms are therefore not pure exposure rescales.  Q1 measures this per arm-kind rather
      than assuming it away.
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

STEM = "2026-09-05_is-the-ladder-even-a-candidate_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
PANELS = ["u56", "broad", "small"]

MGRID = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.05)]   # 25 construction points
MCEIL = [1.00, 1.30]                                            # arm: idea 131's ladder / no-leverage
LADDER131 = [round(x, 2) for x in np.arange(0.10, 1.0001, 0.05)]

PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]               # tuned param 1
DELTAS = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]                   # tuned param 2
PHI0, DELTA0 = 0.70, 0.60                                       # published

BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_IS = ("H1", "H2", "DD", "CAGR")                            # idea 131's IS screen shape
PURE_KINDS = ("ctl", "gate", "stop")   # scale-free instruments: rescaling is a pure exposure change

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 2000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels (idea 131 verbatim)
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
    """SPY's reference numbers on the full sample or inside the IS window."""
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def margins(stat, b, phi, delta):
    """Signed margin on each of 4b's five bars.  > 0 means the bar is cleared."""
    return dict(H1=stat["H1"] - b["s1"], H2=stat["H2"] - b["s2"], OOS=stat["OOS_Sharpe"] - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(stat["MaxDD"]),
                CAGR=stat["CAGR"] - phi * b["scagr"])


def fails(mg, keys):
    return [k for k in keys if mg[k] <= 0]


def pareto_front(df, s="Sharpe", d="MaxDD"):
    S, D = df[s].values, df[d].values
    out = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        if not np.isfinite(S[i]) or not np.isfinite(D[i]):
            out[i] = False
            continue
        dom = (S >= S[i]) & (D >= D[i]) & ((S > S[i]) | (D > D[i]))
        out[i] = not dom.any()
    return out


# ------------------------------------------------------------------ statistics of one series
def stats_of(r, which):
    w = H.window(r, which) if which != "full" else r
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=oos)


# ------------------------------------------------------------------ one (panel, book, cost) cell
def do_cell(pname, px, spy, book, cost, bfull, bIS, v1_net):
    """Every arm x every m.  Returns the long frame and the return series (for the walk-forward)."""
    rows = []
    start = spy.index[0]
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = H.targets(px, book, gate, conv)
        for m_ in MGRID:
            res = H.run(px, W, m=m_, bps=cost, **kw)
            r = res["r"].loc[start:]
            g = res["gross"].loc[start:]
            sf, si = stats_of(r, "full"), stats_of(r, "IS")
            so = metrics(H.window(r, "OOS"))
            mgf = margins(sf, bfull, PHI0, DELTA0)
            mgi = margins(si, bIS, PHI0, DELTA0)
            rows.append(dict(
                panel=pname, book=book, cost=cost, arm=arm, kind=kind, m=m_,
                CAGR=sf["CAGR"], Sharpe=sf["Sharpe"], MaxDD=sf["MaxDD"], H1=sf["H1"], H2=sf["H2"],
                OOS_Sharpe_full=sf["OOS_Sharpe"],
                IS_CAGR=si["CAGR"], IS_Sharpe=si["Sharpe"], IS_MaxDD=si["MaxDD"],
                IS_H1=si["H1"], IS_H2=si["H2"],
                OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"], m_DD=mgf["DD"], m_CAGR=mgf["CAGR"],
                IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
                gross=float(g.mean()), gross_cv=float(g.std() / g.mean()) if g.mean() > 0 else np.nan,
                pass4a=H.pass4a(r, v1_net),
                TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
            ))
    return pd.DataFrame(rows), None


# ------------------------------------------------------------------ verdict machinery
def attach_bars(F, bars_by_panel):
    """Broadcast SPY's reference numbers onto every row so every verdict is vectorised."""
    for key, idx in (("b_s1", "s1"), ("b_s2", "s2"), ("b_soos", "soos"),
                     ("b_sdd", "sdd"), ("b_scagr", "scagr")):
        F[key] = F.panel.map({p: bars_by_panel[p][0][idx] for p in bars_by_panel})
    for key, idx in (("bi_s1", "s1"), ("bi_s2", "s2"), ("bi_sdd", "sdd"), ("bi_scagr", "scagr")):
        F[key] = F.panel.map({p: bars_by_panel[p][1][idx] for p in bars_by_panel})
    F["book_id"] = F.panel + "|" + F.book + "|" + F.cost.astype(str) + "|" + F.arm
    return F


def bar_ok(D, phi, delta, which="full"):
    """Boolean frame, one column per 4b bar, > 0 margin required (idea 131's convention)."""
    if which == "full":
        return pd.DataFrame(dict(
            H1=D.H1 - D.b_s1 > 0, H2=D.H2 - D.b_s2 > 0,
            OOS=D.OOS_Sharpe_full - D.b_soos > 0,
            DD=delta * D.b_sdd.abs() - D.MaxDD.abs() > 0,
            CAGR=D.CAGR - phi * D.b_scagr > 0), index=D.index)
    return pd.DataFrame(dict(
        H1=D.IS_H1 - D.bi_s1 > 0, H2=D.IS_H2 - D.bi_s2 > 0,
        OOS=pd.Series(True, index=D.index),
        DD=delta * D.bi_sdd.abs() - D.IS_MaxDD.abs() > 0,
        CAGR=D.IS_CAGR - phi * D.bi_scagr > 0), index=D.index)


def _verdict_rows(D, phi, delta, bars_by_panel, keys):
    B = bar_ok(D, phi, delta)
    return B[list(keys)].all(axis=1)


def family_verdict(F, phi, delta, bars_by_panel, mmax, drop=None, which="full"):
    """FAMILY-4b: a book passes iff SOME m <= mmax of its own gross family clears every bar."""
    keys = [k for k in (BARS5 if which == "full" else BARS_IS) if k != drop]
    sub = F[F.m <= mmax + 1e-9]
    ok = bar_ok(sub, phi, delta, which)[keys].all(axis=1)
    d = pd.DataFrame(dict(book_id=sub.book_id.values, m=sub.m.values, ok=ok.values))
    g = d.groupby("book_id", sort=False)
    res = pd.DataFrame(dict(passed=g.ok.any(), n_m=g.ok.sum(),
                            m_lo=d[d.ok].groupby("book_id").m.min(),
                            m_hi=d[d.ok].groupby("book_id").m.max())).reindex(
        sub.book_id.drop_duplicates().values)
    res = res.reset_index().rename(columns={"index": "book_id"})
    res["passed"] = res.passed.fillna(False).astype(bool)
    parts = res.book_id.str.split("|", expand=True)
    res["panel"], res["book"], res["cost"], res["arm"] = (
        parts[0], parts[1], parts[2].astype(float), parts[3])
    return res


def main():
    say("=" * 200)
    say("IDEA 144 — is-the-ladder-even-a-candidate.  Convention under test: a STATIC RESCALING "
        "OF A BOOK IS THE SAME BOOK.")
    say(f"corpus = 3 panels x 3 books x 17 arms x 2 costs = 306 BOOKS; gross family = "
        f"{len(MGRID)} points m in [{MGRID[0]}, {MGRID[-1]}] -> {306*len(MGRID)} backtests")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, {GROSS:.0%} target gross at m=1.00, "
        f"costs {COSTS} bps.  Published bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.")
    say("=" * 200)

    FR, V1, SPY, BARS = [], {}, {}, {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        SPY[pname] = spy
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        BARS[pname] = (bfull, bIS)
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
            f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  OOS Sharpe {bfull['soos']:.3f}")
        say(f"    published bars: CAGR floor {PHI0*bfull['scagr']:.2%}/yr   DD cap "
            f"{-DELTA0*abs(bfull['sdd']):.2%}   |   IS SPY: CAGR {bIS['scagr']:.2%} MaxDD {bIS['sdd']:.2%}")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        V1[pname] = v1
        for book in BOOKS:
            for c in COSTS:
                D, _ = do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                FR.append(D)
        say(f"    ... {pname} done ({len(FR)*len(MGRID)*17} rows so far)")

    F = attach_bars(pd.concat(FR, ignore_index=True), BARS)
    bars_full = {p: BARS[p][0] for p in PANELS}
    say(f"\nfull frame: {len(F)} rows = 306 books x {len(MGRID)} m-points")

    # ============================================================ reproduction checks
    say("\n" + "=" * 200)
    say("REPRODUCTION CHECKS (all four must pass before any new number is read)")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    d_ab = float((a - b).abs().max())
    say(f"  (a) H.run vs engine.backtest, ungated EWall u56: max|diff| = {d_ab:.2e} -> "
        f"{'PASS' if d_ab < 1e-12 else 'FAIL'}")

    P = F[F.m == 1.00].copy()
    pub = P[(P.panel == "u56") & (P.book == "EWall") & (P.cost == 10.0) & (P.arm == "vol60-dg")].iloc[0]
    ok_b = abs(pub.CAGR - 0.116) < 5e-4 and abs(pub.Sharpe - 1.133) < 5e-3 and abs(pub.MaxDD + 0.169) < 5e-4
    say(f"  (b) idea 94 published EWall+vol60-dg u56@10bps 11.6%/1.133/-16.9%: got "
        f"{pub.CAGR:.3%}/{pub.Sharpe:.3f}/{pub.MaxDD:.3%} -> {'PASS' if ok_b else 'FAIL'}")

    P = P.reset_index(drop=True)
    P["pareto"] = False
    for k, g in P.groupby(["panel", "book", "cost"], sort=False):
        P.loc[g.index, "pareto"] = pareto_front(g)
    pass_pt, fail_pt = [], []
    for _, row in P.iterrows():
        mg = margins(dict(CAGR=row.CAGR, Sharpe=row.Sharpe, MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                          OOS_Sharpe=row.OOS_Sharpe_full), bars_full[row.panel], PHI0, DELTA0)
        f = fails(mg, BARS5)
        pass_pt.append(len(f) == 0)
        fail_pt.append(",".join(f) or "-")
    P["pass4b"] = pass_pt
    P["fail4b"] = fail_pt
    P["floor_only"] = P.fail4b == "CAGR"
    n306, npar, n4b, nfl = len(P), int(P.pareto.sum()), int(P.pass4b.sum()), int(P.floor_only.sum())

    # idea 131's ladder, rebuilt from the SAME frame (the ungated 'control' arm at 19 m-points)
    LAD = F[(F.arm == "control") & (F.m.isin(LADDER131))].copy()
    lp, lf = [], []
    for _, row in LAD.iterrows():
        mg = margins(dict(CAGR=row.CAGR, Sharpe=row.Sharpe, MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                          OOS_Sharpe=row.OOS_Sharpe_full), bars_full[row.panel], PHI0, DELTA0)
        f = fails(mg, BARS5)
        lp.append(len(f) == 0)
        lf.append(",".join(f) or "-")
    LAD["pass4b"] = lp
    LAD["fail4b"] = lf
    LAD["floor_only"] = LAD.fail4b == "CAGR"
    nlad, nladfl = len(LAD), int(LAD.floor_only.sum())
    mmax_fl = float(LAD.loc[LAD.floor_only, "m"].max()) if nladfl else np.nan
    ok_c = (n306 == 306 and npar == 82 and n4b == 29 and nfl == 27 and nlad == 342
            and nladfl == 97 and mmax_fl <= 0.80 + 1e-9)
    say(f"  (c) idea 131/129 census: rows {n306}/306, Pareto {npar}/82, 4b pass {n4b}/29, "
        f"floor-only {nfl}/27, ladder rows {nlad}/342, ladder floor-only {nladfl}/97 "
        f"(max m = {mmax_fl:.2f} <= 0.80) -> {'PASS' if ok_c else 'FAIL'}")

    def core_is(row):
        return all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD"))
    A = int(sum(core_is(r) and r.IS_m_CAGR > 0 for _, r in P.iterrows()))
    B = int(sum(core_is(r) and r.IS_m_CAGR <= 0 for _, r in P.iterrows()))
    C = 306 - A - B
    say(f"  (d) idea 131 IS-screen groups A/B/C: {A}/{B}/{C}  (published 45/9/252) -> "
        f"{'PASS' if (A, B, C) == (45, 9, 252) else 'FAIL'}")

    # ============================================================ Q1 — is the convention coherent?
    say("\n" + "=" * 200)
    say("Q1 — IS 'THE SAME BOOK' A WELL-DEFINED EQUIVALENCE?  Behaviour along each book's own "
        f"gross family ({F.book_id.nunique()} books x {len(MGRID)} m).")
    say("    A rescale must leave Sharpe alone and move CAGR and |MaxDD| monotonically, or the "
        "convention has no content.")
    q1 = []
    for (pn, bk, c, arm), g in F.groupby(["panel", "book", "cost", "arm"], sort=False):
        g = g.sort_values("m")
        kind = g.kind.iloc[0]
        s = g.Sharpe.values
        q1.append(dict(panel=pn, book=bk, cost=c, arm=arm, kind=kind,
                       sharpe_range=float(np.nanmax(s) - np.nanmin(s)),
                       sharpe_at_1=float(g.loc[g.m == 1.00, "Sharpe"].iloc[0]),
                       cagr_mono=bool(np.all(np.diff(g.CAGR.values) > -1e-12)),
                       dd_mono=bool(np.all(np.diff(np.abs(g.MaxDD.values)) > -1e-12)),
                       cagr_range=float(g.CAGR.max() - g.CAGR.min()),
                       dd_range=float(g.MaxDD.abs().max() - g.MaxDD.abs().min())))
    Q1 = pd.DataFrame(q1)
    say("\n  by arm kind (mean over books in the kind):")
    t = Q1.groupby("kind").agg(n=("arm", "size"), sharpe_range_mean=("sharpe_range", "mean"),
                               sharpe_range_max=("sharpe_range", "max"),
                               cagr_monotone=("cagr_mono", "mean"), dd_monotone=("dd_mono", "mean"))
    say(t.to_string(float_format=lambda x: f"{x:.4f}"))
    NB = len(Q1)
    say(f"\n  CAGR monotone in m: {int(Q1.cagr_mono.sum())}/{NB} books.  "
        f"|MaxDD| monotone in m: {int(Q1.dd_mono.sum())}/{NB}.  "
        f"Sharpe range over the family: median {Q1.sharpe_range.median():.4f}, "
        f"p90 {Q1.sharpe_range.quantile(0.9):.4f}, max {Q1.sharpe_range.max():.4f} "
        f"(vs a cross-book Sharpe sd of {P.Sharpe.std():.3f}).")
    worst = Q1.nlargest(8, "sharpe_range")[["panel", "book", "cost", "arm", "kind", "sharpe_range"]]
    say("\n  PRE-REGISTERED SPLIT (mechanical, from the instrument's units, not from the results):")
    say("    PURE       = kinds ctl/gate/stop — every parameter is scale-free, so scaling the")
    say("                 target weights is a pure exposure change.")
    say("    SCALE-DEP  = kinds dd/bud — the drawdown trigger D and the turnover budget ebud are")
    say("                 ABSOLUTE quantities, so rescaling changes how hard they bite.")
    say(f"    PURE books: CAGR monotone {int(Q1[Q1.kind.isin(PURE_KINDS)].cagr_mono.sum())}/"
        f"{int(Q1.kind.isin(PURE_KINDS).sum())}, |MaxDD| monotone "
        f"{int(Q1[Q1.kind.isin(PURE_KINDS)].dd_mono.sum())}/{int(Q1.kind.isin(PURE_KINDS).sum())}, "
        f"Sharpe range max {Q1[Q1.kind.isin(PURE_KINDS)].sharpe_range.max():.4f}")
    say(f"    SCALE-DEP : CAGR monotone {int(Q1[~Q1.kind.isin(PURE_KINDS)].cagr_mono.sum())}/"
        f"{int((~Q1.kind.isin(PURE_KINDS)).sum())}, |MaxDD| monotone "
        f"{int(Q1[~Q1.kind.isin(PURE_KINDS)].dd_mono.sum())}/{int((~Q1.kind.isin(PURE_KINDS)).sum())}, "
        f"Sharpe range max {Q1[~Q1.kind.isin(PURE_KINDS)].sharpe_range.max():.4f}")
    say("\n  8 largest Sharpe swings along a family (the arms where the rescale is NOT pure):")
    say(worst.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ Q2 — load-bearing, status quo
    say("\n" + "=" * 200)
    say("Q2 — WHICH BARS ARE LOAD-BEARING UNDER THE PUBLISHED (POINT) CONVENTION?")
    say("    load-bearing(bar) = # rows admitted when the bar is DELETED that are not admitted "
        "with all five.  0 => the bar changes no verdict.")

    def lb_table(rows_df, label, keysets, bars_by_panel, phi=PHI0, delta=DELTA0):
        base = _verdict_rows(rows_df, phi, delta, bars_by_panel, BARS5)
        out = [dict(convention=label, bar="(none deleted)", admitted=int(base.sum()),
                    unique_exclusions=0, sole_cause=0)]
        for k in keysets:
            v = _verdict_rows(rows_df, phi, delta, bars_by_panel, tuple(x for x in BARS5 if x != k))
            uniq = int((v & ~base).sum())
            out.append(dict(convention=label, bar=k, admitted=int(v.sum()),
                            unique_exclusions=uniq, sole_cause=uniq))
        return pd.DataFrame(out)

    P_arm = P.copy()
    T_arm = lb_table(P_arm, "POINT-4b, arm corpus only (306)", BARS5, bars_full)
    LADrows = LAD.copy()
    LADrows["OOS_Sharpe_full"] = LADrows["OOS_Sharpe_full"]
    T_both = lb_table(pd.concat([P_arm, LADrows], ignore_index=True),
                      "POINT-4b, arm corpus + ladder (648)", BARS5, bars_full)
    T_lad = lb_table(LADrows, "POINT-4b, ladder only (342)", BARS5, bars_full)
    Q2 = pd.concat([T_arm, T_both, T_lad], ignore_index=True)
    say("\n" + Q2.to_string(index=False))
    say("\n  Read: on the ladder the CAGR floor is the ONLY bar that excludes anything "
        f"({int(T_lad.loc[T_lad.bar=='CAGR','unique_exclusions'].iloc[0])} rows). "
        "That is idea 131's finding restated: the floor exists for the ladder.")

    # ============================================================ Q3 — load-bearing after the fix
    say("\n" + "=" * 200)
    say("Q3 — THE CONSTRUCTION FIX.  Ladder dropped from the corpus; every book judged over its "
        "OWN gross family (FAMILY-4b).")
    q3rows = []
    FAM = {}
    NBOOK = F.book_id.nunique()
    FP = F[F.kind.isin(PURE_KINDS)]
    for mmax in MCEIL:
        base = family_verdict(F, PHI0, DELTA0, BARS, mmax)
        FAM[mmax] = base
        nb = int(base.passed.sum())
        q3rows.append(dict(m_max=mmax, bar="(none deleted)", admitted=nb, unique_exclusions=0))
        for k in BARS5:
            v = family_verdict(F, PHI0, DELTA0, BARS, mmax, drop=k)
            mg = base.merge(v, on="book_id", suffixes=("", "_d"))
            uniq = int((mg.passed_d & ~mg.passed).sum())
            q3rows.append(dict(m_max=mmax, bar=k, admitted=int(v.passed.sum()), unique_exclusions=uniq))
        # same, restricted to the PURE-rescale books, where the convention is exactly defined
        bp = family_verdict(FP, PHI0, DELTA0, BARS, mmax)
        q3rows.append(dict(m_max=mmax, bar="(none deleted) PURE", admitted=int(bp.passed.sum()),
                           unique_exclusions=0))
        for k in BARS5:
            vp = family_verdict(FP, PHI0, DELTA0, BARS, mmax, drop=k)
            mp = bp.merge(vp, on="book_id", suffixes=("", "_d"))
            q3rows.append(dict(m_max=mmax, bar=f"{k} PURE", admitted=int(vp.passed.sum()),
                               unique_exclusions=int((mp.passed_d & ~mp.passed).sum())))
    Q3 = pd.DataFrame(q3rows)
    say("\n" + Q3.to_string(index=False))
    for mmax in MCEIL:
        s = Q3[Q3.m_max == mmax]
        s = s[~s.bar.str.contains("PURE")]
        dead = [r.bar for _, r in s.iterrows() if r.bar != "(none deleted)" and r.unique_exclusions == 0]
        live = [r.bar for _, r in s.iterrows() if r.bar != "(none deleted)" and r.unique_exclusions > 0]
        say(f"\n  m_max={mmax:.2f}: NOT load-bearing {dead or '[]'};  load-bearing {live or '[]'};  "
            f"admitted {int(s.iloc[0].admitted)}/{NBOOK} (POINT-4b admits {n4b}).")

    # joint test: DD and CAGR deleted together
    say("\n  joint deletion (the pair, not the individuals):")
    for mmax in MCEIL:
        base = FAM[mmax]
        sub = F[F.m <= mmax + 1e-9]
        ok = bar_ok(sub, PHI0, DELTA0)[["H1", "H2", "OOS"]].all(axis=1)
        NP = pd.DataFrame(dict(book_id=sub.book_id.values, ok=ok.values)).groupby(
            "book_id", sort=False).ok.any().rename("passed_np").reset_index()
        mg = base.merge(NP, on="book_id")
        say(f"    m_max={mmax:.2f}: Sharpe bars alone admit {int(mg.passed_np.sum())}/{NBOOK}; "
            f"adding the DD+CAGR PAIR removes {int((mg.passed_np & ~mg.passed).sum())} "
            f"-> {int(mg.passed.sum())}.")

    # ============================================================ Q4 — the collapsed bar
    say("\n" + "=" * 200)
    say("Q4 — THE COLLAPSED BAR.  If neither the floor nor the cap is individually load-bearing "
        "but the pair is, they are ONE bar.")
    say("    Closed form: along the family CAGR rises and |MaxDD| rises with m, so the binding "
        "point is m* = the largest admissible m under the DD cap; the pair reduces to")
    say("       CAGR(m*) >= phi x CAGR_SPY   with   |MaxDD(m*)| <= delta x |MaxDD_SPY|")
    say("    and, if the rescale were exactly linear, to the single ratio bar")
    say("       CAGR / |MaxDD|  >=  (phi x CAGR_SPY) / (delta x |MaxDD_SPY|)   [a Calmar bar]")
    q4 = []
    for mmax in MCEIL:
        base = FAM[mmax]
        sub = F[F.m <= mmax + 1e-9]
        recs = []
        for bid, grp in sub.groupby("book_id", sort=False):
            pn, bk, c, arm = bid.split("|")
            c = float(c)
            bb = BARS[pn][0]
            cap = DELTA0 * abs(bb["sdd"])
            ok_dd = grp[grp.MaxDD.abs() <= cap]
            if len(ok_dd) == 0:
                recs.append(dict(book_id=bid, panel=pn, book=bk, cost=c, arm=arm, mstar=np.nan,
                                 pass_star=False, ceiling_binds=False, calmar=np.nan,
                                 calmar_bar=np.nan, pass_calmar=False))
                continue
            star = ok_dd.loc[ok_dd.m.idxmax()]
            mgs = margins(dict(CAGR=star.CAGR, Sharpe=star.Sharpe, MaxDD=star.MaxDD, H1=star.H1,
                               H2=star.H2, OOS_Sharpe=star.OOS_Sharpe_full), bb, PHI0, DELTA0)
            pub_row = grp[grp.m == 1.00].iloc[0]
            cal = pub_row.CAGR / abs(pub_row.MaxDD) if pub_row.MaxDD else np.nan
            cbar = (PHI0 * bb["scagr"]) / (DELTA0 * abs(bb["sdd"]))
            recs.append(dict(book_id=bid, panel=pn, book=bk, cost=c, arm=arm, mstar=float(star.m),
                             pass_star=len(fails(mgs, BARS5)) == 0,
                             ceiling_binds=bool(star.m >= mmax - 1e-9),
                             calmar=cal, calmar_bar=cbar,
                             pass_calmar=bool(cal >= cbar and mgs["H1"] > 0 and mgs["H2"] > 0
                                              and mgs["OOS"] > 0)))
        R = pd.DataFrame(recs)
        mg = base.merge(R, on="book_id")
        agree_star = float((mg.passed == mg.pass_star).mean())
        agree_cal = float((mg.passed == mg.pass_calmar).mean())
        q4.append(dict(m_max=mmax, family_admits=int(mg.passed.sum()),
                       mstar_rule_admits=int(mg.pass_star.sum()), agree_mstar=agree_star,
                       calmar_bar_admits=int(mg.pass_calmar.sum()), agree_calmar=agree_cal,
                       ceiling_binds=int(mg.ceiling_binds.sum()),
                       no_admissible_m=int(mg.mstar.isna().sum())))
        if mmax == 1.30:
            R.to_csv(OUT / f"{STEM}.mstar.csv", index=False)
    Q4 = pd.DataFrame(q4)
    say("\n" + Q4.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  agree_mstar = the m* rule reproduces the exhaustive family verdict (it must, if "
        "Q1's monotonicity holds).")
    say("  agree_calmar = the closed-form single ratio bar reproduces it; the gap is the "
        "non-linearity of compounding plus the m_max ceiling.")

    # ============================================================ Q5 — phi x delta grid
    say("\n" + "=" * 200)
    say("Q5 — ALL 42 GRID POINTS (phi x delta), BOTH CONVENTIONS.  'floor_lb'/'dd_lb' = unique "
        "exclusions of that bar.")
    grid = []
    for phi in PHIS:
        for delta in DELTAS:
            pv = _verdict_rows(P, phi, delta, bars_full, BARS5)
            pv_nf = _verdict_rows(P, phi, delta, bars_full, tuple(k for k in BARS5 if k != "CAGR"))
            pv_nd = _verdict_rows(P, phi, delta, bars_full, tuple(k for k in BARS5 if k != "DD"))
            row = dict(phi=phi, delta=delta, point_admits=int(pv.sum()),
                       point_floor_lb=int((pv_nf & ~pv).sum()), point_dd_lb=int((pv_nd & ~pv).sum()))
            for mmax in MCEIL:
                fv = family_verdict(F, phi, delta, BARS, mmax)
                fv_nf = family_verdict(F, phi, delta, BARS, mmax, drop="CAGR")
                fv_nd = family_verdict(F, phi, delta, BARS, mmax, drop="DD")
                m1 = fv.merge(fv_nf, on="book_id", suffixes=("", "_nf"))
                m2 = fv.merge(fv_nd, on="book_id", suffixes=("", "_nd"))
                tag = f"fam{int(mmax*100)}"
                row[f"{tag}_admits"] = int(fv.passed.sum())
                row[f"{tag}_floor_lb"] = int((m1.passed_nf & ~m1.passed).sum())
                row[f"{tag}_dd_lb"] = int((m2.passed_nd & ~m2.passed).sum())
            grid.append(row)
    G = pd.DataFrame(grid)
    say("\n" + G.to_string(index=False))
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n  points where the CAGR floor is load-bearing:  POINT "
        f"{int((G.point_floor_lb>0).sum())}/42,  FAMILY(m<=1.00) {int((G.fam100_floor_lb>0).sum())}/42,  "
        f"FAMILY(m<=1.30) {int((G.fam130_floor_lb>0).sum())}/42")
    say(f"  points where the DD cap is load-bearing:      POINT "
        f"{int((G.point_dd_lb>0).sum())}/42,  FAMILY(m<=1.00) {int((G.fam100_dd_lb>0).sum())}/42,  "
        f"FAMILY(m<=1.30) {int((G.fam130_dd_lb>0).sum())}/42")

    # ============================================================ Q6 — rule 8 walk-forward
    say("\n" + "=" * 200)
    say("Q6 — RULE 8 WALK-FORWARD.  Screens read 2009-2016 ONLY; the pick is read once on "
        "2017-2026.  18 cells.")
    say("    S0 no screen (argmax IS Sharpe, m=1.00)          S1 IS POINT-4b, published")
    say("    S2 IS POINT-4b minus the CAGR floor              S3 IS FAMILY-4b (screen picks m too)")
    say("    S4 IS FAMILY-4b minus the CAGR floor             S5 IS FAMILY-4b minus the DD cap")
    say("    S6 IS Calmar bar (the Q4 closed form) + Sharpe bars")
    wf = []
    for pname in PANELS:
        bIS = BARS[pname][1]
        spy = SPY[pname]
        for book in BOOKS:
            for c in COSTS:
                sub = F[(F.panel == pname) & (F.book == book) & (F.cost == c)].copy()
                oosm = {(r.arm, round(r.m, 2)): (r.OOS_CAGR, r.OOS_Sharpe, r.OOS_MaxDD)
                        for _, r in sub.iterrows()}
                at1 = sub[sub.m == 1.00]
                cap_is = DELTA0 * abs(bIS["sdd"])
                floor_is = PHI0 * bIS["scagr"]
                cal_bar = floor_is / cap_is

                def is_core(r):
                    return r.IS_m_H1 > 0 and r.IS_m_H2 > 0 and r.IS_m_DD > 0

                cands = {}
                cands["S0"] = [(r.arm, 1.00, r.IS_Sharpe) for _, r in at1.iterrows()]
                cands["S1"] = [(r.arm, 1.00, r.IS_Sharpe) for _, r in at1.iterrows()
                               if is_core(r) and r.IS_m_CAGR > 0]
                cands["S2"] = [(r.arm, 1.00, r.IS_Sharpe) for _, r in at1.iterrows() if is_core(r)]
                # family selectors: admissible (arm, m) pairs on the IS window, m <= 1.30
                fam_ok, fam_nf, fam_nd = [], [], []
                for _, r in sub.iterrows():
                    core = r.IS_m_H1 > 0 and r.IS_m_H2 > 0
                    dd_ok = r.IS_m_DD > 0
                    cg_ok = r.IS_m_CAGR > 0
                    if core and dd_ok and cg_ok:
                        fam_ok.append((r.arm, r.m, r.IS_Sharpe, r.IS_CAGR))
                    if core and dd_ok:
                        fam_nf.append((r.arm, r.m, r.IS_Sharpe, r.IS_CAGR))
                    if core and cg_ok:
                        fam_nd.append((r.arm, r.m, r.IS_Sharpe, r.IS_CAGR))

                def pick_family(pairs, mrule):
                    """arm by argmax IS Sharpe (gross-near-invariant), then m by a stated rule."""
                    if not pairs:
                        return None
                    best_arm = max(pairs, key=lambda t: t[2])[0]
                    ms = [t[1] for t in pairs if t[0] == best_arm]
                    return (best_arm, max(ms) if mrule == "hi" else min(ms))

                cands["S3"] = pick_family(fam_ok, "hi")
                cands["S4"] = pick_family(fam_nf, "hi")
                cands["S5"] = pick_family(fam_nd, "lo")
                cal_pairs = []
                for _, r in at1.iterrows():
                    cal = r.IS_CAGR / abs(r.IS_MaxDD) if r.IS_MaxDD else np.nan
                    if r.IS_m_H1 > 0 and r.IS_m_H2 > 0 and np.isfinite(cal) and cal >= cal_bar:
                        cal_pairs.append((r.arm, 1.00, r.IS_Sharpe, r.IS_CAGR))
                if cal_pairs:
                    ba = max(cal_pairs, key=lambda t: t[2])[0]
                    g = sub[(sub.arm == ba) & (sub.IS_m_DD > 0)]
                    cands["S6"] = (ba, float(g.m.max()) if len(g) else 1.00)
                else:
                    cands["S6"] = None

                mv = metrics(H.window(V1[pname][c], "OOS"))
                ms = metrics(spy.loc[OOS_START:])
                mc = dict(zip(("CAGR", "Sharpe", "MaxDD"), oosm[("control", 1.00)]))
                for s in ["S0", "S1", "S2", "S3", "S4", "S5", "S6"]:
                    cd = cands[s]
                    base = dict(sel=s, panel=pname, book=book, cost=c,
                                spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_CAGR=ms["CAGR"],
                                spy_OOS_MaxDD=ms["MaxDD"], v1_OOS_Sharpe=mv["Sharpe"],
                                v1_OOS_CAGR=mv["CAGR"], v1_OOS_MaxDD=mv["MaxDD"],
                                ctl_OOS_Sharpe=mc["Sharpe"])
                    if s in ("S0", "S1", "S2"):
                        if not cd:
                            wf.append(dict(base, pick="(none)", m=np.nan, OOS_CAGR=np.nan,
                                           OOS_Sharpe=np.nan, OOS_MaxDD=np.nan))
                            continue
                        arm, m_, _ = max(cd, key=lambda t: t[2])
                    else:
                        if cd is None:
                            wf.append(dict(base, pick="(none)", m=np.nan, OOS_CAGR=np.nan,
                                           OOS_Sharpe=np.nan, OOS_MaxDD=np.nan))
                            continue
                        arm, m_ = cd
                    oc, osh, odd = oosm[(arm, round(m_, 2))]
                    wf.append(dict(base, pick=arm, m=m_, OOS_CAGR=oc, OOS_Sharpe=osh,
                                   OOS_MaxDD=odd))
    WF = pd.DataFrame(wf)
    WF["beat_spy"] = WF.OOS_Sharpe > WF.spy_OOS_Sharpe
    WF["beat_v1"] = WF.OOS_Sharpe > WF.v1_OOS_Sharpe
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    def wagg(D):
        return D.groupby("sel").agg(cells=("pick", lambda s: int((s != "(none)").sum())),
                                    OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                                    OOS_MaxDD=("OOS_MaxDD", "mean"),
                                    beat_SPY=("beat_spy", "sum"), beat_v1=("beat_v1", "sum"))
    say("\n  ALL CELLS (a selector with fewer cells is abstaining, not losing):")
    say(wagg(WF).to_string(float_format=lambda x: f"{x:.3f}"))
    cellkey = ["panel", "book", "cost"]
    full = WF[WF.pick != "(none)"].groupby(cellkey).size()
    paired = set(full[full == 7].index)
    PW = WF[WF.set_index(cellkey).index.isin(paired)]
    say(f"\n  PAIRED on the {len(paired)} cells where all 7 selectors enter:")
    if len(paired):
        say(wagg(PW).to_string(float_format=lambda x: f"{x:.3f}"))
    ref = WF.drop_duplicates(cellkey)
    say(f"\n  reference OOS over the 18 cells: SPY Sharpe {ref.spy_OOS_Sharpe.mean():.3f} "
        f"CAGR {ref.spy_OOS_CAGR.mean():.2%} MaxDD {ref.spy_OOS_MaxDD.mean():.2%} | "
        f"RULES v1 Sharpe {ref.v1_OOS_Sharpe.mean():.3f} CAGR {ref.v1_OOS_CAGR.mean():.2%} "
        f"MaxDD {ref.v1_OOS_MaxDD.mean():.2%}")
    moved = []
    for k, d in WF.groupby(cellkey):
        p = {r.sel: (r.pick, r.m) for _, r in d.iterrows()}
        moved.append(dict(panel=k[0], book=k[1], cost=k[2],
                          **{f"{s}": f"{p[s][0]}@{p[s][1]:.2f}" if p[s][0] != "(none)" else "-"
                             for s in ["S0", "S1", "S2", "S3", "S4", "S5", "S6"]}))
    MV = pd.DataFrame(moved)
    say("\n  picks per cell (arm@m):")
    say(MV.to_string(index=False))
    for s in ["S1", "S2", "S3", "S4", "S5", "S6"]:
        n = int(sum(1 for _, r in MV.iterrows() if r[s] != "-" and r[s] != r["S0"]))
        say(f"    {s}: {n}/{len(MV)} cells where the pick differs from S0")

    # ============================================================ both KEEP paths
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS, all 306 books")
    n4a_pt = int(P.pass4a.sum())
    fam130 = FAM[1.30]
    p4a_fam = []
    for _, row in fam130.iterrows():
        g = F[(F.panel == row.panel) & (F.book == row.book) & (F.cost == row.cost)
              & (F.arm == row.arm) & (F.m <= 1.30 + 1e-9)]
        p4a_fam.append(bool(g.pass4a.any()))
    fam130 = fam130.assign(pass4a_family=p4a_fam)
    say(f"  4a: POINT {n4a_pt}/{NBOOK}; FAMILY (some m in the book's own family passes 4a) "
        f"{int(fam130.pass4a_family.sum())}/{NBOOK}")
    say(f"  4b: POINT {n4b}/{NBOOK}; FAMILY m<=1.00 {int(FAM[1.00].passed.sum())}/{NBOOK}; "
        f"FAMILY m<=1.30 {int(FAM[1.30].passed.sum())}/{NBOOK}")
    say(f"  BOTH paths: POINT {int((P.pass4a & P.pass4b).sum())}/{NBOOK}; "
        f"FAMILY {int((fam130.passed & fam130.pass4a_family).sum())}/{NBOOK}")
    say("  NO NEW BOOK IS PROPOSED.  This run re-scores an existing corpus under an alternative "
        "CONSTRUCTION convention, which is the thing being adjudicated.")

    # ============================================================ outputs
    P.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    Q1.to_csv(OUT / f"{STEM}.family_shape.csv", index=False)
    Q2.to_csv(OUT / f"{STEM}.loadbearing_point.csv", index=False)
    Q3.to_csv(OUT / f"{STEM}.loadbearing_family.csv", index=False)
    Q4.to_csv(OUT / f"{STEM}.collapse.csv", index=False)
    MV.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    F.to_csv(OUT / f"{STEM}.family.csv.gz", index=False, compression="gzip")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say("\nwrote: .corpus.csv .family_shape.csv .loadbearing_point.csv .loadbearing_family.csv "
        ".collapse.csv .mstar.csv .grid.csv .walkforward.csv .picks.csv .family.csv.gz .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
