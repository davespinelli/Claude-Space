#!/usr/bin/env python3
"""QUEUE idea 149 — quote-the-lift-not-the-rate  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 149)
    "idea 141 found the raw screen-robustness RATE is non-monotone in screen tightness purely
     because conditioning on a non-empty admissible set selects looser draws (K_Sharpe 0.789 ->
     0.674 -> 0.634 -> 0.652), while the LIFT over the size-matched null E[k/n | k>0] is
     monotone for all six informative selectors.  Test whether the same conditioning artifact
     inflates the other pass-rate statistics this project quotes (idea 90's cell count, idea
     129's POINT census), by re-reading each against its own size-matched null.  Max 2 params."

WHAT IS ACTUALLY BEING TESTED.  Idea 141's finding was about ONE statistic (is the unscreened
    argmax admissible?) under RANDOMISED bars.  Two things could generalise, and they are
    different claims which this run separates:

      (I)  THE CONDITIONING ARTIFACT.  A pass-rate quoted over a denominator that has itself
           been conditioned on non-emptiness is inflated.  This project does that in the open:
           idea 90's headline "the operational KEEP admits 4 of 51 (book, arm) pairs" is a count
           over FOUR large-cap cells, the two small-panel cells having been dropped precisely
           because nothing passes in them.  If (I) generalises, that 4/51 is partly an artifact
           of which cells were kept.
      (II) RAW vs LIFT.  Even with the conditioning made explicit, a raw pass rate confounds
           "this object is special" with "the screen was loose".  The fix idea 141 proposed is
           to quote the LIFT over the size-matched null: the same statistic recomputed when each
           cell's passing set is replaced by a UNIFORMLY RANDOM subset OF THE SAME SIZE.

    Both are asked of the two statistics the queue names, at PROTOCOL's own published bars
    (where the project quotes them) and again across the tightness sweep idea 141 used.

    A LIFT here is additive, immunity - null, exactly as idea 141 defined it, so the two files'
    numbers are directly comparable.  Ratios are also printed where the null is not near zero.

CORPUS — idea 94's, re-derived rather than read
    3 panels (u56 / broad / small) x 3 books (V1u, TOP20, EWall) x 2 cost rungs (10, 25 bps)
    = 18 cells x 17 arms = 306 books = 306 backtests, weekly, t+1, no leverage.
    The 25-point static-gross FAMILY that idea 90's interval statistic is defined on (7,650
    rows) is READ from idea 90's committed `.family.csv.gz` rather than re-derived, and check
    [d] asserts that this run's own 306 re-derived rows equal that file's m = 1.00 slice to
    < 1e-9 before any interval number is read.  That is stated here rather than buried: the
    interval section inherits idea 90's family, the point section does not.

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL grid points reported:
    1. screen tightness qmax in {0.25, 0.50, 0.75, 1.00} — idea 141's dial, unchanged.  Each
       bar is drawn at a quantile q ~ U(0, qmax) of that cell's own 17 arm values of the
       statistic the bar is written on, so the screen keeps 4b's SHAPE and loses its
       calibration.
    2. conditioning convention in {COND, UNCOND} — COND is the project's own (a cell or draw
       that admits nothing is dropped from the denominator), UNCOND counts it as a non-pass.
    4 x 2 = 8 grid points per statistic, every one printed.  The statistic axis (three of them),
    the panels, books, cost rungs, arms and the OOS window are REPORTED axes, never selected on.

STATISTICS RE-READ (three, the first as the anchor)
    A. idea 141's immunity          P(unscreened argmax is admissible), the anchor.  Re-derived
                                    with this run's own draws; agreement with idea 141's
                                    committed .immunity.csv is a Monte-Carlo agreement, not an
                                    identity, and is reported as such.
    B. idea 129's POINT census      two readings, both quoted by the project:
                                    B1  the best arm's CROSS-CELL pass count (how often the
                                        distinguished arm clears 4b across cells)
                                    B2  the FLOOR-ONLY share of KILLs (published 27 of 277),
                                        against a null that preserves each bar's marginal
                                        failure count per cell and randomises WHICH arms fail.
    C. idea 90's cell count         per (book, arm) pair, the number of cells whose 4b-passing
                                    gross interval is non-empty; the project's operational KEEP
                                    is "non-empty in all four large-cap cells", published as
                                    4 of 51.

CONTROLS
    SIZE-NULL   for A, E[k/n | k>0] analytically; for B and C, Monte-Carlo over size-matched
                random subsets (each cell independently, uniform, EXACTLY k_c members).
    RANDOM      a distinguished object with no information (a random arm / random pair).  Its
                statistic IS the null; if it does not land on the null the null is mis-specified
                and every lift in this file is suspect.

WALK-FORWARD (PROTOCOL rule 8) — every selector reads the IS window (through 2016-12-31) ONLY;
    each pick is read ONCE on 2017-01-01..2026 and reported as OOS CAGR / Sharpe / MaxDD against
    that cell's ungated control, RULES v1 (the live book) and SPY.  Both KEEP paths (4a and 4b)
    are evaluated on every distinct picked arm, on the full sample and on the OOS window alone.
    The decision under test is the one this idea bears on: if a raw cross-cell pass count is an
    inflated statistic, does DEBIASING it by its size-matched null change which arm you hold,
    and is the change worth anything out of sample?
        S0 CONTROL   hold the cell's ungated `control` arm (do nothing)
        S1 SHARPE    argmax IS Sharpe                         (the incumbent, rule 8's own)
        S2 RAW       argmax cross-cell RAW IS-4b pass count    (the inflated statistic)
        S3 LIFT      argmax cross-cell pass count MINUS its size-matched expectation
        S4 RANDOM    a random admissible arm                   (control)

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P0  Reproduction: engine equivalence exact; 306 rows equal idea 141's grid to < 1e-9; idea
        129's POINT census comes back 306 / 29 / 27; idea 90's interval census comes back
        72 / 58 / 29 and 4 of 51 pairs.
    P1  (I) generalises: idea 90's 4-of-51 is inflated by cell-dropping — the same operational
        KEEP read over ALL SIX cells admits strictly fewer pairs, and the ratio is >= 2x.
    P2  (II) generalises: across the tightness sweep the RAW rate of B1 and of C is
        NON-monotone in qmax while the LIFT is monotone (the exact signature idea 141 found).
    P3  The published-bar statistics survive their nulls: at PROTOCOL's own bars both B and C
        have LIFT > 0 with a Monte-Carlo p < 0.05, i.e. they are not pure conditioning
        artifacts even though they are inflated.
    P4  Control: the RANDOM distinguished object's statistic is within 0.05 of the size-matched
        null for every statistic at every qmax.
    P5  The walk-forward is inert in the way ideas 132/141 found: S2 and S3 pick the same arm in
        a majority of cells, and no selector beats S0 by more than 0.05 of OOS Sharpe.

CAVEATS carried, not buried
    * Survivorship: all three panels are current constituents (idea 54); the small panel drops
      the 44 tickers with max_1d_move >= 1.0 and its SPY is a held-out benchmark, not a
      constituent.  Every CAGR here is optimistic; no level in this file is an achievable return.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so an IS
      drawdown bar is measured on a window that cannot express a deep drawdown.  This biases
      every selector in the walk-forward identically.
    * Idea 38: the price cache is on a calendar-day index.
    * Idea 126: every row is quoted at t+1 execution only.
    * This run selects among EXISTING arms.  It cannot promote a book and does not try to.  Its
      output is a statement about how this project QUOTES pass rates, not a candidate.
    * The randomised bars are drawn from each cell's own cross-arm distribution.  That is what
      makes tightness comparable across cells; it also means the bars are not SPY-relative, so
      the sweep measures the screen's SHAPE, not 4b's economic content.
    * Section C inherits idea 90's family file (see check [d]); if [d] fails, nothing in C is
      trustworthy and the script says so.

HARNESS
    Idea 94's script (H.run, H.targets, H.arm_specs, H.halves, H.window, H.pass4a), idea 129's
    screen machinery (C129.panel, C129.bars_win, C129.margins_at, C129.fails) and idea 90's
    interval machinery (I90.intervals, I90.bar_ok, I90.attach_bars) are IMPORTED, so the
    statistics under test are computed by literally the code that produced them.

Deterministic (seeded), standalone.  Writes .console.txt, .grid.csv, .anchor.csv,
.published.csv, .sweep.csv and .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402,F401
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_quote-the-lift-not-the-rate_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I90 = OUT / "2026-09-05_gross-interval-as-a-pre-registered-KEEP-bar_B.py"
I141_GRID = OUT / "2026-09-05_is-Calmar-immunity-general_C.grid.csv"
I141_IMM = OUT / "2026-09-05_is-Calmar-immunity-general_C.immunity.csv"
I90_FAMILY = OUT / "2026-09-05_gross-interval-as-a-pre-registered-KEEP-bar_B.family.csv.gz"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C129 = _load(I129, "i129")
I90M = _load(I90, "i90")

FREQ, COSTS, BOOKS = H.FREQ, [10.0, 25.0], H.BOOKS
IS_END, OOS_START = H.IS_END, H.OOS_START
PANELS = ["u56", "broad", "small"]
PHI0, DELTA0 = 0.70, 0.60

QMAXES = [0.25, 0.50, 0.75, 1.00]          # tuned parameter 1
CONVS = ["COND", "UNCOND"]                 # tuned parameter 2
NDRAW = 4000                               # bar draws per (cell, qmax); idea 141's count
NPERM = 20000                              # size-matched null draws at the published bars
SEED = 20260905

LARGE_CELLS = [("u56", 10.0), ("u56", 25.0), ("broad", 10.0), ("broad", 25.0)]
ALL_CELLS = [(p, c) for p in PANELS for c in COSTS]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


# ------------------------------------------------------------------ corpus (idea 141's build)
def build():
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full, desc = C129.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C129.bars_win(spy, "full"), C129.bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, spy=ms, spy_oos=mso, v1=v1, start=start, desc=desc)
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, {px.index[0].date()}.."
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")

        worst = 0.0
        for b in BOOKS:
            W = H.targets(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a] engine-equivalence, 3 ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in BOOKS:
            for c in COSTS:
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = H.targets(px, b, gate, conv)
                    res = H.run(px, W, bps=c, **kw)
                    r = res["r"].loc[start:]
                    rets[(pk, b, c, arm)] = r
                    mm, mo = metrics(r), metrics(H.window(r, "OOS"))
                    ris = H.window(r, "IS")
                    mi = metrics(ris)
                    ih1, ih2 = H.halves(ris)
                    h1, h2 = H.halves(r)
                    mg = C129.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C129.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    rows.append(dict(
                        panel=pk, book=b, cost=c, arm=arm, kind=kind,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=calmar(mi["CAGR"], mi["MaxDD"]),
                        IS_Sortino=mi["Sortino"], IS_H1=ih1, IS_H2=ih2,
                        IS_MinHalf=min(ih1, ih2), IS_NegVol=-mi["Vol"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"],
                        IS_m_CAGR=ismg["CAGR"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                        m_CAGR=mg["CAGR"],
                        pass4b=(len(C129.fails(mg)) == 0), fail4b=",".join(C129.fails(mg)) or "-",
                        pass4a=H.pass4a(r, v1[c])))
    return pd.DataFrame(rows), rets, ref


# ------------------------------------------------------------------ size-matched null helpers
def null_all_cells(ks, n, npairs, nperm, rng):
    """Monte-Carlo: for `npairs` objects and cells with pass-counts `ks` out of `n`, draw
    independent uniform size-matched passing sets and return the distribution of the number of
    objects that pass in EVERY cell."""
    out = np.zeros(nperm, dtype=int)
    for i in range(nperm):
        hit = np.ones(npairs, dtype=bool)
        for k in ks:
            if k <= 0:
                hit[:] = False
                break
            sel = np.zeros(npairs, dtype=bool)
            sel[rng.choice(npairs, size=min(k, npairs), replace=False)] = True
            hit &= sel
        out[i] = int(hit.sum())
    return out


def mc_p(obs, dist):
    """One-sided Monte-Carlo p-value: P(null >= observed), with the +1/+1 correction."""
    return float((1 + int((np.asarray(dist) >= obs).sum())) / (1 + len(dist)))


def main():
    say("=" * 200)
    say(f"IDEA 149 — quote-the-lift-not-the-rate   ({STEM})")
    say("Are the OTHER pass-rate statistics this project quotes inflated by conditioning, and "
        "do they survive their own size-matched null?")
    say("=" * 200)

    df, rets, ref = build()
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)      # PROTOCOL 4b's own IS screen
    df["cell"] = df.panel + "@" + df.cost.astype(int).astype(str)
    df["pair"] = df.book + "|" + df.arm
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    rng = np.random.default_rng(SEED)
    ok = {}

    # ---------------- [b] reproduction of idea 141's corpus
    g141 = pd.read_csv(I141_GRID)
    j = df.merge(g141, on=["panel", "book", "cost", "arm"], suffixes=("", "_141"))
    keys = [k for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_Calmar",
                        "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross",
                        "IS_H1", "IS_H2") if f"{k}_141" in j.columns]
    d = {k: float((j[k] - j[f"{k}_141"]).abs().max()) for k in keys}
    nadm = int((j.adm_S1 != j.adm_S1_141).sum()) if "adm_S1_141" in j.columns else -1
    ok["b"] = (len(j) == len(df) == 306) and max(d.values()) < 1e-9 and nadm == 0
    say(f"\n[b] reproduction of idea 141's grid: {len(j)} of {len(df)} rows matched, "
        + " ".join(f"{k} {v:.2e}" for k, v in d.items())
        + f", adm_S1 disagreements {nadm}  -> {'EXACT' if ok['b'] else 'NOT EXACT — unsafe'}")

    # ---------------- [c] reproduction of idea 129's POINT census
    n_rows, n_pass = len(df), int(df.pass4b.sum())
    floor_only = int((df.fail4b == "CAGR").sum())
    ok["c"] = (n_rows == 306 and n_pass == 29 and floor_only == 27)
    say(f"[c] idea 129's POINT census at m=1.00 (published 306 rows / 29 pass 4b / 27 floor-only"
        f" KILL): {n_rows} / {n_pass} / {floor_only}  -> "
        f"{'REPRODUCED EXACTLY' if ok['c'] else 'DOES NOT REPRODUCE — unsafe'}")

    # ---------------- [d] idea 90's family, and this run's own rows inside it
    F = pd.read_csv(I90_FAMILY)
    F["cell"] = F.panel + "@" + F.cost.astype(int).astype(str)
    f1 = F[np.isclose(F.m, 1.00)].merge(df, on=["panel", "book", "cost", "arm"],
                                        suffixes=("_90", ""))
    dd = {k: float((f1[k] - f1[f"{k}_90"]).abs().max())
          for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
                    "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}
    okd1 = len(f1) == 306 and max(dd.values()) < 1e-6
    # idea 90's family file already carries its own bar columns (b_*, bi_*, bo_*); use them.
    IV130 = I90M.intervals(F, "full", 1.30)
    IV100 = I90M.intervals(F, "full", 1.00)
    fam130, fam100 = int(IV130.passed.sum()), int(IV100.passed.sum())
    ok["d"] = okd1 and fam130 == 72 and fam100 == 58 and n_pass == 29
    say(f"[d] idea 90's family ({len(F)} rows) — this run's 306 re-derived rows vs its m=1.00 "
        f"slice: {len(f1)} matched, max|diff| {max(dd.values()):.2e} "
        f"({'OK' if okd1 else 'MISMATCH'}); published census FAMILY-4b 72 (m<=1.30) / 58 "
        f"(m<=1.00) / POINT-4b 29: {fam130} / {fam100} / {n_pass}  -> "
        f"{'REPRODUCED EXACTLY' if ok['d'] else 'DOES NOT REPRODUCE — section C unsafe'}")

    if not all(ok.values()):
        say("\n[STOP] a pre-check failed; nothing below is trustworthy.")

    # =============================================================== A. the anchor
    say("\n" + "=" * 200)
    say("A. ANCHOR — idea 141's immunity statistic, re-derived with this run's own draws")
    say("=" * 200)
    imm141 = pd.read_csv(I141_IMM)
    cellkeys = sorted({(p, b, c) for p, b, c in zip(df.panel, df.book, df.cost)})
    SEL = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar", "K_CAGR": "IS_CAGR",
           "K_MaxDD": "IS_MaxDD"}

    # pre-compute the randomised-bar admissibility tensors once; every section below reads them
    ADM = {}            # (qmax, cell) -> boolean (NDRAW, n_arms), plus the arm order
    for qmax in QMAXES:
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)].reset_index(drop=True)
            h1, h2 = s.IS_H1.values, s.IS_H2.values
            addv, cg = np.abs(s.IS_MaxDD.values), s.IS_CAGR.values
            q = rng.uniform(0.0, qmax, size=(NDRAW, 4))
            b1, b2 = np.quantile(h1, q[:, 0]), np.quantile(h2, q[:, 1])
            bdd, bc = np.quantile(addv, 1.0 - q[:, 2]), np.quantile(cg, q[:, 3])
            ADM[(qmax, pk, b, c)] = (
                (h1[None, :] > b1[:, None]) & (h2[None, :] > b2[:, None])
                & (addv[None, :] < bdd[:, None]) & (cg[None, :] > bc[:, None]))

    arows = []
    for qmax in QMAXES:
        num = {k: 0 for k in SEL}
        num["K_RANDOM"] = 0
        den, ksum, nne = 0, 0.0, 0
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)].reset_index(drop=True)
            adm = ADM[(qmax, pk, b, c)]
            n = adm.shape[1]
            k = adm.sum(1)
            ne = k > 0
            nne += int(ne.sum())
            den += NDRAW
            ksum += float(k[ne].sum())
            for sel, col in SEL.items():
                v = np.nan_to_num(s[col].values.astype(float), nan=-np.inf)
                amx = int(np.argmax(v))
                num[sel] += int((adm[:, amx] & ne).sum())
            rnd = rng.integers(0, n, size=NDRAW)
            num["K_RANDOM"] += int((adm[np.arange(NDRAW), rnd] & ne).sum())
        nullv = ksum / max(nne, 1) / 17.0
        for sel in list(SEL) + ["K_RANDOM"]:
            raw = num[sel] / max(nne, 1)
            pub = imm141[(imm141.sel == sel) & (np.isclose(imm141.qmax, qmax))]
            arows.append(dict(stat="A_immunity", sel=sel, qmax=qmax, raw=raw, null=nullv,
                              lift=raw - nullv, p_nonempty=nne / den,
                              pub_raw=float(pub.immunity.iloc[0]) if len(pub) else np.nan,
                              pub_lift=float(pub.lift.iloc[0]) if len(pub) else np.nan))
    A = pd.DataFrame(arows)
    A["d_raw"] = (A.raw - A.pub_raw).abs()
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mcerr = float(A.d_raw.max())
    ok["A"] = mcerr < 0.02
    say(f"\n[A] max |this run - idea 141| on the immunity rate = {mcerr:.4f} over "
        f"{len(A)} points (independent draws, so this is Monte-Carlo agreement, not identity; "
        f"bar 0.02) -> {'AGREES' if ok['A'] else 'DISAGREES — the anchor did not re-derive'}")
    ksh = A[A.sel == "K_Sharpe"].sort_values("qmax")
    say(f"    anchor signature, K_Sharpe: raw {' -> '.join(f'{x:.3f}' for x in ksh.raw)}"
        f"  |  lift {' -> '.join(f'{x:.3f}' for x in ksh.lift)}")

    # =============================================================== B. the POINT census
    say("\n" + "=" * 200)
    say("B. idea 129's POINT CENSUS, re-read against its own size-matched null (published bars)")
    say("=" * 200)
    npairs = df.pair.nunique()
    per_cell = (df.groupby(["panel", "cost"]).pass4b.sum().astype(int)
                .reindex(pd.MultiIndex.from_tuples(ALL_CELLS, names=["panel", "cost"]))
                .fillna(0).astype(int))
    say(f"    passing arms per cell (out of 17): "
        + "  ".join(f"{p}@{int(c)} {v}" for (p, c), v in per_cell.items()))

    # B1 — the best (book, arm) pair's cross-cell pass count, vs a size-matched null
    df["_p4b"] = df.pass4b.astype(int)
    piv = df.pivot_table(index="pair", columns="cell", values="_p4b", aggfunc="first")
    brows = []
    for conv in CONVS:
        for cellset, label in ((LARGE_CELLS, "large4"), (ALL_CELLS, "all6")):
            cols = [f"{p}@{int(c)}" for p, c in cellset]
            # a cell here is (panel, cost): 3 books x 17 arms = 51 (book, arm) pairs
            kc = [int(df[(df.panel == p) & (df.cost == c)].pass4b.sum()) for p, c in cellset]
            use = [i for i, k in enumerate(kc) if k > 0] if conv == "COND" else list(range(len(kc)))
            if not use:
                brows.append(dict(stat="B1_cellcount", conv=conv, cellset=label, n_cells=0,
                                  obs_bestcount=0, exp_bestcount_null=0.0, obs_pass_all=0,
                                  null_pass_all=0.0, lift_pass_all=0.0, ratio=np.nan,
                                  p_mc=np.nan, kc=",".join(map(str, kc))))
                continue
            ucols, uk = [cols[i] for i in use], [kc[i] for i in use]
            cnt = piv[ucols].sum(axis=1)
            obs_best = int(cnt.max())
            obs_all = int((cnt == len(ucols)).sum())
            dist = null_all_cells(uk, npairs, npairs, NPERM, rng)
            exp_cnt = sum(k / npairs for k in uk)
            nul_all = npairs * float(np.prod([k / npairs for k in uk]))
            brows.append(dict(stat="B1_cellcount", conv=conv, cellset=label,
                              n_cells=len(ucols), obs_bestcount=obs_best,
                              exp_bestcount_null=exp_cnt, obs_pass_all=obs_all,
                              null_pass_all=nul_all, lift_pass_all=obs_all - nul_all,
                              ratio=(obs_all / nul_all) if nul_all > 1e-12 else np.inf,
                              p_mc=mc_p(obs_all, dist), kc=",".join(map(str, kc))))
    B1 = pd.DataFrame(brows)
    say("\n  B1 — how many of the 51 (book, arm) pairs pass 4b in EVERY cell of the set:")
    say(B1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # B2 — the floor-only share of KILLs, vs a null preserving each bar's marginal failures
    kills = df[~df.pass4b]
    BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
    failmat = pd.DataFrame({b: (df[f"m_{b}"] <= 0).values for b in BARS5}, index=df.index)
    obs_floor_only = int(((failmat.CAGR) & (~failmat[["H1", "H2", "OOS", "DD"]].any(axis=1))).sum())
    obs_share = obs_floor_only / max(len(kills), 1)
    fo = np.zeros(NPERM, dtype=int)
    cell_idx = [df.index[(df.panel == p) & (df.book == b) & (df.cost == c)].to_numpy()
                for (p, b, c) in cellkeys]
    fm = {b: failmat[b].values for b in BARS5}
    for i in range(NPERM):
        perm = {b: np.zeros(len(df), dtype=bool) for b in BARS5}
        for idx in cell_idx:
            for b in BARS5:
                v = fm[b][idx]
                perm[b][idx] = rng.permutation(v)
        other = perm["H1"] | perm["H2"] | perm["OOS"] | perm["DD"]
        fo[i] = int((perm["CAGR"] & ~other).sum())
    B2 = pd.DataFrame([dict(stat="B2_flooronly", obs=obs_floor_only, n_kills=len(kills),
                            obs_share=obs_share, null_mean=float(fo.mean()),
                            null_share=float(fo.mean()) / max(len(kills), 1),
                            lift=obs_floor_only - float(fo.mean()),
                            ratio=obs_floor_only / max(float(fo.mean()), 1e-9),
                            p_mc=mc_p(obs_floor_only, fo))])
    say("\n  B2 — 'floor-only KILL' count (published 27 of 277), against a null that preserves "
        "each bar's per-cell failure count and randomises WHICH arms fail:")
    say(B2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =============================================================== C. idea 90's cell count
    say("\n" + "=" * 200)
    say("C. idea 90's CELL COUNT (non-empty 4b gross interval), re-read against its size-matched"
        " null — and the conditioning test P1")
    say("=" * 200)
    crows = []
    for mmax, IV in ((1.30, IV130), (1.00, IV100)):
        IV = IV.copy()
        IV["pair"] = IV.book + "|" + IV.arm
        IV["_ps"] = IV.passed.astype(int)
        pv = IV.pivot_table(index="pair", columns="cell", values="_ps", aggfunc="first")
        for cellset, label in ((LARGE_CELLS, "large4"), (ALL_CELLS, "all6")):
            cols = [f"{p}@{int(c)}" for p, c in cellset]
            kc = [int(IV[IV.cell == cl].passed.sum()) for cl in cols]
            for conv in CONVS:
                use = [i for i, k in enumerate(kc) if k > 0] if conv == "COND" else list(range(len(kc)))
                if not use:
                    crows.append(dict(stat="C_interval", mmax=mmax, cellset=label, conv=conv,
                                      n_cells=0, obs=0, null=0.0, lift=0.0, ratio=np.nan,
                                      p_mc=np.nan, kc=",".join(map(str, kc))))
                    continue
                ucols, uk = [cols[i] for i in use], [kc[i] for i in use]
                obs = int((pv[ucols].sum(axis=1) == len(ucols)).sum())
                nul = npairs * float(np.prod([k / npairs for k in uk]))
                dist = null_all_cells(uk, npairs, npairs, NPERM, rng)
                crows.append(dict(stat="C_interval", mmax=mmax, cellset=label, conv=conv,
                                  n_cells=len(ucols), obs=obs, null=nul, lift=obs - nul,
                                  ratio=(obs / nul) if nul > 1e-12 else np.inf,
                                  p_mc=mc_p(obs, dist), kc=",".join(map(str, kc))))
    Cdf = pd.DataFrame(crows)
    say(Cdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    c4 = Cdf[(Cdf.mmax == 1.30) & (Cdf.cellset == "large4") & (Cdf.conv == "COND")]
    c6 = Cdf[(Cdf.mmax == 1.30) & (Cdf.cellset == "all6") & (Cdf.conv == "UNCOND")]
    ok["C_repro"] = len(c4) == 1 and int(c4.obs.iloc[0]) == 4
    say(f"\n  [C-repro] idea 90's published 'operational KEEP admits 4 of 51 pairs' "
        f"(4 large-cap cells): {int(c4.obs.iloc[0]) if len(c4) else 'n/a'}  -> "
        f"{'REPRODUCED' if ok['C_repro'] else 'DOES NOT REPRODUCE'}")
    say(f"  [P1, the conditioning test] same operational KEEP read over ALL SIX cells: "
        f"{int(c6.obs.iloc[0]) if len(c6) else 'n/a'} of {npairs} pairs.")

    # =============================================================== sweep: raw vs lift
    say("\n" + "=" * 200)
    say(f"SWEEP — tuned param 1 (qmax, {len(QMAXES)} values) x tuned param 2 (conditioning, "
        f"{len(CONVS)} values) = {len(QMAXES) * len(CONVS)} grid points per statistic, all "
        f"printed.  {NDRAW} bar draws per (cell, qmax).")
    say("=" * 200)
    srows = []
    pairs = sorted(df.pair.unique())
    pidx = {p: i for i, p in enumerate(pairs)}
    for qmax in QMAXES:
        # per (cell) admissibility, re-indexed onto the (book, arm) pair axis
        adm_by_cell = {}
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)].reset_index(drop=True)
            M = np.zeros((NDRAW, len(pairs)), dtype=bool)
            cols = np.array([pidx[f"{b}|{a}"] for a in s.arm.values])
            M[:, cols] = ADM[(qmax, pk, b, c)]
            adm_by_cell[(pk, c)] = adm_by_cell.get((pk, c), np.zeros((NDRAW, len(pairs)),
                                                                    dtype=bool)) | M
        # a pair only exists in the 17 arm-slots of its own book, so the OR above is a
        # book-blockwise fill, not an aggregation across books.
        for conv in CONVS:
            for cellset, label in ((LARGE_CELLS, "large4"), (ALL_CELLS, "all6")):
                stack = np.stack([adm_by_cell[(p, c)] for p, c in cellset])   # (cells, D, pairs)
                kc = stack.sum(2)                                             # (cells, D)
                if conv == "COND":
                    live = kc > 0
                    ncell = live.sum(0)
                    cnt = (stack & live[:, :, None]).sum(0)
                    keep = ncell > 0
                    allpass = (cnt == ncell[:, None]) & keep[:, None]
                    nul = np.where(keep, np.prod(np.where(live, kc / len(pairs), 1.0), axis=0),
                                   0.0) * len(pairs)
                else:
                    ncell = np.full(NDRAW, len(cellset))
                    cnt = stack.sum(0)
                    keep = np.ones(NDRAW, dtype=bool)
                    allpass = cnt == len(cellset)
                    nul = np.prod(kc / len(pairs), axis=0) * len(pairs)
                obs = allpass.sum(1).astype(float)
                raw = float(obs[keep].mean()) if keep.any() else np.nan
                nullv = float(nul[keep].mean()) if keep.any() else np.nan
                srows.append(dict(stat="C_cellcount_sweep", qmax=qmax, conv=conv,
                                  cellset=label, p_nonempty=float(keep.mean()),
                                  mean_k=float(kc.mean()), raw=raw, null=nullv,
                                  lift=raw - nullv,
                                  ratio=(raw / nullv) if nullv > 1e-12 else np.nan))
                # B1 form: the best pair's cross-cell pass COUNT, normalised to a rate
                rawc = float((cnt.max(1) / np.maximum(ncell, 1))[keep].mean()) if keep.any() else np.nan
                nulc = float((kc.sum(0) / np.maximum(ncell, 1) / len(pairs))[keep].mean()) \
                    if keep.any() else np.nan
                srows.append(dict(stat="B1_bestcount_sweep", qmax=qmax, conv=conv,
                                  cellset=label, p_nonempty=float(keep.mean()),
                                  mean_k=float(kc.mean()), raw=rawc, null=nulc,
                                  lift=rawc - nulc,
                                  ratio=(rawc / nulc) if nulc > 1e-12 else np.nan))
    S = pd.DataFrame(srows)
    for st in ("B1_bestcount_sweep", "C_cellcount_sweep"):
        say(f"\n  {st}:")
        say(S[S.stat == st].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    def monotone(v):
        v = np.asarray(v, float)
        return bool(np.all(np.diff(v) <= 1e-9) or np.all(np.diff(v) >= -1e-9))

    say("\n  [P2] monotonicity in qmax (the idea-141 signature is: RAW non-monotone, LIFT "
        "monotone):")
    p2rows = []
    for st in ("B1_bestcount_sweep", "C_cellcount_sweep"):
        for conv in CONVS:
            for label in ("large4", "all6"):
                g = S[(S.stat == st) & (S.conv == conv) & (S.cellset == label)].sort_values("qmax")
                if len(g) != len(QMAXES):
                    continue
                p2rows.append(dict(stat=st, conv=conv, cellset=label,
                                   raw_monotone=monotone(g.raw.values),
                                   lift_monotone=monotone(g.lift.values),
                                   raw=" -> ".join(f"{x:.3f}" for x in g.raw),
                                   lift=" -> ".join(f"{x:.3f}" for x in g.lift)))
    P2 = pd.DataFrame(p2rows)
    say(P2.to_string(index=False))
    sig = int(((~P2.raw_monotone) & P2.lift_monotone).sum())
    say(f"    idea-141 signature (raw non-monotone AND lift monotone) in {sig} of {len(P2)} "
        f"reported readings.")

    # ---------------- P4 control
    say("\n  [P4] RANDOM-object control at each qmax (a pair chosen at random should land ON "
        "the null):")
    p4 = A[A.sel == "K_RANDOM"][["qmax", "raw", "null", "lift"]]
    say(p4.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok["P4"] = bool(p4.lift.abs().max() < 0.05)
    say(f"    max |random - null| = {p4.lift.abs().max():.4f} (bar 0.05) -> "
        f"{'HELD' if ok['P4'] else 'FAILED — the null is mis-specified'}")

    # =============================================================== rule 8 walk-forward
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — every selector reads the IS window (<= 2016-12-31) ONLY; each "
        "pick read ONCE on 2017-01-01..2026")
    say("=" * 200)
    # cross-cell IS statistics: RAW pass count and its size-matched expectation
    kIS = {}
    for (pk, b, c) in cellkeys:
        s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)]
        kIS[(pk, b, c)] = int(s.adm_S1.sum())
    raw_cnt, lift_cnt = {}, {}
    for pair in pairs:
        b, a = pair.split("|")
        cnt = expc = 0.0
        for (pk, bb, c) in cellkeys:
            if bb != b:
                continue
            s = df[(df.panel == pk) & (df.book == bb) & (df.cost == c) & (df.arm == a)]
            cnt += float(s.adm_S1.iloc[0])
            expc += kIS[(pk, bb, c)] / 17.0
        raw_cnt[pair], lift_cnt[pair] = cnt, cnt - expc

    wrows, picks = [], {}
    for (pk, b, c) in cellkeys:
        s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)].reset_index(drop=True)
        ctl = int(np.flatnonzero(s.arm.values == "control")[0])
        adm = s.adm_S1.values
        cand = np.flatnonzero(adm)
        sel_idx = {}
        sel_idx["S0_CONTROL"] = ctl
        sel_idx["S1_SHARPE"] = int(np.argmax(np.nan_to_num(s.IS_Sharpe.values, nan=-np.inf)))
        for nm, tbl in (("S2_RAW", raw_cnt), ("S3_LIFT", lift_cnt)):
            v = np.array([tbl[f"{b}|{a}"] for a in s.arm.values], float)
            # ties broken by IS Sharpe, the incumbent statistic
            tie = np.nan_to_num(s.IS_Sharpe.values, nan=-np.inf)
            order = np.lexsort((-tie, -v))
            sel_idx[nm] = int(order[0])
        sel_idx["S4_RANDOM"] = int(rng.choice(cand)) if len(cand) else ctl
        for nm, i in sel_idx.items():
            r = s.iloc[i]
            picks.setdefault(nm, {})[(pk, b, c)] = r.arm
            wrows.append(dict(sel=nm, panel=pk, book=b, cost=c, arm=r.arm,
                              IS_adm=bool(r.adm_S1), OOS_CAGR=r.OOS_CAGR,
                              OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                              pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))
    W = pd.DataFrame(wrows)
    agg = W.groupby("sel").agg(OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                               OOS_MaxDD=("OOS_MaxDD", "mean"), n_cells=("arm", "size"),
                               pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"))
    spy_oos = pd.DataFrame([dict(panel=p, CAGR=ref[p]["spy_oos"]["CAGR"],
                                 Sharpe=ref[p]["spy_oos"]["Sharpe"],
                                 MaxDD=ref[p]["spy_oos"]["MaxDD"]) for p in PANELS])
    v1_oos = []
    for pk in PANELS:
        for c in COSTS:
            m = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            v1_oos.append(dict(panel=pk, cost=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                               MaxDD=m["MaxDD"]))
    V1 = pd.DataFrame(v1_oos)
    say("\n  mean over the 18 cells (equal weight; picks read once):")
    say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\n  reference — SPY OOS by panel:\n{spy_oos.to_string(index=False, float_format=lambda x: f'{x:.4f}')}")
    say(f"\n  reference — RULES v1 OOS by cell:\n{V1.to_string(index=False, float_format=lambda x: f'{x:.4f}')}")

    base = agg.loc["S0_CONTROL"]
    say("\n  paired against the do-nothing control S0, per selector:")
    for nm in ("S1_SHARPE", "S2_RAW", "S3_LIFT", "S4_RANDOM"):
        a = W[W.sel == nm].set_index(["panel", "book", "cost"]).sort_index()
        b0 = W[W.sel == "S0_CONTROL"].set_index(["panel", "book", "cost"]).sort_index()
        d = a.OOS_Sharpe - b0.OOS_Sharpe
        say(f"    {nm}: dOOS_Sharpe mean {d.mean():+.4f}, better in {int((d > 0).sum())} of "
            f"{len(d)} cells, dOOS_CAGR {(a.OOS_CAGR - b0.OOS_CAGR).mean():+.4%}, "
            f"dOOS_MaxDD {(a.OOS_MaxDD - b0.OOS_MaxDD).mean():+.4%}")
    same = sum(1 for k in picks["S2_RAW"] if picks["S2_RAW"][k] == picks["S3_LIFT"][k])
    ok["P5"] = same >= len(cellkeys) / 2 and max(
        abs(agg.loc[nm, "OOS_Sharpe"] - base["OOS_Sharpe"])
        for nm in ("S1_SHARPE", "S2_RAW", "S3_LIFT")) <= 0.05
    say(f"\n  [P5] S2_RAW and S3_LIFT agree in {same} of {len(cellkeys)} cells; "
        f"max |selector - S0| OOS Sharpe = "
        f"{max(abs(agg.loc[nm, 'OOS_Sharpe'] - base['OOS_Sharpe']) for nm in ('S1_SHARPE', 'S2_RAW', 'S3_LIFT')):.4f}"
        f" -> {'HELD' if ok['P5'] else 'FAILED'}")

    say("\n  BOTH KEEP PATHS on every distinct arm any selector picked:")
    dist_arms = W.drop_duplicates(["panel", "book", "cost", "arm"])
    say(f"    {len(dist_arms)} distinct (cell, arm) picks; 4a passes {int(dist_arms.pass4a.sum())}"
        f", 4b passes (full sample) {int(dist_arms.pass4b.sum())}")
    # 4b read on the OOS window alone, from each panel's own OOS SPY bars
    oos_pass = []
    for _, r in W.iterrows():
        rr = rets[(r.panel, r.book, r.cost, r.arm)]
        b = _oos_bars(ref, r.panel)
        mg = C129.margins_at(rr, b, PHI0, DELTA0, "OOS")
        oos_pass.append(all(mg[k] > 0 for k in ("H1", "H2", "DD", "CAGR")))
    W["pass4b_oos"] = oos_pass
    say(f"    4b read on the OOS window alone: {int(W.drop_duplicates(['panel','book','cost','arm']).pass4b_oos.sum())}"
        f" of {len(dist_arms)} distinct picks")

    # =============================================================== outputs
    A.to_csv(OUT / f"{STEM}.anchor.csv", index=False)
    pd.concat([B1, B2, Cdf], ignore_index=True).to_csv(OUT / f"{STEM}.published.csv", index=False)
    S.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS — outcome")
    say("=" * 200)
    for k, v in ok.items():
        say(f"    {k}: {'HELD/OK' if v else 'FAILED'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


_SPY_CACHE = {}


def _spyret(ref, pk):
    if pk not in _SPY_CACHE:
        px, spy_full, _ = C129.panel(pk)
        _SPY_CACHE[pk] = spy_full.reindex(px.index).fillna(0.0).loc[ref[pk]["start"]:]
    return _SPY_CACHE[pk]


def _oos_bars(ref, pk):
    return C129.bars_win(_spyret(ref, pk), "OOS")


if __name__ == "__main__":
    main()
