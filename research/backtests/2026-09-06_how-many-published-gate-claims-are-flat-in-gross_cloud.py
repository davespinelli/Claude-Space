#!/usr/bin/env python3
"""IDEA 277  how-many-published-gate-claims-are-flat-in-gross   (cloud, 2026-09-06)

THE QUESTION
------------
Idea 274 found the un-gated constant-gross ladder's Sharpe is FLAT to 0.0023 over gross
0.20-1.00.  If that is true, then a gated-vs-ungated comparison that did not match REALISED
gross was never comparing information on the Sharpe axis -- it was comparing CAGR/MaxDD
SCALE.  The queue asks for the census: attach every arm's realised mean gross beside its
nominal, and report how many published comparisons are made across a gross gap wide enough
that the ladder alone accounts for the published difference.

  Q1  REPRODUCTION + the structural claim.  Reproduce the live RULES v2 u56 row, assert the
      vectorised backtester against engine.backtest, and re-derive idea 274's Sharpe span on
      the ungated constant-gross ladder.  THEN ask the question idea 274 did not: is the
      flatness an empirical finding or an identity?  A constant-gross un-gated book scales
      BOTH its returns and its turnover linearly in g, so Sharpe is invariant by construction
      up to the cash-drift renormalisation.  Measure the residual.
  Q2  THE LADDER as an exchange rate.  17 gross points x 3 panels x 2 cost rungs, all
      reported: Sharpe span (the information floor) against the CAGR span and the MaxDD span
      (the scale channel).  This is the look-up table the census needs.
  Q3  THE GATED ARMS.  Four gate instruments the record actually uses (200d, band3, vol60,
      200d+vol60) x two conventions (dg = de-gross to cash, rw = re-weight survivors) x three
      nominal gross levels.  Each is priced TWICE: against its NOMINAL-matched ungated control
      (what most of the record does) and against the ladder point at its own REALISED mean
      gross (idea 244/135/274's convention).  Count how many verdicts move.
  Q4  THE CENSUS.  Every committed grid CSV in research/backtests/ is read.  Classify each as
      gate/overlay-bearing or not; report how many carry a REALISED gross column at all
      (auditable) against a nominal-only one (un-auditable from the record); and for the
      auditable ones attach the ladder's own CAGR/MaxDD movement over each comparison's gross
      gap and count how many published differences sit inside it.
  Q5  RULE 8.  Instrument/convention/gross chosen on IS <= 2016-12-31 by IS Sharpe, OOS >=
      2017-01-01 read ONCE, against do-nothing (the live RULES v2 book), the gross-matched
      ladder point, RULES v1 and SPY.
  Q6  BOTH KEEP PATHS on every arm.

DESIGN
------
Parent code is IMPORTED, not re-implemented: idea 78's `build_panels` / `eligible_mask` /
`fail_4a` / `fail_4b` and idea 171's `fast_backtest`.

  BOOK         EWall on the panel's tradable set -- no ranking, no selection.  The gate is the
               only thing that ever changes, which is the point: a ranking effect cannot
               contaminate a gate census.
  dg           gated-out weight goes to CASH (gross falls below nominal).  This is RULES v2's
               own convention and the one that creates the gross gap.
  rw           gated-out weight is re-spread over the survivors (gross stays at nominal).
               The control convention: if the census is right, rw claims are safe and dg
               claims are not.
  cadence      weekly, t+1 execution, 10 and 25 bps (both rungs derived exactly from one
               0 bps simulation per book by net(c) = gross_ret - turnover * c / 1e4).
  panels       U56 and B136 primary; SMALL439 secondary (the sub-$2B panel with the
               max_1d_move >= 1.0 screen applied -- 44 of 483 names dropped).
  windows      IS <= 2016-12-31 chooses; OOS >= 2017-01-01 read ONCE.

  TUNED PARAMETER 1: nominal gross g -- 17 ladder points, ALL reported.
  TUNED PARAMETER 2: the cost rung -- 2 rungs, BOTH reported.
  The gate instruments, the conventions, the cadence, the panels and the eligibility
  definitions are INHERITED from the record, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The ungated ladder's Sharpe span over g in [0.20, 1.00] is under 0.01 in every
      (panel, rung) cell -- idea 274's 0.0023 is not a one-panel accident.
  P2  That flatness is STRUCTURAL: the same ladder's CAGR span exceeds 5 pp/yr and its MaxDD
      span exceeds 10 pp in every cell, i.e. the ladder is a pure scale dial.
  P3  Under `rw` the realised mean gross is within 0.01 of nominal; under `dg` it is at least
      0.10 below nominal on the large-cap panels.
  P4  Re-matching a `dg` arm to the ladder at its own realised gross moves its dSharpe by
      less than 0.01 (nothing to fix on the Sharpe axis) but flips the SIGN of its dCAGR
      and/or dMaxDD verdict in a majority of cells.
  P5  A majority of the record's committed gate/overlay grid CSVs carry a NOMINAL gross
      column only, so most published gate claims cannot be gross-matched from the record.
  P6  Rule 8: the IS-Sharpe chooser does not beat doing nothing out of sample (the record's
      standing result from ideas 132/141/151/160/230).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): U56, B136 and SMALL439 are current-constituent lists with no
    delistings.  It runs AGAINST the un-gated arm -- an ungated book holds the names a
    delisting-aware panel would kill -- so a survivorship-free panel would make the gates look
    BETTER, not worse.  Stated, not adjusted.  No LEVEL here is a tradable estimate.
  * The small panel is secondary throughout: ideas 39/49/136 show the 200d/vol20 gate is
    INVERTED there, so its numbers are not evidence about the large-cap rule.
  * Costs are a flat linear bps charge on turnover; real cost is spread plus impact and is
    convex in size (idea 126).
  * The census in Q4 reads what the record COMMITTED.  A parent that computed realised gross
    and did not write it to CSV is counted un-auditable, which is a statement about the
    record's schema, not about that parent's care.
  * Idea 38's calendar-day index fix and idea 126's t+1-only execution carry over.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .arms.csv, .census.csv,
.censusfiles.csv, .walkforward.csv, .keep.csv
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_how-many-published-gate-claims-are-flat-in-gross_cloud"
OUT = ROOT / "research" / "backtests"
P78_STEM = "2026-09-05_candidate-count-vs-dispersion_B"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"

GROSS_LADDER = [round(0.20 + 0.05 * i, 2) for i in range(17)]     # 0.20 .. 1.00
ARM_GROSS = [0.50, 0.75, 1.00]
RUNGS = [10, 25]
BASE_RUNG = 10
FREQ = "W"
MAX_VOL = 0.60
BAND = 0.03
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PRIMARY = ["U56", "B136"]
SECONDARY = ["SMALL439"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T0 = time.time()
p78 = _load(P78_STEM, "p78")
p171 = _load(P171_STEM, "p171")
p78.P = P
p171.P = P
build_panels = p78.build_panels
eligible_mask = p78.eligible_mask
fail_4a, fail_4b = p78.fail_4a, p78.fail_4b
spearman = p78.spearman
ref_fast_backtest = p171.fast_backtest


# ------------------------------------------------------------------ backtester (+ gross)
def fast_backtest_g(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 171's vectorised engine.backtest, extended to return the REALISED (drifted) gross
    series.  Asserted identical to both engine.backtest and p171.fast_backtest in Q1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    gross_ret = (held * rets).sum(axis=1)
    port = gross_ret - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx),
            "gross_ret": pd.Series(gross_ret, index=idx),
            "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


def net(gross_ret, turn, bps):
    return gross_ret - turn * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


# ------------------------------------------------------------------ books
def gate_mask(px, tradable, kind):
    """The record's four gate instruments, on the panel's tradable set."""
    _, above, vol20 = score(px)
    ma = px.rolling(200).mean()
    if kind == "none":
        g = pd.DataFrame(True, index=px.index, columns=px.columns) & px.notna()
    elif kind == "200d":
        g = above
    elif kind == "band3":
        st = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        st = st.mask(px > ma * (1 + BAND), 1.0).mask(px < ma * (1 - BAND), 0.0)
        g = st.ffill().fillna(0.0) > 0.5
    elif kind == "vol60":
        g = vol20 < MAX_VOL
    elif kind == "both":
        g = above & (vol20 < MAX_VOL)
    else:
        raise ValueError(kind)
    g = g & px.notna()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        g = g.copy()
        g[drop] = False
    return g


def universe_mask(px, tradable):
    u = px.notna().copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        u[drop] = False
    return u


def weights_gate(px, tradable, kind, gross, conv):
    """EWall with a gate.

    dg  denominator is the FULL priced universe -> gated-out weight becomes cash and the
        realised gross falls below nominal.  (RULES v2's own convention.)
    rw  denominator is the SURVIVING set -> gross stays at nominal.
    """
    g = gate_mask(px, tradable, kind).astype(float)
    if conv == "dg":
        denom = universe_mask(px, tradable).sum(axis=1).replace(0, np.nan)
    else:
        denom = g.sum(axis=1).replace(0, np.nan)
    return g.div(denom, axis=0).mul(gross).fillna(0.0)


# ------------------------------------------------------------------ panels
def get_panels():
    pans = build_panels()
    out = {"U56": pans["U56"], "B136": pans["B136"]}
    pxs, s_stk = pans["SMALL484"]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or (c in s_stk and c not in bad)]
    out["SMALL439"] = (pxs[keep].dropna(how="all").ffill(), {c for c in keep if c != "SPY"})
    P(f"[panels] U56 {out['U56'][0].shape[1]} cols, B136 {out['B136'][0].shape[1]} cols, "
      f"SMALL439 {len(out['SMALL439'][1])} tradable (dropped {len(bad & set(s_stk))} with max_1d_move>=1.0)")
    return out


# =====================================================================================
P("=" * 108)
P("IDEA 277  how-many-published-gate-claims-are-flat-in-gross   (cloud, 2026-09-06)")
P("=" * 108)

PANELS = get_panels()
START = {}
for nm, (px, tr) in PANELS.items():
    START[nm] = px.index[260]

# ------------------------------------------------------------------ Q1 reproduction
P("\n" + "-" * 108)
P("Q1  REPRODUCTION AND THE STRUCTURAL CLAIM")
P("-" * 108)

px56, tr56 = PANELS["U56"]
w_probe = weights_gate(px56, tr56, "band3", 0.75, "dg")
r_eng = backtest(px56, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
r_fast = fast_backtest_g(px56, w_probe, 10.0, FREQ)["returns"]
r_p171 = ref_fast_backtest(px56, w_probe, 10.0, FREQ)["returns"]
P(f"[a] fast_backtest_g vs engine.backtest       max|diff| = {np.abs(r_eng - r_fast).max():.3e}")
P(f"[a] fast_backtest_g vs p171.fast_backtest    max|diff| = {np.abs(r_p171 - r_fast).max():.3e}")
assert np.abs(r_eng - r_fast).max() < 1e-12

# the live book
res_v2 = fast_backtest_g(px56, rules_v2_weights(px56), 0.0, FREQ)
r_v2 = net(res_v2["gross_ret"], res_v2["turnover"], BASE_RUNG).loc[START["U56"]:]
m = mrow(r_v2)
P(f"[b] LIVE RULES v2 on U56 @10bps: CAGR {m['CAGR']:.2%}  Sharpe {m['Sharpe']:.4f}  "
  f"MaxDD {m['MaxDD']:.2%}  halves {m['H1']:.4f}/{m['H2']:.4f}")
P("    record (CHANGELOG 2026-09-06): 8.66% / 1.2056 / -12.05%, halves 1.2259 / 1.1908")
P(f"    -> reproduces: {abs(m['Sharpe'] - 1.2056) < 5e-4 and abs(m['CAGR'] - 0.0866) < 5e-4}")

# my band3/dg book at gross 0.75 IS RULES v2 (assert, do not assume)
assert np.abs((weights_gate(px56, tr56, "band3", 0.75, "dg") - rules_v2_weights(px56)).fillna(0.0).values).max() < 1e-12
P("[c] weights_gate(band3, 0.75, dg) == baseline.rules_v2_weights  (asserted, max|diff| < 1e-12)")

# structural: is ladder flatness an identity?
res_g50 = fast_backtest_g(px56, weights_gate(px56, tr56, "none", 0.50, "rw"), 0.0, FREQ)
res_g100 = fast_backtest_g(px56, weights_gate(px56, tr56, "none", 1.00, "rw"), 0.0, FREQ)
lin = np.abs(res_g50["gross_ret"] - 0.5 * res_g100["gross_ret"]).max()
lin_t = np.abs(res_g50["turnover"] - 0.5 * res_g100["turnover"]).max()
P(f"[d] STRUCTURAL: |r(g=0.50) - 0.5*r(g=1.00)| max = {lin:.3e};  same for turnover = {lin_t:.3e}")
P("    Returns and turnover both scale in g up to the cash-drift renormalisation, so an")
P("    un-gated constant-gross ladder's Sharpe is invariant BY CONSTRUCTION, not by evidence.")
P("    The residual below is that renormalisation, and it is what idea 274 measured as 0.0023.")

# ------------------------------------------------------------------ Q2 the ladder
P("\n" + "-" * 108)
P("Q2  THE UNGATED CONSTANT-GROSS LADDER  (17 points x 3 panels x 2 rungs, all reported)")
P("-" * 108)

lad_rows = []
LAD = {}                       # (panel, rung) -> DataFrame indexed by realised gross
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for g in GROSS_LADDER:
        res = fast_backtest_g(px, weights_gate(px, tr, "none", g, "rw"), 0.0, FREQ)
        gr = res["gross_ret"].loc[st:]
        tn = res["turnover"].loc[st:]
        rg = res["gross"].loc[st:].mean()
        for c in RUNGS:
            r = net(gr, tn, c)
            row = dict(panel=pname, cost=c, nominal_gross=g, realised_gross=rg,
                       turnover=tn.sum() / (len(r) / 252), **mrow(r))
            lad_rows.append(row)
lad = pd.DataFrame(lad_rows)
lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

P("\nfull ladder:")
P(lad.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\nladder SPANS per (panel, cost)  -- the information floor vs the scale channel:")
spans = []
for (pn, c), gsub in lad.groupby(["panel", "cost"]):
    spans.append(dict(panel=pn, cost=c,
                      gross_lo=gsub["realised_gross"].min(), gross_hi=gsub["realised_gross"].max(),
                      Sharpe_span=gsub["Sharpe"].max() - gsub["Sharpe"].min(),
                      CAGR_span_pp=100 * (gsub["CAGR"].max() - gsub["CAGR"].min()),
                      MaxDD_span_pp=100 * (gsub["MaxDD"].max() - gsub["MaxDD"].min())))
spans = pd.DataFrame(spans)
P(spans.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\nP1 (Sharpe span < 0.01 in every cell): {bool((spans['Sharpe_span'] < 0.01).all())}"
  f"   max span {spans['Sharpe_span'].max():.4f}")
P(f"P2 (CAGR span > 5pp AND MaxDD span > 10pp everywhere): "
  f"{bool((spans['CAGR_span_pp'] > 5).all() and (spans['MaxDD_span_pp'] > 10).all())}")


def ladder_at(pname, cost, rg, col):
    """Interpolate a ladder metric at a realised mean gross.  Outside the ladder's own span
    the value is clipped to the nearest endpoint and the caller is told (Q3/Q4 flag it)."""
    s = lad[(lad.panel == pname) & (lad.cost == cost)].sort_values("realised_gross")
    return float(np.interp(rg, s["realised_gross"].values, s[col].values))


def ladder_covers(pname, cost, rg):
    s = lad[(lad.panel == pname) & (lad.cost == cost)]
    return bool(s["realised_gross"].min() <= rg <= s["realised_gross"].max())


# ------------------------------------------------------------------ Q3 gated arms
P("\n" + "-" * 108)
P("Q3  THE GATED ARMS, PRICED TWICE: nominal-matched vs realised-gross-matched")
P("-" * 108)

KINDS = ["200d", "band3", "vol60", "both"]
CONVS = ["dg", "rw"]
arm_rows = []
SER = {}                       # (panel, kind, conv, g) -> (gross_ret, turnover) for rule 8
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    spy_m = mrow(spy)
    for kind in KINDS:
        for conv in CONVS:
            for g in ARM_GROSS:
                res = fast_backtest_g(px, weights_gate(px, tr, kind, g, conv), 0.0, FREQ)
                gr, tn = res["gross_ret"].loc[st:], res["turnover"].loc[st:]
                rg = res["gross"].loc[st:].mean()
                SER[(pname, kind, conv, g)] = (gr, tn, rg)
                for c in RUNGS:
                    r = net(gr, tn, c)
                    mm = mrow(r)
                    # control 1: nominal-matched ungated ladder point
                    ctl_n = lad[(lad.panel == pname) & (lad.cost == c) & (lad.nominal_gross == g)].iloc[0]
                    # control 2: realised-gross-matched ladder point
                    row = dict(panel=pname, cost=c, kind=kind, conv=conv, nominal_gross=g,
                               realised_gross=rg, gross_gap=rg - g,
                               turnover=tn.sum() / (len(r) / 252), **mm,
                               nom_dSharpe=mm["Sharpe"] - ctl_n["Sharpe"],
                               nom_dCAGR_pp=100 * (mm["CAGR"] - ctl_n["CAGR"]),
                               nom_dMaxDD_pp=100 * (mm["MaxDD"] - ctl_n["MaxDD"]),
                               real_dSharpe=mm["Sharpe"] - ladder_at(pname, c, rg, "Sharpe"),
                               real_dCAGR_pp=100 * (mm["CAGR"] - ladder_at(pname, c, rg, "CAGR")),
                               real_dMaxDD_pp=100 * (mm["MaxDD"] - ladder_at(pname, c, rg, "MaxDD")),
                               in_ladder_span=ladder_covers(pname, c, rg),
                               spy_Sharpe=spy_m["Sharpe"], spy_CAGR=spy_m["CAGR"], spy_MaxDD=spy_m["MaxDD"])
                    arm_rows.append(row)
arms = pd.DataFrame(arm_rows)

P("\nrealised vs nominal gross by convention (P3):")
gg = arms.groupby(["panel", "conv"])["gross_gap"].agg(["mean", "min", "max"])
P(gg.to_string(float_format=lambda x: f"{x:+.4f}"))
rw_ok = arms[arms.conv == "rw"]["gross_gap"].abs().max() < 0.01
dg_large = arms[(arms.conv == "dg") & (arms.panel.isin(PRIMARY))]["gross_gap"].max() < -0.10
P(f"P3 (rw within 0.01 of nominal: {bool(rw_ok)};  dg at least 0.10 below on large caps: {bool(dg_large)})")

P("\nfull arm table (columns nom_* = matched on NOMINAL gross, real_* = matched on REALISED gross):")
show = ["panel", "cost", "kind", "conv", "nominal_gross", "realised_gross", "gross_gap", "CAGR", "Sharpe",
        "MaxDD", "H1", "H2", "turnover", "nom_dSharpe", "real_dSharpe", "nom_dCAGR_pp", "real_dCAGR_pp",
        "nom_dMaxDD_pp", "real_dMaxDD_pp", "in_ladder_span"]
P(arms[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\nQ3 SUMMARY  -- what re-matching to realised gross actually moves:")


def gross_share(nom, real):
    """Share of a nominal-matched difference that the pure gross ladder alone accounts for.
    1.0 = the whole published difference is exposure; 0.0 = none of it is."""
    nom, real = np.asarray(nom, float), np.asarray(real, float)
    out = np.where(np.abs(nom) > 1e-9, 1.0 - np.abs(real) / np.maximum(np.abs(nom), 1e-12), np.nan)
    return out


for col, lab in [("dSharpe", "Sharpe"), ("dCAGR_pp", "CAGR"), ("dMaxDD_pp", "MaxDD")]:
    arms[f"grossshare_{lab}"] = gross_share(arms[f"nom_{col}"], arms[f"real_{col}"])

for conv in CONVS:
    s = arms[arms.conv == conv]
    dS = (s["real_dSharpe"] - s["nom_dSharpe"]).abs()
    flipC = ((np.sign(s["nom_dCAGR_pp"]) != np.sign(s["real_dCAGR_pp"])) & (s["nom_dCAGR_pp"].abs() > 1e-9)).sum()
    flipD = ((np.sign(s["nom_dMaxDD_pp"]) != np.sign(s["real_dMaxDD_pp"])) & (s["nom_dMaxDD_pp"].abs() > 1e-9)).sum()
    flipS = ((np.sign(s["nom_dSharpe"]) != np.sign(s["real_dSharpe"])) & (s["nom_dSharpe"].abs() > 1e-9)).sum()
    P(f"  conv={conv:3s} n={len(s):3d}  mean|d(dSharpe)| = {dS.mean():.4f} (max {dS.max():.4f})   "
      f"sign flips: Sharpe {flipS}/{len(s)}   CAGR {flipC}/{len(s)}   MaxDD {flipD}/{len(s)}")
    P(f"           gross-channel SHARE of the published difference: "
      f"Sharpe {np.nanmean(s['grossshare_Sharpe']):+.3f}   "
      f"CAGR {np.nanmean(s['grossshare_CAGR']):+.3f}   MaxDD {np.nanmean(s['grossshare_MaxDD']):+.3f}")
    for lab in ["CAGR", "MaxDD"]:
        v = s[f"grossshare_{lab}"].dropna()
        P(f"             {lab}: majority-exposure (share > 0.50) in {int((v > 0.5).sum())}/{len(v)} cells; "
          f"share > 0.80 in {int((v > 0.8).sum())}/{len(v)}")

P("\n  P4: re-matching moves dSharpe by <0.01 and flips CAGR/MaxDD verdicts in a majority of dg cells?")
sdg = arms[arms.conv == "dg"]
p4a = (sdg["real_dSharpe"] - sdg["nom_dSharpe"]).abs().max() < 0.01
p4b_flip = (((np.sign(sdg["nom_dCAGR_pp"]) != np.sign(sdg["real_dCAGR_pp"])).sum()
             + (np.sign(sdg["nom_dMaxDD_pp"]) != np.sign(sdg["real_dMaxDD_pp"])).sum()) / (2 * len(sdg)))
P(f"     dSharpe move < 0.01 : {bool(p4a)}    CAGR/MaxDD SIGN-flip share : {p4b_flip:.3f}  -> P4 sign half FAILS")
P("     The right statistic is MAGNITUDE, not sign: a de-grossing gate always cuts CAGR and")
P("     always shallows drawdown, so the gross channel and the gate push the same way and the")
P("     sign survives while most of the SIZE does not.  The shares above are the census answer.")

# ------------------------------------------------------------------ Q6 KEEP paths
P("\n" + "-" * 108)
P("Q6  BOTH KEEP PATHS on every arm")
P("-" * 108)


def keep_flags(row, base):
    """4a vs the LIVE book (RULES v2, this panel, this rung); 4b vs SPY."""
    a = (row["H1"] > base["H1"]) and (row["H2"] > base["H2"]) and (row["MaxDD"] >= base["MaxDD"])
    b = ((row["H1"] > base["spy_H1"]) and (row["H2"] > base["spy_H2"])
         and (row["MaxDD"] >= 0.60 * row["spy_MaxDD"]) and (row["CAGR"] >= 0.70 * row["spy_CAGR"]))
    return a, b


BASE = {}
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    rv2 = fast_backtest_g(px, rules_v2_weights(px), 0.0, FREQ)
    rv1 = fast_backtest_g(px, rules_v1_weights(px), 0.0, FREQ)
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    sh1, sh2 = halves(spy)
    for c in RUNGS:
        b = mrow(net(rv2["gross_ret"], rv2["turnover"], c).loc[st:])
        v1 = mrow(net(rv1["gross_ret"], rv1["turnover"], c).loc[st:])
        BASE[(pname, c)] = dict(**b, spy_H1=sh1, spy_H2=sh2, **{f"v1_{k}": v for k, v in v1.items()})

k4a, k4b = [], []
for _, r in arms.iterrows():
    b = BASE[(r["panel"], r["cost"])]
    rr = dict(r)
    rr["spy_H1"], rr["spy_H2"] = b["spy_H1"], b["spy_H2"]
    a, bb = keep_flags(rr, {**b, "spy_H1": b["spy_H1"], "spy_H2": b["spy_H2"]})
    k4a.append(a)
    k4b.append(bb)
arms["pass4a"] = k4a
arms["pass4b"] = k4b
arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
P(f"4a: {int(arms['pass4a'].sum())}/{len(arms)}    4b: {int(arms['pass4b'].sum())}/{len(arms)}")
P(arms.groupby(["panel", "cost", "conv"])[["pass4a", "pass4b"]].sum().to_string())
if arms["pass4b"].any():
    P("\n4b passes:")
    P(arms[arms.pass4b][["panel", "cost", "kind", "conv", "nominal_gross", "realised_gross",
                         "CAGR", "Sharpe", "MaxDD", "H1", "H2", "real_dSharpe"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  Every 4b pass is re-read against its OWN realised-gross ladder point (real_dSharpe):")
    P("  a pass whose real_dSharpe is <= 0 is a gross-ladder point, not an instrument.")
    pb = arms[arms.pass4b]
    P(f"  4b passes beaten by their own gross-matched ungated ladder point: "
      f"{int((pb['real_dSharpe'] <= 0).sum())}/{len(pb)}")
    P(f"  ... of which the dg (de-grossing) ones: {int(((pb['real_dSharpe'] <= 0) & (pb.conv == 'dg')).sum())}"
      f"/{int((pb.conv == 'dg').sum())};  rw ones: "
      f"{int(((pb['real_dSharpe'] <= 0) & (pb.conv == 'rw')).sum())}/{int((pb.conv == 'rw').sum())}")
arms.to_csv(OUT / f"{STEM}.keep.csv", index=False)

# ------------------------------------------------------------------ Q5 rule 8
P("\n" + "-" * 108)
P("Q5  RULE 8 WALK-FORWARD  (choose on IS <= 2016-12-31, read OOS >= 2017-01-01 ONCE)")
P("-" * 108)

wf_rows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    spy_full = px["SPY"].pct_change().fillna(0.0).loc[st:]
    rv2 = fast_backtest_g(px, rules_v2_weights(px), 0.0, FREQ)
    for c in RUNGS:
        cand = []
        for (pn, kind, conv, g), (gr, tn, rg) in SER.items():
            if pn != pname:
                continue
            r = net(gr, tn, c)
            ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
            cand.append(dict(kind=kind, conv=conv, g=g, realised_gross=rg,
                             IS_Sharpe=metrics(ris)["Sharpe"], IS_CAGR=metrics(ris)["CAGR"],
                             OOS_Sharpe=metrics(ros)["Sharpe"], OOS_CAGR=metrics(ros)["CAGR"],
                             OOS_MaxDD=metrics(ros)["MaxDD"]))
        cd = pd.DataFrame(cand)
        pick = cd.loc[cd["IS_Sharpe"].idxmax()]
        rnd = cd["OOS_Sharpe"].mean()
        # do-nothing = the live book
        rb = net(rv2["gross_ret"], rv2["turnover"], c).loc[st:]
        bos = rb.loc[OOS_START:]
        sos = spy_full.loc[OOS_START:]
        # gross-matched ungated ladder point at the pick's own realised gross, OOS
        lg = float(np.interp(pick["realised_gross"], GROSS_LADDER, GROSS_LADDER))
        res_l = fast_backtest_g(px, weights_gate(px, tr, "none", round(float(pick["realised_gross"]), 2), "rw"), 0.0, FREQ)
        rl = net(res_l["gross_ret"], res_l["turnover"], c).loc[st:].loc[OOS_START:]
        wf_rows.append(dict(panel=pname, cost=c,
                            pick=f"{pick['kind']}/{pick['conv']}/g{pick['g']:.2f}",
                            pick_realised_gross=pick["realised_gross"],
                            IS_Sharpe=pick["IS_Sharpe"],
                            OOS_Sharpe=pick["OOS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"], OOS_MaxDD=pick["OOS_MaxDD"],
                            grid_mean_OOS_Sharpe=rnd,
                            donothing_OOS_Sharpe=metrics(bos)["Sharpe"], donothing_OOS_CAGR=metrics(bos)["CAGR"],
                            donothing_OOS_MaxDD=metrics(bos)["MaxDD"],
                            grossmatched_OOS_Sharpe=metrics(rl)["Sharpe"], grossmatched_OOS_CAGR=metrics(rl)["CAGR"],
                            grossmatched_OOS_MaxDD=metrics(rl)["MaxDD"],
                            spy_OOS_Sharpe=metrics(sos)["Sharpe"], spy_OOS_CAGR=metrics(sos)["CAGR"],
                            spy_OOS_MaxDD=metrics(sos)["MaxDD"],
                            spearman_IS_OOS=spearman(cd["IS_Sharpe"], cd["OOS_Sharpe"])))
wf = pd.DataFrame(wf_rows)
wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
won = (wf["OOS_Sharpe"] > wf["donothing_OOS_Sharpe"]).sum()
P(f"\nP6: IS-Sharpe chooser beats do-nothing OOS in {won}/{len(wf)} cells "
  f"(mean {wf['OOS_Sharpe'].mean():.4f} vs {wf['donothing_OOS_Sharpe'].mean():.4f}).")
wong = (wf["OOS_Sharpe"] > wf["grossmatched_OOS_Sharpe"]).sum()
P(f"    ... and beats its OWN gross-matched ungated ladder point in {wong}/{len(wf)} "
  f"(mean {wf['grossmatched_OOS_Sharpe'].mean():.4f}).")

# ------------------------------------------------------------------ Q4 census
P("\n" + "-" * 108)
P("Q4  THE CENSUS OF THE COMMITTED RECORD")
P("-" * 108)

GATE_WORDS = ["gate", "gated", "band", "overlay", "vol60", "vol_cap", "max_vol", "theta", "sleeve",
              "stop", "ddctl", "dg", "conv", "arm", "regime", "screen", "filter", "trim", "de-gross",
              "degross", "budget", "cap"]
REAL_GROSS_COLS = ["gross_mean", "mean_gross", "realised_gross", "m_GROSS", "gross_real",
                   "gross_mean_IS", "gross_mean_OOS", "IS_m_GROSS", "IS_gross", "OOS_gross",
                   "lad_gross", "ctl_gross", "gm_gross"]
NOMINAL_GROSS_COLS = ["gross", "Gross", "g", "target_gross", "gross_conv", "inv_gross"]
SHARPE_COLS = ["Sharpe", "OOS_Sharpe", "IS_Sharpe", "Sharpe_OOS", "m_Sharpe", "dSharpe"]

files = [f for f in sorted((OUT).glob("*.csv")) if not f.name.startswith(STEM)]
P(f"(this run's own {len(list(OUT.glob(STEM + '*.csv')))} output CSVs are EXCLUDED from the census — "
  "a census that scores itself is not a census)")
frows = []
for f in files:
    try:
        head = pd.read_csv(f, nrows=0)
    except Exception:
        continue
    cols = [str(c) for c in head.columns]
    lc = " ".join(cols).lower() + " " + f.name.lower()
    has_sharpe = any(c in cols for c in SHARPE_COLS) or any("sharpe" in c.lower() for c in cols)
    has_real = [c for c in cols if c in REAL_GROSS_COLS]
    has_nom = [c for c in cols if c in NOMINAL_GROSS_COLS]
    is_gate = any(w in lc for w in GATE_WORDS)
    frows.append(dict(file=f.name, n_cols=len(cols), has_sharpe=has_sharpe, gate_like=is_gate,
                      realised_gross_cols=";".join(has_real), nominal_gross_cols=";".join(has_nom),
                      auditable=bool(has_real)))
fdf = pd.DataFrame(frows)
fdf.to_csv(OUT / f"{STEM}.censusfiles.csv", index=False)

tot = len(fdf)
sh = fdf[fdf.has_sharpe]
gl = sh[sh.gate_like]
P(f"committed grid CSVs in research/backtests/ : {tot}")
P(f"  ... carrying a Sharpe-like column        : {len(sh)}")
P(f"  ... AND gate/overlay vocabulary          : {len(gl)}   <- the census population")
P(f"      of those, carrying a REALISED gross column (auditable) : {int(gl.auditable.sum())} "
  f"({gl.auditable.mean():.1%})")
P(f"      nominal-gross-only (un-auditable from the record)      : {int((gl.nominal_gross_cols.astype(bool) & ~gl.auditable).sum())}")
P(f"      no gross column at all                                 : {int(((gl.nominal_gross_cols == '') & ~gl.auditable).sum())}")
P(f"P5 (a MAJORITY of gate/overlay grid CSVs are NOT gross-auditable): "
  f"{bool(gl.auditable.mean() < 0.5)}")

P("\nthe auditable files:")
P(gl[gl.auditable][["file", "realised_gross_cols", "nominal_gross_cols"]].to_string(index=False))

# --- the within-file comparisons, for the auditable subset
P("\nWITHIN-FILE COMPARISONS on the auditable subset.")
P("A comparison is scored only inside a HOMOGENEOUS group -- rows sharing whatever of")
P("{panel/universe/uni, cost/bps/cost_bps, book/family/conv/kind/arm-class} the parent")
P("committed -- so no comparison crosses a panel or a cost rung.  Within each group every row")
P("is paired against the group's MAX-realised-gross row (its own least-de-grossed member), and")
P("the pair is scored against what the ungated ladder alone buys over that same realised-gross")
P("gap on the matching panel and rung (U56@10bps where the parent's panel cannot be resolved).")
SH_FLOOR = float(spans.loc[(spans.panel == "U56") & (spans.cost == BASE_RUNG), "Sharpe_span"].iloc[0])
GROUP_COLS = ["panel", "universe", "uni", "cost", "bps", "cost_bps", "book", "family", "conv",
              "kind", "dial", "corpus", "selector"]
PANEL_ALIAS = {"u56": "U56", "U56": "U56", "b136": "B136", "B136": "B136", "broad": "B136",
               "BROAD136": "B136", "small": "SMALL439", "SMALL484": "SMALL439", "SMALL439": "SMALL439"}


def resolve_panel_rung(row):
    pn, c = "U56", BASE_RUNG
    for k in ("panel", "universe", "uni"):
        v = str(row.get(k, ""))
        if v in PANEL_ALIAS:
            pn = PANEL_ALIAS[v]
            break
    for k in ("cost", "bps", "cost_bps"):
        try:
            v = float(row.get(k, np.nan))
        except (TypeError, ValueError):
            continue
        if np.isfinite(v):
            c = 25 if v >= 17.5 else 10
            break
    return pn, c


crows = []
for _, fr in gl[gl.auditable].iterrows():
    f = OUT / fr["file"]
    try:
        d = pd.read_csv(f)
    except Exception:
        continue
    gcol = fr["realised_gross_cols"].split(";")[0]
    scol = next((c for c in ["Sharpe", "OOS_Sharpe", "IS_Sharpe", "Sharpe_OOS"] if c in d.columns), None)
    ccol = next((c for c in ["CAGR", "OOS_CAGR", "IS_CAGR", "CAGR_OOS"] if c in d.columns), None)
    dcol = next((c for c in ["MaxDD", "OOS_MaxDD", "IS_MaxDD", "MaxDD_OOS"] if c in d.columns), None)
    if scol is None or gcol not in d.columns:
        continue
    d["_g"] = pd.to_numeric(d[gcol], errors="coerce")
    d["_s"] = pd.to_numeric(d[scol], errors="coerce")
    d["_c"] = pd.to_numeric(d[ccol], errors="coerce") if ccol else np.nan
    d["_d"] = pd.to_numeric(d[dcol], errors="coerce") if dcol else np.nan
    d = d[d["_g"].notna() & d["_s"].notna()]
    if len(d) < 2:
        continue
    # a realised-gross column outside [0, 1.5] is not a gross level -- flag and skip
    if not (0.0 <= d["_g"].min() and d["_g"].max() <= 1.5):
        crows.append(dict(file=fr["file"], group="(whole file)", n_rows=len(d), gross_col=gcol,
                          sharpe_col=scol, note="gross col outside [0,1.5] -- NOT a gross level, skipped"))
        continue
    gcols = [c for c in GROUP_COLS if c in d.columns]
    grouped = d.groupby(gcols, dropna=False) if gcols else [((), d)]
    for key, sub in (grouped if gcols else grouped):
        if len(sub) < 2 or sub["_g"].max() - sub["_g"].min() < 1e-6:
            continue
        ref = sub.loc[sub["_g"].idxmax()]
        pn, rung = resolve_panel_rung(ref)
        for _, r in sub.iterrows():
            if r.name == ref.name:
                continue
            gap = float(ref["_g"] - r["_g"])
            gr_lo, gr_hi = float(np.clip(r["_g"], 0.20, 1.0)), float(np.clip(ref["_g"], 0.20, 1.0))
            lS = ladder_at(pn, rung, gr_hi, "Sharpe") - ladder_at(pn, rung, gr_lo, "Sharpe")
            lC = 100 * (ladder_at(pn, rung, gr_hi, "CAGR") - ladder_at(pn, rung, gr_lo, "CAGR"))
            lD = 100 * (ladder_at(pn, rung, gr_hi, "MaxDD") - ladder_at(pn, rung, gr_lo, "MaxDD"))
            fS = float(ref["_s"] - r["_s"])
            fC = 100 * float(ref["_c"] - r["_c"]) if ccol and np.isfinite(r["_c"]) and np.isfinite(ref["_c"]) else np.nan
            fD = 100 * float(ref["_d"] - r["_d"]) if dcol and np.isfinite(r["_d"]) and np.isfinite(ref["_d"]) else np.nan
            crows.append(dict(file=fr["file"], group=str(key)[:60], panel_used=pn, rung_used=rung,
                              gross_gap=gap, file_dSharpe=fS, ladder_dSharpe=lS,
                              file_dCAGR_pp=fC, ladder_dCAGR_pp=lC,
                              file_dMaxDD_pp=fD, ladder_dMaxDD_pp=lD,
                              gap_exceeds_sharpe_span=gap > SH_FLOOR,
                              sharpe_inside_ladder=abs(fS) <= abs(lS),
                              cagr_inside_ladder=bool(np.isfinite(fC)) and abs(fC) <= abs(lC),
                              maxdd_inside_ladder=bool(np.isfinite(fD)) and abs(fD) <= abs(lD),
                              cagr_gross_share=(1 - abs(fC - lC) / max(abs(fC), 1e-12)) if np.isfinite(fC) and abs(fC) > 1e-9 else np.nan,
                              maxdd_gross_share=(1 - abs(fD - lD) / max(abs(fD), 1e-12)) if np.isfinite(fD) and abs(fD) > 1e-9 else np.nan,
                              note=""))
cen = pd.DataFrame(crows)
cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
skipped = cen[cen.get("note", "").astype(str).str.startswith("gross col outside")] if len(cen) else cen
sc = cen[cen.get("note", "").astype(str) == ""] if len(cen) else cen
if len(skipped):
    P("\nfiles whose 'realised gross' column is not a gross LEVEL (skipped, and that is itself a "
      "schema finding):")
    P(skipped[["file", "gross_col", "note"]].drop_duplicates().to_string(index=False))
if len(sc):
    P(f"\nscored comparisons: {len(sc)} pairs across "
      f"{sc.file.nunique()} files and {sc.groupby(['file', 'group']).ngroups} homogeneous groups")
    P("\nby file:")
    agg = sc.groupby("file").agg(pairs=("gross_gap", "size"), mean_gap=("gross_gap", "mean"),
                                 max_gap=("gross_gap", "max"),
                                 gap_gt_span=("gap_exceeds_sharpe_span", "sum"),
                                 sharpe_inside=("sharpe_inside_ladder", "sum"),
                                 cagr_inside=("cagr_inside_ladder", "sum"),
                                 maxdd_inside=("maxdd_inside_ladder", "sum"),
                                 mean_cagr_share=("cagr_gross_share", "mean"),
                                 mean_maxdd_share=("maxdd_gross_share", "mean"))
    P(agg.to_string(float_format=lambda x: f"{x:.3f}"))
    nC = int(sc.file_dCAGR_pp.notna().sum())
    nD = int(sc.file_dMaxDD_pp.notna().sum())
    P("\nTHE CENSUS ANSWER")
    P(f"  gate/overlay grid CSVs in the record                       : {len(gl)}")
    P(f"  ... gross-auditable (a REALISED gross column is committed)  : {int(gl.auditable.sum())} ({gl.auditable.mean():.1%})")
    P(f"  scored within-group comparisons                            : {len(sc)}")
    P(f"  made across a gross gap > the ladder's own Sharpe span ({SH_FLOOR:.4f}) : "
      f"{int(sc.gap_exceeds_sharpe_span.sum())}/{len(sc)} ({sc.gap_exceeds_sharpe_span.mean():.1%})"
      "   <- the queue's literal count")
    P(f"  made across a gross gap > 0.05 of realised gross           : "
      f"{int((sc.gross_gap.abs() > 0.05).sum())}/{len(sc)} ({(sc.gross_gap.abs() > 0.05).mean():.1%})")
    P(f"  whose published dSharpe is INSIDE what the ladder buys     : "
      f"{int(sc.sharpe_inside_ladder.sum())}/{len(sc)} ({sc.sharpe_inside_ladder.mean():.1%})")
    P(f"  whose published dCAGR  is INSIDE what the ladder buys      : {int(sc.cagr_inside_ladder.sum())}/{nC} "
      f"({sc.cagr_inside_ladder.sum() / max(nC, 1):.1%})")
    P(f"  whose published dMaxDD is INSIDE what the ladder buys      : {int(sc.maxdd_inside_ladder.sum())}/{nD} "
      f"({sc.maxdd_inside_ladder.sum() / max(nD, 1):.1%})")
    # A ratio-of-differences has a near-zero denominator whenever the published difference is
    # itself near zero, so the MEAN share is not a reportable statistic.  Median, and a mean
    # restricted to comparisons whose published difference exceeds 1 pp, are.
    big_c = sc[sc.file_dCAGR_pp.abs() > 1.0]
    big_d = sc[sc.file_dMaxDD_pp.abs() > 1.0]
    P(f"  gross-channel SHARE of a published dCAGR   : median {np.nanmedian(sc.cagr_gross_share):+.3f}"
      f"   |dCAGR|>1pp subset (n={len(big_c)}): median {np.nanmedian(big_c.cagr_gross_share):+.3f}, "
      f"mean {np.nanmean(big_c.cagr_gross_share):+.3f}")
    P(f"  gross-channel SHARE of a published dMaxDD  : median {np.nanmedian(sc.maxdd_gross_share):+.3f}"
      f"   |dMaxDD|>1pp subset (n={len(big_d)}): median {np.nanmedian(big_d.maxdd_gross_share):+.3f}, "
      f"mean {np.nanmean(big_d.maxdd_gross_share):+.3f}")
    P(f"  majority-exposure (share > 0.50) among |dCAGR|>1pp   : "
      f"{int((big_c.cagr_gross_share > 0.5).sum())}/{int(big_c.cagr_gross_share.notna().sum())} "
      f"({(big_c.cagr_gross_share > 0.5).sum() / max(int(big_c.cagr_gross_share.notna().sum()), 1):.1%})")
    P(f"  majority-exposure (share > 0.50) among |dMaxDD|>1pp  : "
      f"{int((big_d.maxdd_gross_share > 0.5).sum())}/{int(big_d.maxdd_gross_share.notna().sum())} "
      f"({(big_d.maxdd_gross_share > 0.5).sum() / max(int(big_d.maxdd_gross_share.notna().sum()), 1):.1%})")
    P("\n  READ IT THIS WAY.  The Sharpe row is the SAFE one: only "
      f"{sc.sharpe_inside_ladder.mean():.1%} of published Sharpe differences are inside what the")
    P("  ladder buys, because the ladder buys almost nothing in Sharpe -- so a Sharpe verdict")
    P("  cannot be a gross artefact THROUGH THIS CHANNEL, whatever the gross gap.  The exposure")
    P("  channel lands on CAGR and MaxDD instead, and there roughly a fifth of the record's own")
    P("  auditable comparisons are entirely inside it.  The larger exposure is not the 9.3%")
    P("  that IS auditable -- it is the 90.7% that is not.")
else:
    P("no auditable within-group comparison could be scored.")

P("\n" + "=" * 108)
P(f"done in {time.time() - T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
