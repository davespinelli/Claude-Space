#!/usr/bin/env python3
"""QUEUE idea 141 — is-Calmar-immunity-general  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 141)
    "idea 132 found IS-Calmar is as immune to the IS 4b screen as IS-Sharpe (0 moves,
     unscreened argmax admissible in 100% of non-empty cells) while IS-CAGR (57%) and
     IS-MaxDD (29%) are not, i.e. the immunity belongs to risk-adjusted-return selectors as
     a class.  Test whether ANY risk-adjusted-return argmax is immune to a screen built from
     Sharpe-like bars, by re-running with randomised bar values.  Bears directly on idea 110."

    Two rival explanations of idea 132's 100% / 100% / 57% / 29%:
      (C) CLASS PROPERTY — being a risk-adjusted-return statistic is what buys immunity.  Then
          every RA selector should stay immune when the bar LEVELS are randomised, and every
          non-RA selector should not.
      (D) CO-MONOTONICITY — immunity is bought by a selector's statistic being rank-aligned with
          the statistics the bars are written on (IS half-Sharpes, IS MaxDD, IS CAGR), and
          "risk-adjusted" is only a proxy for that alignment.  Then immunity should be a
          function of the alignment, RA selectors should SPLIT (some immune, some not), and a
          well-aligned non-RA selector should be immune.
    The discriminator needs RA selectors that differ in alignment.  Five are run, deliberately
    spanning it, against three non-RA selectors; if (C) is right the class boundary predicts
    immunity and the alignment does not add to it.

WHY RANDOMISED BARS.  Idea 132 measured immunity at ONE point: PROTOCOL 4b's own bars
    (phi=0.70, delta=0.60, SPY's IS half-Sharpes).  A single bar vector cannot distinguish a
    structural property from a calibration coincidence: if the published bars happen to sit
    where the admissible set is large, EVERY argmax survives and the ranking is noise.  This
    run replaces the four bar levels with draws from the cell's own cross-arm distribution, so
    the screen keeps 4b's SHAPE (four one-sided inequalities in the same directions on the same
    four statistics) and loses its calibration.

CORPUS — idea 132's, unchanged and re-derived rather than read
    3 panels (u56 / broad / small) x 3 books (V1u, TOP20, EWall) x 2 cost rungs (10, 25 bps)
    = 18 cells, each with idea 94's 17 arms = 306 arm-rows = 306 backtests, weekly, t+1.
    Check [a] asserts this run's 306 rows equal idea 132's published .grid.csv arm-for-arm and
    check [b] reproduces idea 132's four published immunity rates BEFORE any new number is
    read.  If either check is not exact nothing downstream is trustworthy and the script says so.

TUNED PARAMETERS — exactly two, both swept exhaustively and ALL grid points reported:
    1. the IS selector statistic, 8 values (5 risk-adjusted, 3 not), all reported:
         RA : K_Sharpe   argmax IS Sharpe                     (idea 132's incumbent)
              K_Calmar   argmax IS CAGR / |IS MaxDD|          (the idea's subject)
              K_Sortino  argmax IS mean / IS downside deviation
              K_MinHalf  argmax min(IS H1 Sharpe, IS H2 Sharpe)
              K_H2Sharpe argmax IS second-half Sharpe
         NRA: K_CAGR     argmax IS CAGR
              K_MaxDD    argmax IS MaxDD (shallowest)
              K_NegVol   argmin IS volatility
    2. the screen tightness qmax, 4 values: 0.25 / 0.50 / 0.75 / 1.00.  Each bar is drawn at a
       quantile q ~ U(0, qmax) of that cell's own 17 arm values of the statistic the bar is
       written on, so qmax is literally "how much of the cell a bar may cut".
    8 x 4 = 32 grid points, every one printed.  R = 4000 independent bar draws per (cell, qmax),
    seeded; panels, books, cost rungs, arms and the OOS window are reported axes, never
    selected on.

CONTROLS (not selectors under test, they exist to make the numbers readable)
    K_RANDOM   argmax of a random score, redrawn every draw: measures what immunity a selector
               with NO information about the bars gets.  Its immunity IS the size-matched null.
    SIZE-NULL  E[k/n | k>0], the analytic version of the same thing.
    A selector is immune only if it beats BOTH; "100%" against a screen that admits 16 of 17
    arms is not immunity, it is a loose screen.

WALK-FORWARD (PROTOCOL rule 8) — every screen and every selector reads the IS window
    (through 2016-12-31) ONLY; each resulting pick is read ONCE on 2017-01-01..2026 and
    reported as OOS CAGR / Sharpe / MaxDD against that cell's ungated control, RULES v1 (the
    live book) and SPY.  Both KEEP paths are evaluated for every distinct picked arm, on the
    full sample and again on the OOS window alone.  Under randomised bars a screen can admit
    nothing, so the FALLBACK convention of idea 132 is used and stated: a screen that admits
    nothing holds the cell's ungated control.

PRE-REGISTERED PREDICTIONS (written before any randomised-bar number was read)
    P0  Reproduction: 306 rows match idea 132's grid to < 1e-9 and its four published immunity
        rates come back exactly (100 / 100 / 57 / 29 %).
    P1  The idea's premise, tested: under randomised bars at EVERY qmax, K_Sharpe and K_Calmar
        keep immunity >= 0.90 AND beat the size-matched null by >= 0.10.  If immunity collapses
        to the null, idea 132's 100% was a calibration artifact and the premise is KILLED.
    P2  (D) beats (C): at least one RA selector has immunity below the best non-RA selector at
        some qmax, i.e. the class boundary does NOT partition immunity.
    P3  Immunity is non-increasing in qmax for every selector (a tighter screen can only cut
        more), and the SPREAD between selectors widens with qmax.
    P4  Immunity is explained by alignment: across the 8 selectors, Spearman(mean minimum
        rank-correlation with the four bar statistics, immunity at qmax=1.00) >= +0.70.
    P5  Control: K_RANDOM's immunity is within 0.05 of the analytic size-matched null at every
        qmax (if not, the null is mis-specified and every lift in this file is suspect).

CAVEATS carried, not buried
    * Survivorship: all three panels are current constituents (idea 54); the small panel drops
      the 44 tickers with max_1d_move >= 1.0 and its SPY is a held-out benchmark.  Every CAGR
      here is optimistic; no level in this file is an achievable return.
    * Idea 128: the IS window's drawdown is shallower than the OOS window's, so an IS drawdown
      bar is measured on a window that cannot express a deep drawdown.  This biases the DD bar
      toward admitting too much for every selector equally.
    * Idea 126: every row is quoted at t+1 execution only.
    * This run selects among EXISTING arms.  It cannot promote a book and does not try to; its
      output is a statement about PROTOCOL rule 8's screen, not a candidate.
    * The randomised bars are drawn from each cell's own cross-arm distribution.  That is what
      makes tightness comparable across cells; it also means the bars are not SPY-relative, so
      this file measures the screen's SHAPE, not 4b's economic content.

HARNESS
    Idea 94's script is IMPORTED (H.run, H.targets, H.arm_specs, H.halves, H.window, H.pass4a,
    H.spearman) and idea 129's screen machinery too (C.panel, C.bars_win, C.margins_at,
    C.fails), so the screen under test is literally the code that produced the result under test.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .immunity.csv, .cells.csv,
.alignment.csv and .walkforward.csv.
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

STEM = "2026-09-05_is-Calmar-immunity-general_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I132_GRID = OUT / "2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ, COSTS, BOOKS = H.FREQ, [10.0, 25.0], H.BOOKS
IS_END, OOS_START = H.IS_END, H.OOS_START
PANELS = ["u56", "broad", "small"]
PHI0, DELTA0 = 0.70, 0.60
QMAXES = [0.25, 0.50, 0.75, 1.00]
NDRAW = 4000
SEED = 20260905

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


# selector name -> (grid column to MAXIMISE, class)
SELECTORS = {
    "K_Sharpe":   ("IS_Sharpe", "RA"),
    "K_Calmar":   ("IS_Calmar", "RA"),
    "K_Sortino":  ("IS_Sortino", "RA"),
    "K_MinHalf":  ("IS_MinHalf", "RA"),
    "K_H2Sharpe": ("IS_H2", "RA"),
    "K_CAGR":     ("IS_CAGR", "NRA"),
    "K_MaxDD":    ("IS_MaxDD", "NRA"),
    "K_NegVol":   ("IS_NegVol", "NRA"),
}
# the four statistics the bars are written on, oriented so that MORE IS BETTER
BARSTATS = ["IS_H1", "IS_H2", "IS_MaxDD", "IS_CAGR"]


# ------------------------------------------------------------------ corpus
def build():
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, spy=ms, spy_oos=mso, v1=v1, start=start,
                       spy_ret=spy, desc=desc)
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, {px.index[0].date()}.."
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        say(f"    IS-window SPY bars (what the published screen sees): halves "
            f"{bIS['s1']:.3f}/{bIS['s2']:.3f} MaxDD {bIS['sdd']:.2%} CAGR {bIS['scagr']:.2%}")

        worst = 0.0
        for b in BOOKS:
            W = H.targets(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a0] engine-equivalence, 3 ungated books: max|diff| = {worst:.3e} "
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
                    mg = C.margins_at(r, ref[pk]["bfull"], PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
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
                        pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                        pass4a=H.pass4a(r, v1[c])))
    return pd.DataFrame(rows), rets, ref


def main():
    df, rets, ref = build()
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)      # PROTOCOL 4b's own IS screen
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---------------- [a] reproduction of idea 132's corpus, before any new number is read
    g132 = pd.read_csv(I132_GRID)
    j = df.merge(g132, on=["panel", "book", "cost", "arm"], suffixes=("", "_132"))
    keys = [k for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_Calmar",
                        "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross")
            if f"{k}_132" in j.columns]
    d = {k: float((j[k] - j[f"{k}_132"]).abs().max()) for k in keys}
    nadm = int((j.adm_S1 != j.adm_S1_132).sum()) if "adm_S1_132" in j.columns else -1
    okA = (len(j) == len(df)) and max(d.values()) < 1e-9 and nadm == 0
    say(f"\n[a] reproduction of idea 132's grid: {len(j)} of {len(df)} rows matched, "
        + " ".join(f"{k} {v:.2e}" for k, v in d.items())
        + f", adm_S1 disagreements {nadm}"
        + ("  EXACT" if okA else "  NOT EXACT — nothing below is trustworthy"))

    # ---------------- [b] reproduction of idea 132's four published immunity rates
    say("\n[b] reproduction of idea 132's published immunity at PROTOCOL's own bars "
        "(published: K_Sharpe 100%, K_Calmar 100%, K_CAGR 57%, K_MaxDD 29%)")
    pub, cells = {}, []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        row = dict(panel=pk, book=b, cost=c, n_arms=len(s), adm_S1=int(s.adm_S1.sum()))
        for sel, (col, _) in SELECTORS.items():
            row[f"{sel}_in_S1"] = bool(s.loc[s[col].idxmax()].adm_S1)
        cells.append(row)
    A = pd.DataFrame(cells)
    ne = A[A.adm_S1 > 0]
    for sel in SELECTORS:
        pub[sel] = float(ne[f"{sel}_in_S1"].mean())
    say(f"    non-empty in {len(ne)} of {len(A)} cells; median admitted "
        f"{A.adm_S1.median():.1f} of 17")
    say("    " + "  ".join(f"{k} {v:.0%}" for k, v in pub.items()))
    okB = (round(pub["K_Sharpe"], 2) == 1.00 and round(pub["K_Calmar"], 2) == 1.00
           and round(pub["K_CAGR"] * 100) == 57 and round(pub["K_MaxDD"] * 100) == 29)
    say(f"    -> {'REPRODUCED EXACTLY' if okB else 'DOES NOT REPRODUCE — unsafe'}")
    if not (okA and okB):
        say("\n[STOP] a pre-check failed; the randomised-bar section below is NOT trustworthy.")

    # ---------------- randomised-bar experiment
    say(f"\n[RANDOMISED BARS] each bar drawn at quantile q ~ U(0, qmax) of the cell's own 17 "
        f"arm values of the statistic it bars; {NDRAW} draws x 18 cells x {len(QMAXES)} qmax; "
        f"seed {SEED}.  Screen shape is 4b's: IS_H1 > b1, IS_H2 > b2, |IS_MaxDD| < bDD, "
        f"IS_CAGR > bC.")
    rng = np.random.default_rng(SEED)
    cellkeys = sorted({(p, b, c) for p, b, c in zip(df.panel, df.book, df.cost)})
    irows, cellrows, alrows = [], [], []
    # OOS bookkeeping for the walk-forward: accumulate per (sel, qmax) over draws x cells
    wf = {(sel, q): dict(sh=[], cg=[], dd=[], picks={}) for sel in
          list(SELECTORS) + ["K_RANDOM"] for q in QMAXES}

    for qmax in QMAXES:
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)].reset_index(drop=True)
            n = len(s)
            h1, h2 = s.IS_H1.values, s.IS_H2.values
            adddv, cg = np.abs(s.IS_MaxDD.values), s.IS_CAGR.values
            q = rng.uniform(0.0, qmax, size=(NDRAW, 4))
            b1 = np.quantile(h1, q[:, 0])
            b2 = np.quantile(h2, q[:, 1])
            bdd = np.quantile(adddv, 1.0 - q[:, 2])
            bc = np.quantile(cg, q[:, 3])
            adm = ((h1[None, :] > b1[:, None]) & (h2[None, :] > b2[:, None])
                   & (adddv[None, :] < bdd[:, None]) & (cg[None, :] > bc[:, None]))
            k = adm.sum(1)
            ne_ = k > 0
            nne = int(ne_.sum())
            oos_sh, oos_cg, oos_dd = s.OOS_Sharpe.values, s.OOS_CAGR.values, s.OOS_MaxDD.values
            # per-bar admissibility, for exclusion attribution
            single = dict(H1=(h1[None, :] > b1[:, None]), H2=(h2[None, :] > b2[:, None]),
                          DD=(adddv[None, :] < bdd[:, None]), CAGR=(cg[None, :] > bc[:, None]))

            for sel in list(SELECTORS) + ["K_RANDOM"]:
                if sel == "K_RANDOM":
                    sc = rng.random((NDRAW, n))
                    ordr = np.argsort(-sc, axis=1, kind="stable")
                    amx = ordr[:, 0]
                else:
                    col = SELECTORS[sel][0]
                    v = s[col].values.astype(float)
                    order1 = np.argsort(-np.nan_to_num(v, nan=-np.inf), kind="stable")
                    ordr = np.broadcast_to(order1, (NDRAW, n))
                    amx = np.full(NDRAW, order1[0])
                admo = np.take_along_axis(adm, ordr, axis=1)
                first = admo.argmax(1)
                pidx = np.take_along_axis(ordr, first[:, None], axis=1)[:, 0]
                pidx = np.where(ne_, pidx, np.arange(n)[s.arm.values == "control"][0])
                argmax_adm = adm[np.arange(NDRAW), amx]
                moved = ne_ & (pidx != amx)

                w = wf[(sel, qmax)]
                w["sh"].append(oos_sh[pidx])
                w["cg"].append(oos_cg[pidx])
                w["dd"].append(oos_dd[pidx])
                for a_ in np.unique(pidx):
                    w["picks"][(pk, b, c, s.arm.values[a_])] = True

                excl = {}
                bad = ne_ & (~argmax_adm)
                for nm, m_ in single.items():
                    excl[nm] = float((bad & (~m_[np.arange(NDRAW), amx])).sum() / max(bad.sum(), 1))
                cellrows.append(dict(
                    qmax=qmax, sel=sel, panel=pk, book=b, cost=c, n_arms=n,
                    p_nonempty=nne / NDRAW, mean_k=float(k[ne_].mean()) if nne else np.nan,
                    immunity=float(argmax_adm[ne_].mean()) if nne else np.nan,
                    null=float((k[ne_] / n).mean()) if nne else np.nan,
                    move_rate=float(moved[ne_].mean()) if nne else np.nan,
                    exc_H1=excl["H1"], exc_H2=excl["H2"], exc_DD=excl["DD"], exc_CAGR=excl["CAGR"],
                    n_bad=int(bad.sum())))

    CELL = pd.DataFrame(cellrows)
    CELL.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    # ---------------- alignment (the mechanism (D) proposes), IS window only
    for sel, (col, cls) in SELECTORS.items():
        per = []
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)]
            cs = [H.spearman(s[col].values, s[bs].values) for bs in BARSTATS]
            per.append(dict(panel=pk, book=b, cost=c, sel=sel, cls=cls,
                            **{f"rho_{bs}": v for bs, v in zip(BARSTATS, cs)},
                            rho_min=float(np.nanmin(cs)), rho_mean=float(np.nanmean(cs))))
        alrows += per
    AL = pd.DataFrame(alrows)
    AL.to_csv(OUT / f"{STEM}.alignment.csv", index=False)
    ALS = AL.groupby(["sel", "cls"]).agg(
        rho_H1=("rho_IS_H1", "mean"), rho_H2=("rho_IS_H2", "mean"),
        rho_DD=("rho_IS_MaxDD", "mean"), rho_CAGR=("rho_IS_CAGR", "mean"),
        rho_min=("rho_min", "mean"), rho_mean=("rho_mean", "mean")).reset_index()

    # ---------------- the 32-point grid, ALL points reported
    say("\n[GRID 8x4] immunity = P(unscreened argmax admissible | admissible set non-empty), "
        "pooled over 18 cells x 4000 draws.  null = E[k/n | k>0] (size-matched).  "
        "lift = immunity - null.  ALL 32 points, plus the K_RANDOM control.")
    def _wavg(v, w):
        v, w = np.asarray(v, float), np.asarray(w, float)
        ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
        return float(np.sum(v[ok] * w[ok]) / np.sum(w[ok])) if ok.any() else np.nan

    grows = []
    for (sel, qm), x in CELL.groupby(["sel", "qmax"]):
        grows.append(dict(
            sel=sel, qmax=qm,
            immunity=_wavg(x.immunity, x.p_nonempty), null=_wavg(x["null"], x.p_nonempty),
            move_rate=_wavg(x.move_rate, x.p_nonempty), mean_k=_wavg(x.mean_k, x.p_nonempty),
            p_nonempty=float(x.p_nonempty.mean()),
            exc_H1=_wavg(x.exc_H1, x.n_bad), exc_H2=_wavg(x.exc_H2, x.n_bad),
            exc_DD=_wavg(x.exc_DD, x.n_bad), exc_CAGR=_wavg(x.exc_CAGR, x.n_bad)))
    G = pd.DataFrame(grows)
    G["lift"] = G.immunity - G["null"]
    G["cls"] = G.sel.map(lambda s_: SELECTORS[s_][1] if s_ in SELECTORS else "CTL")
    G["pub_immunity"] = G.sel.map(lambda s_: pub.get(s_, np.nan))
    G = G.sort_values(["qmax", "immunity"], ascending=[True, False])
    G.to_csv(OUT / f"{STEM}.immunity.csv", index=False)
    with pd.option_context("display.max_rows", None):
        say(G[["qmax", "sel", "cls", "immunity", "null", "lift", "move_rate", "mean_k",
               "p_nonempty", "exc_H1", "exc_H2", "exc_DD", "exc_CAGR", "pub_immunity"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n[ALIGNMENT] mean rank-correlation of each selector's statistic with the four "
        "statistics the bars are written on (IS window, across the 17 arms, 18 cells)")
    say(ALS.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))

    # ---------------- rule-8 walk-forward, OOS read once
    say("\n[WALK-FORWARD, PROTOCOL rule 8] every screen and selector reads 2009..2016 only; "
        "OOS 2017..2026 read once.  FALLBACK: a screen admitting nothing holds the cell's "
        "ungated control.  Means are over 18 cells x 4000 draws.")
    wrows = []
    ctl_sh, ctl_cg, ctl_dd, v1_sh, v1_cg, v1_dd, sp_sh, sp_cg, sp_dd = ([] for _ in range(9))
    for (pk, b, c) in cellkeys:
        ctl = H.window(rets[(pk, b, c, "control")], "OOS")
        mc = metrics(ctl)
        mv = metrics(H.window(ref[pk]["v1"][c], "OOS"))
        mso = ref[pk]["spy_oos"]
        ctl_sh.append(mc["Sharpe"]); ctl_cg.append(mc["CAGR"]); ctl_dd.append(mc["MaxDD"])
        v1_sh.append(mv["Sharpe"]); v1_cg.append(mv["CAGR"]); v1_dd.append(mv["MaxDD"])
        sp_sh.append(mso["Sharpe"]); sp_cg.append(mso["CAGR"]); sp_dd.append(mso["MaxDD"])
    REF = dict(ctl=(np.mean(ctl_cg), np.mean(ctl_sh), np.mean(ctl_dd)),
               v1=(np.mean(v1_cg), np.mean(v1_sh), np.mean(v1_dd)),
               spy=(np.mean(sp_cg), np.mean(sp_sh), np.mean(sp_dd)))
    for (sel, qmax), w in wf.items():
        sh = np.concatenate(w["sh"]); cg = np.concatenate(w["cg"]); dd = np.concatenate(w["dd"])
        wrows.append(dict(sel=sel, qmax=qmax,
                          cls=SELECTORS[sel][1] if sel in SELECTORS else "CTL",
                          OOS_CAGR=float(cg.mean()), OOS_Sharpe=float(sh.mean()),
                          OOS_MaxDD=float(dd.mean()),
                          OOS_Sharpe_p10=float(np.quantile(sh, 0.10)),
                          OOS_Sharpe_p90=float(np.quantile(sh, 0.90)),
                          beat_ctl=float((sh > np.repeat(ctl_sh, NDRAW)).mean()),
                          beat_v1=float((sh > np.repeat(v1_sh, NDRAW)).mean()),
                          beat_spy=float((sh > np.repeat(sp_sh, NDRAW)).mean()),
                          n_distinct_arms=len(w["picks"])))
    W = pd.DataFrame(wrows).sort_values(["qmax", "OOS_Sharpe"], ascending=[True, False])
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    with pd.option_context("display.max_rows", None):
        say(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"  reference OOS means over the same 18 cells — ungated control "
        f"{REF['ctl'][0]:.2%}/{REF['ctl'][1]:.3f}/{REF['ctl'][2]:.2%}; RULES v1 "
        f"{REF['v1'][0]:.2%}/{REF['v1'][1]:.3f}/{REF['v1'][2]:.2%}; SPY "
        f"{REF['spy'][0]:.2%}/{REF['spy'][1]:.3f}/{REF['spy'][2]:.2%}  (CAGR/Sharpe/MaxDD)")

    # the published-bar (S1) walk-forward, for the same selectors, as the reference point
    say("\n[WALK-FORWARD, published bars] the same selectors under PROTOCOL 4b's OWN IS screen "
        "(one bar vector, not randomised), FALLBACK convention, 18 cells:")
    prows = []
    for sel, (col, cls) in SELECTORS.items():
        sh_, cg_, dd_ = [], [], []
        for (pk, b, c) in cellkeys:
            s = df[(df.panel == pk) & (df.book == b) & (df.cost == c)]
            cand = s[s.adm_S1]
            p = cand.loc[cand[col].idxmax()] if len(cand) else s[s.arm == "control"].iloc[0]
            sh_.append(p.OOS_Sharpe); cg_.append(p.OOS_CAGR); dd_.append(p.OOS_MaxDD)
        prows.append(dict(sel=sel, cls=cls, OOS_CAGR=np.mean(cg_), OOS_Sharpe=np.mean(sh_),
                          OOS_MaxDD=np.mean(dd_),
                          beat_spy=int(np.sum(np.array(sh_) > np.array(sp_sh))),
                          beat_v1=int(np.sum(np.array(sh_) > np.array(v1_sh)))))
    P = pd.DataFrame(prows).sort_values("OOS_Sharpe", ascending=False)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- KEEP paths, every distinct arm any randomised screen ever picked
    say("\n[KEEP PATHS] both paths for every distinct arm picked by ANY selector at ANY qmax, "
        "full sample AND OOS window alone")
    picked = set()
    for w in wf.values():
        picked |= set(w["picks"])
    krows = []
    for (pk, b, c, arm) in sorted(picked):
        g = df[(df.panel == pk) & (df.book == b) & (df.cost == c) & (df.arm == arm)].iloc[0]
        spyo = ref[pk]["spy_ret"].loc[OOS_START:]
        mgo = C.margins_at(H.window(rets[(pk, b, c, arm)], "OOS"), C.bars_win(spyo, "full"),
                           PHI0, DELTA0, "full")
        fo = C.fails(mgo)
        krows.append(dict(panel=pk, book=b, cost=c, arm=arm, CAGR=g.CAGR, Sharpe=g.Sharpe,
                          MaxDD=g.MaxDD, H1=g.H1, H2=g.H2, full_4a=bool(g.pass4a),
                          full_4b=bool(g.pass4b), full_fail4b=g.fail4b, OOS_CAGR=g.OOS_CAGR,
                          OOS_Sharpe=g.OOS_Sharpe, OOS_MaxDD=g.OOS_MaxDD,
                          oos_window_4b=(len(fo) == 0), oos_window_fail=",".join(fo) or "-"))
    K = pd.DataFrame(krows)
    with pd.option_context("display.max_rows", None):
        say(K.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"[KEEP PATHS] distinct picked arms {len(K)}; full-sample 4a passes "
        f"{int(K.full_4a.sum())}, full-sample 4b passes {int(K.full_4b.sum())}, "
        f"OOS-window 4b passes {int(K.oos_window_4b.sum())}")

    # ---------------- predictions, scored
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    say(f"   P0 corpus + published-immunity reproduction -> "
        f"{'HELD' if (okA and okB) else 'FAILED'}")

    prem = []
    for sel in ("K_Sharpe", "K_Calmar"):
        g = G[G.sel == sel]
        prem.append((sel, float(g.immunity.min()), float(g.lift.min())))
    p1 = all(i >= 0.90 and lf >= 0.10 for _, i, lf in prem)
    say(f"   P1 K_Sharpe and K_Calmar keep immunity >= 0.90 and lift >= 0.10 at EVERY qmax: "
        + "; ".join(f"{s_} min imm {i:.3f} min lift {lf:+.3f}" for s_, i, lf in prem)
        + f" -> {'HELD (immunity is not a calibration artifact)' if p1 else 'FAILED (idea 132s 100% does not survive randomised bars)'}")

    worst_ra, best_nra, p2cells = {}, {}, []
    for q in QMAXES:
        g = G[(G.qmax == q) & (G.cls != "CTL")]
        ra, nra = g[g.cls == "RA"], g[g.cls == "NRA"]
        wr, bn = ra.loc[ra.immunity.idxmin()], nra.loc[nra.immunity.idxmax()]
        worst_ra[q], best_nra[q] = wr, bn
        p2cells.append(wr.immunity < bn.immunity)
        say(f"      qmax {q:.2f}: worst RA = {wr.sel} {wr.immunity:.3f}; best NRA = {bn.sel} "
            f"{bn.immunity:.3f}; class boundary {'BROKEN' if wr.immunity < bn.immunity else 'holds'}")
    p2 = any(p2cells)
    say(f"   P2 the RA/NRA class boundary does NOT partition immunity: broken at "
        f"{sum(p2cells)} of {len(QMAXES)} qmax -> "
        f"{'HELD -> (D) co-monotonicity, not (C) class' if p2 else 'FAILED -> (C) class property survives'}")

    mono, spreads = {}, {}
    for sel in list(SELECTORS) + ["K_RANDOM"]:
        v = G[G.sel == sel].sort_values("qmax").immunity.values
        mono[sel] = bool(np.all(np.diff(v) <= 1e-9))
    for q in QMAXES:
        g = G[(G.qmax == q) & (G.cls != "CTL")]
        spreads[q] = float(g.immunity.max() - g.immunity.min())
    p3 = all(mono.values()) and spreads[QMAXES[-1]] > spreads[QMAXES[0]]
    say(f"   P3 immunity non-increasing in qmax for all: {mono}; spread "
        + " ".join(f"{q:.2f}:{v:.3f}" for q, v in spreads.items())
        + f" -> {'HELD' if p3 else 'FAILED'}")

    gi = G[(G.qmax == QMAXES[-1]) & (G.cls != "CTL")].merge(ALS.drop(columns=["cls"]), on="sel")
    rho = H.spearman(gi.rho_min.values, gi.immunity.values)
    rho2 = H.spearman(gi.rho_mean.values, gi.immunity.values)
    p4 = np.isfinite(rho) and rho >= 0.70
    say(f"   P4 alignment explains immunity at qmax=1.00: Spearman(rho_min, immunity) = "
        f"{rho:+.3f} (rho_mean {rho2:+.3f}, 8 selectors) -> {'HELD' if p4 else 'FAILED'}")
    say("      " + gi[["sel", "cls", "rho_min", "rho_mean", "immunity"]]
        .sort_values("immunity", ascending=False)
        .to_string(index=False, float_format=lambda x: f"{x:+.3f}").replace("\n", "\n      "))

    gr = G[G.sel == "K_RANDOM"]
    gap = float((gr.immunity - gr["null"]).abs().max())
    p5 = gap < 0.05
    say(f"   P5 K_RANDOM tracks the analytic size-matched null (max|imm - null| = {gap:.4f} "
        f"< 0.05) -> {'HELD' if p5 else 'FAILED — every lift in this file is suspect'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
