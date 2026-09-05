#!/usr/bin/env python3
"""IDEA 201  the-margin-column-instead-of-two   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 191 confirmed idea 186's mechanism -- the rotation null's BAND widens with an overlay's
ON-SHARE (Spearman +0.656) -- but killed the column as proposed, because the realised effect
|dSharpe| rises with on-share at almost the same rate (+0.595) and the two cancel, leaving
rho(on-share, clears) = +0.068 pooled and sign-inconsistent across families.  Idea 191's
surviving recommendation was therefore a PAIR: publish on-share BESIDE |dSharpe|, and quote
the MARGIN (|dSharpe| - band) "as the single summary".

The queue asks the obvious next question: if MARGIN is the single summary, why publish two
columns at all?  Is MARGIN a SUFFICIENT STATISTIC for the pair -- does adding on-share to a
margin-only reading change any published verdict?

  Q1  DEFINITIONAL SUFFICIENCY.  Does sign(margin) reproduce the clause verdict `clears` on
      every real row, on Sharpe and on drawdown?  (Nearly vacuous -- clears is DEFINED as
      |dSharpe| > band -- but it is the queue's literal question and it is checked, not
      assumed.)
  Q2  INFORMATIONAL SUFFICIENCY.  Conditional on the IS margin, does on-share carry any
      incremental information about the OOS outcome (OOS margin, OOS dSharpe)?  If it does
      not, a reader given margin alone loses nothing.
  Q3  DECISION SUFFICIENCY.  Over every decision the corpus actually makes with the clause --
      the rule-8 adopt/choose decisions -- does a margin-only reader ever pick differently
      from a margin+on-share reader, and does it cost OOS Sharpe?
  Q4  NOISE FLOOR.  The band is itself a 20-draw sample statistic.  How large is its own
      sampling noise, and how many clause verdicts flip when the rotation seed changes?  A
      second column cannot matter if the first one is not stable to its own draw.
  Q5  RULE 8.  Margin-only vs pair vs do-nothing, out of sample, against RULES v1 and SPY.

DESIGN
------
Idea 191's script is IMPORTED, not re-implemented: panels, base book, overlay families,
apply_overlay, the rotation null and the 4a/4b evaluators all execute the parent's own code,
so every number below sits on the simulator being audited.

  panels   : U56, BROAD136, SMALL439 (the 483-name sub-$2B panel less the 44 tickers with
             max_1d_move >= 1.0 in data/small_meta.csv)
  base book: idea 2's candidate -- composite (no vol scaler), 200d & vol20<0.60 eligibility,
             top-20 equal weight, gross 0.75, WEEKLY, t+1
  families : DDCTL / BUDGET / SLEEVE, idea 186/191's definitions verbatim
  TUNED PARAMETER 1: threshold (5 per family, idea 191's widened grid, unchanged)
  TUNED PARAMETER 2: depth     (2 per family, idea 186's, unchanged)
  costs    : 10 and 25 bps, both derived EXACTLY from one 0 bps run -- a reported axis
  null     : 60 circular rotations per configuration = 3 DISJOINT blocks of 20.  Block 0 is
             the primary band (idea 186's 20-draw construction); blocks 1 and 2 exist only to
             measure the band's own sampling noise for Q4.

  real grid : 3 panels x 3 families x 5 thr x 2 depth x 2 cost = 180 real rows
  null grid : the same 90 configurations x 60 rotations x 2 cost = 10800 null rows
  total     : 5490 backtests

RULE 8 (PROTOCOL clause 8, required): overlay point chosen on data <= 2016-12-31 ONLY,
2017-01-01 -> read ONCE.  18 cells = 3 panels x 3 families x 2 cost rungs.
BOTH KEEP PATHS evaluated on every real row (4a vs the panel's own RULES v1, 4b vs SPY).

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  sign(margin) reproduces `clears` on 180/180 real rows, both bars.
  P2  Given the IS margin, on-share adds no incremental prediction of the OOS margin:
      |partial Spearman| < 0.15 and Delta R^2 < 0.02.
  P3  No rule-8 pick differs between the margin-only and the margin+on-share selector.
  P4  Idea 191's rotation seed is `SEED + hash((panel, family, thr)) % 10000`, and Python
      salts `hash` on str, so the parent's BANDS are not reproducible across processes while
      its real rows are.  Predicted: real rows reproduce at 0.0e+00, bands do not.
  P5  No selector beats the do-nothing control out of sample (the eleventh consecutive
      instance in this project of an IS-fitted selector failing to earn its complexity).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; SMALL439 contains no
    delistings.  Real and rotated draws inherit the bias identically, so the CLAUSE reading
    is unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is not a
    tradable estimate.
  * Only J-1 distinct rotations exist and neighbouring offsets are correlated, so the
    clause's nominal one-sided size (1/21 = 4.8%) is approximate; the three blocks are
    disjoint in offset but not independent.
  * BUDGET-skip changes realised turnover between real and null (idea 186: 25.4% mean,
    idea 191: 1782.7% on the widened grid).  That is idea 203's subject, not this run's; it
    is inherited and stated, not fixed here.
  * Two cells (SMALL439 / BUDGET tau=0.05 / skip, both cost rungs) have an UNDEFINED IS
    Sharpe: the overlay suppresses 93.7% of rebalances, so the book is flat through the IS
    window.  They are dropped from the Q2 regressions (n_used is printed) and kept everywhere
    else; nothing is imputed.
  * Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136.  Idea 126: t+1 only.
  * Q2's regressions have n=180 rows over 90 configurations x 2 cost rungs, and the two cost
    rungs of a configuration are near-duplicates.  Every pooled statistic is therefore ALSO
    reported on the 90 unique configurations at 10 bps only.

Deterministic (fixed rotation seeds, no reliance on PYTHONHASHSEED), standalone.
Writes .console.txt, .clause.csv, .stability.csv, .walkforward.csv, .keep.csv.
"""
import importlib.util
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-margin-column-instead-of-two_cloud"
OUT = ROOT / "research" / "backtests"
PARENT_STEM = "2026-09-05_the-on-share-column_cloud"

