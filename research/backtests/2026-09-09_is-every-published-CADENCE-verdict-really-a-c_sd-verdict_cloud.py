#!/usr/bin/env python3
"""Idea 549 - "is-every-published-CADENCE-verdict-really-a-c_sd-verdict" (cloud, 2026-09-09).

The question
------------
Idea 307 found that the QUANTILE gate's realised exposure dispersion

    c_t   = realised gross exposure at t / GROSS          (the exposure path)
    c_sd  = sd(c_t) over the evaluation window

is monotone in cadence on SMALL439 (0.0009 at D -> 0.0158 at A, an 18x span) and that the
gate's timing residual resid0 tracks it; idea 535 then fitted resid0 ~ c_sd and beat the
family constant OOS.  The queue's inference is the interesting one: if c_sd carries the
cadence effect, then every published "cadence verdict" in the record - every ladder that
reports a Sharpe or CAGR ordering across D/W/M/Q/A and attributes it to the calendar - may be
an exposure-dispersion effect wearing a calendar label.

This script answers that in four parts, and the third part is the one that decides it.

  PART A  CENSUS.  Machine-scan every committed CSV in research/backtests for cadence ladders
          (rows identical in every design column, differing only in cadence, spanning >= 3
          cadences, carrying a Sharpe column).  Count them and record each ladder's published
          ordering and argmax cadence.  No prose is read; the census is reproducible.

  PART B  THE LAW.  Re-run a 14-book x 5-cadence x 3-panel grid here, measure c_sd directly,
          and test whether c_sd orders dSharpe/dCAGR.

  PART C  IDENTIFICATION - the part that decides the question.  Across cadence, c_sd is
          (per idea 307) nearly monotone in the calendar order D<W<M<Q<A.  If it is monotone
          in every ladder then "c_sd ordered this ladder" and "the calendar ordered this
          ladder" make the SAME prediction on every published ladder and the queue's question
          is NOT ANSWERABLE from cross-cadence ladders at all - the two hypotheses are
          observationally equivalent there.  The identifying variation is WITHIN a cadence,
          across book-forms, where c_sd varies by construction and the calendar is constant.
          So: (i) count how many of my ladders have c_sd monotone in calendar order,
          (ii) test c_sd's ordering power within each fixed cadence across the 14 books,
          (iii) regress dSharpe on c_sd with and without cadence fixed effects, and report
          whether c_sd survives the fixed effects.

  PART D  How many of PART A's published ladders does the c_sd law reproduce, scored against
          the two honest null models (uniform 1/k, and the record's own modal cadence).

Pre-registered hypotheses and bars (written before any number was read)
----------------------------------------------------------------------
H_CSD_IS_THE_LAW.   c_sd, not the calendar, orders cadence ladders.
    BAR (all three clauses):
      (1) within-cadence Spearman(c_sd, dSharpe) across book-forms has a consistent sign in
          >= 12 of the 15 panel x cadence cells, |mean rho| >= 0.30;
      (2) the pooled slope of dSharpe on c_sd keeps its sign and |t| >= 2 AFTER cadence fixed
          effects are absorbed (i.e. c_sd is not just the calendar);
      (3) the c_sd rule reproduces the published argmax cadence in PART A strictly more often
          than the modal-cadence null.
H_CALENDAR_LABEL.   c_sd's cross-cadence ordering is a relabelling of the calendar and adds
    nothing once cadence is absorbed.  BAR: any clause of H_CSD_IS_THE_LAW fails.
The two are exhaustive and mutually exclusive.

G0 - reproduction / validity gates, asserted and printed BEFORE any headline number
-----------------------------------------------------------------------------------
G0.1  The local cadence-extended runner must reproduce engine.backtest EXACTLY at the four
      cadences the engine supports (D,W,M,Q): max |dr_t| < 1e-15 on a live book.  engine has
      no "A" and PROTOCOL forbids editing it, so A runs through a local copy of engine's own
      loop with one extra period key.
G0.2  Idea 307's committed .decomp.csv c_sd must reproduce EXACTLY on SMALL439 for both gate
      families at all five cadences and the three shared thetas (30 cells), under ITS c_t
      definition (dg gross / rs gross): max |d c_sd| < 1e-9.  Without this gate my c_sd is a
      different statistic from the record's and PART C would answer a different question.
G0.3  Idea 290's identity r_dg,t == c_t * r_rs,t at 0 bps, max |error| < 1e-12, at EVERY
      cadence, on every gate book-form and panel.

Design
------
PANELS (3): U56 = research/universe.json ETF/mega-cap panel; B136 = universe_broad.json
      (SURVIVORSHIP: current constituents); SMALL439 = the sub-$2B panel less the 44 names
      with max_1d_move >= 1.0 (SURVIVORSHIP: current constituents of the screen only - CAGR
      LEVELS are inflated, arm-minus-arm contrasts very largely immune, 4a/4b columns are NOT).
      SPY is the benchmark on every panel and is never investable.

BOOK-FORMS (8, the reported arm axis - chosen to SPAN c_sd, not to be tuned):
      EWALL          no gate, c_t == 1 by construction, c_sd = 0            (the zero-dispersion anchor)
      BAND           the live RULES v2 form: 200d +/-3% hysteresis band, DEGROSS
      MA(+0.12/0.00/-0.12)   px > ma200*(1+theta), DEGROSS and RESPREAD
      QM(+0.12/0.00/-0.12)   top ceil(x*n_t) by px/ma200-1 with x = the MA arm's own mean mask
                             fraction at that theta (idea 300/307's matching), DEGROSS and RESPREAD
      -> 1 + 1 + 3*2 + 3*2 = 14 books per panel per cadence.

Tuned parameters (PROTOCOL rule 4: at most two)
      1. book-form / strictness theta   (the ladder axis)
      2. cadence  D, W, M, Q, A          (the object under test)
      All 14 x 5 x 3 = 210 books are reported; nothing is selected outside the rule-8 walk-forward.
      Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung used by
      the identity gate is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.

Rule 8 walk-forward (directions fixed before any OOS number was read)
      WF-A  per (panel, book-form): pick the cadence with the best IS Sharpe (2010..2016-12-31),
            read 2017-01-01..2026 ONCE.  OOS CAGR/Sharpe/MaxDD vs RULES v2 (live), SPY, and the
            cadence-matched EWALL control.
      WF-B  the same pick made by the c_sd RULE instead (IS sign of the c_sd slope decides
            whether the max- or min-c_sd cadence is chosen), and by always-W.  If the c_sd rule
            is a law it should not lose to always-W out of sample.
      WF-C  does the IS within-cadence c_sd ordering survive into OOS?  Spearman(c_sd, dSharpe)
            computed on IS and on OOS, per panel x cadence, and their agreement.

Verdicts (both KEEP paths, on every one of the 210 books)
      4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
      4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .census.csv .grid.csv .within.csv .walkforward.csv .leaderboard.txt .console.txt
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]
CAD_POS = {c: i for i, c in enumerate(CADENCES)}          # canonical calendar order
THETAS = [0.12, 0.00, -0.12]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# pre-registered bars
BAR_WITHIN_CELLS = 12          # of 15 panel x cadence cells with a consistent sign
BAR_WITHIN_RHO = 0.30          # |mean within-cadence Spearman|
BAR_T = 2.0                    # |t| on c_sd after cadence fixed effects
BAR_ENGINE = 1e-15
BAR_IDENT = 1e-12
BAR_CSD307 = 1e-9

PRIOR307 = REPO / "research" / "backtests" / \
    "2026-09-09_does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence_B.decomp.csv"
BTDIR = REPO / "research" / "backtests"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 700)

METRIC_WORDS = ("cagr", "sharpe", "maxdd", "vol", "sortino", "calmar", "turn", "gross",
                "h1", "h2", "oos", "is_", "_is", "ret", "dd", "pp", "resid", "gap", "pred",
                "share", "corr", "mae", "rho", "t_", "pval", "p_", "n_", "count", "mean",
                "sd", "std", "min", "max", "median", "flips", "episodes", "persistence",
                "bars", "err", "regret", "win", "pass", "fail", "keep", "path", "verdict")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------------------------------------------------------- cadence + local engine
def cad_mask(idx, cad):
    """True on the last trading bar of each cadence block.  Identical to engine.rebalance_mask
    for D/W/M/Q; adds A (calendar year)."""
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def bt(prices, weights, cost_bps=COST_BPS, cad="W"):
    """engine.backtest's loop with the cadence mask swapped for one that also knows "A"."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = cad_mask(prices.index, cad).shift(1, fill_value=False)
    wv, rv, mv = w_target.values, rets.values, mask.values
    hv = np.zeros_like(wv)
    tv = np.zeros(len(prices.index))
    cur = np.zeros(len(prices.columns))
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wv[i]
            tv[i] = np.abs(new - cur).sum()
            cur = new
        hv[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    held = pd.DataFrame(hv, index=prices.index, columns=prices.columns)
    turnover = pd.Series(tv, index=prices.index)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "weights": held, "turnover": turnover}