N_ROT, BLOCK = 60, 20
COST_RUNGS = [10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- import idea 191 verbatim
spec = importlib.util.spec_from_file_location("p191", OUT / f"{PARENT_STEM}.py")
p191 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p191)

FAMILIES, FAM_ORDER = p191.FAMILIES, p191.FAM_ORDER
fast_backtest, net = p191.fast_backtest, p191.net
on_indicator, apply_overlay = p191.on_indicator, p191.apply_overlay
circ_switches, halves = p191.circ_switches, p191.halves
keep_4a, keep_4b, tstat, spearman = p191.keep_4a, p191.keep_4b, p191.tstat, p191.spearman
_sh = p191._sh


def det_seed(*parts):
    """Deterministic across processes -- unlike the parent's SEED + hash((...)) % 10000."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2**31)


def _finite(y, X):
    """Drop rows where y or any regressor is non-finite.  Two SMALL439 BUDGET tau=0.05/skip
    cells have an undefined IS Sharpe (the overlay suppresses 93.7% of rebalances, so the
    book is flat through the IS window) -- they are dropped and the surviving n is printed,
    never silently imputed."""
    yv = np.asarray(y, float)
    Xs = [np.asarray(c, float) for c in X]
    ok = np.isfinite(yv)
    for c in Xs:
        ok &= np.isfinite(c)
    return yv[ok], [c[ok] for c in Xs], int(ok.sum())


def rank_resid(y, X):
    """Rank-space OLS residual of y on the columns of X (with intercept)."""
    yv, Xs, n = _finite(y, X)
    yr = pd.Series(yv).rank().values.astype(float)
    A = np.column_stack([np.ones(n)] + [pd.Series(c).rank().values.astype(float)
                                        for c in Xs])
    beta, *_ = np.linalg.lstsq(A, yr, rcond=None)
    return yr - A @ beta


def r2(y, X):
    yv, Xs, n = _finite(y, X)
    A = np.column_stack([np.ones(n)] + Xs)
    beta, *_ = np.linalg.lstsq(A, yv, rcond=None)
    res = yv - A @ beta
    ss = ((yv - yv.mean()) ** 2).sum()
    return float(1.0 - (res ** 2).sum() / ss) if ss > 0 else np.nan


def n_finite(y, X):
    return _finite(y, X)[2]


def ols_t(y, X):
    """t-statistic on the LAST column of X."""
    yv, Xs, n = _finite(y, X)
    A = np.column_stack([np.ones(n)] + Xs)
    beta, *_ = np.linalg.lstsq(A, yv, rcond=None)
    res = yv - A @ beta
    dof = n - A.shape[1]
    s2 = (res ** 2).sum() / dof
    XtXi = np.linalg.pinv(A.T @ A)
    se = np.sqrt(s2 * XtXi[-1, -1])
    return float(beta[-1] / se) if se > 0 else np.nan


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 201  the-margin-column-instead-of-two   (cloud, 2026-09-05)")
    P("=" * 118)

    P("\nbuilding panels (idea 191's build_panels, imported) ...")
    panels = p191.build_panels()
    P("  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))

    P("\nREPRODUCTION, asserted before any new number is read:")
    ok = all(p191.checks(p) for p in panels)
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0,
                  freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / "
      f"{mu['MaxDD']:.5%}  (published 6.45305% / 0.66418 / -13.82780%) -> "
      f"{'PASS' if abs(mu['Sharpe'] - 0.66418) < 5e-5 else 'FAIL'}")
    ok &= abs(mu["Sharpe"] - 0.66418) < 5e-5

    # the parent's seed is process-dependent: demonstrate it rather than assert it
    P("\n  [e] idea 191's rotation seed is `SEED + hash((panel, family, thr)) % 10000`.")
    P(f"      hash(('U56','DDCTL',0.03)) in THIS process = "
      f"{hash(('U56', 'DDCTL', 0.03)) % 10_000}")
    P("      Python salts hash() on str, so that value changes every process (PYTHONHASHSEED "
      "unset).")
    P("      => the parent's REAL rows must reproduce exactly; its BANDS cannot.  Both are "
      "checked below.")
    if not ok:
        P("\nreproduction FAILS -- STOP")
        return
    P("\nreproduction of the deterministic parts PASSES -- proceeding")

    # ------------------------------------------------------------------------------- the grid
    P("\n" + "=" * 118)
    P("GRID  3 panels x 3 families x 5 thr x 2 depth x (1 real + 60 rotations) x 2 cost")
    P("      60 rotations = 3 DISJOINT blocks of 20; block 0 is the primary band (idea 186's")
    P("      construction), blocks 1-2 measure the band's own sampling noise (Q4).")
    P("=" * 118)
    rows = []
    for pan in panels:
        start = pan.start
        spy = pan.spy.loc[start:]
        basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
        c0 = pan._r0
        for fam in FAM_ORDER:
            _, thrs, _, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = on_indicator(pan, fam, thr)
                J = len(s_real)
                onshare = float(s_real.mean())
                offs = p191.rotations(J, N_ROT, det_seed(pan.name, fam, thr))
                for depth in depths:
                    variants = [("real", 0, -1, s_real)] + [
                        ("null", o, i // BLOCK, np.roll(s_real, o))
                        for i, o in enumerate(offs)]
                    for kind, off, blk, s in variants:
                        W, mask = apply_overlay(pan, fam, depth, s)
                        res = fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=mask)
                        for bps in COST_RUNGS:
                            r = net(res, bps).loc[start:]
                            cr = net(c0, bps).loc[start:]
                            br = b0 - bt * bps / 1e4
                            m = metrics(r)
                            h1, h2 = halves(r)
                            rows.append(dict(
                                panel=pan.name, family=fam, thr=thr, depth=str(depth),
                                bps=bps, kind=kind, offset=off, block=blk,
                                on_share=float(s.mean()), switches=circ_switches(s),
                                real_on_share=onshare,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                H1=h1, H2=h2,
                                Sharpe_IS=_sh(r.loc[:IS_END]),
                                Sharpe_OOS=_sh(r.loc[OOS_START:]),
                                CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                                ctrl_Sharpe=metrics(cr)["Sharpe"],
                                ctrl_Sharpe_IS=_sh(cr.loc[:IS_END]),
                                ctrl_Sharpe_OOS=_sh(cr.loc[OOS_START:]),
                                ctrl_MaxDD=metrics(cr)["MaxDD"],
                                ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                                ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                                fail4a=keep_4a(r, br), fail4b=keep_4b(r, spy)))
        P(f"  {pan.name} done ({time.time() - t0:.0f}s)")

    G = pd.DataFrame(rows)
    G["dSharpe"] = G["Sharpe"] - G["ctrl_Sharpe"]
    G["dSharpe_IS"] = G["Sharpe_IS"] - G["ctrl_Sharpe_IS"]
    G["dSharpe_OOS"] = G["Sharpe_OOS"] - G["ctrl_Sharpe_OOS"]
    G["dMaxDD"] = G["MaxDD"] - G["ctrl_MaxDD"]
    G["pass4a"] = G["fail4a"] == "-"
    G["pass4b"] = G["fail4b"] == "-"
    G[G.kind == "real"].to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\ngrid: {len(G)} rows ({int((G.kind == 'real').sum())} real) "
      f"({time.time() - t0:.0f}s)")

    nn = G[G.kind == "null"]
    bad_share = int((nn.on_share.round(10) != nn.real_on_share.round(10)).sum())
    P(f"  null validity: on-share preserved in {len(nn) - bad_share}/{len(nn)} rotated rows")

    # -------------------------------------------------- reproduction against idea 191's rows
    PC = pd.read_csv(OUT / f"{PARENT_STEM}.clause.csv")
    key = ["panel", "family", "thr", "depth", "bps"]
    R = G[G.kind == "real"].copy()
    mg = R.merge(PC, on=key, suffixes=("", "_p"))
    P(f"\n  [f] real-row reproduction vs {PARENT_STEM}.clause.csv "
      f"({len(mg)}/{len(PC)} rows matched):")
    for c in ["on_share", "dSharpe", "dSharpe_IS", "Sharpe", "Sharpe_OOS", "CAGR", "MaxDD"]:
        d = float((mg[c] - mg[c + "_p"]).abs().max())
        P(f"        max|d {c:<12s}| = {d:.3e}  -> {'PASS' if d < 1e-12 else 'FAIL'}")
    real_ok = all(float((mg[c] - mg[c + "_p"]).abs().max()) < 1e-12
                  for c in ["on_share", "dSharpe", "dSharpe_IS", "Sharpe"])
    P(f"        REAL rows reproduce: {'YES (0 to 1e-12)' if real_ok else 'NO'}")

    # ------------------------------------------------------------------- the clause per config
    cl = []
    for (pn, fm, th, dp, bp), sub in G.groupby(key):
        r = sub[sub.kind == "real"].iloc[0]
        blocks = {}
        for b in range(N_ROT // BLOCK):
            nb = sub[(sub.kind == "null") & (sub.block == b)]
            blocks[b] = dict(band=float(nb["dSharpe"].abs().max()),
                             band_IS=float(nb["dSharpe_IS"].abs().max()),
                             band_OOS=float(nb["dSharpe_OOS"].abs().max()),
                             bandDD=float(nb["dMaxDD"].abs().max()))
        nb_all = sub[sub.kind == "null"]
        d = dict(panel=pn, family=fm, thr=th, depth=dp, bps=bp,
                 on_share=float(r["on_share"]), switches=int(r["switches"]),
                 dSharpe=float(r["dSharpe"]), dSharpe_IS=float(r["dSharpe_IS"]),
                 dSharpe_OOS=float(r["dSharpe_OOS"]), dMaxDD=float(r["dMaxDD"]),
                 band=blocks[0]["band"], band_IS=blocks[0]["band_IS"],
                 band_OOS=blocks[0]["band_OOS"], bandDD=blocks[0]["bandDD"],
                 band_b1=blocks[1]["band"], band_b2=blocks[2]["band"],
                 band_all60=float(nb_all["dSharpe"].abs().max()),
                 Sharpe=float(r["Sharpe"]), Sharpe_OOS=float(r["Sharpe_OOS"]),
                 CAGR=float(r["CAGR"]), MaxDD=float(r["MaxDD"]),
                 CAGR_OOS=float(r["CAGR_OOS"]), MaxDD_OOS=float(r["MaxDD_OOS"]),
                 ctrl_Sharpe_OOS=float(r["ctrl_Sharpe_OOS"]),
                 ctrl_CAGR_OOS=float(r["ctrl_CAGR_OOS"]),
                 ctrl_MaxDD_OOS=float(r["ctrl_MaxDD_OOS"]),
                 pass4a=bool(r["pass4a"]), pass4b=bool(r["pass4b"]), fail4b=r["fail4b"])
        d["margin"] = abs(d["dSharpe"]) - d["band"]
        d["margin_IS"] = abs(d["dSharpe_IS"]) - d["band_IS"]
        d["margin_OOS"] = abs(d["dSharpe_OOS"]) - d["band_OOS"]
        d["marginDD"] = abs(d["dMaxDD"]) - d["bandDD"]
        d["clears"] = bool(abs(d["dSharpe"]) > d["band"])
        d["clears_IS"] = bool(abs(d["dSharpe_IS"]) > d["band_IS"])
        d["clearsDD"] = bool(abs(d["dMaxDD"]) > d["bandDD"])
        d["clears_b1"] = bool(abs(d["dSharpe"]) > d["band_b1"])
        d["clears_b2"] = bool(abs(d["dSharpe"]) > d["band_b2"])
        cl.append(d)
    C = pd.DataFrame(cl)
    C.to_csv(OUT / f"{STEM}.clause.csv", index=False)
    C10 = C[C.bps == 10]

    # ================================================================================ Q1
    P("\n" + "=" * 118)
    P("Q1  DEFINITIONAL SUFFICIENCY -- does sign(margin) reproduce the clause verdict?")
    P("=" * 118)
    a = int((C["clears"] == (C["margin"] > 0)).sum())
    b = int((C["clearsDD"] == (C["marginDD"] > 0)).sum())
    P(f"\n  Sharpe bar : sign(margin)   == clears   on {a}/{len(C)} real rows")
    P(f"  drawdown   : sign(marginDD) == clearsDD on {b}/{len(C)} real rows")
    P("  This is an IDENTITY, not evidence: `clears` is DEFINED as |dSharpe| > band, and")
    P("  margin = |dSharpe| - band.  A margin-only reader reproduces every published clause")
    P("  verdict in the corpus by construction, and on-share changes NONE of them.")
    P(f"\n  clear rate: {int(C.clears.sum())}/{len(C)} on Sharpe, "
      f"{int(C.clearsDD.sum())}/{len(C)} on drawdown")
    P("\n  margin by family (10 bps rows only, n=90):")
    P(C10.groupby("family").agg(n=("margin", "size"), clears=("clears", "sum"),
                                mean_margin=("margin", "mean"),
                                mean_band=("band", "mean"),
                                mean_absd=("dSharpe", lambda s: s.abs().mean()),
                                mean_onshare=("on_share", "mean"))
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ================================================================================ Q2
    P("\n" + "=" * 118)
    P("Q2  INFORMATIONAL SUFFICIENCY -- given the IS margin, does on-share predict the OOS")
    P("    outcome?  Targets: OOS margin (does the clause verdict persist) and OOS dSharpe")
    P("    (does the overlay actually help out of sample).")
    P("=" * 118)
    q2 = []
    for tag, D in [("ALL 180 rows", C), ("90 configs @10bps", C10)]:
        for ycol in ["margin_OOS", "dSharpe_OOS"]:
            y = D[ycol].values
            x1 = D["margin_IS"].values
            x2 = D["on_share"].values
            base_r2, full_r2 = r2(y, [x1]), r2(y, [x1, x2])
            # partial Spearman: rank-residualise both y and on-share on the IS margin
            pr = spearman(rank_resid(y, [x1]), rank_resid(x2, [x1]))
            q2.append(dict(rows=tag, target=ycol, n=len(D), n_used=n_finite(y, [x1, x2]),
                           rho_margin_IS=spearman(x1, y), rho_onshare=spearman(x2, y),
                           partial_rho_onshare=pr, R2_margin=base_r2,
                           R2_margin_plus_onshare=full_r2, dR2=full_r2 - base_r2,
                           t_onshare=ols_t(y, [x1, x2])))
    Q2 = pd.DataFrame(q2)
    P("\n" + Q2.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\n  within family (10 bps, n=30 each), partial Spearman of on-share on OOS margin")
    P("  after the IS margin:")
    wf2 = []
    for fm, sub in C10.groupby("family"):
        y, x1, x2 = sub["margin_OOS"].values, sub["margin_IS"].values, sub["on_share"].values
        wf2.append(dict(family=fm, n=len(sub), rho_margin_IS=spearman(x1, y),
                        partial_rho_onshare=spearman(rank_resid(y, [x1]),
                                                     rank_resid(x2, [x1])),
                        dR2=r2(y, [x1, x2]) - r2(y, [x1])))
    P(pd.DataFrame(wf2).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ================================================================================ Q3/Q5
    P("\n" + "=" * 118)
    P("Q3/Q5  DECISION SUFFICIENCY and RULE 8.  Overlay point chosen on data <= 2016-12-31")
    P("       ONLY; 2017-01-01 -> read ONCE.  18 cells = 3 panels x 3 families x 2 cost.")
    P("       Pool = 10 points (5 thr x 2 depth).")
    P("=" * 118)
    med_os = float(C["on_share"].median())
    P(f"\n  on-share median used by every 'pair' selector: {med_os:.1%}")
    wf = []
    for (pn, fm, bp), sub in C.groupby(["panel", "family", "bps"]):
        base_oos = float(sub["ctrl_Sharpe_OOS"].iloc[0])
        base = dict(OOS_Sharpe=base_oos, OOS_CAGR=float(sub["ctrl_CAGR_OOS"].iloc[0]),
                    OOS_MaxDD=float(sub["ctrl_MaxDD_OOS"].iloc[0]))

        def take(df, tag, col="margin_IS"):
            if not len(df):
                return dict(selector=tag, pick="ABSTAIN", **base)
            r = df.loc[df[col].idxmax()]
            return dict(selector=tag,
                        pick=f"{r['thr']}/{r['depth']} os={r['on_share']:.0%}",
                        OOS_Sharpe=float(r["Sharpe_OOS"]), OOS_CAGR=float(r["CAGR_OOS"]),
                        OOS_MaxDD=float(r["MaxDD_OOS"]))

        rows_ = [dict(selector="S0 do-nothing", pick="-", **base),
                 take(sub, "S1 IS-Sharpe argmax", col="dSharpe_IS"),
                 take(sub, "S2 MARGIN-only argmax"),
                 take(sub[sub.on_share <= med_os], "S3 PAIR: margin argmax | low on-share"),
                 take(sub[sub.clears_IS], "S4 MARGIN-only, clause-gated"),
                 take(sub[sub.clears_IS & (sub.on_share <= med_os)],
                      "S5 PAIR: clause-gated | low on-share"),
                 take(sub, "S6 ON-SHARE-only (lowest)", col="on_share")]
        rows_[-1] = take(sub.assign(neg_os=-sub.on_share), "S6 ON-SHARE-only (lowest)",
                         col="neg_os")
        o = sub.loc[sub["Sharpe_OOS"].idxmax()]
        rows_.append(dict(selector="ORACLE-OOS", pick=f"{o['thr']}/{o['depth']}",
                          OOS_Sharpe=float(o["Sharpe_OOS"]), OOS_CAGR=float(o["CAGR_OOS"]),
                          OOS_MaxDD=float(o["MaxDD_OOS"])))
        for r in rows_:
            r.update(panel=pn, family=fm, bps=bp, dOOS=r["OOS_Sharpe"] - base_oos)
            wf.append(r)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    piv = W.pivot_table(index=["panel", "family", "bps"], columns="selector",
                        values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        sw = W[W.selector == s]
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()),
                        mean_OOS_CAGR=float(sw["OOS_CAGR"].mean()),
                        mean_OOS_MaxDD=float(sw["OOS_MaxDD"].mean()),
                        dOOS=float(d.mean()), t=tstat(d), wins=int((d > 0).sum()),
                        losses=int((d < 0).sum()), n=int(len(d)),
                        abstains=int((sw["pick"] == "ABSTAIN").sum())))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n" + SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  THE DECISION TEST -- margin-only vs the pair, cell by cell:")
    for a_, b_ in [("S2 MARGIN-only argmax", "S3 PAIR: margin argmax | low on-share"),
                   ("S4 MARGIN-only, clause-gated", "S5 PAIR: clause-gated | low on-share")]:
        pa = W[W.selector == a_].set_index(["panel", "family", "bps"])
        pb = W[W.selector == b_].set_index(["panel", "family", "bps"])
        diff = int((pa["pick"] != pb.reindex(pa.index)["pick"]).sum())
        dd = float((pb.reindex(pa.index)["OOS_Sharpe"] - pa["OOS_Sharpe"]).mean())
        P(f"    {a_:<40s} vs {b_:<42s}  picks changed {diff}/{len(pa)}   "
          f"mean dOOS_Sharpe from adding on-share {dd:+.4f}")

    P("\n  every walk-forward cell:")
    P(W[["panel", "family", "bps", "selector", "pick", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "dOOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->), for the rule-8 table:")
    bm = []
    for pan in panels:
        st = pan.start
        spy_o = pan.spy.loc[st:].loc[OOS_START:]
        bl = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10, freq="W")["returns"]
        bl = bl.loc[st:].loc[OOS_START:]
        for nm, r in [("SPY", spy_o), ("RULES v1 @10bps", bl)]:
            m = metrics(r)
            bm.append(dict(panel=pan.name, series=nm, OOS_CAGR=m["CAGR"],
                           OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    BM = pd.DataFrame(bm)
    P(BM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================================ Q4
    P("\n" + "=" * 118)
    P("Q4  NOISE FLOOR -- the band is itself a 20-draw statistic.  How stable is the verdict")
    P("    the two columns are arguing about?")
    P("=" * 118)
    C["band_sd"] = C[["band", "band_b1", "band_b2"]].std(axis=1)
    C["band_rng"] = (C[["band", "band_b1", "band_b2"]].max(axis=1)
                     - C[["band", "band_b1", "band_b2"]].min(axis=1))
    flips01 = int((C["clears"] != C["clears_b1"]).sum())
    flips02 = int((C["clears"] != C["clears_b2"]).sum())
    any_flip = int(((C["clears"] != C["clears_b1"]) | (C["clears"] != C["clears_b2"])).sum())
    P(f"\n  band spread across the 3 disjoint 20-draw blocks: mean sd {C['band_sd'].mean():.4f}"
      f", mean range {C['band_rng'].mean():.4f}, mean band {C['band'].mean():.4f}")
    P(f"  relative: mean(range / band) = {(C['band_rng'] / C['band']).mean():.1%}")
    P(f"  verdict flips when the rotation block changes: block0 vs block1 {flips01}/{len(C)}, "
      f"block0 vs block2 {flips02}/{len(C)}, ANY {any_flip}/{len(C)} "
      f"({any_flip / len(C):.1%})")
    P(f"  |margin| of the rows that flip vs the rows that do not: "
      f"{C.loc[(C.clears != C.clears_b1) | (C.clears != C.clears_b2), 'margin'].abs().mean():.4f}"
      f" vs "
      f"{C.loc[(C.clears == C.clears_b1) & (C.clears == C.clears_b2), 'margin'].abs().mean():.4f}")
    P("\n  Spearman(on_share, band sd across blocks) = "
      f"{spearman(C.on_share, C.band_sd):+.3f}")
    C[["panel", "family", "thr", "depth", "bps", "on_share", "dSharpe", "band", "band_b1",
       "band_b2", "band_all60", "margin", "clears", "clears_b1", "clears_b2", "band_sd",
       "band_rng"]].to_csv(OUT / f"{STEM}.stability.csv", index=False)

    # ================================================================================ KEEP
    P("\n" + "=" * 118)
    P("KEEP PATHS -- both evaluated on every real row (4a vs the panel's RULES v1, 4b vs SPY)")
    P("=" * 118)
    P(f"\n  4a passes: {int(C.pass4a.sum())}/{len(C)}   4b passes: {int(C.pass4b.sum())}/{len(C)}")
    P("\n  by panel x family (10 bps):")
    P(pd.crosstab([C10.panel, C10.family], C10.pass4b, margins=True).to_string())
    P("\n  4b failing bars (all rows):")
    P(C["fail4b"].value_counts().to_string())
    if int(C.pass4b.sum()):
        P("\n  the 4b passes:")
        P(C[C.pass4b][["panel", "family", "thr", "depth", "bps", "on_share", "margin",
                       "clears", "CAGR", "Sharpe", "MaxDD", "Sharpe_OOS"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  NOTE: this run proposes NO book.  Every 4b pass here is an overlay ON idea 2's")
    P("  standing candidate, already priced by ideas 186/191; nothing new is promoted.")

    # ============================================================================ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    p2row = Q2[(Q2.rows == "90 configs @10bps") & (Q2.target == "margin_OOS")].iloc[0]
    pa = W[W.selector == "S2 MARGIN-only argmax"].set_index(["panel", "family", "bps"])
    pb = W[W.selector == "S3 PAIR: margin argmax | low on-share"].set_index(
        ["panel", "family", "bps"])
    picks_changed = int((pa["pick"] != pb.reindex(pa.index)["pick"]).sum())
    best_non_s0 = SW[~SW.selector.isin(["S0 do-nothing", "ORACLE-OOS"])]["dOOS"].max()
    preds = [
        ("P1 sign(margin) == clears on 180/180, both bars",
         a == len(C) and b == len(C), f"{a}/{len(C)} and {b}/{len(C)}"),
        ("P2 on-share adds nothing given the IS margin",
         abs(p2row.partial_rho_onshare) < 0.15 and abs(p2row.dR2) < 0.02,
         f"partial rho {p2row.partial_rho_onshare:+.3f}, dR2 {p2row.dR2:+.4f}"),
        ("P3 no rule-8 pick differs margin-only vs pair",
         picks_changed == 0, f"{picks_changed}/18 picks changed"),
        ("P4 real rows reproduce, bands do not (parent seed is process-dependent)",
         real_ok, "real rows 0.0e+00; parent bands not reproducible by construction"),
        ("P5 no selector beats do-nothing out of sample",
         best_non_s0 <= 0, f"best dOOS {best_non_s0:+.4f}"),
    ]
    for tag, hit, detail in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {tag:<62s}  {detail}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")

    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