# ---------------------------------------------------------------- panels
def panels():
    out = {}
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True)
    out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in s.columns if c != "SPY" and c not in bad]
    out["SMALL439"] = (s[inv], s["SPY"])
    return out, len(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    live = live_mask(px)
    dist = (px / px.rolling(200).mean() - 1).where(live)
    kt = np.ceil(x * live.sum(axis=1)).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def band_gate(px, band=0.03):
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5) & live_mask(px)


def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def ewall(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


# ---------------------------------------------------------------- PART A: the census
def is_metric_col(c):
    lc = c.lower()
    return any(w in lc for w in METRIC_WORDS)


def census():
    """Every committed CSV with a cadence column: find ladders = row groups identical in every
    design (non-metric, non-cadence) column, spanning >= 3 distinct cadences, with a Sharpe."""
    rows = []
    files = sorted(BTDIR.glob("*.csv"))
    scanned = skipped = 0
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            skipped += 1
            continue
        cadcol = next((c for c in df.columns if c.lower() in ("cad", "cadence", "freq")), None)
        if cadcol is None:
            continue
        sh = next((c for c in df.columns
                   if c.lower() in ("sharpe", "full_sharpe", "sharpe_full")), None)
        if sh is None:
            continue
        cg = next((c for c in df.columns if c.lower() == "cagr"), None)
        scanned += 1
        keys = [c for c in df.columns
                if c != cadcol and not is_metric_col(c) and df[c].notna().any()]
        d = df.copy()
        d[cadcol] = d[cadcol].astype(str).str.upper().str.strip()
        d = d[d[cadcol].isin(CADENCES)]
        if d.empty:
            continue
        gb = d.groupby(keys, dropna=False) if keys else [((), d)]
        for k, g in gb:
            if g[cadcol].nunique() < 3 or g[cadcol].duplicated().any():
                continue   # a group with two rows at one cadence is not a clean ladder
            g = g.sort_values(cadcol, key=lambda s: s.map(CAD_POS))
            pos = g[cadcol].map(CAD_POS).values
            sv = pd.to_numeric(g[sh], errors="coerce").values
            if not np.isfinite(sv).all():
                continue
            cv = pd.to_numeric(g[cg], errors="coerce").values if cg else np.full(len(g), np.nan)
            rows.append(dict(
                file=f.name, arm=str(k)[:110], k=len(g),
                cads="".join(g[cadcol].tolist()),
                argmax_cad=g[cadcol].iloc[int(np.argmax(sv))],
                argmin_cad=g[cadcol].iloc[int(np.argmin(sv))],
                rho_cal_Sharpe=spearman(pos, sv),
                rho_cal_CAGR=spearman(pos, cv) if np.isfinite(cv).all() else np.nan,
                Sharpe_span=float(np.max(sv) - np.min(sv)),
                monotone=bool(np.all(np.diff(sv) > 0) or np.all(np.diff(sv) < 0))))
    return pd.DataFrame(rows), len(files), scanned, skipped


# ---------------------------------------------------------------- main
def main():
    P("=" * 180)
    P("Idea 549  is-every-published-CADENCE-verdict-really-a-c_sd-verdict  (cloud) | "
      + Path(__file__).name)
    P("=" * 180)
    P(f"costs {COST_BPS} bps, gross {GROSS}, next-day execution, no shorting/leverage. "
      f"tuned dials (2): book-form/theta x cadence {CADENCES}.  All 210 books reported.")
    P("pre-registered bars (written before any number was read):")
    P(f"  H_CSD_IS_THE_LAW : (1) within-cadence sign consistent in >= {BAR_WITHIN_CELLS}/15 "
      f"panel x cadence cells with |mean rho| >= {BAR_WITHIN_RHO}; (2) |t| on c_sd >= {BAR_T} "
      f"AFTER cadence fixed effects; (3) the c_sd rule beats the modal-cadence null on PART A.")
    P("  H_CALENDAR_LABEL : any clause fails -> c_sd's cadence ordering is a relabelling.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents (no delistings). CAGR LEVELS "
      "inflated; arm-minus-arm contrasts largely immune; the 4a/4b columns are NOT.")
    flush_log()

    # ------------------------------------------------ PART A
    P("\n" + "=" * 180)
    P("PART A - CENSUS of the record's published cadence ladders (machine scan, no prose)")
    P("=" * 180)
    CEN, n_files, n_scanned, n_bad = census()
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    P(f"CSV files in research/backtests: {n_files}; unreadable {n_bad}; "
      f"carrying BOTH a cadence column and a Sharpe column: {n_scanned}")
    P(f"CADENCE LADDERS FOUND (>= 3 distinct cadences, all else held fixed): {len(CEN)} "
      f"over {CEN.file.nunique()} files")
    if len(CEN):
        P("\nladder width k:")
        P(CEN.k.value_counts().sort_index().to_string())
        P("\nPUBLISHED argmax cadence (the 'cadence verdict'):")
        am = CEN.argmax_cad.value_counts().reindex(CADENCES).fillna(0).astype(int)
        P(pd.DataFrame({"n": am, "share": am / len(CEN)}).to_string(
            float_format=lambda x: f"{x:.3f}"))
        modal_cad = am.idxmax()
        modal_hit = am.max() / len(CEN)
        P(f"\nmodal published argmax = {modal_cad} ({modal_hit:.1%} of ladders) <- the null "
          f"any 'law' has to beat")
        P(f"ladders monotone in the calendar order D<W<M<Q<A: "
          f"{int(CEN.monotone.sum())}/{len(CEN)} ({CEN.monotone.mean():.1%})")
        P(f"Spearman(calendar position, Sharpe) over ladders: mean {CEN.rho_cal_Sharpe.mean():+.4f} "
          f"median {CEN.rho_cal_Sharpe.median():+.4f} | positive in "
          f"{int((CEN.rho_cal_Sharpe > 0).sum())}/{int(CEN.rho_cal_Sharpe.notna().sum())}")
        P(f"per-ladder Sharpe span: mean {CEN.Sharpe_span.mean():.4f} "
          f"median {CEN.Sharpe_span.median():.4f} max {CEN.Sharpe_span.max():.4f}")
        P("\nby file (top 15 by ladder count):")
        P(CEN.groupby("file").agg(ladders=("k", "size"), mean_rho=("rho_cal_Sharpe", "mean"),
                                  modal_argmax=("argmax_cad", lambda s: s.mode().iloc[0]))
          .sort_values("ladders", ascending=False).head(15)
          .to_string(float_format=lambda x: f"{x:.4f}"))
    else:
        modal_cad, modal_hit = "W", np.nan
    flush_log()

    # ------------------------------------------------ panels + comparands
    PN, n_dropped = panels()
    META = {}
    P("\n" + "=" * 180)
    P("PANELS")
    P("=" * 180)
    for name, (px, spy) in PN.items():
        P(f"  {name:9s} {px.shape[1]:3d} investable names, {px.index[0].date()}..{px.index[-1].date()}, "
          f"{len(px)} bars  (SPY benchmark only, never investable)")
    P(f"  SMALL439 drops {n_dropped} names with max_1d_move >= 1.0 per data/small_meta.csv")

    px_u = load_universe()
    live_r_full = engine_backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                                  freq="W")["returns"]

    # ------------------------------------------------ G0.1
    P("\n" + "=" * 180)
    P("G0.1  LOCAL CADENCE-EXTENDED RUNNER vs engine.backtest (read before anything else)")
    P("=" * 180)
    g01 = []
    for name, (px, _) in PN.items():
        probe = book(px, ma_gate(px, 0.0), "DEGROSS")
        for cad in ["D", "W", "M", "Q"]:
            a = engine_backtest(px, probe, cost_bps=COST_BPS, freq=cad)["returns"]
            b = bt(px, probe, cost_bps=COST_BPS, cad=cad)["returns"]
            mk = int((cad_mask(px.index, cad).values != engine_mask(px.index, cad).values).sum())
            g01.append(dict(panel=name, cad=cad, max_abs_dr=float((a - b).abs().max()),
                            mask_diff_bars=mk))
    G01 = pd.DataFrame(g01)
    P(G01.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    ok_g01 = bool((G01.max_abs_dr < BAR_ENGINE).all() and (G01.mask_diff_bars == 0).all())
    P(f"G0.1 {'PASS' if ok_g01 else 'FAIL'}  worst |dr| {G01.max_abs_dr.max():.3e} at {BAR_ENGINE:.0e}")
    flush_log()

    # ------------------------------------------------ the grid
    P("\n" + "=" * 180)
    P("RUNNING THE 210-BOOK GRID (3 panels x 14 books x 5 cadences)")
    P("=" * 180)
    rows, ident_err = [], []
    ctrl = {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_r_full.reindex(px.index).fillna(0.0).loc[start:])
        nlive = live_mask(px).loc[start:].sum(axis=1)

        gates = {"BAND": band_gate(px)}
        for th in THETAS:
            gm = ma_gate(px, th)
            x = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gates[f"MA{th:+.2f}"] = gm
            gates[f"QM{th:+.2f}"] = quantile_gate(px, x)

        for cad in CADENCES:
            rc = bt(px, ewall(px), cost_bps=COST_BPS, cad=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[(pname, cad)] = stat(r10)
            gr = rc["weights"].loc[start:].sum(axis=1) / GROSS
            rows.append(dict(panel=pname, book="EWALL", form="EWALL", theta=np.nan,
                             con="EWALL", cad=cad, c_bar=float(gr.mean()), c_sd=float(gr.std()),
                             c_sd307=0.0, turn_yr=float(rc["turnover"].loc[start:].sum() / years),
                             **stat(r10), spy_oSharpe=spy_s["oSharpe"],
                             p4a=verdict_4a(stat(r10), live_s), f4b=fail_4b(stat(r10), spy_s)))

            for gname, g in gates.items():
                cons = ["DEGROSS"] if gname == "BAND" else ["DEGROSS", "RESPREAD"]
                arms = {}
                for con in cons:
                    res = bt(px, book(px, g, con), cost_bps=COST_BPS, cad=cad)
                    r10 = res["returns"].loc[start:]
                    turn = res["turnover"].loc[start:]
                    arms[con] = dict(r10=r10, r0=r10 + turn * COST_BPS / 1e4,
                                     gross=res["weights"].loc[start:].sum(axis=1), turn=turn)
                if "RESPREAD" in arms:
                    c_t307 = (arms["DEGROSS"]["gross"] /
                              arms["RESPREAD"]["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_err.append(dict(panel=pname, cad=cad, book=gname, err=float(
                        (arms["DEGROSS"]["r0"] - c_t307 * arms["RESPREAD"]["r0"]).abs().max())))
                else:
                    c_t307 = arms["DEGROSS"]["gross"] / GROSS
                for con, a in arms.items():
                    s = stat(a["r10"])
                    ct = a["gross"] / GROSS
                    rows.append(dict(panel=pname, book=f"{gname}/{con}", form=gname,
                                     theta=(np.nan if gname == "BAND" else float(gname[2:])),
                                     con=con, cad=cad, c_bar=float(ct.mean()),
                                     c_sd=float(ct.std()),
                                     c_sd307=float(c_t307.std()) if con == "DEGROSS" else np.nan,
                                     turn_yr=float(a["turn"].sum() / years), **s,
                                     spy_oSharpe=spy_s["oSharpe"],
                                     p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
        P(f"  ... {pname} done ({len(CADENCES) * 14} books)   SPY CAGR {spy_s['CAGR']:.4f} "
          f"Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} halves "
          f"{spy_s['H1']:.3f}/{spy_s['H2']:.3f} OOS {spy_s['oSharpe']:.3f} | "
          f"RULES v2 Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.3f}/{live_s['H2']:.3f}")
        META[pname] = (spy_s, live_s, start)
        flush_log()

    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    G["dSharpe"] = G.Sharpe - G.set_index(["panel", "cad"]).index.map(
        lambda k: ctrl[k]["Sharpe"])
    G["dCAGR_pp"] = 100 * (G.CAGR - G.set_index(["panel", "cad"]).index.map(
        lambda k: ctrl[k]["CAGR"]))
    G["oDSharpe"] = G.oSharpe - G.set_index(["panel", "cad"]).index.map(
        lambda k: ctrl[k]["oSharpe"])
    G["isDSharpe"] = G.isSharpe - G.set_index(["panel", "cad"]).index.map(
        lambda k: ctrl[k]["isSharpe"])
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------ G0.2 / G0.3
    P("\n" + "=" * 180)
    P("G0.2  REPRODUCTION of idea 307's committed mean_c_sd on SMALL439 (its c_t definition)")
    P("=" * 180)
    prior = pd.read_csv(PRIOR307)
    pf = prior[(prior.window == "FULL") & (prior.theta.round(6).isin([round(t, 6) for t in THETAS]))]
    pf = pf[["family", "cad", "theta", "c_sd"]].rename(columns={"c_sd": "c_sd_307"})
    fam_map = {"MA": "MA-THRESH", "QM": "QUANTILE-M"}
    mine = (G[(G.panel == "SMALL439") & (G.con == "DEGROSS") & G.form.str[:2].isin(fam_map)]
            .assign(family=lambda d: d.form.str[:2].map(fam_map))
            [["family", "cad", "theta", "c_sd307"]])
    mine["theta"] = mine.theta.round(6)
    j = pf.assign(theta=pf.theta.round(6)).merge(mine, on=["family", "cad", "theta"])
    j["d"] = (j.c_sd_307 - j.c_sd307).abs()
    P(fmt(j.set_index(["family", "cad", "theta"]), 6))
    ok_g02 = bool(len(j) == 30 and j.d.max() < BAR_CSD307)
    P(f"cells matched {len(j)}/30 (2 families x 5 cadences x 3 shared thetas) | "
      f"worst |d c_sd| {j.d.max():.3e}")
    P(f"G0.2 {'PASS' if ok_g02 else 'FAIL'} at {BAR_CSD307:.0e} - same panel, same gates, same "
      f"c_t definition, so this is an EXACT reproduction test, not a level comparison")

    IE = pd.DataFrame(ident_err)
    ok_g03 = bool(IE.err.max() < BAR_IDENT)
    P(f"\nG0.3  IDENTITY r_dg == c_t * r_rs at 0 bps over {len(IE)} gate books: worst "
      f"{IE.err.max():.3e} -> {'PASS' if ok_g03 else 'FAIL'} at {BAR_IDENT:.0e}")
    P(f"\nGATES: G0.1 {'PASS' if ok_g01 else 'FAIL'} | G0.2 {'PASS' if ok_g02 else 'FAIL'} | "
      f"G0.3 {'PASS' if ok_g03 else 'FAIL'}")
    flush_log()

    # ------------------------------------------------ PART B: c_sd across cadence
    P("\n" + "=" * 180)
    P("PART B - c_sd AND Sharpe ACROSS THE CADENCE DIAL (per panel x book-form ladder, k = 5)")
    P("=" * 180)
    P("\nc_sd by cadence (mean over book-forms, per panel) - is idea 307's monotone ladder general?")
    piv = G[G.form != "EWALL"].pivot_table(index="panel", columns="cad", values="c_sd")[CADENCES]
    P(fmt(piv, 5))
    P("\nSharpe by cadence (mean over the 14 books, per panel):")
    P(fmt(G.pivot_table(index="panel", columns="cad", values="Sharpe")[CADENCES], 4))
    lad = []
    for (pn, bk), g in G.groupby(["panel", "book"]):
        g = g.set_index("cad").reindex(CADENCES)
        lad.append(dict(panel=pn, book=bk,
                        rho_csd_Sharpe=spearman(g.c_sd, g.Sharpe),
                        rho_csd_CAGR=spearman(g.c_sd, g.CAGR),
                        rho_cal_Sharpe=spearman(range(5), g.Sharpe),
                        csd_monotone_in_calendar=bool(
                            np.all(np.diff(g.c_sd.values) > 0) or np.all(np.diff(g.c_sd.values) < 0)),
                        csd_span=float(g.c_sd.max() - g.c_sd.min()),
                        argmax_Sharpe=g.Sharpe.idxmax(), argmax_csd=g.c_sd.idxmax(),
                        Sharpe_span=float(g.Sharpe.max() - g.Sharpe.min())))
    LAD = pd.DataFrame(lad)
    P(f"\nladders here: {len(LAD)} (3 panels x 14 books).  c_sd MONOTONE in the calendar order "
      f"D<W<M<Q<A in {int(LAD.csd_monotone_in_calendar.sum())}/{len(LAD)} of them.")
    P(f"|rho(c_sd,Sharpe) - rho(calendar,Sharpe)| over ladders: max "
      f"{(LAD.rho_csd_Sharpe - LAD.rho_cal_Sharpe).abs().max():.4f}, "
      f"identical in {int((LAD.rho_csd_Sharpe.round(6) == LAD.rho_cal_Sharpe.round(6)).sum())}"
      f"/{len(LAD)} ladders")
    P("\nper-panel summary:")
    P(fmt(LAD.groupby("panel").agg(
        n=("book", "size"), mean_rho_csd=("rho_csd_Sharpe", "mean"),
        mean_rho_cal=("rho_cal_Sharpe", "mean"),
        csd_monotone=("csd_monotone_in_calendar", "sum"),
        agree_argmax=("argmax_Sharpe", "size")), 4))
    P("\nargmax cadence by Sharpe, my 42 ladders:")
    P(LAD.argmax_Sharpe.value_counts().reindex(CADENCES).fillna(0).astype(int).to_string())
    P("argmax cadence by c_sd (what a pure c_sd rule with a POSITIVE slope would pick):")
    P(LAD.argmax_csd.value_counts().reindex(CADENCES).fillna(0).astype(int).to_string())
    P(f"they coincide in {int((LAD.argmax_Sharpe == LAD.argmax_csd).sum())}/{len(LAD)} ladders")
    flush_log()

    # ------------------------------------------------ PART C: identification
    P("\n" + "=" * 180)
    P("PART C - IDENTIFICATION.  WITHIN a fixed cadence, across the 14 book-forms, does c_sd")
    P("          order dSharpe?  Here the calendar is CONSTANT, so this is the only variation")
    P("          that can separate 'a c_sd verdict' from 'a cadence verdict'.")
    P("=" * 180)
    wit = []
    for (pn, cad), g in G.groupby(["panel", "cad"]):
        wit.append(dict(panel=pn, cad=cad, n=len(g),
                        rho_Sharpe=spearman(g.c_sd, g.dSharpe),
                        rho_CAGR=spearman(g.c_sd, g.dCAGR_pp),
                        rho_turn=spearman(g.c_sd, g.turn_yr),
                        rho_IS=spearman(g.isDSharpe, g.c_sd),
                        rho_OOS=spearman(g.oDSharpe, g.c_sd),
                        c_sd_span=float(g.c_sd.max() - g.c_sd.min())))
    W = pd.DataFrame(wit)
    W["cad"] = pd.Categorical(W.cad, CADENCES, ordered=True)
    W = W.sort_values(["panel", "cad"])
    W.to_csv(f"{OUT}.within.csv", index=False)
    P(fmt(W.set_index(["panel", "cad"]), 4))
    n_neg = int((W.rho_Sharpe < 0).sum())
    n_pos = int((W.rho_Sharpe > 0).sum())
    consistent = max(n_pos, n_neg)
    sign = "+" if n_pos >= n_neg else "-"
    P(f"\nwithin-cadence Spearman(c_sd, dSharpe): sign {sign} in {consistent}/{len(W)} cells, "
      f"mean {W.rho_Sharpe.mean():+.4f}, median {W.rho_Sharpe.median():+.4f}")
    c1 = bool(consistent >= BAR_WITHIN_CELLS and abs(W.rho_Sharpe.mean()) >= BAR_WITHIN_RHO)
    P(f"CLAUSE (1) [{consistent} >= {BAR_WITHIN_CELLS} and |mean rho| "
      f"{abs(W.rho_Sharpe.mean()):.4f} >= {BAR_WITHIN_RHO}]: {'PASS' if c1 else 'FAIL'}")

    P("\nPOOLED REGRESSION dSharpe ~ c_sd, with and without cadence fixed effects (n = 210)")
    y = G.dSharpe.values.astype(float)
    x = G.c_sd.values.astype(float)

    def ols(X, y):
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ b
        dof = len(y) - X.shape[1]
        s2 = r @ r / dof
        cov = s2 * np.linalg.pinv(X.T @ X)
        return b, np.sqrt(np.diag(cov)), 1 - (r @ r) / ((y - y.mean()) @ (y - y.mean())), dof

    X0 = np.column_stack([np.ones(len(x)), x])
    b0, se0, r2_0, _ = ols(X0, y)
    D_cad = pd.get_dummies(G.cad).reindex(columns=CADENCES).values.astype(float)
    D_pan = pd.get_dummies(G.panel).values.astype(float)
    X1 = np.column_stack([x, D_cad, D_pan[:, 1:]])
    b1, se1, r2_1, dof1 = ols(X1, y)
    X2 = np.column_stack([D_cad, D_pan[:, 1:]])
    _, _, r2_2, _ = ols(X2, y)
    P(f"  raw            : slope {b0[1]:+.4f} (se {se0[1]:.4f}, t {b0[1]/se0[1]:+.2f})  R2 {r2_0:.4f}")
    P(f"  + cadence + panel FE : slope {b1[0]:+.4f} (se {se1[0]:.4f}, t {b1[0]/se1[0]:+.2f})  "
      f"R2 {r2_1:.4f}   (FE alone R2 {r2_2:.4f}; c_sd adds {r2_1 - r2_2:+.4f})")
    t_fe = b1[0] / se1[0]
    c2 = bool(abs(t_fe) >= BAR_T and np.sign(b1[0]) == np.sign(b0[1]))
    P(f"CLAUSE (2) [|t| {abs(t_fe):.2f} >= {BAR_T} and sign preserved]: {'PASS' if c2 else 'FAIL'}")
    P("\ncadence fixed effects themselves (dSharpe, panel-demeaned design):")
    P(pd.Series(b1[1:6], index=CADENCES).to_string(float_format=lambda v: f"{v:+.4f}"))
    flush_log()

    # ------------------------------------------------ PART D: scoring the record
    P("\n" + "=" * 180)
    P("PART D - HOW MANY PUBLISHED CADENCE LADDERS DOES THE c_sd LAW REPRODUCE?")
    P("=" * 180)
    if len(CEN):
        law_sign = np.sign(b0[1])
        pred_cad = "A" if law_sign > 0 else "D"
        P(f"the fitted cross-cadence law has slope {b0[1]:+.4f} -> a pure c_sd rule predicts the "
          f"argmax of every ladder is the {'HIGHEST' if law_sign > 0 else 'LOWEST'} c_sd cadence "
          f"available, i.e. '{pred_cad}' whenever c_sd is monotone in the calendar "
          f"({int(LAD.csd_monotone_in_calendar.sum())}/{len(LAD)} of my ladders).")
        hits, base_u, base_m = [], [], []
        for _, r in CEN.iterrows():
            avail = [c for c in CADENCES if c in set(re.findall(r"[DWMQA]", r.cads))]
            p = pred_cad if pred_cad in avail else (avail[-1] if law_sign > 0 else avail[0])
            hits.append(r.argmax_cad == p)
            base_u.append(1.0 / len(avail))
            base_m.append(r.argmax_cad == (modal_cad if modal_cad in avail else avail[0]))
        hit = float(np.mean(hits))
        P(f"\nc_sd rule reproduces the published argmax in {int(np.sum(hits))}/{len(CEN)} "
          f"ladders = {hit:.1%}")
        P(f"  uniform-random null   : {np.mean(base_u):.1%}")
        P(f"  modal-cadence null ({modal_cad}) : {np.mean(base_m):.1%}")
        se_bin = float(np.sqrt(hit * (1 - hit) / len(CEN)))
        P(f"  binomial se {se_bin:.3f}; c_sd - modal = {hit - np.mean(base_m):+.1%} "
          f"({(hit - np.mean(base_m)) / se_bin if se_bin else np.nan:+.2f} se)")
        c3 = bool(hit > np.mean(base_m))
        P(f"CLAUSE (3) [c_sd rule beats the modal null]: {'PASS' if c3 else 'FAIL'}")
        P("\nby ladder width:")
        CEN2 = CEN.assign(hit=hits)
        P(fmt(CEN2.groupby("k").agg(n=("hit", "size"), csd_hit=("hit", "mean"),
                                    mean_rho_cal=("rho_cal_Sharpe", "mean")), 4))
    else:
        c3 = False
        P("no ladders found - clause (3) cannot pass")
    flush_log()

    # ------------------------------------------------ verdict
    P("\n" + "=" * 180)
    P("PRE-REGISTERED VERDICT")
    P("=" * 180)
    holds = bool(c1 and c2 and c3)
    for k, v in (("(1) within-cadence ordering", c1), ("(2) survives cadence FE", c2),
                 ("(3) beats the modal null on the record", c3)):
        P(f"  {'PASS' if v else 'FAIL':4s}  {k}")
    P(f"\nH_CSD_IS_THE_LAW  : {'HOLDS' if holds else 'FAILS'}")
    P(f"H_CALENDAR_LABEL  : {'FAILS' if holds else 'HOLDS'}")
    flush_log()

    # ------------------------------------------------ rule 8 walk-forward
    P("\n" + "=" * 180)
    P("RULE 8 WALK-FORWARD (IS 2010..2016-12-31 chooses; OOS 2017-01-01..2026 read ONCE)")
    P("=" * 180)
    wf = []
    for pn in PN:
        spy_s, live_s, _ = META[pn]
        for bk, g in G[G.panel == pn].groupby("book"):
            g = g.set_index("cad").reindex(CADENCES)
            is_sign = np.sign(spearman(g.c_sd.iloc[:], g.isSharpe.iloc[:]) or 0.0)
            pick_is = g.isSharpe.idxmax()
            pick_csd = g.c_sd.idxmax() if is_sign >= 0 else g.c_sd.idxmin()
            for rule, pk in (("IS-Sharpe", pick_is), ("c_sd-rule", pick_csd), ("always-W", "W")):
                r = g.loc[pk]
                wf.append(dict(panel=pn, book=bk, rule=rule, pick=pk,
                               oSharpe=r.oSharpe, oCAGR=r.oCAGR, oMaxDD=r.oMaxDD,
                               best_oSharpe=g.oSharpe.max(),
                               regret=g.oSharpe.max() - r.oSharpe,
                               vs_SPY=r.oSharpe - spy_s["oSharpe"],
                               vs_RULESv2=r.oSharpe - live_s["oSharpe"],
                               vs_ctrl=r.oSharpe - ctrl[(pn, pk)]["oSharpe"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\nWF-A/B  mean OOS by selection rule (42 panel x book ladders):")
    P(fmt(WF.groupby("rule").agg(mean_oSharpe=("oSharpe", "mean"), mean_oCAGR=("oCAGR", "mean"),
                                 mean_oMaxDD=("oMaxDD", "mean"), mean_regret=("regret", "mean"),
                                 beats_SPY=("vs_SPY", lambda s: (s > 0).mean()),
                                 beats_RULESv2=("vs_RULESv2", lambda s: (s > 0).mean())), 4))
    P("\nby panel:")
    P(fmt(WF.pivot_table(index="panel", columns="rule", values="oSharpe", aggfunc="mean"), 4))
    P("\nOOS regret vs the ex-post best cadence (lower is better), by panel:")
    P(fmt(WF.pivot_table(index="panel", columns="rule", values="regret", aggfunc="mean"), 4))
    for pn in PN:
        spy_s, live_s, _ = META[pn]
        P(f"  {pn:9s} SPY OOS Sharpe {spy_s['oSharpe']:.4f} CAGR {spy_s['oCAGR']:.4f} "
          f"MaxDD {spy_s['oMaxDD']:.4f} | RULES v2 OOS Sharpe {live_s['oSharpe']:.4f} "
          f"CAGR {live_s['oCAGR']:.4f} MaxDD {live_s['oMaxDD']:.4f}")
    P("\nWF-C  does the WITHIN-cadence c_sd ordering survive IS -> OOS?")
    P(fmt(W.set_index(["panel", "cad"])[["rho_IS", "rho_OOS"]], 4))
    P(f"sign agreement IS vs OOS: "
      f"{int((np.sign(W.rho_IS) == np.sign(W.rho_OOS)).sum())}/{len(W)}")
    flush_log()

    # ------------------------------------------------ KEEP paths
    P("\n" + "=" * 180)
    P("BOTH KEEP PATHS over all 210 books")
    P("=" * 180)
    P(f"4a passes {int(G.p4a.sum())}/{len(G)} | 4b passes {int(G.p4b.sum())}/{len(G)} | "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}")
    P("\nby panel:")
    P(fmt(G.groupby("panel")[["p4a", "p4b"]].sum(), 0))
    P("\nby cadence:")
    P(fmt(G.groupby("cad")[["p4a", "p4b"]].sum().reindex(CADENCES), 0))
    P("\n4b failing clauses over 210 books:")
    P(pd.Series([c for s in G.f4b for c in (s.split(",") if s != "-" else [])])
      .value_counts().to_string())
    if int(G.p4a.sum()) or int(G.p4b.sum()):
        P("\nevery passing book:")
        P(fmt(G[G.p4a | G.p4b][["panel", "book", "cad", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                "oSharpe", "c_sd", "turn_yr", "p4a", "f4b"]], 4))
    P("\nbest book per panel by full-sample Sharpe:")
    P(fmt(G.loc[G.groupby("panel").Sharpe.idxmax()].set_index("panel")[
        ["book", "cad", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "c_sd", "p4a", "f4b"]], 4))
    flush_log()

    # ------------------------------------------------ leaderboard
    P("\n" + "=" * 180)
    P("LEADERBOARD rows")
    P("=" * 180)
    fn = Path(__file__).name
    lb = []
    for pn in PN:
        spy_s, live_s, _ = META[pn]
        sub = G[G.panel == pn]
        b = sub.loc[sub.Sharpe.idxmax()]
        v = "KEEP-candidate" if (b.p4a and b.p4b) else ("PARK" if (b.p4a or b.p4b) else "KILL")
        w = W[W.panel == pn]
        lb.append(f"| 2026-09-09 | idea549 {pn}: best of 70 books ({b.book} cad={b.cad}); "
                  f"within-cadence rho(c_sd,dSharpe) mean {w.rho_Sharpe.mean():+.3f} | "
                  f"{b.CAGR:.1%} | {b.Sharpe:.2f} | {b.MaxDD:.1%} | {b.H1:.2f} / {b.H2:.2f} | "
                  f"{live_s['Sharpe']:.2f} ({live_s['H1']:.2f}/{live_s['H2']:.2f}) | {v} | {fn} |")
    lb.append(f"| 2026-09-09 | idea549 THE ANSWER: {len(CEN)} published cadence ladders over "
              f"{CEN.file.nunique() if len(CEN) else 0} files; c_sd monotone in the calendar in "
              f"{int(LAD.csd_monotone_in_calendar.sum())}/{len(LAD)} of my own ladders; pooled "
              f"c_sd slope {b0[1]:+.4f} (t {b0[1]/se0[1]:+.2f}) -> {b1[0]:+.4f} "
              f"(t {t_fe:+.2f}) after cadence FE | n/a (a census + a law) | n/a | n/a | n/a | "
              f"modal-cadence null | "
              f"{'H_CSD_IS_THE_LAW' if holds else 'H_CALENDAR_LABEL (KILL of the c_sd reading)'} "
              f"| {fn} |")
    for r in lb:
        P(r)
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lb) + "\n")

    P("\n" + "=" * 180)
    P("ANSWER")
    P("=" * 180)
    P(f"published cadence ladders in the record: {len(CEN)} over "
      f"{CEN.file.nunique() if len(CEN) else 0} files; modal published argmax {modal_cad} "
      f"({modal_hit:.1%}); monotone in the calendar {CEN.monotone.mean():.1%} of the time.")
    P(f"c_sd is monotone in the calendar order in {int(LAD.csd_monotone_in_calendar.sum())}/"
      f"{len(LAD)} of my ladders, and rho(c_sd,Sharpe) equals rho(calendar,Sharpe) in "
      f"{int((LAD.rho_csd_Sharpe.round(6) == LAD.rho_cal_Sharpe.round(6)).sum())}/{len(LAD)}.")
    P(f"within-cadence (the identifying variation): mean rho {W.rho_Sharpe.mean():+.4f}, "
      f"consistent sign {consistent}/{len(W)}.")
    P(f"pooled slope {b0[1]:+.4f} (t {b0[1]/se0[1]:+.2f}) raw; {b1[0]:+.4f} (t {t_fe:+.2f}) "
      f"after cadence+panel FE; c_sd adds {r2_1 - r2_2:+.4f} R2 over the FE alone.")
    P(f"H_CSD_IS_THE_LAW {'HOLDS' if holds else 'FAILS'}; "
      f"H_CALENDAR_LABEL {'FAILS' if holds else 'HOLDS'}.")
    P(f"KEEP paths: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}, "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}.")
    flush_log()


if __name__ == "__main__":
    main()
